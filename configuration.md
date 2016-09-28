# Seed Maternal Health Configuration

The following describes the connective configuration of a Seed Maternal Health
stack. It is a multi-step process with some reliance between services that in
some instances requires initial bootstrapping then returning re-configuration
and restarting. All services in this stack are optimised for Docker-based
deployment and Dockerfile's are provided in each repo, however the components
can also be deployed using traditional methods too. Most components are expected
to use Environment Variables to configure their setup for things like databases
and other pre-reqs. Furthermore, this guide provides additional advice and scripts
for a Praekelt Mission Control based deployment.


## Deployment order

It is recommended that the deployment takes place in the following order:

1. Shared Backend Services
2. Project specific hub
3. Control interface
4. Connectivity
5. Applications
6. Help Desk (optional)


## Prereqs

The following pre-reqs must be in place before attempting deployment and configuration
of a Seed Maternal Health Stack.

1. Seperate Postgres databases for each Backend Service, Control Interface and Help Desk.
2. Seperate RabbitMQ vhosts for each Backend Service.
3. Shared RabbitMQ vhost for Junebug
4. Shared Redis KV store
5. Graphite
6. Sentry (optional)


## 1. Deploy Shared Backend Services

In this repo you will find a helper script for deployment on Mission Control.

It expects the following variables set:

* prefix - project slug (e.g. "hellomama")
* domain - added to prefix (e.g. "prefix.seed.example.org")
* dockerhub - FQDN of private Docker image host
* redis - FQDN of shared redis cluster or node
* amqp - FQDN of shared APQP service like RabbitMQ
* amqp_user - shared APQP service vhost username
* amqp_pass - shared APQP service vhost password
* postgres - shared Postres service
* sentry - FQDN of shared Sentry service

Providing a consistent approach to naming credentials has taken place it also
needs the following variables setting. We also provide the full list of script
variable required for if this has not taken place below.

* SECRET_KEY_IDENTITIES - Django secret key
* DB_PASS_IDENTITIES - Identity Store Postgres DB password
* IDENTITIES_SENTRY_DSN - Sentry DSN

* SECRET_KEY_SBM - Django secret key
* DB_PASS_SBM - Stage Based Messaging Postgres DB password
* STAGE_BASED_MESSAGING_SENTRY_DSN - Sentry DSN
* SCHEDULER_API_TOKEN_SBM - Auth token to talk to Scheduler
* SCHEDULER_INBOUND_API_TOKEN_SBM - Auth token Scheduler should talk to Stage Based Messaging with
* IDENTITY_STORE_TOKEN_SBM - Auth token to talk to Identity Store
* MESSAGE_SENDER_TOKEN_SBM - Auth token to talk to Message Sender

* SECRET_KEY_MS - Django secret key
* DB_PASS_MS - Message Sender Postgres DB password
* MESSAGE_SENDER_SENTRY_DSN - Sentry DSN
* MESSAGE_SENDER_VUMI_API_URL_TEXT - FQDN of Vumi API for SMS sending
* MESSAGE_SENDER_VUMI_ACCOUNT_KEY_TEXT - Account Key of Vumi API (SMS)
* MESSAGE_SENDER_VUMI_CONVERSATION_KEY_TEXT - Conversation Key of Vumi API (SMS)
* MESSAGE_SENDER_VUMI_ACCOUNT_TOKEN_TEXT - Auth Token of Vumi API (SMS)
* MESSAGE_SENDER_VUMI_API_URL_VOICE - FQDN of Vumi API for Audio sending
* MESSAGE_SENDER_VUMI_ACCOUNT_KEY_VOICE - Account Key of Vumi API (Voice)
* MESSAGE_SENDER_VUMI_CONVERSATION_KEY_VOICE - Conversation Key of Vumi API (Voice)
* MESSAGE_SENDER_VUMI_ACCOUNT_TOKEN_VOICE - Auth Token of Vumi API (Voice)

* SECRET_KEY_SCH - Django secret key
* DB_PASS_SCH - Scheduler Postgres DB password
* SCHEDULER_SENTRY_DSN - Sentry DSN

* SECRET_KEY_SVCRATE - Django secret key
* DB_PASS_SVCRATE - Service Rating Postgres DB password
* SERVICE_RATING_SENTRY_DSN - Sentry DSN

* SECRET_KEY_HUB - Django secret key
* DB_PASS_HUB - Hub Postgres DB password
* HUB_SENTRY_DSN - Sentry DSN
* STAGE_BASED_MESSAGING_TOKEN_HUB - Auth token to talk to Stage Based Messaging
* IDENTITY_STORE_TOKEN_HUB - Auth token to talk to Identity Store
* MESSAGE_SENDER_TOKEN_HUB - Auth token to talk to Message Sender


