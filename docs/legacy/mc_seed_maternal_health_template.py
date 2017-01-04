#!/usr/bin/env python

from HTMLParser import HTMLParser
from urlparse import urlparse

import requests

MC2_URL = 'https://mc.example.io/'


class MC2Wrangler(object):
    ORG_PATH = '/admin/organizations/organization/'
    ADD_ORG_PATH = ORG_PATH + 'add/'
    SELECT_ORG_PATH = '/organizations/%s/select/'
    ADD_APP_PATH = '/docker/add/'

    def __init__(self, mc2_url):
        self.base_url = mc2_url
        self.session = requests.Session()
        self.session.headers.update({'referer': 'https://mc.example.io/'})

    def url(self, path):
        if urlparse(path).scheme:
            return path
        return ''.join([self.base_url, path])

    def get(self, path, **kw):
        return self.session.get(self.url(path), **kw)

    def post(self, path, **kw):
        return self.session.post(self.url(path), **kw)

    def post_form(self, path, data, **kw):
        r = self.get(path)
        data = data.copy()
        data['csrfmiddlewaretoken'] = r.cookies['csrftoken']
        return self.post(path, data=data, **kw)

    def login(self, user, pw):
        login_url = self.get('/').url
        return self.post_form(login_url, {'username': user, 'password': pw})

    def list_orgs(self):
        r = self.get(self.ORG_PATH)
        dalp = DjangoAdminListParser()
        dalp.feed(r.text)
        return dalp.items

    def add_org(self, name):
        orgs = self.list_orgs()
        if name in orgs:
            print "Org %s already exists, not creating." % (name,)
            return

        return self.post_form(self.ADD_ORG_PATH, data={
            "name": name,
            "slug": name,
            "organizationuserrelation_set-TOTAL_FORMS": "1",
            "organizationuserrelation_set-INITIAL_FORMS": "0",
            "organizationuserrelation_set-MIN_NUM_FORMS": "0",
            "organizationuserrelation_set-MAX_NUM_FORMS": "1000",
            "organizationuserrelation_set-0-user": "1",
            "organizationuserrelation_set-0-is_admin": "on",
            "organizationuserrelation_set-0-organization": "",
            "organizationuserrelation_set-0-id": "",
            "organizationuserrelation_set-__prefix__-user": "",
            "organizationuserrelation_set-__prefix__-organization": "",
            "organizationuserrelation_set-__prefix__-id": "",
            "_save": "Save",
        })

    def select_org(self, name):
        return self.get(self.SELECT_ORG_PATH % (name,))

    def add_app(self, **kw):
        app_fields = {
            "name": "",
            "description": "",
            "domain_urls": "",
            "docker_image": "",
            "port": "8080",
            "volume_needed": "False",
            "volume_path": "",
            "env-TOTAL_FORMS": "1",
            "env-INITIAL_FORMS": "0",
            "env-MIN_NUM_FORMS": "0",
            "env-MAX_NUM_FORMS": "1000",
            "env-0-id": "",
            "env-0-key": "",
            "env-0-value": "",
            "label-TOTAL_FORMS": "1",
            "label-INITIAL_FORMS": "0",
            "label-MIN_NUM_FORMS": "0",
            "label-MAX_NUM_FORMS": "1000",
            "label-0-id": "",
            "label-0-name": "",
            "label-0-value": "",
            "link-TOTAL_FORMS": "1",
            "link-INITIAL_FORMS": "0",
            "link-MIN_NUM_FORMS": "0",
            "link-MAX_NUM_FORMS": "1000",
            "marathon_cmd": "",
            "marathon_cpus": "0.1",
            "marathon_mem": "128.0",
            "marathon_instances": "1",
            "marathon_health_check_path": "",
            "webhook_token": "",
            "organization": "12",
            "postgres_db_needed": "False",
        }
        app_fields.update(kw)
        return self.post_form(self.ADD_APP_PATH, data=app_fields)


class DjangoAdminListParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.items = []
        self.found_item = False

    def handle_starttag(self, tag, attrs):
        if tag == 'th' and ('class', 'field-name') in attrs:
            self.found_item = True

    def handle_data(self, data):
        if self.found_item:
            self.items.append(data)
            self.found_item = False


w = MC2Wrangler(MC2_URL)
r = w.login('REPLACEME', 'REPLACEME')
print 'login:', r

r = w.select_org('REPLACEME')
print 'select org:', r

prefix = "prefix"
domain = "%s.p16n.org" % prefix
dockerhub = "prd-mesos-mc01.za.p16n.org:5000"
redis = "REPLACEME"
amqp = "REPLACEME"
amqp_user = "REPLACEME"
amqp_pass = "REPLACEME"
postgres = "REPLACEME"
sentry = "unknown"


junebug = {
    "name": "%s - Junebug" % prefix,
    "domain_urls": "junebug.%s" % domain,
    "docker_image": "%s/junebug" % dockerhub,
    "port": "80",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "8",
    "env-0-id": "",
    "env-0-key": "REDIS_HOST",
    "env-0-value": redis,
    "env-1-id": "",
    "env-1-key": "REDIS_PORT",
    "env-1-value": "6379",
    "env-2-id": "",
    "env-2-key": "REDIS_DB",
    "env-2-value": "1",
    "env-3-id": "",
    "env-3-key": "AMQP_HOST",
    "env-3-value": amqp,
    "env-4-id": "",
    "env-4-key": "AMQP_PORT",
    "env-4-value": "5672",
    "env-5-id": "",
    "env-5-key": "AMQP_VHOST",
    "env-5-value": "/%s_junebug" % prefix,
    "env-6-id": "",
    "env-6-key": "AMQP_USER",
    "env-6-value": amqp_user,
    "env-7-id": "",
    "env-7-key": "AMQP_PASSWORD",
    "env-7-value": amqp_pass
}

SECRET_KEY_IDENTITIES = "REPLACEME"
DB_PASS_IDENTITIES = "REPLACEME"
IDENTITIES_SENTRY_DSN = "REPLACEME"

identity_store = {
    "name": "%s - Identity Store" % prefix,
    "domain_urls": "identity-store.%s" % domain,
    "docker_image": "praekeltfoundation/seed-identity-store",
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "5",
    "env-0-id": "",
    "env-0-key": "DJANGO_SETTINGS_MODULE",
    "env-0-value": "seed_identity_store.settings",
    "env-1-id": "",
    "env-1-key": "SECRET_KEY",
    "env-1-value": SECRET_KEY_IDENTITIES,
    "env-2-id": "",
    "env-2-key": "IDENTITIES_DATABASE",
    "env-2-value":
        "postgres://identitystore:%s@%s/identitystore" % (
            DB_PASS_IDENTITIES, postgres),
    "env-3-id": "",
    "env-3-key": "IDENTITIES_SENTRY_DSN",
    "env-3-value": IDENTITIES_SENTRY_DSN,
    "env-4-id": "",
    "env-4-key": "BROKER_URL",
    "env-4-value": "amqp://%s:%s@%s:5672//%s_seed_identity_store" % (
        amqp_user, amqp_pass, amqp, prefix,)
}

identity_store_celery = identity_store.copy()
identity_store_celery["name"] += " (Celery Workers)"
identity_store_celery["domain_urls"] = ""
identity_store_celery["marathon_cmd"] = \
    "celery worker --app seed_identity_store --loglevel info " \
    "-Q seed_identity_store,priority,mediumpriority,metrics"

SECRET_KEY_SBM = "REPLACEME"
DB_PASS_SBM = "REPLACEME"
STAGE_BASED_MESSAGING_SENTRY_DSN = "None"
SCHEDULER_API_TOKEN_SBM = "REPLACEME"
SCHEDULER_INBOUND_API_TOKEN_SBM = "REPLACEME"
IDENTITY_STORE_TOKEN_SBM = "REPLACEME"
MESSAGE_SENDER_TOKEN_SBM = "REPLACEME"

