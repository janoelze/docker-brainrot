from lib.helpers import log_message
import paramiko

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
            log_message("info", f"Connected to {self.host}")
        except Exception as e:
            log_message("error", f"Failed to connect to {self.host}: {e}")
            raise

    def execute(self, command):
        """Executes a command on the remote server."""
        if not self.client:
            raise ValueError("SSH connection not established.")
        stdin, stdout, stderr = self.client.exec_command(command)
        stdout_output = stdout.read().decode()
        stderr_output = stderr.read().decode()
        if stderr_output:
            log_message("error", f"Error executing command '{command}': {stderr_output}")
        return stdout_output

    def upload_file(self, local_content, remote_path):
        """Uploads a file to the remote server."""
        if not self.client:
            raise ValueError("SSH connection not established.")
        sftp = self.client.open_sftp()
        try:
            with sftp.file(remote_path, "w") as remote_file:
                remote_file.write(local_content)
            log_message("info", f"File uploaded to {remote_path}")
        finally:
            sftp.close()

    def close(self):
        """Closes the SSH connection."""
        if self.client:
            self.client.close()