**NOTE:** You can set "SUPERUSER_PASSWORD" on all Django Docker containers which
will create a user called "admin" with that password if it doesn't exist. You
*must* change that password once the service is bootstrapped.


### 1.1 Seed Identity Store

**Requires Celery Worker: ** Yes  
**Requires Celery Beat:** No  

**Environment Variable:**

* DJANGO_SETTINGS_MODULE - Django settings module
* SECRET_KEY - Django secret key
* IDENTITIES_DATABASE - dj_database_url style config
* IDENTITIES_SENTRY_DSN - Sentry DSN
* BROKER_URL - AMQP setup
* METRICS_URL - URL of Metrics HTTP API
* METRICS_AUTH_TOKEN - Auth token of Metrics HTTP API


### 1.2 Seed Stage Based Messaging

**Requires Celery Worker: ** Yes  
**Requires Celery Beat:** No  

**Environment Variable:**

* DJANGO_SETTINGS_MODULE - Django settings module
* SECRET_KEY - Django secret key
* STAGE_BASED_MESSAGING_DATABASE - dj_database_url style config
* STAGE_BASED_MESSAGING_SENTRY_DSN - Sentry DSN
* BROKER_URL - AMQP setup
* METRICS_URL - URL of Metrics HTTP API
* METRICS_AUTH_TOKEN - Auth token of Metrics HTTP API
* SCHEDULER_URL - FQDN of Scheduler API
* SCHEDULER_API_TOKEN - Auth token to talk to Scheduler
* SCHEDULER_INBOUND_API_TOKEN - Auth token Scheduler should talk to Stage Based Messaging with
* IDENTITY_STORE_URL - FQDN of Scheduler API
* IDENTITY_STORE_TOKEN - Auth token to talk to Identity Store
* MESSAGE_SENDER_URL - FQDN of Scheduler API
* MESSAGE_SENDER_TOKEN - Auth token to talk to Message Sender
* STAGE_BASED_MESSAGING_URL - URL of Subscriptions endpoint on this service (FQDN plus /api/v1/subscriptions)


### 1.3 Seed Scheduler

**Requires Celery Worker: ** Yes  
**Requires Celery Beat:** Yes  

**Environment Variable:**

* DJANGO_SETTINGS_MODULE - Django settings module
* SECRET_KEY - Django secret key
* SCHEDULER_DATABASE - dj_database_url style config
* SCHEDULER_SENTRY_DSN - Sentry DSN
* BROKER_URL - AMQP setup
* METRICS_URL - URL of Metrics HTTP API
* METRICS_AUTH_TOKEN - Auth token of Metrics HTTP API


### 1.4 Seed Message Sender

**Requires Celery Worker: ** Yes  
**Requires Celery Beat:** No  

**Environment Variable:**

* DJANGO_SETTINGS_MODULE - Django settings module
* SECRET_KEY - Django secret key
* MESSAGE_SENDER_DATABASE - dj_database_url style config
* MESSAGE_SENDER_SENTRY_DSN - Sentry DSN
* BROKER_URL - AMQP setup
* METRICS_URL - URL of Metrics HTTP API
* METRICS_AUTH_TOKEN - Auth token of Metrics HTTP API
* VUMI_API_URL_VOICE - FQDN of Vumi API for Audio sending
* VUMI_ACCOUNT_KEY_VOICE - Account Key of Vumi API (Voice)
* VUMI_CONVERSATION_KEY_VOICE - Conversation Key of Vumi API (Voice)
* VUMI_ACCOUNT_TOKEN_VOICE - Auth Token of Vumi API (Voice)
* VUMI_API_URL_TEXT - FQDN of Vumi API for SMS sending
* VUMI_ACCOUNT_KEY_TEXT - Account Key of Vumi API (SMS)
* VUMI_CONVERSATION_KEY_TEXT - Conversation Key of Vumi API (SMS)
* VUMI_ACCOUNT_TOKEN_TEXT - Auth Token of Vumi API (SMS)
* MESSAGE_SENDER_MAX_RETRIES - maximum attempts per message
* MESSAGE_SENDER_MAX_FAILURES - when to view concurrent failures as subscription termination

**Required Configuration:**

The application needs users with auth tokens for each unique frontend application that
is required to have access. The best thing to do is "app_type_transport" for
consistency. For example, "app_public_ussd".  

The application also needs users with auth tokens for each unique service
account that is required to have access. The best thing to do is
"service_servicename" for consistency. For example, "service_control_interface".

For the Message Sender this includes:
* service_stage_based_messaging
* service_hub


### 1.5 Seed Service Rating

**Requires Celery Worker: ** Yes  
**Requires Celery Beat:** No  

**Environment Variable:**

