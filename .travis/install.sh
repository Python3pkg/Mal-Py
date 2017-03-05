#!/bin/bash
set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    sw_vers
    brew update && brew upgrade pyenv
    PYENV_ROOT="$HOME/.pyenv"
    PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"

    case "${TOXENV}" in
        py27)
            curl -O https://bootstrap.pypa.io/get-pip.py
            python get-pip.py --user
            ;;
        py33)
            pyenv install 3.3.6
            pyenv global 3.3.6
            ;;
        py34)
            pyenv install 3.4.5
            pyenv global 3.4.5
            ;;
        py35)
            pyenv install 3.5.2
            pyenv global 3.5.2
            ;;
        py36)
            pyenv install 3.6.0
            pyenv global 3.6.0
            ;;
        pypy*)
            pyenv install "pypy-$PYPY_VERSION"
            pyenv global "pypy-$PYPY_VERSION"
            ;;
        pypy3)
            pyenv install pypy3-2.4.0
            pyenv global pypy3-2.4.0
            ;;
        docs)
            brew install enchant
            curl -O https://bootstrap.pypa.io/get-pip.py
            python get-pip.py --user
            ;;
    esac
    pyenv rehash
    python -m pip install --user virtualenv
else
    # temporary pyenv installation to get latest pypy until the travis
    # container infra is upgraded
    if [[ "${TOXENV}" = pypy* ]]; then
        curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
        PYENV_ROOT="$HOME/.pyenv"
        PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init -)"
        pyenv update
        pyenv install "pypy-$PYPY_VERSION"
        pyenv global "pypy-$PYPY_VERSION"
    fi
    pip install virtualenv
fi

python -m virtualenv ~/.venv
source ~/.venv/bin/activate
pip install tox codecov