stage_based_messaging = {
    "name": "%s - Stage Based Messaging" % prefix,
    "domain_urls": "stage-based-messaging.%s" % domain,
    "docker_image": "praekeltfoundation/seed-stage-based-messaging",
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "13",
    "env-0-id": "",
    "env-0-key": "DJANGO_SETTINGS_MODULE",
    "env-0-value": "seed_stage_based_messaging.settings",
    "env-1-id": "",
    "env-1-key": "SECRET_KEY",
    "env-1-value": SECRET_KEY_SBM,
    "env-2-id": "",
    "env-2-key": "STAGE_BASED_MESSAGING_DATABASE",
    "env-2-value":
        "postgres://stage_based_messaging:%s@%s/"
        "stage_based_messaging" % (
            DB_PASS_SBM, postgres,),
    "env-3-id": "",
    "env-3-key": "STAGE_BASED_MESSAGING_SENTRY_DSN",
    "env-3-value": STAGE_BASED_MESSAGING_SENTRY_DSN,
    "env-4-id": "",
    "env-4-key": "BROKER_URL",
    "env-4-value": "amqp://%s:%s@%s:5672//%s_seed_stage_based_messaging" % (
        amqp_user, amqp_pass, amqp, prefix,),
    "env-5-id": "",
    "env-5-key": "SCHEDULER_URL",
    "env-5-value": "http://scheduler.%s/api/v1" % (domain,),
    "env-6-id": "",
    "env-6-key": "SCHEDULER_API_TOKEN",
    "env-6-value": SCHEDULER_API_TOKEN_SBM,
    "env-7-id": "",
    "env-7-key": "SCHEDULER_INBOUND_API_TOKEN",
    "env-7-value": SCHEDULER_INBOUND_API_TOKEN_SBM,
    "env-8-id": "",
    "env-8-key": "IDENTITY_STORE_URL",
    "env-8-value": "http://identity-store.%s/api/v1" % (domain,),
    "env-9-id": "",
    "env-9-key": "IDENTITY_STORE_TOKEN",
    "env-9-value": IDENTITY_STORE_TOKEN_SBM,
    "env-10-id": "",
    "env-10-key": "MESSAGE_SENDER_URL",
    "env-10-value": "http://message-sender.%s/api/v1" % (domain,),
    "env-11-id": "",
    "env-11-key": "MESSAGE_SENDER_TOKEN",
    "env-11-value": MESSAGE_SENDER_TOKEN_SBM,
    "env-12-id": "",
    "env-12-key": "STAGE_BASED_MESSAGING_URL",
    "env-12-value": "http://stage-based-messaging.%s/api/v1/subscriptions" % (
        domain,)
}

stage_based_messaging_celery = stage_based_messaging.copy()
stage_based_messaging_celery["name"] += " (Celery Workers)"
stage_based_messaging_celery["domain_urls"] = ""
stage_based_messaging_celery["marathon_cmd"] = \
    "celery worker --app seed_stage_based_messaging --loglevel info " \
    "-Q seed_stage_based_messaging,priority,mediumpriority,metrics,celery"

SECRET_KEY_MS = "REPLACEME"
DB_PASS_MS = "REPLACEME"
MESSAGE_SENDER_SENTRY_DSN = "REPLACEME"
MESSAGE_SENDER_VUMI_API_URL_TEXT = "http://http-api-sms.%s/prefix/infr/vumi-api-sms" % domain
MESSAGE_SENDER_VUMI_ACCOUNT_KEY_TEXT = "REPLACEME"
MESSAGE_SENDER_VUMI_CONVERSATION_KEY_TEXT = "REPLACEME"
MESSAGE_SENDER_VUMI_ACCOUNT_TOKEN_TEXT = "REPLACEME"

