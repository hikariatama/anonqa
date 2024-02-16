#!/bin/bash

# Format HTML+CSS via Prettier
prettier --write --list-different --ignore-unknown . --log-level silent
echo -e "\e[32m\e[1mHTML+CSS formatted with \033[38;5;208mprettier\x1b[0m \xF0\x9F\x98\x81\e[0m"

# Format Python imports using isort
isort . --quiet
echo -e "\e[32m\e[1mPython imports formatted with \033[38;5;208misort\x1b[0m \xF0\x9F\x98\x81\e[0m"

# Format Python code with black
black . --preview --quiet
echo -e "\e[32m\e[1mPython code formatted with \033[38;5;208mblack\x1b[0m \xF0\x9F\x98\x81\e[0m"

# Run Ruff checks
if ruff check .; then
    echo -e "\e[1m\033[38;5;208mRuff\e[32m checks passed \xF0\x9F\x98\x81\e[0m"
fi
