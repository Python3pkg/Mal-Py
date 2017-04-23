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
LOAD R1, R0
STORE R1, R0
MOVE R1, R0
ADD R2, R1, R0
INC R2
SUB R2, R1, R0,
DEC R2
MOVEI V63, R1
MUL R2, R1, R0
DIV R2, R1, R0
BLT R2, R1, L14
BGT R2, R1, L14
BEQ R2, R1, L14
BR L3
END
EOF

# error.mal -- run call testing with error in code
cat << EOF > error.mal
LOAD
END
EOF

tox -- $TOX_FLAGS