message_sender = {
    "name": "%s - Message Sender" % prefix,
    "domain_urls": "message-sender.%s" % domain,
    "docker_image": "praekeltfoundation/seed-message-sender",
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "9",
    "env-0-id": "",
    "env-0-key": "DJANGO_SETTINGS_MODULE",
    "env-0-value": "seed_message_sender.settings",
    "env-1-id": "",
    "env-1-key": "SECRET_KEY",
    "env-1-value": SECRET_KEY_MS,
    "env-2-id": "",
    "env-2-key": "MESSAGE_SENDER_DATABASE",
    "env-2-value":
        "postgres://message_sender:%s@%s/message_sender" % (
            DB_PASS_MS, postgres,),
    "env-3-id": "",
    "env-3-key": "MESSAGE_SENDER_SENTRY_DSN",
    "env-3-value": MESSAGE_SENDER_SENTRY_DSN,
    "env-4-id": "",
    "env-4-key": "BROKER_URL",
    "env-4-value": "amqp://%s:%s@%s:5672//%s_seed_message_sender" % (
        amqp_user, amqp_pass, amqp, prefix,),
    "env-5-id": "",
    "env-5-key": "MESSAGE_SENDER_VUMI_API_URL_TEXT",
    "env-5-value": MESSAGE_SENDER_VUMI_API_URL_TEXT,
    "env-6-id": "",
    "env-6-key": "MESSAGE_SENDER_VUMI_ACCOUNT_KEY_TEXT",
    "env-6-value": MESSAGE_SENDER_VUMI_ACCOUNT_KEY_TEXT,
    "env-7-id": "",
    "env-7-key": "MESSAGE_SENDER_VUMI_CONVERSATION_KEY_TEXT",
    "env-7-value": MESSAGE_SENDER_VUMI_CONVERSATION_KEY_TEXT,
    "env-8-id": "",
    "env-8-key": "MESSAGE_SENDER_VUMI_ACCOUNT_TOKEN_TEXT",
    "env-8-value": MESSAGE_SENDER_VUMI_ACCOUNT_TOKEN_TEXT
}

message_sender_celery = message_sender.copy()
message_sender_celery["name"] += " (Celery Workers)"
message_sender_celery["domain_urls"] = ""
message_sender_celery["marathon_cmd"] = \
    "celery worker --app seed_message_sender --loglevel info " \
    "-Q seed_message_sender,priority,mediumpriority,metrics,celery"

SECRET_KEY_SCH = "REPLACEME"
DB_PASS_SCH = "REPLACEME"
SCHEDULER_SENTRY_DSN = "REPLACEME"

scheduler = {
    "name": "%s - Scheduler" % prefix,
    "domain_urls": "scheduler.%s" % domain,
    "docker_image": "praekeltfoundation/seed-scheduler",
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "5",
    "env-0-id": "",
    "env-0-key": "DJANGO_SETTINGS_MODULE",
    "env-0-value": "seed_scheduler.settings",
    "env-1-id": "",
    "env-1-key": "SECRET_KEY",
    "env-1-value": SECRET_KEY_SCH,
    "env-2-id": "",
    "env-2-key": "SCHEDULER_DATABASE",
    "env-2-value": "postgres://scheduler:%s@%s/scheduler" % (
        DB_PASS_SCH, postgres,),
    "env-3-id": "",
    "env-3-key": "SCHEDULER_SENTRY_DSN",
    "env-3-value": SCHEDULER_SENTRY_DSN,
    "env-4-id": "",
    "env-4-key": "BROKER_URL",
    "env-4-value": "amqp://%s:%s@%s:5672//%s_seed_scheduler" % (
        amqp_user, amqp_pass, amqp, prefix,)
}

scheduler_celery = scheduler.copy()
scheduler_celery["name"] += " (Celery Workers)"
scheduler_celery["domain_urls"] = ""
scheduler_celery["marathon_cmd"] = \
    "celery worker --app seed_scheduler --loglevel info " \
    "-Q seed_scheduler,priority,mediumpriority,metrics,celery"

scheduler_celery_beat = scheduler_celery.copy()
scheduler_celery["name"] += " (Celery Beat)"
scheduler_celery["marathon_cmd"] = \
    "celery beat --app seed_scheduler --loglevel info"

SECRET_KEY_SVCRATE = "REPLACEME"
DB_PASS_SVCRATE = "REPLACEME"
SERVICE_RATING_SENTRY_DSN = "REPLACEME"