* DJANGO_SETTINGS_MODULE - Django settings module
* SECRET_KEY - Django secret key
* SERVICE_RATING_DATABASE - dj_database_url style config
* SERVICE_RATING_SENTRY_DSN - Sentry DSN
* BROKER_URL - AMQP setup
* METRICS_URL - URL of Metrics HTTP API
* METRICS_AUTH_TOKEN - Auth token of Metrics HTTP API


### 1.6 Seed Control Interface Service

**Requires Celery Worker: ** Yes  
**Requires Celery Beat:** Yes  

**Environment Variable:**

* DJANGO_SETTINGS_MODULE - Django settings module
* SECRET_KEY - Django secret key
* IDENTITIES_DATABASE - dj_database_url style config
* IDENTITIES_SENTRY_DSN - Sentry DSN
* BROKER_URL - AMQP setup
* METRICS_URL - URL of Metrics HTTP API
* METRICS_AUTH_TOKEN - Auth token of Metrics HTTP API

**Required Configuration:**

The Control Interface Service needs an account on every other service with Staff
level access. That account (best named control_interface_service) needs a token
and the combination of service name (from below), API URL (without the /api/v1)
and token should be added to the Services application. Required service names:

* SEED_SCHEDULER
* SEED_MESSAGE_SENDER
* SEED_STAGE_BASED_MESSAGING
* HUB
* SEED_IDENTITY_SERVICE

There then needs to be two scheduled tasks set up in the Periodic Task application.

1. To poll those services at the rate the deployment requires. It should call "services.tasks.QueuePollService" every x minutes
2. To pull metric names from each service. It should call "services.tasks.QueueServiceMetricSync"
something like once per hour. 

### 1.7 Seed Auth API

**Requires Celery Worker: ** No  
**Requires Celery Beat:** No  

**Environment Variable:**

* DJANGO_SETTINGS_MODULE - Django settings module
* SECRET_KEY - Django secret key
* IDENTITIES_DATABASE - dj_database_url style config
* IDENTITIES_SENTRY_DSN - Sentry DSN
* BROKER_URL - AMQP setup

**Required Configuration:**

Documentation on the Auth API can be found at: http://seed-auth-api.rtfd.org  
It needs to be bootstrapped in the following order:
* Create an organisation
* Create two teams in that organisation for CI Admins and CI Users
* Grant those teams "ci:view" permissions

Users should be placed in the "CI Users" team  to get access to the CI
(we haven't implemented granular permissions yet). Once a user has been given
basic permissions, the responsibility for creating Seed Service specific access
tokens is given to the Seed Control Interface Service. This will allow all
data manipulation to be done in the users context, providing an audit trail.

## 1.8 Project Specific Hub

**Requires Celery Worker: ** Yes  
**Requires Celery Beat:** No  

**Environment Variable:**

* DJANGO_SETTINGS_MODULE - Django settings module
* SECRET_KEY - Django secret key
* HUB_DATABASE - dj_database_url style config
* HUB_SENTRY_DSN - Sentry DSN
* BROKER_URL - AMQP setup
* METRICS_URL - URL of Metrics HTTP API
* METRICS_AUTH_TOKEN - Auth token of Metrics HTTP API
* IDENTITY_STORE_URL - FQDN of Scheduler API
* IDENTITY_STORE_TOKEN - Auth token to talk to Identity Store
* MESSAGE_SENDER_URL - FQDN of Scheduler API
* MESSAGE_SENDER_TOKEN - Auth token to talk to Message Sender
* STAGE_BASED_MESSAGING_URL - FQDN of Stage Based Messaging API
* STAGE_BASED_MESSAGING_TOKEN - Auth token to talk to Stage Based Messaging

**Required Configuration:**

The application needs users with auth tokens for each unique frontend application that
is required to have access. The best thing to do is "app_type_transport" for
consistency. For example, "app_public_ussd".  

The application also needs users with auth tokens for each unique service
account that is required to have access. For the hub this includes the Control
Interface Service. The best thing to do is "service_servicename" for
consistency. For example, "service_control_interface".  

Each application also needs a Source defining in the Registrations app. This
sets the authority level for each registration which can influence the message set
the recipient is signed up for.

### 1.9 Control Interface

**Requires Celery Worker: ** No  
**Requires Celery Beat:** No  

**Environment Variable:**

* DJANGO_SETTINGS_MODULE - Django settings module
* SECRET_KEY - Django secret key
* CONTROL_INTERFACE_DATABASE - dj_database_url style config
* CONTROL_INTERFACE_SENTRY_DSN - Sentry DSN
* CONTROL_INTERFACE_SERVICE_TOKEN - Token to access CI Service API
* CONTROL_INTERFACE_SERVICE_URL - URL of CI Service API
* AUTH_SERVICE_URL - URL of Auth Service (no API endpoint)
* CI_LOGO_URL - link to logo PNG file for UI
* METRIC_API_URL - URL of Metrics API

**Required Configuration:**

Only above env vars.