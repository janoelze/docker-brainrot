docker-brainrot  
===============  

as part of my – our! – ongoing effort to avoid learning any actual Docker deployment workflows and to accelerate coding workflows to absurd speeds, I’m releasing docker-brainrot, a Python script that takes a Dockerfile and deploys it to a Docker host of your choice.

* Allows one-command deploys of Dockerfiles to remote hosts.
* Collects files referenced via COPY and ADD commands in the Dockerfile and uploads them to the remote host.
* Automatically (re)builds and runs the Docker container on the remote host.

## INSTALLATION

Create an alias in your shell profile:

```bash
alias docker-brainrot='uv run "https://raw.githubusercontent.com/janoelze/docker-brainrot/main/d.py?v=$(date +%s)"'
```

## USAGE

### Set up a Dockerfile

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

Note the `Container-Name` header, which is used to identify the container, and the `Port-Map` header, which specifies the port mapping for the container.

## Deploy the Dockerfile

```bash
$ docker-brainrot -f ./path/to/Dockerfile -H "user@100.98.129.49:22"
```

````bash
[04:19:41] Connected to 100.98.129.49
           Build context created at /tmp/build_context_a77d38a7-f631-4ddd-9808-58a84993bf23.tar.gz
           Uploading build context... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
           Build context uploaded to /tmp/build_context_a96f598e-68fd-4c24-a6a4-c832db85972b/build_context.tar.gz
[04:19:42] Checking for existing container: docker-brainrot-test-app
           Stopping and removing existing container: docker-brainrot-test-app
[04:19:52] Building the Docker image...
[04:19:53] Running the Docker container...
[04:19:54] Container docker-brainrot-test-app is now running.
           Cleaning up remote build context directory: /tmp/build_context_a96f598e-68fd-4c24-a6a4-c832db85972b
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