service_rating = {
    "name": "%s - Service Rating" % prefix,
    "domain_urls": "service-rating.%s" % domain,
    "docker_image": "praekeltfoundation/seed-service-rating",
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "5",
    "env-0-id": "",
    "env-0-key": "DJANGO_SETTINGS_MODULE",
    "env-0-value": "seed_service_rating.settings",
    "env-1-id": "",
    "env-1-key": "SECRET_KEY",
    "env-1-value": SECRET_KEY_SVCRATE,
    "env-2-id": "",
    "env-2-key": "SERVICE_RATING_DATABASE",
    "env-2-value":
        "postgres://service_rating:%s@%s/service_rating" % (
            DB_PASS_SVCRATE, postgres,),
    "env-3-id": "",
    "env-3-key": "SERVICE_RATING_SENTRY_DSN",
    "env-3-value": SERVICE_RATING_SENTRY_DSN,
    "env-4-id": "",
    "env-4-key": "BROKER_URL",
    "env-4-value": "amqp://%s:%s@%s:5672//%s_seed_service_rating" % (
        amqp_user, amqp_pass, amqp, prefix,)
}

service_rating_celery = service_rating.copy()
service_rating_celery["name"] += " (Celery Workers)"
service_rating_celery["domain_urls"] = ""
service_rating_celery["marathon_cmd"] = \
    "celery worker --app seed_service_rating --loglevel info " \
    "-Q seed_service_rating,priority,mediumpriority,metrics,celery"

SECRET_KEY_HUB = "REPLACEME"
DB_PASS_HUB = "REPLACEME"
HUB_SENTRY_DSN = "REPLACEME"
STAGE_BASED_MESSAGING_TOKEN_HUB = "REPLACEME"
IDENTITY_STORE_TOKEN_HUB = "REPLACEME"
MESSAGE_SENDER_TOKEN_HUB = "REPLACEME"

hub = {
    "name": "%s - Hub" % prefix,
    "domain_urls": "hub.%s" % domain,
    "docker_image": "%s/%s-hub" % (dockerhub, prefix,),
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "11",
    "env-0-id": "",
    "env-0-key": "DJANGO_SETTINGS_MODULE",
    "env-0-value": "%s_hub.settings" % prefix,
    "env-1-id": "",
    "env-1-key": "SECRET_KEY",
    "env-1-value": SECRET_KEY_HUB,
    "env-2-id": "",
    "env-2-key": "HUB_DATABASE",
    "env-2-value":
        "postgres://hub:%s@%s/hub" % (
            DB_PASS_HUB, postgres,),
    "env-3-id": "",
    "env-3-key": "HUB_SENTRY_DSN",
    "env-3-value": HUB_SENTRY_DSN,
    "env-4-id": "",
    "env-4-key": "BROKER_URL",
    "env-4-value": "amqp://%s:%s@%s:5672//%s_hub" % (
        amqp_user, amqp_pass, amqp, prefix,),
    "env-5-id": "",
    "env-5-key": "STAGE_BASED_MESSAGING_URL",
    "env-5-value": "http://stage-based-messaging.%s/api/v1" % (domain,),
    "env-6-id": "",
    "env-6-key": "STAGE_BASED_MESSAGING_TOKEN",
    "env-6-value": STAGE_BASED_MESSAGING_TOKEN_HUB,
    "env-7-id": "",
    "env-7-key": "IDENTITY_STORE_URL",
    "env-7-value": "http://identity-store.%s/api/v1" % (domain,),
    "env-8-id": "",
    "env-8-key": "IDENTITY_STORE_TOKEN",
    "env-8-value": IDENTITY_STORE_TOKEN_HUB,
    "env-9-id": "",
    "env-9-key": "MESSAGE_SENDER_URL",
    "env-9-value": "http://message-sender.%s/api/v1" % (domain,),
    "env-10-id": "",
    "env-10-key": "MESSAGE_SENDER_TOKEN",
    "env-10-value": MESSAGE_SENDER_TOKEN_HUB,
}

