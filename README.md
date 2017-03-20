# GuruComunication
A generic library for sending communications via various methods (SMS, Email or in-app notification)



## Backends

### SMS

#### Twillio

**Requirements:**

* `twilio`

**Configuration:**

**Settings.py**

```
TWILLIO_SID='..'
TWILLIO_AUTH_TOKEN='..'
TWILLIO_PHONE_NUMBER='..' # twilio phone number to send from

...
GURU_COMMUNICATIONS = {
    SMS_BACKEND = 'TWILIO',
    ..
}
```

#### Email:

E-mails leverage the [Django-Anymail](https://anymail.readthedocs.io/en/stable/) package for sending e-mail. Please refer to the anymail docs for setting up your project