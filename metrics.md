# Seed Maternal Health Metrics Configuration

## Overview

### Where metrics are stored

Metrics are stored in Graphite via Graphite's Carbon metrics collector and its RabbitMQ listener.

### How metrics are retrieved from Graphite

The metrics API worker provides a standard programmatic API on top of Graphite's web interface. 

### Firing metrics

Metrics are fired via the metrics API or the Javascript sandbox metrics resource. Both of these publish metrics to the Vumi metrics workers via RabbitMQ.

### Vumi metrics workers

The Vumi metrics workers aggregate metrics into fixed time-steps since Graphite does not support metrics fired at arbitrary times. There are two sets of workers.

The time-bucketing workers hash metrics to a set of RabbitMQ queues based on the metric name and timestamp (each metric name and time bucket range is mapped to a consistent queue).

The aggregation workers read from these queues and aggregate the metrics into a fixed time series for Graphite (since Graphite can only handle fixed size gaps between metrics).

Roughly these workers perform the same task as statsd or a Storm field grouping on the metric name and time bucket fields.

## Deployment and Configuration

The deployment setup of all the components for metrics are detailed in the mc_seed_maternal_health_template script except for Graphite. Graphite can be deployed on Mission Control too now with the following setup:

### Graphite

[Graphite](https://graphiteapp.org/) is where time series data is stored.

**Docker image:** [praekeltfoundation/graphite](https://hub.docker.com/r/praekeltfoundation/graphite/)  
**Require storage:** Yes  
**Volume path:** /opt/graphite/storage

**Environment Variables:**

* GRAPHITE_WEB_SECRET_KEY - Django secret key
* ENABLE_AMQP - should it use AMQP (set to `True`)
* AMQP_VERBOSE - should it use AMQP verbose (set to `True`)
* AMQP_HOST - RabbitMQ FQDN
* AMQP_PORT - Usually `5672`
* AMQP_USER - RabbitMQ username
* AMQP_PASSWORD - RabbitMQ password
* AMQP_VHOST - RabbitMQ vhost the user has access to (including leading slash)
* DATABASE_URL - SQLite DB (usually `sqlite:////opt/graphite/storage/graphite.db`)
* AMQP_METRIC_NAME_IN_BODY - set to `""`

