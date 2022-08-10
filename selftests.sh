#!/bin/bash

function run_device_selftest()
{
    python3 -m lava_test_plans --variables variables.ini --device-type $1 --dry-run --test-case $2
    echo $?
}

exit_code=0
for DEVICE_TYPE in ./lava_test_plans/devices/*
do
    for TEST in ./lava_test_plans/testcases/*.yaml
    do
        if [ -d $DEVICE_TYPE ]
        then
            for NESTED_DEVICE_TYPE in $DEVICE_TYPE/*
            do
                device_exit_code=$(run_device_selftest $(basename $DEVICE_TYPE)/$(basename $NESTED_DEVICE_TYPE) $(basename $TEST))
                if [ $device_exit_code -gt $exit_code ]; then exit_code=$device_exit_code; fi
            done
        else
            device_exit_code=$(run_device_selftest $(basename $DEVICE_TYPE) $(basename $TEST))
            if [ $device_exit_code -gt $exit_code ]; then exit_code=$device_exit_code; fi
        fi
    done
done
exit $exit_code
