# Seed Maternal Health Webhooks Configuration

### Overview

The usage of webhooks are designed to allow the Seed Service to distribute data around to other internal or external components without the need to know about each other in advance. We utilise the [Django REST Hooks](https://github.com/zapier/django-rest-hooks) package from Zapier and implement them as Celery tasks to ensure they are non-blocking. 

### Known limitations

Currently we use an environment variable as token auth for all outbound webhooks. This is sub-optimal and we should look at signing hooks instead using something [HMAC](https://en.wikipedia.org/wiki/Hash-based_message_authentication_code) like MailGun do. There is an [open issue](https://github.com/praekelt/hellomama-registration/issues/56) for this with links to sample code.

There are no retries implemented at the moment. See [the docs](https://github.com/zapier/django-rest-hooks#some-gotchas) for how this could be done with a back-off.

If you want to ensure exceptions are captured correctly then the Celery worker container must have the `SENTRY_DSN` correctly set.

### Seed Services using Webhooks

The places webhooks must be configured currently are:

1. Between a project Hub and Seed Stage-Based Messaging. For `subscriptionrequest.added` to 	`/api/v1/subscriptions/request` on SBM.
2. If Unique ID generation is required for a project: between Identity Store and project Hub. For `identity.created` to `/api/v1/uniqueid/` on Hub.

