from dataclasses import dataclass

from scp import SCPClient

from .key_pair import keyPair
from typing import Optional,BinaryIO
from .discovery import find
from paramiko import SSHClient

import paramiko
import socket
import concurrent.futures
from . import discovery
import requests
import datetime

@dataclass
class SSHCommandResult:
    """The result of a command that was run remotely over SSH."""

    exit_status: int
    stdout: bytes
    stderr: bytes


class SSHCommandTimeoutError(Exception):
    """Raised when an SSH command doesn't complete in a reasonable time."""

    pass


class SSHCommandExitStatusError(Exception):
    """Raised when an SSH command completes, but exits with a non-zero status code."""

    result: SSHCommandResult
    """The details of the failure."""

    def __init__(self, result: SSHCommandResult) -> None:
        super().__init__("SSH command exited with non-zero status.", result)
        self.result = result


class RobotApi():
    hostname_ip : str
    _key_pair : keyPair


    def __init__(self, hostname_or_ip: str, key_pair:Optional[keyPair] = None)->None:
        self.hostname_or_ip = hostname_or_ip
        self._api_url_base = "http://{}:31950".format(hostname_or_ip)
        if not key_pair:
            key_pair = keyPair.generate()
        self._key_pair = key_pair


    def __enter__(self)->"RobotApi":
        healthresp = requests.get(self._api_url_base + "/server/update/health")
        if healthresp.status_code != 200:
            raise AssertionError(f"Could not connect to robot {self.hostname_or_ip}")
        self.put_pubkey()
        return self

    def __exit__(self,
            exc_type,  # noqa: ANN001
            exc_value,  # noqa: ANN001
            traceback,  # noqa: ANN001
            ) -> None:
        self.remove_pubkey(self._key_pair.public_id)

    def put_pubkey(self) -> None:
        """Add an SSH public key to the list the robot accepts."""
        pres_resp = requests.get(self._api_url_base + "/server/ssh_keys")
        if pres_resp.status_code != 200:
            raise AssertionError(f"Could not poll pubkeys to {pres_resp.status_code}")

        keys = pres_resp.json()["public_keys"]
        if self._key_pair.public_id in [key["key_md5"] for key in keys]:
            return
        post_resp = requests.post(
            self._api_url_base + "/server/ssh_keys", json={"key": self._key_pair.public}
        )
        status = post_resp.status_code
        if status != 201:
            msg = f"Could not put pubkey on {self._api_url_base}: {status}"
            raise AssertionError(msg)

    def remove_pubkey(self, key_id: str) -> None:
        """Remove a single SSH public key from the robot, by the key's ID."""
        del_resp = requests.delete(self._api_url_base + f"/server/ssh_keys/{key_id}")

    def remove_all_pubkeys(self) -> None:
        """Remove all SSH public keys on the robot."""
        get_resp = requests.get(self._api_url_base + "/server/ssh_keys")
        keys = get_resp.json().get("public_keys", [])
        for key in keys:
            key_id = key["key_md5"]
            self.remove_pubkey(key_id)

    def run_ssh_command(
            self,
            cmdstring: str,
            timeout_seconds: float = 60 * 2,
            raise_on_bad_exit_status: bool = True,
    ) -> SSHCommandResult:
        """Run an SSH command on the robot, and return its output and exit status.

        :param cmdstring: The command to execute.

        :raises SSHCommandTimeoutError: If `timeout_seconds` passes without the
            command completing.
        :raises SSHCommandExitStatusError: If raise_on_bad_exit_status is true
            and the command completes with a non-zero exit status.
        """
        with self.ssh_connect() as client:
            result = _run_ssh_command(client, cmdstring, timeout_seconds)
            if result.exit_status and raise_on_bad_exit_status:
                raise SSHCommandExitStatusError(result)
            return result

    def ssh_connect(self) -> SSHClient:
        """Connect to the robot via SSH.

        Used as a component of other commands, mostly.
        """
        client = SSHClient()
        # We're connecting to many robots so we don't really care about host
        # keys
        client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
        # todo(mm, 2021-01-25): A timeout on connect() might be a good idea.
        client.connect(
            self.hostname_or_ip, username="root", pkey=self._key_pair.private,
        )
        return client

    def put_file(
            self, local_path: str, remote_path: str
    ) -> None:
        """Copy a single file to the robot.

        :param local_path: The file on this computer to copy.
        :param remote_path: The path on the robot's filesystem for the new file.
            The parent directory must already exist. If a file already exists
            at this path, it's overwritten. If a directory already exists at
            this path, the new file is placed inside it.
        """
        with self.ssh_connect() as c, SCPClient(c.get_transport()) as scp:
            scp.put(files=local_path, remote_path=remote_path)

    def start_shell(self, client: SSHClient = None) -> paramiko.channel.Channel:
        """Connect to the robot and start an interactive SSH session.

        :param client: If specified, a connected client to reuse
        :returns: The connected channel with a live interactive terminal, ready for
                  use with :py:meth:`paramiko.demos.interactive.interactive_shell`
        """
        if not client:
            client = self.ssh_connect()
        return client.invoke_shell()


def find(timeout_sec: Optional[float] = None) -> RobotApi:
    """Find a robot.

    Block until a robot appears on USB and then return an initialized RobotAPI.

    :param timeout_sec: A timeout before giving up finding a robot. If `None`,
                        wait forever if necessary.
    """
    then = datetime.datetime.now()
    while True:
        try:
            robot_addr = discovery.find()
        except discovery.NoRobotFoundError:
            if timeout_sec:
                since = datetime.datetime.now() - then
                if since.total_seconds() > timeout_sec:
                    raise
        else:
            break
    return RobotApi(robot_addr)


def _run_ssh_command(
    client: SSHClient, command: str, timeout_seconds: float
) -> SSHCommandResult:
    stdin, stdout, stderr = client.exec_command(
        command=command, timeout=timeout_seconds
    )

    def read_all_bytes(file_like: BinaryIO) -> bytes:
        try:
            return file_like.read()
        except socket.timeout:
            raise SSHCommandTimeoutError(
                f"SSH command {repr(command)} timed out"
                f" after {timeout_seconds} seconds."
            )

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # To avoid deadlocks, read from stdout and stderr concurrently. Both streams
        # share flow control; if we read them serially, the first read() could be
        # blocked by data waiting to be consumed by the second read().
        # https://github.com/paramiko/paramiko/issues/1790
        stdout_bytes, stderr_bytes = executor.map(read_all_bytes, [stdout, stderr])

    # To avoid hanging, this must come after reading stdout and stderr to completion.
    exit_status = stdout.channel.recv_exit_status()

    result = SSHCommandResult(
        exit_status=exit_status, stdout=stdout_bytes, stderr=stderr_bytes
    )
    return result

#
if __name__ == '__main__':

    find()
