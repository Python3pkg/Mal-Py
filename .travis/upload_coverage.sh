#!/bin/bash

set -e
set -x

case "${TOXENV}" in
    pypy-nocoverage);;
    pep8);;
    py3pep8);;
    docs);;
    *)
        bash <(curl -s https://codecov.io/bash) -e TRAVIS_OS_NAME,TOXENV
        ;;
esac