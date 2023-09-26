from .constants import MAILING_LIST_FORM_PREFIX
from .forms import MailingListSignupForm


def signup_form(request):
    initial = {"source_url": request.path}

    if MAILING_LIST_FORM_PREFIX in request.POST:
        mailing_list_form = MailingListSignupForm(
            initial=initial,
            data=request.POST,
        )
    else:
        mailing_list_form = MailingListSignupForm(initial=initial)

    return {
        "mailing_list_form": mailing_list_form,
    }
