all: typecheck test style flake8

export PROJECT := lava_test_plans

include $(shell tuxpkg get-makefile)
