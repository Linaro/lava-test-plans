![Build Status](https://github.com/Linaro/lava-test-plans/actions/workflows/test-plans-pipeline.yml/badge.svg)
![REUSE Compliance Check](https://github.com/Linaro/lava-test-plans/actions/workflows/reuse.yml/badge.svg)

# LAVA Test Plans
The `lava-test-plans` project makes it easier to generate [LAVA](https://www.lavasoftware.org/) job definition files from a set of templates.

# Installation
Install `lava-test-plans` from pip:

```shell
pip install lava-test-plans
````
or with podman/docker:
```shell
docker run -i -t lavasoftware/lava-test-plans /bin/bash
```

## Versions
- `lavasoftware/lava-test-plans:latest` points to the latest released version.
- `lavasoftware/lava-test-plans:master` points to the latest development.

If the above commands succeed, you can run to check that the program starts correctly
```shell
lava-test-plans -h
```

## Development
To install the latest development version:
```shell
git clone https://github.com/Linaro/lava-test-plans.git
cd ./lava-test-plans
pip3 install flit
flit install --symlink
```
or you can use Docker:
```shell
docker run --volume /path/to/lava-test-plans:/xyz -i -t lavasoftware/lava-test-plans /bin/bash
cd /xyz
```
There will be a directory with `/lava-test-plans` from either a "released" version or directly from master.

If the above commands succeed, you can run to check that the program starts correctly:
```shell
python3 -m lava_test_plans --version
```
output should be similar to:
```
__main__.py, 7c588ece
```

# External variables
External variables are set in the *variables.ini* file. Each line in this file
is in the `key=value` form.

Lines starting with `#` are omitted. 

Variables can also be set using
`--overwrite-variables` parameter.

List of used variables:

 * `PROJECT_NAME`: used as the first part in the test job name. Can be set to differentiate LAVA test jobs between different teams/projects.
 * `BUILD_NUMBER`: used as last part in the test job name.
 * `KERNEL_BRANCH`: used in test job name.
 * `OS_INFO`: used in test job name.
 * `LAVA_JOB_PRIORITY`: priority of the LAVA job, used by LAVA scheduler.
 * `LAVA_JOB_VISIBILITY`: defaults to *public*. This block can be used to restrict job visibility to user or group.
 * `LAVA_JOB_VISIBILITY_GROUPS`: variable should contain groups required by job. Formatting is important and this variable should be formatted as comma separated list. For example: `group1, group2`. In case of using just one group, end string with comma - `group1,`.
 * `AUTO_LOGIN_`: default *PROMPT='login:', *USERNAME='root' and *PASSWORD=''.
 * `BOOT_LABEL`: default is `boot`.
 * `TAGS`: variable should contain tags required by job. Formatting is important and this variable should be
 formatted comma separated list. For example: `tag1, tag2`. In case of using just one tag, end string with comma - 
 `tag1,`.
 * `UBOOT_VERSION_STRING`: string that is matched in the U-Boot shell after command `version`.
 * `OVERLAY_MODULES_`: overlays modules into the rootfs.
 * `TEST_DEFINITIONS_REPOSITORY`: points to the test repository to use, default: https://github.com/Linaro/test-definitions.git

Variables can also be stored in YAML-formatted file - `variables.yaml`

# Timeouts
Overall job timeout is a sum of action timeouts. There are several components:
 * `deploy_timeout`
 * `boot_timeout`
 * `install_fastboot_timeout`
 * `fastboot_deploy_timeout`
 * `target_deploy_timeout`
 * `TARGET_BOOT_TIMEOUT`
 * `test_timeout`, is defined for each test template.

### Notes
1. When LXC is not in use all `lxc_*` timeouts are set to 0. 
2. `target_*` timeouts can be set separately for each device.

# CI for Docker multi-arch builds
`lava-test-plans` repo gets mirrored to [Gitlab](https://gitlab.com/Linaro/lava-test-plans)
 to build multi-arch Docker containers
and publish them to [Docker Hub](https://hub.docker.com/r/lavasoftware/lava-test-plans).

# Contributing
Pull requests are welcome to https://github.com/linaro/lava-test-plans!