FROM python:3.9-slim-bullseye AS builder
ARG DEBIAN_FRONTEND=noninteractive

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --yes --no-install-recommends flit git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /lava-test-plans
RUN cd /lava-test-plans && \
    version=$(git describe | sed "s#-#.#") && \
    sed -i -e "s/^__version__.*/__version__ = \"${version}\"/" /lava-test-plans/lava_test_plans/__init__.py && \
    rm -rf .git && \
    FLIT_ALLOW_INVALID=1 flit build

FROM python:3.9-slim-bullseye
ARG DEBIAN_FRONTEND=noninteractive

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends  curl jq gcc libc6-dev python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    find /usr -depth -name __pycache__ -type d -exec rm -rf {} \;

COPY --from=builder /lava-test-plans /tmp/lava-test-plans/
RUN python3 -m pip install --no-cache-dir $(find /tmp/lava-test-plans/dist/ -name "lava_test_plans-*-py3-none-any.whl") && \
    rm -rf /tmp/lava-test-plans/ && \
    find /usr -depth -name __pycache__ -type d -exec rm -rf {} \;
