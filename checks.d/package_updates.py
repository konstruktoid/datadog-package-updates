#!/usr/bin/python3
"""
Send metrics regarding package updates to DataDog.
https://docs.datadoghq.com/metrics/agent_metrics_submission/?tab=gauge
"""

import os
import subprocess
import sys
from checks import AgentCheck

UBUNTU_APT_CHECK = "/usr/lib/update-notifier/apt_check.py"

__version__ = "0.0.1"


class PackageUpdates(AgentCheck):
    """The PackageUpdates class."""

    def check(self, instance):
        """Return the number of available updates."""

        try:
            if os.path.isfile(UBUNTU_APT_CHECK):
                query_process = subprocess.run(
                    UBUNTU_APT_CHECK,
                    shell=False,
                    stdout=subprocess.PIPE,
                    check=True,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
                package_updates = list(query_process.stdout.split(";"))[0]
                package_updates_security = list(query_process.stdout.split(";"))[1]

        except Exception as exception_string:
            print("Exception: ", str(exception_string), file=sys.stderr)
            sys.exit(1)

        try:
            self.gauge(
                "system.package.updates",
                package_updates,
                tags=["metric_submission_type:gauge"],
            )

            self.gauge(
                "system.package.updates.security",
                package_updates_security,
                tags=["metric_submission_type:gauge"],
            )

        except Exception as exception_string:
            print("Exception: ", str(exception_string), file=sys.stderr)
            sys.exit(1)
