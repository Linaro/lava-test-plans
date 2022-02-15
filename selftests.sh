#!/bin/bash

function run_device_selftest()
{
    ./submit_for_testing.py --variables variables.ini --device-type $1 --dry-run --test-case $2
    echo $?
}

function test_for_android_templates(){
    local exit_code=0
    for F_DEVICE_TYPE in ./devices/android/*; do
        DEVICE_TYPE=$(basename "${F_DEVICE_TYPE}")
        for F_TESTCASE in ./testcases/android/*.yaml; do
            TEST=$(basename ${F_TESTCASE})
            ./submit_for_testing.py \
                --testplan-path ./testcases/android/ \
                --testplan-device-path ./devices/android/ \
                --test-case ${TEST} \
                --variables variables-android.ini \
                --device-type ${DEVICE_TYPE} \
                --dry-run \

           [ $? -ne 0 ] && exit_code=$?
        done
    done
    return ${exit_code}
}

function test_for_lts_templates(){
    local exit_code=0
    for DEVICE_TYPE in ./devices/*
    do
        if [ "X$(basename ${DEVICE_TYPE})" = "Xandroid" ]; then
            # test for android templates will be done separately
            continue
        fi
        for TEST in ./testcases/*.yaml
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

    return $exit_code
}

test_for_lts_templates
test_for_android_templates
