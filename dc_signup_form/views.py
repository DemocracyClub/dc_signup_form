from django.contrib import messages
from django.urls import reverse
from django.utils.http import is_safe_url
from django.views.generic import FormView
from .forms import EmailSignupForm
from .wrappers import SendGridWrapper, TestWrapper


class SignupFormView(FormView):
    template_name = 'email_form/email_form_view.html'
    form_class = EmailSignupForm

    mailing_lists = []  # list of the mailing lists this user should be added to
    get_vars = []  # list of get vars we want to store with the user
    extras = {}  # dict of hard-coded key/value pairs we want to store with the user
    thanks_message = "Thanks for joining. We'll be in touch soon!"

    backends = {
        'test': TestWrapper(),
        'sendgrid': SendGridWrapper()
    }
    backend = 'test'

    def get_success_url(self):
        messages.success(
            self.request, self.thanks_message)

        source_url = self.request.POST.get('source_url')
        if is_safe_url(source_url) and source_url != reverse('email_signup_view'):
            return source_url
        else:
            return "/"

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        for var in self.get_vars:
            data[var] = self.request.GET.get(var, None)
        for extra in self.extras:
            data[extra] = self.extras[extra]

        self.backends[self.backend].submit(data, self.mailing_lists)

        return super(SignupFormView, self).form_valid(form)
