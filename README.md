# Package Updates DataDog agent Plugin

This plugin sends metrics regarding package updates to a DataDog instance.

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
sudo cp checks.d/package_updates.py /etc/datadog-agent/checks.d/
sudo cp -R conf.d/package_updates.d/ /etc/datadog-agent/conf.d/
sudo chown -R dd-agent:dd-agent /etc/datadog-agent/conf.d/package_updates.d/
sudo chown -R dd-agent:dd-agent /etc/datadog-agent/checks.d/package_updates.py
sudo systemctl restart datadog-agent
```
