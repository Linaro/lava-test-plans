FROM python:3.8-slim-buster
ARG DEBIAN_FRONTEND=noninteractive

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3-pip \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

COPY . /lava-test-plans
RUN pip3 install -r /lava-test-plans/requirements.txt
