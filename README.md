[![Build Status](https://travis-ci.org/mwasilew/lava-test-plans.svg?branch=master)](https://travis-ci.org/mwasilew/lava-test-plans)

# Installation

To install the latest development version:

    git clone https://github.com/Linaro/lava-test-plans.git
    cd ./lava-test-plans

You need to install Python dependencies:

    pip3 install -r requirements.txt

If the above commands succeed, you can run to check that the program starts correctly

    ./submit_for_testing.py -h

# External variables

External variables are set in the *variables.ini* file. Each line in this file
is in the form
```
key=value
```
Lines starting with *#* are omited. Variables can also be set using
*--overwrite-variables* parameter to *submit_for_testing.py* script. List of used
variables:

 * *PROJECT_NAME*: used as the first part in the test job name. Can be set to
   differentiate LAVA test jobs between different teams/projects
 * *BUILD_NUMBER*: used as last part in the test job name.
 * *KERNEL_BRANCH*: used in test job name
 * *OS_INFO*: used in test job name
 * *LAVA_JOB_PRIORITY*: priority of the LAVA job, used by LAVA scheduler
 * *LAVA_JOB_VISIBILITY*: defaults to *public*. This block can be used to restrict job visibility to user or group.

## Timeouts

Overall job timeout is a sum of action timeouts. There are 6 components:
 * *lxc_deploy_timeout*
 * *lxc_boot_timeout*
 * *lxc_install_fastboot_timeout*
 * *target_deploy_timeout*
 * *target_boot_timeout*
 * *test_timeout*

When LXC is not in use all *lxc_* timeouts are set to 0. *test_timeout* is defined for each test template. *target_* timeouts can be set separately for each device.
