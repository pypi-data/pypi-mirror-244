# Scrypture – a standalone event store

## Install

**TODO**


## Configure

The application is configured using environment variables.

The available configuration variables are:

- `SCRYPTURE_READ_ONLY`
- `SCRYPTURE_DSN`
- `SCRYPTURE_REDIS_HOST`
- `SCRYPTURE_REDIS_PORT`
- `SCRYPTURE_REDIS_DB`


## Initialise

Once configured, you must initialise the database with the dedicated command:

```console
$ scrypture init-db
```


## Run

It requires Redis:

```console
docker run --rm --name scrypture-redis -p 6379:6379 redis
```

As a Flask application, it can be run using any WSGI server,
for instance, with [Gunicorn](https://gunicorn.org):

```console
$ gunicorn \
  --access-logfile="-" \
  --worker-class gevent \
  --workers 4 \
  --bind 127.0.0.1:5000 \
  "bl_scrypture.configuration.wsgi:app()"
```

Notice that we are using `gevent` workers as some clients might follow some streams.


## Contribute

See [CONTRIBUTING.md]() to set up a development environment.
