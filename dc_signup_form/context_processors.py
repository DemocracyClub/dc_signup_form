from .forms import EmailSignupForm


def signup_form(request):
    initial = {
        'source_url': request.path
    }

    if request.POST:
        return {
            'signup_form': EmailSignupForm(initial=initial, data=request.POST)
        }
    else:
        return {
            'signup_form': EmailSignupForm(initial=initial)
        }
