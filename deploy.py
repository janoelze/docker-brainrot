# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "paramiko",
#   "rich",
#   "click"
# ]
# ///

import sys
import paramiko
import os
import tarfile
import re
import uuid
import click
from rich.console import Console
from rich.progress import track

console = Console()

class SSHClient:
    """Helper class to manage SSH connections and commands."""
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.client = None

    def connect(self):
        """Establishes an SSH connection."""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.host, port=self.port, username=self.username)
            console.log(f"[bold green]Connected to {self.host}")
        except Exception as e:
            console.log(f"[bold red]Failed to connect to {self.host}: {e}")
            raise

    def execute(self, command):
        """Executes a command on the remote server."""
        if not self.client:
            raise ValueError("SSH connection not established.")
        stdin, stdout, stderr = self.client.exec_command(command)
        stdout_output = stdout.read().decode()
        stderr_output = stderr.read().decode()
        if stderr_output:
            console.log(f"[bold red]Error executing command '{command}': {stderr_output}")
        return stdout_output

    def upload_file(self, local_content, remote_path):
        """Uploads a file to the remote server."""
        if not self.client:
            raise ValueError("SSH connection not established.")
        sftp = self.client.open_sftp()
        try:
            with sftp.file(remote_path, "w") as remote_file:
                remote_file.write(local_content)
            console.log(f"[bold green]File uploaded to {remote_path}")
        finally:
            sftp.close()

    def close(self):
        """Closes the SSH connection."""
        if self.client:
            self.client.close()
            console.log(f"[bold green]Disconnected from {self.host}")

def parse_comment_header(dockerfile_content):
    """Parses the comment header of the Dockerfile to extract metadata."""
    container_name = None
    port_map = None

    for line in dockerfile_content.splitlines():
        # Parse Container-Name
        name_match = re.match(r"^#\s*Container-Name:\s*(.+)$", line)
        if name_match:
            container_name = name_match.group(1).strip()
        
        # Parse Port-Map
        port_match = re.match(r"^#\s*Port-Map:\s*(.+)$", line)
        if port_match:
            port_map = port_match.group(1).strip()

    return container_name, port_map

def create_build_context(dockerfile_path):
    """Creates a tarball of the build context."""
    unique_id = str(uuid.uuid4())
    context_path = f"/tmp/build_context_{unique_id}.tar.gz"
    # read the Dockerfile
    dockerfile_contents = open(dockerfile_path, "r").read()
    dockerfile_dir = os.path.dirname(dockerfile_path)
    with tarfile.open(context_path, "w:gz") as tar:
        # add the Dockerfile to the tarball
        tar.add(dockerfile_path, arcname=os.path.basename(dockerfile_path))
        # iterate over the lines in the Dockerfile
        for line in dockerfile_contents.splitlines():
            # if the line is a COPY or ADD command
            if line.startswith("COPY") or line.startswith("ADD"):
                # extract the source path
                source_path = re.search(r"(?<=\s)(.*)(?=\s)", line).group(0)
                # if the path is a URL, skip it
                if source_path.startswith("http://") or source_path.startswith("https://"):
                    continue
                # construct the full path to the source file
                full_source_path = os.path.join(dockerfile_dir, source_path)
                # add the source file to the tarball
                tar.add(full_source_path, arcname=source_path)
    return context_path

def send_build_context(ssh_client, context_path, container_name):
    """Uploads the build context tarball to the server."""
    build_dir = f"build_context_{uuid.uuid4()}"
    remote_path = f"/tmp/{build_dir}/build_context.tar.gz"
    ssh_client.execute(f"mkdir -p /tmp/{build_dir}")
    with open(context_path, "rb") as tarball:
        sftp = ssh_client.client.open_sftp()
        try:
            with sftp.file(remote_path, "wb") as remote_file:
                for _ in track(range(1), description="[cyan]Uploading build context..."):
                    remote_file.write(tarball.read())
            console.log(f"[bold green]Build context uploaded to {remote_path}")
        finally:
            sftp.close()
    ssh_client.execute(f"cd /tmp/{build_dir} && tar -xzf build_context.tar.gz")
    return build_dir

