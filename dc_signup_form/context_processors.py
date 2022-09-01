from .forms import ElectionRemindersSignupForm, MailingListSignupForm
from .constants import MAILING_LIST_FORM_PREFIX, ELECTION_REMINDERS_FORM_PREFIX


def signup_form(request):
    initial = {"source_url": request.path}

    if MAILING_LIST_FORM_PREFIX in request.POST:
        mailing_list_form = MailingListSignupForm(
            initial=initial,
            data=request.POST,
        )
    else:
        mailing_list_form = MailingListSignupForm(initial=initial)

    if ELECTION_REMINDERS_FORM_PREFIX in request.POST:
        election_reminders_form = ElectionRemindersSignupForm(
            initial=initial,
            data=request.POST,
        )
    else:
        election_reminders_form = ElectionRemindersSignupForm(initial=initial)

    return {
        "mailing_list_form": mailing_list_form,
        "election_reminders_form": election_reminders_form,
    }
