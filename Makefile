# define the name of the virtual environment directory
VENV := venv
APP_DIR := app

# default target, when make executed without arguments
all: venv

#
$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r ./requirements/requirements.txt -r ./requirements/requirements-dev.txt

venv: $(VENV)/bin/activate

test: venv
	./$(VENV)/bin/python3 -m pytest

run: venv
	./$(VENV)/bin/python3 $(APP_DIR)/main.py

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean

