"""
Module that connects to remote host and execute operations on remote host
"""

import logging

from paramiko import AutoAddPolicy, SSHClient
from paramiko.auth_handler import AuthenticationException, SSHException


log = logging.getLogger(__name__)


class Connection(object):
    """
    A class that connects to remote host
    """

    def __init__(
        self,
        host,
        user=None,
        private_key=None,
        password=None,
        stdout=False,
    ):
        """
        Initialize all required variables

        Args:
            host (str): Hostname or IP to connect
            user (str): Username to connect
            private_key (str): Private key  to connect to host
            password (password): Password for host
            stdout (bool): output stdout to console

        """
        self.host = host
        self.user = user
        self.private_key = private_key
        self.password = password
        self.stdout = stdout
        self.client = self._connect()

    def _connect(self):
        """
        Get connection to host

        Returns:
            paramiko.client: Paramiko SSH client connection to host

        Raises:
            authException: In-case of authentication failed
            sshException: In-case of ssh connection failed

        """
        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            if self.private_key:
                client.connect(
                    self.host,
                    username=self.user,
                    key_filename=self.private_key,
                )
            elif self.password:
                client.connect(
                    self.host,
                    username=self.user,
                    password=self.password,
                )
        except AuthenticationException as authException:
            log.error(f"Authentication failed: {authException}")
            raise authException
        except SSHException as sshException:
            log.error(f"SSH connection failed: {sshException}")
            raise sshException

        return client

    def close(self):
        self.client.close()

    def exec_cmd(self, cmd):
        """
        Executes command on host

        Args:
            cmd (str): Command to run on host

        Returns:
            tuple: tuple which contains command return code, output and error

        """
        log.info(f"Executing cmd: {cmd} on {self.host}")
        _, out, err = self.client.exec_command(cmd)
        retcode = out.channel.recv_exit_status()
        stdout = out.read().decode("utf-8").strip("\n")
        try:
            stderr = err.read().decode("utf-8").strip("\n")
        except UnicodeDecodeError:
            stderr = err.read()
        log.debug(f"retcode: {retcode}")
        log.info(f"stdout: {stdout}") if self.stdout else log.debug(f"stdout: {stdout}")
        log.debug(f"stderr: {stderr}")
        return retcode, stdout, stderr

    def upload_file(self, localpath, remotepath):
        """
        Upload a file to remote host

        Args:
            localpath (str): local file to upload
            remotepath (str): target path on the remote host. filename should be included

        """
        try:
            ssh = self.client
            ssh.set_missing_host_key_policy(AutoAddPolicy())

            sftp = ssh.open_sftp()
            log.info(f"uploading {localpath} to {self.user}@{self.host}:{remotepath}")
            sftp.put(localpath, remotepath)
            sftp.close()
        except AuthenticationException as authException:
            log.error(f"Authentication failed: {authException}")
            raise authException
        except SSHException as sshException:
            log.error(f"SSH connection failed: {sshException}")
            raise sshException
