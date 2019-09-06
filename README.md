[![Build Status](https://travis-ci.org/mwasilew/lava-test-plans.svg?branch=master)](https://travis-ci.org/mwasilew/lava-test-plans)

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
