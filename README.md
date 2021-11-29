# Server / Service Monitoring Helper

Listen and send **ping** or **http** request when receive a request through http POST. 

> Use case: we have self monitoring service and want to check status from multi-location. 

# Deploy note

## Run dev

```cmd
python app.py
```

## Run production

> `gunicorn` incompatible with Windows

```cmd
gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 main:app
```

## Run with Docker

```cmd
docker build --tag ssm-helper-test .
docker run --rm --name ssm-helper-test-con -e PORT=8080 -e BEAT_URL=http://foo.bar/beat -p 8080:8080 ssm-helper-test
```

* `--rm` to remove container when it stop
* `-e BEAT_URL=http://foo.bar/beat` is optional to set heartbeat server

# Usage and note

* HTTP check: from another service, send POST request with content type `application/json` to endpoint: `/http`, payload: `{"server_host": "http://google.com"}`
    * Respond: `{"status": true}` if from this service request to `server_host` is ok, or response `{"status": false, "message": "..."}` if request failed
    
* PING check: from another service, send POST request with content type `application/json` to endpoint: `/ping`, payload: `{"server_host": "8.8.8.8"}`
    * Respond: `{"status": true}` if from this service ping to `server_host` is ok, or `{"status": false, "message": "..."}` if ping failed
    
* Endpoint: `/beat` (optional): when service receive a GET request to this endpoint, it will create a POST request 
to heartbeat server with data: `{"json_data": {{"client_name": "foo", "client_version": "bat"}}}` 
(You must setup the server to handle this post, this endpoint only using for make sure this service is alive)
