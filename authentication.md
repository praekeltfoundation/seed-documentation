# Seed Maternal Health Authentication Configuration

## Overview

### Where service authentication tokens are stored

Each seed service is reponsible for it's own authentication and permission and uses [Django REST Framework's Token Auth](http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) support that hooks into Django User model and allows us to associate creation and updating of data to a user account.

### Where Control Interface authentication tokens are stored

The Control Interface uses the Seed Auth API to manage users and permission for access and decorators on each view to link permissions to a view.

### Bootstrapping Auth API

When the Auth API is deployed it still needs configuring with:

1. an Organization (the z is important)
2. Teams in the Organization
3. Permissions for the Team (currently just `ci:view` permissions)
4. Users in the Team

Full API documentation is [here](http://seed-auth-api.readthedocs.io/en/develop/) but here is a guide for what to do:

* Login with your superuser to `/admin` in the browser
* Create a token manually for your superuser in the Auth Tokens/Tokens app in Django admin
* The rest of the instructions should be done against the API using a tool like curl or Postman if you prefer to be able to save your requests for later review.
* Create an organisation by POSTing the `title` of it to `/organizations/` (note, US-centric organization spelling) using the Authorization header "Token insertyourSUtoken" and Content-Type "application/json" and note the returned organisation numerical ID (if it's the first, it's likely to be 1)
* Create a team in the organisation by POSTing the `title` to `/organizations/(int: organization_id)/teams/` 
* Create a user by POSTing to `/users/ `and note the returned user numerical ID
* Add the user to a team by PUTing `/teams/(int: team_id)/users/(int: user_id)/` (you will get no response from this request)
* Assign the team some permissions by POSTing to `/teams/(int: team_id)/permissions/` 
* Validate the end-to-end by POSTing email and password to `/user/tokens/` (ensure you drop your previous Token auth setting from your request and note `user` not `users`). Then with the returned token as your auth make a GET to `/user/` to check permissions are listed.  

### Adding users to API

The [Seed Services CLI](https://github.com/praekelt/seed-services-cli) tool can be used for [adding new users](https://github.com/praekelt/seed-services-cli#adding-users-to-auth-with-team-access).

Once the user has been added then use the CLI to also [create Seed Service tokens](https://github.com/praekelt/seed-services-cli#generate-user-tokens) for that new user so they can use the CI. 

### How the Control Interface permissions flow

Currently the following process happens when a user logs on to the CI

1. Email and password validated against Seed Auth API and token returned
2. User permissions are looked up using Seed Auth API token and stored in the user Session for duration of that session
3. User permissions are checked using a decorator on each view in Control Interface
4. Users Seed Service tokens are retrieved from Control Interface Service API and are used to make calls directly from the Control Interface to the Seed Services. Tokens are never passed to the users browser.



