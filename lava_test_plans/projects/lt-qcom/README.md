# Qualcomm Landing Team LAVA test plans

## Brief

The Qualcomm Landing Team supports testing of the Kernel and Distros (Debian/OE RPB) using this set of templates.

These LAVA templates are based on LKFT fastboot and extends to add LXC support, We are planning to migrate to docker but
certain tasks needs to be done like create docker image to access QCOM remote lab boards (qcs-4k-* and sdm845-mtp).

## Testing

For generate example of LAVA jobs manually,


Kernel bootrr ramdisk based testing,

$ python3 -m lava_test_plans --variables projects/lt-qcom/variables.ini --testplan-device-path projects/lt-qcom/devices --device-type dragonboard-410c --dry-run --verbose 1 --test-case testcases/kernel-bootrr.yaml

Kernel rootfs based testing,

$ python3 -m lava_test_plans --variables projects/lt-qcom/variables-db845c-rootfs.ini --testplan-device-path projects/lt-qcom/devices --device-type dragonboard-845c --dry-run --verbose 1 --test-case testcases/kernel-smoke.yaml