hub_celery = hub.copy()
hub_celery["name"] += " (Celery Workers)"
hub_celery["domain_urls"] = ""
hub_celery["marathon_cmd"] = \
    "celery worker --app %s_hub --loglevel info " \
    "-Q %s_hub,priority,mediumpriority,metrics,celery" % (prefix, prefix,)


graphite_metrics_collector = {
    "name": "%s - Graphite Metrics Collector" % prefix,
    "domain_urls": "",
    "docker_image": "praekeltfoundation/vumi",
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "5",
    "env-0-id": "",
    "env-0-key": "WORKER_CLASS",
    "env-0-value": "vumi.blinkenlights.GraphiteMetricsCollector",
    "env-1-id": "",
    "env-1-key": "AMQP_HOST",
    "env-1-value": amqp,
    "env-2-id": "",
    "env-2-key": "AMQP_VHOST",
    "env-2-value": "/%s" % prefix,
    "env-3-id": "",
    "env-3-key": "AMQP_USERNAME",
    "env-3-value": amqp_user,
    "env-4-id": "",
    "env-4-key": "AMQP_PASSWORD",
    "env-4-value": amqp_pass
}

metrics_aggregator_1 = {
    "name": "%s - Metric Aggregator 1" % prefix,
    "domain_urls": "",
    "docker_image": "praekeltfoundation/vumi",
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "7",
    "env-0-id": "",
    "env-0-key": "WORKER_CLASS",
    "env-0-value": "vumi.blinkenlights.MetricAggregator",
    "env-1-id": "",
    "env-1-key": "AMQP_HOST",
    "env-1-value": amqp,
    "env-2-id": "",
    "env-2-key": "AMQP_VHOST",
    "env-2-value": "/%s" % amqp_user,
    "env-3-id": "",
    "env-3-key": "AMQP_USERNAME",
    "env-3-value": amqp_user,
    "env-4-id": "",
    "env-4-key": "AMQP_PASSWORD",
    "env-4-value": amqp_pass,
    "env-5-id": "",
    "env-5-key": "VUMI_OPT_BUCKET",
    "env-5-value": "1",
    "env-6-id": "",
    "env-6-key": "VUMI_OPT_BUCKET_SIZE",
    "env-6-value": "10"
}

metrics_aggregator_2 = {
    "name": "%s - Metric Aggregator 2" % prefix,
    "domain_urls": "",
    "docker_image": "praekeltfoundation/vumi",
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "7",
    "env-0-id": "",
    "env-0-key": "WORKER_CLASS",
    "env-0-value": "vumi.blinkenlights.MetricAggregator",
    "env-1-id": "",
    "env-1-key": "AMQP_HOST",
    "env-1-value": amqp,
    "env-2-id": "",
    "env-2-key": "AMQP_VHOST",
    "env-2-value": "/%s" % amqp_user,
    "env-3-id": "",
    "env-3-key": "AMQP_USERNAME",
    "env-3-value": amqp_user,
    "env-4-id": "",
    "env-4-key": "AMQP_PASSWORD",
    "env-4-value": amqp_pass,
    "env-5-id": "",
    "env-5-key": "VUMI_OPT_BUCKET",
    "env-5-value": "2",
    "env-6-id": "",
    "env-6-key": "VUMI_OPT_BUCKET_SIZE",
    "env-6-value": "10"
}

metrics_aggregator_3 = {
    "name": "%s - Metric Aggregator 3" % prefix,
    "domain_urls": "",
    "docker_image": "praekeltfoundation/vumi",
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "7",
    "env-0-id": "",
    "env-0-key": "WORKER_CLASS",
    "env-0-value": "vumi.blinkenlights.MetricAggregator",
    "env-1-id": "",
    "env-1-key": "AMQP_HOST",
    "env-1-value": amqp,
    "env-2-id": "",
    "env-2-key": "AMQP_VHOST",
    "env-2-value": "/%s" % amqp_user,
    "env-3-id": "",
    "env-3-key": "AMQP_USERNAME",
    "env-3-value": amqp_user,
    "env-4-id": "",
    "env-4-key": "AMQP_PASSWORD",
    "env-4-value": amqp_pass,
    "env-5-id": "",
    "env-5-key": "VUMI_OPT_BUCKET",
    "env-5-value": "3",
    "env-6-id": "",
    "env-6-key": "VUMI_OPT_BUCKET_SIZE",
    "env-6-value": "10"
}

