from django.contrib import messages
from django.core.urlresolvers import NoReverseMatch
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.utils.http import is_safe_url
from django.views.generic import FormView
from .forms import EmailSignupForm
from .backends import (
    LocalDbBackend,
    RemoteDbBackend,
    TestBackend,
)


class SignupFormView(FormView):
    mailing_lists = [
        'main_list', 'election_reminders'
    ]  # list of the mailing lists we support joining
    get_vars = []  # list of get vars we want to store with the user
    extras = {}  # dict of hard-coded key/value pairs we want to store with the user
    thanks_message = "Thanks for joining. We'll be in touch soon!"

    backends = {
        'test': TestBackend(),
        'local_db': LocalDbBackend(),
        'remote_db': RemoteDbBackend(),
    }
    backend = 'remote_db'

    def get_success_url(self):
        messages.success(
            self.request, self.thanks_message)

        source_url = self.request.POST.get('source_url')

        try:
            mailing_list_signup_view = reverse(
                'dc_signup_form:mailing_list_signup_view')
        except NoReverseMatch:
            mailing_list_signup_view = ''
        try:
            election_reminders_signup_view = reverse(
                'dc_signup_form:election_reminders_signup_view')
        except NoReverseMatch:
            election_reminders_signup_view = ''

        if is_safe_url(source_url) and\
            source_url != mailing_list_signup_view and\
            source_url != election_reminders_signup_view:
            return source_url
        else:
            return "/"

    def form_valid(self, form):

        mailing_lists = []
        data = form.cleaned_data.copy()

        # mailing lists
        for lst in self.mailing_lists:
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
        self.backends[self.backend].submit(data, mailing_lists)

        return super(SignupFormView, self).form_valid(form)
