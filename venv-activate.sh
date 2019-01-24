#!/usr/bin/env bash

function venv-activate() {
    function display_venvs {
        $(which ls) -1 ${HOME}/venvs/ | sed 's/^/* /'
    }
    if [[ -z "$1" ]]; then
        printf "\nEnter a virtual environment:\n"
        display_venvs
    elif [[ -d "${HOME}/venvs/$1" ]]; then
        source "${HOME}/venvs/$1/bin/activate"
        return 0
    else
        printf "\n$1 is not a valid virtual environment."
        printf "\nSelect from one of:\n"
        display_venvs
    fi
    return 1
}
