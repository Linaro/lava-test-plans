all: typecheck test style flake8

export PROJECT := lava_test_plans
export NUM_WORKERS=$(shell nproc)

include $(shell tuxpkg get-makefile)
