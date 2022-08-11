![Build Status](https://github.com/Linaro/lava-test-plans/actions/workflows/test-plans-pipeline.yml/badge.svg)
![REUSE Compliance Check](https://github.com/Linaro/lava-test-plans/actions/workflows/reuse.yml/badge.svg)

# Installation

To install the latest development version:

    git clone https://github.com/Linaro/lava-test-plans.git
    cd ./lava-test-plans

You need to install Python dependencies:

    pip3 install -r requirements.txt

or

You need to do if you have docker installed:
    docker run --volume $HOME/path/to/lava-test-plans:/xyz -i -t lavasoftware/lava-test-plans /bin/bash
    cd /xyz

lavasoftware/lava-test-plans:latest points to the latest released version.
lavasoftware/lava-test-plans:master points to the latest development.

There will be a directory with /lava-test-plans from either a "released"
version or directly from master.

If the above commands succeed, you can run to check that the program starts correctly

    python3 -m lava_test_plans -h

# External variables

External variables are set in the *variables.ini* file. Each line in this file
is in the form
```
key=value
```
Lines starting with *#* are omited. Variables can also be set using
*--overwrite-variables* parameter. List of used variables:

 * *PROJECT_NAME*: used as the first part in the test job name. Can be set to
   differentiate LAVA test jobs between different teams/projects
 * *BUILD_NUMBER*: used as last part in the test job name.
 * *KERNEL_BRANCH*: used in test job name
 * *OS_INFO*: used in test job name
 * *LAVA_JOB_PRIORITY*: priority of the LAVA job, used by LAVA scheduler
 * *LAVA_JOB_VISIBILITY*: defaults to *public*. This block can be used to restrict job visibility to user or group.
 * *AUTO_LOGIN_*: default *PROMPT='login:', *USERNAME='root' and *PASSWORD=''.
 * *BOOT_LABEL*: default BOOT_LABEL='boot'.
 * *TAGS*: variable should contain tags required by job. Formtatting is important and this variable should be
 formatted comma separated list. Example: tag1, tag2. In case of using just one tag, end string with comma. Example:
 tag1,
 * *UBOOT_VERSION_STRING*: string that is matched in the u-boot shell from output of command *version*
 * *OVERLAY_MODULES_* *: overlays modules into the rootfs.
 * *TEST_DEFINITIONS_REPOSITORY*: points to the test repository to use, default: https://github.com/Linaro/test-definitions.git

Variables can also be stored in YAML file. Usual YAML syntax applies.

## Timeouts

Overall job timeout is a sum of action timeouts. There are 6 components:
 * *deploy_timeout*
 * *boot_timeout*
 * *install_fastboot_timeout*
 * *fastboot_deploy_timeout*
 * *target_deploy_timeout*
 * *TARGET_BOOT_TIMEOUT*
 * *test_timeout*

When LXC is not in use all *lxc_* timeouts are set to 0. *test_timeout* is defined for each test template. *target_* timeouts can be set separately for each device.

# CI for docker multiarch builds
lava-test-plans gets mirrored to gitlab
https://gitlab.com/Linaro/lava-test-plans to build multiarch docker containers
and publish them to https://hub.docker.com/r/lavasoftware/lava-test-plans, that
is why there is a .gitlab-ci.yml in this repository.

# Repository
Pull requests are welcome to https://github.com/linaro/lava-test-plans.
