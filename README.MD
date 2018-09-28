Telemetry Server
------------------------------

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
$ nosetests
```

### Production
```
$ gunicorn -w 4 -k flask_sockets.worker server:app
```