metrics_time_bucket = {
    "name": "%s - Metric Time Bucket" % prefix,
    "domain_urls": "",
    "docker_image": "praekeltfoundation/vumi",
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "7",
    "env-0-id": "",
    "env-0-key": "WORKER_CLASS",
    "env-0-value": "vumi.blinkenlights.MetricTimeBucket",
    "env-1-id": "",
    "env-1-key": "AMQP_HOST",
    "env-1-value": amqp,
    "env-2-id": "",
    "env-2-key": "AMQP_VHOST",
    "env-2-value": "/%s" % amqp_user,
    "env-3-id": "",
    "env-3-key": "AMQP_USERNAME",
    "env-3-value": amqp_user,
    "env-4-id": "",
    "env-4-key": "AMQP_PASSWORD",
    "env-4-value": amqp_pass,
    "env-5-id": "",
    "env-5-key": "VUMI_OPT_BUCKETS",
    "env-5-value": "3",
    "env-6-id": "",
    "env-6-key": "VUMI_OPT_BUCKET_SIZE",
    "env-6-value": "10"
}

metrics_api = {
    "name": "%s - Metrics API" % prefix,
    "domain_urls": "metrics.%s" % domain,
    "docker_image": "praekeltfoundation/go-metrics-api:0.1.9",
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "7",
    "env-0-id": "",
    "env-0-key": "WORKER_CLASS",
    "env-0-value": "vumi.blinkenlights.MetricTimeBucket",
    "env-1-id": "",
    "env-1-key": "AMQP_HOST",
    "env-1-value": amqp,
    "env-2-id": "",
    "env-2-key": "AMQP_VHOST",
    "env-2-value": "/%s" % amqp_user,
    "env-3-id": "",
    "env-3-key": "AMQP_USERNAME",
    "env-3-value": amqp_user,
    "env-4-id": "",
    "env-4-key": "AMQP_PASSWORD",
    "env-4-value": amqp_pass,
    "env-5-id": "",
    "env-5-key": "VUMI_OPT_BUCKETS",
    "env-5-value": "3",
    "env-6-id": "",
    "env-6-key": "VUMI_OPT_BUCKET_SIZE",
    "env-6-value": "10"
}

control_interface_service = {
    "name": "%s - Control Interface Service" % prefix,
    "domain_urls": "control-interface-service.%s" % domain,
    "docker_image": "%s/seed-control-interface-service" % dockerhub,
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "5",
    "env-0-id": "",
    "env-0-key": "DJANGO_SETTINGS_MODULE",
    "env-0-value": "seed_control_interface_service.settings",
    "env-1-id": "",
    "env-1-key": "SECRET_KEY",
    "env-1-value": SECRET_KEY_CISVC,
    "env-2-id": "",
    "env-2-key": "SEED_CONTROL_INTERFACE_SERVICE_DATABASE",
    "env-2-value": "postgres://%s_seed_control_interface_service:%s@%s/%s_seed_control_interface_service" % (
        prefix, DB_PASS_CISVC, postgres, prefix,),
    "env-3-id": "",
    "env-3-key": "SEED_CONTROL_INTERFACE_SERVICE_SENTRY_DSN",
    "env-3-value": SEED_CONTROL_INTERFACE_SERVICE_SENTRY_DSN,
    "env-4-id": "",
    "env-4-key": "BROKER_URL",
    "env-4-value": "amqp://%s:%s@%s:5672//%s_seed_control_interface_service" % (
        amqp_user, amqp_pass, amqp, prefix,)
}

control_interface_service_celery = control_interface_service.copy()
control_interface_service_celery["name"] += " (Celery Workers)"
control_interface_service_celery["domain_urls"] = ""
control_interface_service_celery["marathon_cmd"] = \
    "celery worker --app seed_control_interface_service --loglevel info " \
    "-Q seed_control_interface_service,priority,mediumpriority,metrics,celery"

