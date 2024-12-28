# docker-brainrot

as part of my ongoing effort to avoid learning actual Docker deployment workflows and to accelerate web development to absurd speeds, I’m releasing docker-brainrot, a Python script that takes a Dockerfile and deploys it to a Docker host of your choice.

Here’s what it does:

* Collects directories referenced in the Dockerfile
* Creates a tarball of these directories and moves it to a build directory on the remote host
* Builds and runs the container
* Cleans up after itself like a good script

## using docker-brainrot

docker-brainrot requires no installation if run through uv. however you'll need to add custom headers to your Dockerfile to get persistent container names and port handling.

```
# Container-Name: python-app
# Port-Map: 8000:8000

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Serve the /app/index.html file
CMD ["python", "-m", "http.server", "8000"]

# Make port 8000 available to the world outside this container
EXPOSE 8000
```

## let's deploy it!!

```
$ uv run https://raw.githubusercontent.com/janoelze/docker-brainrot/main/deploy.sh < Dockerfile
```
```
[02:43:32] Reading Dockerfile from standard input...                                                                                                                                                                                    deploy.py:174
           Connected to 100.98.129.49                                                                                                                                                                                                    deploy.py:42
Uploading build context... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
[02:43:33] Build context uploaded to /tmp/local_image_build_f36d63d6-fd49-4ca6-a0ee-82e278d72aca/build_context.tar.gz                                                                                                                   deploy.py:123
           Checking for existing container: python-app                                                                                                                                                                                  deploy.py:131
           Stopping and removing existing container: python-app                                                                                                                                                                         deploy.py:135
[02:43:44] Building the Docker image...                                                                                                                                                                                                 deploy.py:143
[02:43:47] Docker Build Output:                                                                                                                                                                                                         deploy.py:145
> Sending build context to Docker daemon  4.608kB
>
> Step 1/5 : FROM python:3.9-slim
>  ---> 473b3636d11e
> Step 2/5 : WORKDIR /app
>  ---> Using cache
>  ---> aa5e78f9ecd1
> Step 3/5 : COPY . /app
>  ---> d81b971a5920
> Step 4/5 : CMD ["python", "-m", "http.server", "8000"]
>  ---> Running in ead44d0d82b9
> Removing intermediate container ead44d0d82b9
>  ---> ad0e806eca18
> Step 5/5 : EXPOSE 8000
>  ---> Running in fb3ad67429ca
> Removing intermediate container fb3ad67429ca
>  ---> 5d0ae80c0049
> Successfully built 5d0ae80c0049
> Successfully tagged local_image:latest
           Running the Docker container...                                                                                                                                                                                              deploy.py:152
           Container python-app is now running.                                                                                                                                                                                         deploy.py:154
           Cleaning up remote build context directory: /tmp/local_image_build_f36d63d6-fd49-4ca6-a0ee-82e278d72aca                                                                                                                      deploy.py:158
           Disconnected from 100.98.129.49
```
