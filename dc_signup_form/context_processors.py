from .forms import ElectionRemindersSignupForm, MailingListSignupForm


def signup_form(request):
    initial = {
        'source_url': request.path
    }

    if request.POST:
        return {
            'mailing_list_form': MailingListSignupForm(
                initial=initial, data=request.POST),
            'election_reminders_form': ElectionRemindersSignupForm(
                initial=initial, data=request.POST),
        }
    else:
        return {
            'mailing_list_form': MailingListSignupForm(
                initial=initial),
            'election_reminders_form': ElectionRemindersSignupForm(
                initial=initial),
        }
