Telemetry Server
by Javier Onglao
------------------------------
[![Build Status](https://circleci.com/gh/starpogi/fr_telemetry.svg?style=svg)](https://circleci.com/gh/starpogi/fr_telemetry)


Server that handles Telemetry events, and an endpoint for analytics.


## Assumptions
- Events from clients are forward in time, which means clients can't
retroactively push past events. Events pushed from the past are dropped.
- Events are pushed in-order, but may be processed out-of-order due to
process failures, and non-deterministic latencies in a parallelized processing
environment.
- Robot names are case-sensitive unique and can only occupy one instance.
For instance, `McDonalds != mcdonalds`.
- An event occupies only one timestamp per robot. This means that a robot
cannot possibly have 2 events at the same millisecond.


## Requirements
- Python 3.6 (this is important if you want celery to work correctly)

  On OSX, you will need Brew. If you don't have Brew, you can run this

  ```
  $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  ```

  and then run the following commands to get the correct version of Python

  ```
  $ brew install python
  $ brew unlink python
  $ brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/e128fa1bce3377de32cbf11bd8e46f7334dfd7a6/Formula/python.rb
  $ brew switch python 3.6.5
  ```

- MySQL 8.0.12

  On OSX, you can run this to install MySQL
  ```
  brew install mysql
  ```

- Redis 4.0.11

  On OSX, you can run this to install Redis
  ```
  brew install redis
  ```


## Setup
```
$ . setup.sh create
```

## Run

### Development
The dev environment does not support WebSockets because of how the WSGI routing works with Werkzeug. You will need to use `gunicorn` if you want to run it with WebSockets.
```
$ . setup.sh env dev
$ flask run
```

### Test
```
$ . setup.sh env dev
$ pytest
```

### Production
You will need to run `celery` in the background either by using `&` at the end, or opening a new terminal, or using a process-management system like `circus` or `systemd`.

```
$ . setup.sh env prod
$ gunicorn -w 4 -k flask_sockets.worker wsgi:app &
$ celery -A server:celery worker --autoscale=16,3 &
```

## API

You can query the system by using the following HTTP calls

```
GET /api/robots
```

Returns the lists of all the robots in the system.

```
GET /api/robots/<robot>
```

Narrows down the query to a specific robot

```
GET /api/robots/<robot>/events
GET /api/robots/<robot>/events?start_time=0&end_time=2
```

Returns the location events for a specific robot with query params `start_time`
and `end_time` to filter by time interval.


```
GET /api/robots/<robot>/odometer
GET /api/robots/<robot>/odometer?start_time=0&end_time=2
```

Returns the total accumulated distance that a robot has travelled with
query params `start_time` and `end_time` to filter by time interval.


### Websocket

The WebSocket address is `ws://127.0.0.1:8000/upstream`. You can send it data
in the following format:

```
x,y,timestamp,robot_name
```

A single event should use a single `send` command.


## TODOs

- Security for WebSockets
- Error Handling of HTTP Errors as a JSON
- Deferred Database Commits of Stream, so we can have majority of the data in
the Redis cache, but this will increase the risk of data loss during outages
(unrecoverable at this point)
