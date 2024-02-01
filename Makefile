# define the name of the virtual environment directory
VENV := venv
APP_DIR := app

# default target, when make executed without arguments
all: test

#
$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r ./requirements/requirements.txt -r ./requirements/requirements-dev.txt

venv: $(VENV)/bin/activate

# Use `yq` to parse config/testing.toml and set the env variables. Then run pytest.
test: venv
	touch .gitignore  # used to force make to run test every time 
	$(shell yq -o='shell' '.env_variables' config/testing.toml | tr '\n' ' ' | sed 's|$$|./$(VENV)/bin/python3 -m pytest|')

run: venv
	./$(VENV)/bin/python3 $(APP_DIR)/main.py

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all test venv run clean

