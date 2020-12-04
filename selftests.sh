#!/bin/bash

function run_device_selftest()
{
    ./submit_for_testing.py --variables variables.ini --device-type $1 --dry-run --test-case $2
}

exit_code=0
for DEVICE_TYPE in ./devices/*
do
    for TEST in ./testcases/*.yaml
    do
        if [ -d $DEVICE_TYPE ]
        then
            for NESTED_DEVICE_TYPE in $DEVICE_TYPE/*
            do
                run_device_selftest $(basename $DEVICE_TYPE)/$(basename $NESTED_DEVICE_TYPE) $(basename $TEST)
                device_exit_code=$?
                if [ $device_exit_code -gt $exit_code ]; then exit_code=$device_exit_code; fi
            done
        else
            run_device_selftest $(basename $DEVICE_TYPE) $(basename $TEST)
            device_exit_code=$?
            if [ $device_exit_code -gt $exit_code ]; then exit_code=$device_exit_code; fi
        fi
    done
done
exit $exit_code
