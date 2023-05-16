# DC Signup Form

[![Build Status](https://travis-ci.org/DemocracyClub/dc_signup_form.svg?branch=master)](https://travis-ci.org/DemocracyClub/dc_signup_form)
[![Coverage Status](https://coveralls.io/repos/github/DemocracyClub/dc_signup_form/badge.svg?branch=master)](https://coveralls.io/github/DemocracyClub/dc_signup_form?branch=master)

Django app with Email signup form for use on Democracy Club websites. Currently, this app is used on: 
* [Democracy Club](https://democracyclub.org.uk)
* [Who Can I Vote For?](https://whocanivotefor.co.uk)
* [Where Do I Vote?](https://wheredoivote.co.uk)


## Installation

Add to project requirements:

```
git+git://github.com/DemocracyClub/dc_base_theme.git
git+git://github.com/DemocracyClub/dc_signup_form.git
```

## Configuration

Using the remote backend (default):

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

EMAIL_SIGNUP_API_KEY = 'f00b42'
EMAIL_SIGNUP_ENDPOINT = 'https://foo.bar/baz/'
```

Using the local backend:

```python
INSTALLED_APPS = [
    ...
    'dc_signup_form',
    'dc_signup_form.signup_server',
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

## Usage

Default routes:

```python
url(r'^emails/', include('dc_signup_form.urls')),
```

Routes for local backend:
```python
url(r'^emails/api_signup/', include('dc_signup_form.signup_server.urls')),
```

Custom routes:

```python
from dc_signup_form.views import SignupFormView

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
            backend='local_db'
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

