#!/bin/sh
set -euo pipefail

for toxenv in py37 flake8 pylint mypy
do
        sudo docker run \
                --rm -t \
                -v "$PWD"/massdevextractor:/data \
                -w /data \
                -e TOX_WORK_DIR=/tmp \
                xsteadfastx/tox-python:full \
                /bin/sh -c " sudo apt-get update; sudo apt-get install -y gcc; tox -v -e $toxenv"
done
