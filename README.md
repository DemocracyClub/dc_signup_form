# DC Signup Form

![Tests](https://github.com/DemocracyClub/dc_signup_form/actions/workflows/run_tests.yaml/badge.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Django app with Email signup form for use on Democracy Club websites. Currently, this app is used on: 
* [Democracy Club](https://democracyclub.org.uk)
* [Who Can I Vote For?](https://whocanivotefor.co.uk)



## Installation

Add to project requirements:

```
git+git://github.com/DemocracyClub/dc_signup_form.git
```

This project depends on [`dc_django_utils`](https://github.com/DemocracyClub/dc_django_utils) 
and we assume this is already set up on the project.

For deployments in AWS you need to ensure that the role has 
`events:put_events` permission on the EventBridge ARN.

## Configuration

`dc_signup_form` needs to be in `INSTALLED_APPS` and
`dc_signup_form.context_processors.signup_form` needs to be added as a 
context processor.


```python

EMAIL_SIGNUP_BACKEND = "event_bridge"
EMAIL_SIGNUP_BACKEND_KWARGS = {
    "source": "NAME OF THIS SOURCE, e.g the project name",
    "bus_arn": "[ARN of the event bridge bus. Take this from the dev handbook]"
}

```

Note that `bus_arn` needs to change for dev, stage and prod accounts. It's 
recommended to take this from the environment when running the app.


## Usage


```python
from dc_signup_form.views import SignupFormView
from dc_signup_form.forms import MailingListSignupForm

email_urls = [
    url(r'^$',
        SignupFormView.as_view(
            template_name='email_form/mailing_list_form_view.html',
            form_class=MailingListSignupForm,
            get_vars=['postcode'],
            extras={
                'source': 'EveryElection',
            },
            thanks_message="My custom thanks message",
            backend='event_bridge',
            backend_kwargs=settings.EMAIL_SIGNUP_BACKEND_KWARGS
        ),
        name='mailing_list_signup_view'),
]

# any custom urls we create must be declared in the 'dc_signup_form' namespace
urlpatterns += [
    url(r'^mailing_list/',
        include(email_urls, 'dc_signup_form', 'dc_signup_form')
    ),
]
```

Use as a standalone view

```django
<a href="{% url 'dc_signup_form:mailing_list_signup_view' %}">Mailing List</a>
```


or display the form inline:

```django
{% if not messages %}
  <div class="row">
    <div class="columns large-12">
      <div class="card">
        Sign up for our mailing list to receive election reminders
        {% include "email_form/election_reminders_form.html" %}
      </div>
    </div>
  </div>
{% endif %}
```

## Tests

run ```python run_tests.py```
