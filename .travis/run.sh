#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == "Darwin" || "${TOXENV}" == pypy* ]]; then
    # initialize our pyenv
    PYENV_ROOT="$HOME/.pyenv"
    PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
fi

source ~/.venv/bin/activate

###I/O files for testing
# basic.mal -- run call testing
cat << EOF > basic.mal
MOVEI V00, R0
END
EOF

tox -- $TOX_FLAGS
