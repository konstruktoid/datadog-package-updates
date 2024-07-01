#!/usr/bin/python3
"""Send metrics regarding package updates to DataDog.

See https://docs.datadoghq.com/metrics/agent_metrics_submission/?tab=gauge.
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

from checks import AgentCheck
from dateutil.relativedelta import relativedelta

UBUNTU_APT_CHECK = "/usr/lib/update-notifier/apt_check.py"
UBUNTU_REBOOT_REQUIRED = "/var/run/reboot-required"

__version__ = "0.0.4"


class PackageUpdates(AgentCheck):
    """The PackageUpdates class."""

    def check(self, instance):  # noqa: ARG002
        """Return the number of available updates."""
        try:
            lsb_release = shutil.which("lsb_release")

            if os.path.isfile(lsb_release):
                lsb_process = subprocess.run(
                    [lsb_release, "-rsd"],
                    shell=False,  # noqa: S603
                    stdout=subprocess.PIPE,
                    check=True,
                    stderr=subprocess.STDOUT,
                    text=True,
                )

                lsb_output = lsb_process.stdout.split(" ")
                lsb_distribution = lsb_output[0]
                lsb_release = lsb_output[1]

                if lsb_distribution == "Ubuntu":
                    release_year = "20" + next(iter(lsb_release.split("."))).strip()
                    release_month = list(lsb_release.split("."))[1].strip()
                    release_date = datetime.datetime(
                        int(release_year),
                        int(release_month),
                        1,
                        tzinfo=timezone.utc,
                    )

                    release_eol = release_date + relativedelta(months=+9)
                    date_now = datetime.datetime.now()

                    if int(release_month) != int("04"):
                        release_eol = 1 if release_eol < date_now else 0
                    elif int(release_month) == int("04"):
                        release_eol = release_date + relativedelta(years=+4)
                        release_eol = 1 if release_eol < date_now else 0
                    else:
                        release_eol = None

            if os.path.isfile(UBUNTU_APT_CHECK):
                query_process = subprocess.run(
                    UBUNTU_APT_CHECK,
                    shell=False,  # noqa: S603
                    stdout=subprocess.PIPE,
                    check=True,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
                package_updates = next(iter(query_process.stdout.split(";")))
                package_updates_security = list(query_process.stdout.split(";"))[1]

            reboot_required = 1 if os.path.isfile(UBUNTU_REBOOT_REQUIRED) else 0

        except Exception as exception_string:  # noqa: BLE001
            print("Exception: ", str(exception_string), file=sys.stderr)
            sys.exit(1)

        try:
            self.gauge(
                "system.reboot.required",
                reboot_required,
                tags=["metric_submission_type:gauge"],
            )

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

            self.gauge(
                "system.release.eol",
                release_eol,
                tags=["metric_submission_type:gauge"],
            )

        except Exception as exception_string:  # noqa: BLE001
            print("Exception: ", str(exception_string), file=sys.stderr)
            sys.exit(1)
