#!/bin/bash
export LC_ALL=C
sudo -H pip3 install virtualenv
virtualenv -p /usr/bin/python3 source/server/server_venv
. source/server/server_venv/bin/activate
pip install Flask
deactivate
# . source/server/server_venv/bin/deactivate
# virtualenv -p /usr/bin/python3 source/client/client_venv
# . source/client/client_venv/bin/activate
# pip install pqdict
# deactivate