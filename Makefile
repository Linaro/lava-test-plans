all: typecheck test style flake8

export PROJECT := lava_test_plans
#export NUM_WORKERS=$(shell nproc)
export TUXPKG_MIN_COVERAGE := 45

include $(shell tuxpkg get-makefile)
