FROM python:3.8-slim-buster AS git_builder
ARG DEBIAN_FRONTEND=noninteractive

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
      git \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

COPY . /lava-test-plans
RUN echo "lava-test-plans version: $(git -C /lava-test-plans describe)"> /lava-test-plans/.version
RUN rm -rf /lava-test-plans/.git

FROM python:3.8-slim-buster
ARG DEBIAN_FRONTEND=noninteractive

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      jq \
      python3-pip \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

COPY --from=git_builder /lava-test-plans /lava-test-plans
RUN pip3 install -r /lava-test-plans/requirements.txt
