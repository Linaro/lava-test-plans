all: typecheck test style flake8

export PROJECT := lava-test-plans

include $(shell tuxpkg get-makefile)