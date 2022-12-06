all: typecheck test style flake8

export PROJECT := lava-test-plans
export NUM_WORKERS=$(shell nproc)
export TUXPKG_MIN_COVERAGE := 57

include $(shell tuxpkg get-makefile)
