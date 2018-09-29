Telemetry Server
------------------------------
[![Build Status](https://circleci.com/gh/starpogi/fr_telemetry.svg?style=svg)](https://circleci.com/gh/starpogi/fr_telemetry)


Server that handles Telemetry events, and an endpoint for analytics

## Setup
```
$ . setup.sh
```

## Run

### Development
```
$ flask run
```

### Test
```
$ pytest
```

### Production
```
$ gunicorn -w 4 -k flask_sockets.worker server:app
```
