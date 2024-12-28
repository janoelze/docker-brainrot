docker-brainrot  
===============  

as part of my – our! – ongoing effort to avoid learning any actual Docker deployment workflows and to accelerate coding workflows to absurd speeds, I’m releasing docker-brainrot, a Python script that takes a Dockerfile and deploys it to a Docker host of your choice.

* Allows one-command deploys of Dockerfiles to remote hosts.
* Collects files referenced via COPY and ADD commands in the Dockerfile and uploads them to the remote host.
* Automatically (re)builds and runs the Docker container on the remote host.

## USAGE

### Create a Dockerfile with custom headers

```Dockerfile
# Container-Name: my-cool-app
# Port-Map: 8001:8001

FROM python:3.9-slim
WORKDIR /app
COPY ./html /app
ADD https://place-hold.it/100x100 /app/logo.png
CMD ["python", "-m", "http.server", "8001"]
EXPOSE 8001
```

## Run docker-brainrot via uv

```bash
$ uv run https://raw.githubusercontent.com/janoelze/docker-brainrot/main/d.py \
  -f ./path/to/Dockerfile \
  -H "user@100.98.129.49:22"
```

## OPTIONS

| Option         | Description                                                                                       |
|----------------|---------------------------------------------------------------------------------------------------|
| `-f, --file`   | **Required**<br>The path to the Dockerfile to be deployed. Must be a valid and accessible file.   |
| `-H, --host`   | **Required**<br>Specifies the remote Docker host in the format `username@host:port`.<br>- `username`: SSH username for authentication.<br>- `host`: Hostname or IP of the Docker host.<br>- `port`: Port for SSH (e.g., `22`). |

## DOCKERFILE HEADERS

| Header          | Description                                                                                       |
|-----------------|---------------------------------------------------------------------------------------------------|
| `Container-Name`| **Required**<br>The name of the container to be deployed. Must be unique and consist of alphanumeric characters and dashes (-). |
| `Port-Map`      | **Optional**<br>The port mapping for the container. Must be in the format `host-port:container-port`. |


## NOTES

- You can create an alias for easier invocation, but uv allows you to run the script directly via a URL.
- Ensure that the Container-Name header is set in the Dockerfile, as this is used to identify containers.
- Container names must consist of alphanumeric characters and dashes (-).
