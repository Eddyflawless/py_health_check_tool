.PHONY=init

init:
	- @python3 -m venv venv
	- @echo "-------------VIRTUAL ENVIRONMENT UP-------------------"

setup:
	- ./setup.sh

start:
	- @python3 main.py
