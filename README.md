docker-brainrot  
===============  

as part of my ongoing effort to avoid learning any actual Docker deployment workflows and to accelerate coding workflows to absurd speeds, I’m releasing docker-brainrot, a Python script that takes a Dockerfile and deploys it to a Docker host of your choice.

* One-command deploys to remote docker hosts
* Collects files referenced via COPY/ADD in the Dockerfile and uploads them to the host
* Builds, restarts/runs the Docker container on the host

## INSTALLATION

Create an alias in your shell profile:

```bash
export DOCKER_BRAINROT_URL="https://raw.githubusercontent.com/janoelze/docker-brainrot/main/d.py?v=$(date +%s)"
alias docker-brainrot='uv run "$DOCKER_BRAINROT_URL"'
```

`uv` allows execution of scripts via remote URLs. It'll install docker-brainrot's dependencies locally in a virtual environment.

## USAGE

### Set up a Dockerfile

```Dockerfile
# Container-Name: my-cool-app
# Port-Map: 8050:8050

FROM python:3.9-slim
WORKDIR /app
COPY ./html /app
CMD ["python", "-m", "http.server", "8050"]
EXPOSE 8050
```

Note the `Container-Name` header, which is used to identify the container, and the `Port-Map` header, which specifies the port mapping for the container.

### Deploy the Dockerfile

```bash
$ docker-brainrot -f ./path/to/Dockerfile -H "user@100.98.129.49:22"
```

````
[04:19:41] Connected to 100.98.129.49
           Build context created at /tmp/build_context.tar.gz
           Uploading build context... ━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:25
           Build context uploaded to /tmp/my-cool-app_build_context/build_context.tar.gz
[04:19:42] Checking for existing container: my-cool-app
           Stopping and removing existing container: my-cool-app
[04:19:52] Building the Docker image...
[04:19:53] Running the Docker container...
[04:19:54] Container my-cool-app is now running.
````

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