def stop_and_remove_container(ssh_client, container_name):
    """Stops and removes an existing container."""
    console.log(f"[cyan]Checking for existing container: {container_name}")
    result = ssh_client.execute(f"docker ps -a -q --filter name=^{container_name}$").strip()

    if result:
        console.log(f"[yellow]Stopping and removing existing container: {container_name}")
        ssh_client.execute(f"docker stop {container_name}")
        ssh_client.execute(f"docker rm {container_name}")
    else:
        console.log(f"[green]No existing container with the name {container_name} found.")

def build_and_run_container(ssh_client, container_name, build_dir, port_map):
    """Builds and runs the Docker container on the remote server."""
    console.log("[cyan]Building the Docker image...")
    build_output = ssh_client.execute(f"cd /tmp/{build_dir} && docker build -t {container_name} .")
    console.log("[bold green]Docker Build Output:")
    for line in build_output.splitlines():
        console.print(f"> {line}")

    # Prepare the port mapping argument
    port_mapping = f"-p {port_map}" if port_map else ""
    
    console.log("[cyan]Running the Docker container...")
    ssh_client.execute(f"docker run -d {port_mapping} --name {container_name} {container_name}")
    console.log(f"[bold green]Container {container_name} is now running.")

def clean_up_build_context(ssh_client, build_dir):
    """Removes the build context directory from the remote server."""
    console.log(f"[cyan]Cleaning up remote build context directory: /tmp/{build_dir}")
    ssh_client.execute(f"rm -rf /tmp/{build_dir}")

def print_container_logs(ssh_client, container_name):
    """Prints the last 20 lines of the container logs."""
    console.log(f"[cyan]Fetching logs for container: {container_name}")
    logs = ssh_client.execute(f"docker logs --tail 20 {container_name}")
    console.log("[bold green]Container Logs:")
    for line in logs.splitlines():
        console.print(f"> {line}")

@click.command()
@click.option("-f", "--file", required=True, type=click.Path(exists=True), help="Path to the Dockerfile.")
@click.option("-H", "--host", required=True, help="SSH host in the format username@host:port.")
@click.option("-l", "--logs", is_flag=True, help="Show logs of the container after deployment.")
def main(file, host, logs):
    # Parse host information
    match = re.match(r"^(?P<user>[a-zA-Z0-9_.-]+)@(?P<host>[a-zA-Z0-9_.-]+):(?P<port>\d+)$", host)
    if not match:
        console.log("[bold red]Error: Invalid host format. Use username@host:port.")
        sys.exit(1)

    ssh_user = match.group("user")
    ssh_host = match.group("host")
    ssh_port = int(match.group("port"))

    # set the full, absolute path to the Dockerfile
    file = os.path.abspath(file)

    # Read the Dockerfile
    with open(file, "r") as dockerfile:
        dockerfile_content = dockerfile.read()

    if not dockerfile_content.strip():
        console.log("[bold red]Error: Dockerfile is empty. Exiting.")
        sys.exit(1)

    # Parse the Dockerfile header for container metadata
    container_name, port_map = parse_comment_header(dockerfile_content)

    # Ensure that the container name is only alphanumeric characters with dashes
    if not re.match(r"^[a-zA-Z0-9-]+$", container_name):
        console.log("[bold red]Error: Container name must be alphanumeric with dashes only. Exiting.")
        sys.exit(1)

    if not container_name:
        console.log("[bold red]Error: 'Container-Name' header not set in the Dockerfile. Exiting.")
        sys.exit(1)

    ssh_client = SSHClient(ssh_host, ssh_port, ssh_user)

    try:
        ssh_client.connect()

        # Create and send build context
        context_path = create_build_context(file)
        build_dir = send_build_context(ssh_client, context_path, container_name)

        stop_and_remove_container(ssh_client, container_name)
        build_and_run_container(ssh_client, container_name, build_dir, port_map)

        if logs:
            print_container_logs(ssh_client, container_name)

        # Clean up remote build context
        clean_up_build_context(ssh_client, build_dir)

        # Clean up local context tarball
        os.remove(context_path)

    except Exception as e:
        console.log(f"[bold red]Error: {e}")
        sys.exit(1)
    finally:
        ssh_client.close()

if __name__ == "__main__":
    main()