control_interface_service_celery_beat = control_interface_service_celery.copy()
control_interface_service_celery["name"] += " (Celery Beat)"
control_interface_service_celery["marathon_cmd"] = \
    "celery beat --app seed_control_interface_service --loglevel info"

control_interface = {
    "name": "%s - Control Interface" % prefix,
    "domain_urls": "control-interface.%s" % domain,
    "docker_image": "%s/seed-control-interface" % dockerhub,
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "10",
    "env-0-id": "",
    "env-0-key": "DJANGO_SETTINGS_MODULE",
    "env-0-value": "seed_control_interface.settings",
    "env-1-id": "",
    "env-1-key": "SECRET_KEY",
    "env-1-value": SECRET_KEY_CI,
    "env-2-id": "",
    "env-2-key": "SEED_CONTROL_INTERFACE_DATABASE",
    "env-2-value": "postgres://%s_seed_control_interface:%s@%s/%s_seed_control_interface" % (
        prefix, DB_PASS_CI, postgres, prefix,),
    "env-3-id": "",
    "env-3-key": "SEED_CONTROL_INTERFACE_SENTRY_DSN",
    "env-3-value": SEED_CONTROL_INTERFACE_SENTRY_DSN,
    "env-4-id": "",
    "env-4-key": "BROKER_URL",
    "env-4-value": "amqp://%s:%s@%s:5672//%s_seed_control_interface" % (
        amqp_user, amqp_pass, amqp, prefix,),
    "env-5-id": "",
    "env-5-key": "CONTROL_INTERFACE_SERVICE_TOKEN",
    "env-5-value": "REPLACEME",
    "env-6-id": "",
    "env-6-key": "CONTROL_INTERFACE_SERVICE_URL",
    "env-6-value": "http://control-interface-service.%s/api/v1" % domain,
    "env-7-id": "",
    "env-7-key": "AUTH_SERVICE_URL",
    "env-7-value": "http://auth.%s" % domain,
    "env-8-id": "",
    "env-8-key": "CI_LOGO_URL",
    "env-8-value": "REPLACEME",
    "env-9-id": "",
    "env-9-key": "METRIC_API_URL",
    "env-9-value": "REPLACEME"
}

auth_api = {
    "name": "%s - Auth" % prefix,
    "domain_urls": "auth.%s" % domain,
    "docker_image": "%s/seed-auth-api" % dockerhub,
    "port": "8000",
    "label-0-id": "",
    "label-0-name": "",
    "label-0-value": "",
    "env-TOTAL_FORMS": "3",
    "env-0-id": "",
    "env-0-key": "DJANGO_SETTINGS_MODULE",
    "env-0-value": "seed_auth_api.settings",
    "env-1-id": "",
    "env-1-key": "SECRET_KEY",
    "env-1-value": SECRET_KEY_AUTH,
    "env-2-id": "",
    "env-2-key": "AUTH_API_DATABASE",
    "env-2-value": "postgres://%s_seed_auth_api:%s@%s/%s_seed_auth_api" % (
        prefix, DB_PASS_AUTH, postgres, prefix,)


base_stack = [junebug, identity_store, identity_store_celery,
              stage_based_messaging, stage_based_messaging_celery,
              message_sender, message_sender_celery,
              scheduler, scheduler_celery, scheduler_celery_beat,
              service_rating, service_rating_celery,
              hub, hub_celery]

# ci_stack = [metrics_api, graphite_metrics_collector,
#          metrics_aggregator_1, metrics_aggregator_2, metrics_aggregator_3,
#          metrics_time_bucket, control_interface_service,
#          control_interface_service_celery, control_interface_service_celery_beat,
#          control_interface, auth_api]

for service in base_stack:
    print "adding %s" % service["name"]
    r = w.add_app(**service)
    if r.status_code == 200:
        print "live at: http://%s" % service["domain_urls"]
    else:
        print 'result:', r.text

print "all done"
