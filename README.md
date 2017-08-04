# DC Signup Form

Django app with Email signup form for use on Democracy Club websites

## Installation

Add to project requirements:

```
git+git://github.com/DemocracyClub/dc_base_theme.git
git+git://github.com/DemocracyClub/dc_signup_form.git
```

## Usage

```python
INSTALLED_APPS = [
    ...
    'dc_signup_form',
]

TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'dc_signup_form.context_processors.signup_form',
            ],
        },
    }
]

SENDGRID_API_KEY = 'f00b42'
```

Default:

```python
url(r'^mailing_list/', include('dc_signup_form.urls')),
```

Custom:

```python
from dc_signup_form.views import SignupFormView

url(
    r'^mailing_list/',
    SignupFormView.as_view(
        mailing_lists=['main list', 'election reminders'],
        get_vars=['postcode'],
        extras={
            'source': 'EveryElection',
        },
        thanks_message="Thanks for joining. We'll also send you a reminder when there's an upcoming election in your area",
        backend='sendgrid'
    ),
    name='email_signup_view'
),
```

Use as a standalone view, or display the form inline:

```
{% if not messages %}
  <div class="row">
    <div class="columns large-12">
      <div class="card">
        Sign up for our mailing list to receive election reminders
        {% include "email_form/email_form.html" %}
      </div>
    </div>
  </div>
{% endif %}
```
