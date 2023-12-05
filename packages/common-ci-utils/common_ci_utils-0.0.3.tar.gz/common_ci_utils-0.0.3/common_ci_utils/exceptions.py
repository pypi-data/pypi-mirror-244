"""
This module contains various user defined exceptions
"""


class AggregateNodeStatusCheckFailed(Exception):
    pass


class PermissionsFailedToChange(Exception):
    pass


class RPMInstallationFailed(Exception):
    pass


class ServiceRunningFailed(Exception):
    pass


class ServiceStartFailed(Exception):
    pass


class ServiceStopFailed(Exception):
    pass


class StorageStatusCheckFailed(Exception):
    pass
