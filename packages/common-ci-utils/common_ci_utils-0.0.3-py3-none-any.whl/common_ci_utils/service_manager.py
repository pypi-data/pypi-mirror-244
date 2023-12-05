"""
This module handles all the service related operation like start, start etc...
"""

import logging

from common_ci_utils.command_runner import exec_cmd
from common_ci_utils.exceptions import ServiceStartFailed, ServiceStopFailed

log = logging.getLogger(__name__)


def start_service(name, use_sudo=True):
    """
    Start the service

    Args:
        name: service name to start
        use_sudo (bool): If True cmd will be executed with sudo

    Raises:
        ServiceStartFailed: In case service failed to start

    """
    cmd = f"systemctl start {name}"
    result = exec_cmd(cmd=cmd, use_sudo=use_sudo)
    if result.returncode == 0:
        log.info(f"Successfully started service '{name}'")
    else:
        raise ServiceStartFailed(
            f"Error in starting service '{name}':\n{result.stderr}"
        )


def stop_service(name, use_sudo=True):
    """
    Stop the service

    Args:
        name: service name to stop
        use_sudo (bool): If True cmd will be executed with sudo

    Raises:
        ServiceStopFailed: In case service failed to stop

    """
    cmd = f"systemctl stop {name}"
    result = exec_cmd(cmd=cmd, use_sudo=use_sudo)
    if result.returncode == 0:
        log.info(f"Successfully stopped service '{name}'")
    else:
        raise ServiceStopFailed(f"Error in stopping service '{name}':\n{result.stderr}")


def is_service_running(name, use_sudo=True):
    """
    checks whether the service is running or not

    Args:
        name: service name to check
        use_sudo (bool): If True cmd will be executed with sudo

    Returns:
        bool: True in case service is running, else False

    """
    is_running = False
    cmd = f"systemctl is-active {name}"
    result = exec_cmd(cmd=cmd, use_sudo=use_sudo)
    if result.returncode == 0:
        log.info(f"'{name}' service is running")
        is_running = True
    return is_running
