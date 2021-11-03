# Package Updates DataDog agent Plugin

This plugin sends metrics regarding package updates to a DataDog instance.

```console
Work in progress.
```

Currently only supporting [Ubuntu](https://ubuntu.com/) and Linux distributions
using `/usr/lib/update-notifier/apt_check.py`.

## Metrics

[https://docs.datadoghq.com/metrics/agent_metrics_submission/?tab=gauge](https://docs.datadoghq.com/metrics/agent_metrics_submission/?tab=gauge)

```console
system.package.updates
system.package.updates.security
```

## Files

```console
/etc/datadog-agent/checks.d/package_updates.py
/etc/datadog-agent/conf.d/package_updates.d/package_updates.yaml
```

## Installation example

```sh
git clone https://github.com/konstruktoid/datadog-package-updates
cd datadog-package-updates/
sudo cp -vnR checks.d/ conf.d/ /etc/datadog-agent/
sudo chown -R dd-agent:dd-agent /etc/datadog-agent/conf.d/package_updates.d/
sudo chown -R dd-agent:dd-agent /etc/datadog-agent/checks.d/package_updates.py
sudo systemctl restart datadog-agent
```
