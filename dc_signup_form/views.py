from django.contrib import messages
from django.urls import NoReverseMatch, reverse
from django.views.generic import FormView

from .backends import (
    EventBridgeBackend,
    TestBackend,
)


def get_http(request, host):
    try:
        from django.utils.http import is_safe_url

        return is_safe_url(request, host)
    except ImportError:
        from django.utils.http import url_has_allowed_host_and_scheme

        return url_has_allowed_host_and_scheme(request, host)


class SignupFormView(FormView):
    mailing_lists = [
        "main_list",
        "election_reminders",
    ]  # list of the mailing lists we support joining
    get_vars = []  # list of get vars we want to store with the user
    extras = (
        {}
    )  # dict of hard-coded key/value pairs we want to store with the user
    thanks_message = "Thanks for joining the Democracy Club mailing list. We will be in touch soon!"

    backends = {
        "test": TestBackend,
        "event_bridge": EventBridgeBackend,
    }
    backend = "remote_db"
    backend_kwargs = {}

    def get_success_url(self):
        messages.success(self.request, self.thanks_message)

        form_name = self.get_form_class().prefix
        source_url = self.request.POST.get(f"{form_name}-source_url")

        try:
            mailing_list_signup_view = reverse(
                "dc_signup_form:mailing_list_signup_view"
            )
        except NoReverseMatch:
            mailing_list_signup_view = ""
        try:
            election_reminders_signup_view = reverse(
                "dc_signup_form:election_reminders_signup_view"
            )
        except NoReverseMatch:
            election_reminders_signup_view = ""

        source_url_safe = get_http(source_url, host=self.request.get_host())

        if (
            source_url_safe
            and source_url != mailing_list_signup_view
            and source_url != election_reminders_signup_view
        ):
            return source_url
        return "/"

    def form_invalid(self, form):
        """
        Add the form to the context using the form prefix as the var name.

        This is because we use the prefix in the template to render this form,
        without this we would render the 'clean' form from the context
        processor, hiding any errors thrown.
        """
        context_form_name = form.prefix
        return self.render_to_response(
            self.get_context_data(**{context_form_name: form})
        )

    def form_valid(self, form):
        mailing_lists = []
        data = form.cleaned_data.copy()

        # mailing lists
        for lst in self.mailing_lists:
            "-".join([self.form_class.prefix, lst])
            if data.pop(lst, False):
                mailing_lists.append(lst)

        # get params
        for var in self.get_vars:
            data[var] = self.request.GET.get(var, None)

        # other hard-coded vars
        for extra in self.extras:
            data[extra] = self.extras[extra]

        # pass the payload off to a backend object
        # to deal with persisting the data to a db
        self.backends[self.backend](**self.backend_kwargs).submit(
            data, mailing_lists
        )

        return super(SignupFormView, self).form_valid(form)
