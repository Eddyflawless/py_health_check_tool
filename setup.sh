#!/bin/bash

which python3

if [[ $? -eq 1 ]]; then
    echo ""
    echo "python 3 isnot installed on this system"
    exit

fi


echo ""
echo "Upgrading pip...."

python3 -m pip install --user --upgrade pip

echo ""
echo "Installing virtualenv...."

python3 -m pip install --user virtualenv

echo ""
echo "Activating virtual environment...."

python3 -m venv env

echo ""
echo "Installing dependencies..."

sleep 5

source venv/bin/activate

if [[ -f "requirements.txt" ]]; then

    python3 -m pip install -r requirements.txt

else
    echo ""
    echo "Skipping requirements.txt because we couldnot find it"
    echo "Try pip freeze > requirements.txt to generate on"

    #python3 -m pip freeze > requirements


fi

