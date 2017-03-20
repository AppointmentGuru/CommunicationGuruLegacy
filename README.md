# GuruComunication
A generic library for sending transactional communications via various methods (SMS, Email or in-app notification)

**NB:** This is a work in progress

This library provides a simple mechanism for sending communications over a variety of transports.

It provides an interface for creating templates which can be used for sending and customizing transactions e-mails.

## API

### Python

``` python

from gurucommunication.sender import send_template
send_template(
        to=Recipient.from_user(user),
        sender=Sender.from_user(sender_user),
        template_id='hello-world',
        context={},
        template_owner=user)
)
```

* See the tests

### REST

**Create a message (send a message).**

```
POST {base}/message
```

> Send the message to the best backend

**Get information on messages sent**

```
GET {}/message
```

> Returns a list of messages. You can search and filter this list

**Get detailed information on a message**

```
GET {}/message/:id/
```

> Returns details (including updated status from delivery backend) on a Message that has been sent


### Roadmap / todo

**Phase 1**

- [ ] All e-mails that are sent must be logged and stored
- [ ] Make the sending API a little more user-friendly
- [ ] Intelligently send to the best medium: `message.preferred_medium`, then `settings.PREFERENCE_ORDER`
- [ ] Subject should be tokenizable (e.g.: 'Hello {{name}}')
- [ ] Implement RESTful API
- [ ] Handle attachements (email)

**Backends**

- [x] Twilio
- [x] E-mail (via anymail)

**Phase 2**

- [ ] Multi-part templates (e-mail base templates with multiple blocks in them)
- [ ] ...

**Backends**

- [ ] In-app notification
- [ ] Facebook
- [ ] Slack
- [ ] Hipchat


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