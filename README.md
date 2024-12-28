# docker-brainrot

as part of an ongoing effort to not learn any actual docker deploy workflows and accalerate web development to mind-numbing speeds i'm releasing docker-brainrot, a python script that will take a Dockerfile and send it to a docker host of your choice.

it'll:

* collect directories referenced from the `Dockerfile`
* tarball these and move them to a build directory on the remote host
* build the container
* run the container
* clean up after itself like a good script

## using docker-brainrot

docker-brainrot requires no installation if run through uv.

```
$ uv run ~/src/docker-howard-deploy/deploy.py < Dockerfile
```
```
~/s/docker-test $ uv run https://raw.githubusercontent.com/janoelze/docker-brainrot/main/deploy.sh < Dockerfile
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
