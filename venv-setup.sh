#!/bin/bash

cd ./back

VENV_DIR="./.venv"

if [ -d "$VENV_DIR" ]; then
    echo "$VENV_DIR already exists."
    read -p "Do you want to delete $VENV_DIR and start over? (y/n): " answer

    case "$answer" in
        [Nn]* )
            read -p "Do you want to install additional packages? (y/n): " answer
            case "$answer" in
                [Yy]* )
                    source ./.venv/bin/activate
                    pip install -e .[dev]
                    exit 0
                    ;;
                [Nn]* )
                    echo "No additional packages installed. Exiting."
                    exit 0
                    ;;
            esac
            ;;
        [Yy]* )
            echo "Replacing $VENV_DIR..."
            rm -rf "$VENV_DIR"
            ;;
        * )
            echo "Invalid response. Exiting."
            exit 1
            ;;
    esac
fi

python3.13 -m venv .venv

source ./.venv/bin/activate
pip install -e .[dev]
