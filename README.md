# Seed Maternal Health Overview

The following describes the components of a Seed Maternal Health stack.


## Overview

A fully configured stack consists of the following elements:

1. Connectivity - one or more channels in the form of SMS, USSD, Voice or other
Vumi transports, generally managed via a Junebug deployment.
2. Applications - one or more javascript sandbox applications providing user
interactions that guide the participant through a registration, change management or
information dispersal flow.
3. Backend Services - REST-based API's that receive, store, process and present data in
a number of logically grouped collections.
4. Control Interface - Web-based administration tools for supporting the platform.
5. Help Desk - Optional, web-based end user support tool for responding to ad-hoc queries.


## Shared Backend Services

The following services are available for a complete Seed Maternal Health Stack.

### Seed Identity Store

**GitHub:** [https://github.com/praekelt/seed-identity-store](https://github.com/praekelt/seed-identity-store)  
**Responsibility:** This service creates a UUID per end user of the system against
which multiple addresses of many types can be stored. For example, MSISDN (cell number),
email address, Facebook ID. It is also a central store of requests to be opt-ed out,
which are then broadcast to all services via webhooks.   


### Seed Stage Based Messaging

**GitHub:** [https://github.com/praekelt/seed-stage-based-messaging](https://github.com/praekelt/seed-stage-based-messaging)  
**Responsibility:** This service stores the details of all subscriptions to
stage-based content on the system plus the content itself and default schedules.

It processes data as follows:
1. Inbound subscriptions come in via REST API
2. Subscription to message set is created
3. Schedule of the message set is read and Seed Scheduler entry created
4. Send next message call is triggered by Scheduler
5. Message content is delivered to Seed Message Sender
6. At end of message set, optional next subscription is created

### Seed Scheduler

**GitHub:** [https://github.com/praekelt/seed-scheduler](https://github.com/praekelt/seed-scheduler)  
**Responsibility:** This service listens for requests to hit other REST API's with
at the provided interval. This can be in cron or every-x based format. It will
either continue indefinitely or until the requested number of times is reached.
The service can also be provided with a payload and auth token to pass along
without outbound requests.


### Seed Message Sender

**GitHub:** [https://github.com/praekelt/seed-message-sender](https://github.com/praekelt/seed-message-sender)  
**Responsibility:** This service is responsible for storing and sending messages to
upstream Vumi HTTP API endpoints. It will retry the sending if those messages are
unavailable when the attempt is made. It can also be used as in incoming message
store but nothing will process those currently.


### Seed Service Rating

**GitHub:** [https://github.com/praekelt/seed-service-rating](https://github.com/praekelt/seed-service-rating)  
**Responsibility:** This service provides backend services store requests for
service rating (invites) and the results of those ratings once undertaken.


### Seed Control Interface Service

**GitHub:** [https://github.com/praekelt/seed-control-interface-service](https://github.com/praekelt/seed-control-interface-service)  
**Responsibility:** This service provides backend services to the Control Interface
web service. It keeps track of other service configuration including their URL,
metrics, health and user tokens. Dashboards configurations are also stored here.


### Seed Auth API

**GitHub:** [https://github.com/praekelt/seed-auth-api](https://github.com/praekelt/seed-auth-api)  
**Responsibility:** This service provides authentication and user and permission
management for role-based access to the Control Interface.


## Project Specific Hub

Each project should also have a custom Django project that has been called both
"Registration" and more recently "Hub". This project is responsible for project
specific business logic such as registration and change validation and integration
into 3rd party systems. Examples of this are:

* HelloMama (Nigeria): [https://github.com/praekelt/hellomama-registration](https://github.com/praekelt/hellomama-registration)
* FamilyConnect (Uganda): [https://github.com/praekelt/familyconnect-registration](https://github.com/praekelt/familyconnect-registration)
* NDOH - MomConnect/NurseConnect (South Africa): [https://github.com/praekeltfoundation/ndoh-hub](https://github.com/praekeltfoundation/ndoh-hub)


## Prereqs

The following pre-reqs must be in place before attempting deployment and configuration
of a Seed Maternal Health Stack.

1. Seperate Postgres databases for each Backend Service, Control Interface and Help Desk.
2. Seperate RabbitMQ vhosts for each Backend Service.
3. Shared RabbitMQ vhost for Junebug
4. Shared Redis KV store
5. Graphite
6. Sentry (optional)


## Deployment order

It is recommended that the deployment takes place in the following order:

1. Shared Backend Services
2. Project specific hub
3. Control interface
4. Connectivity
5. Applications
6. Help Desk (optional)
