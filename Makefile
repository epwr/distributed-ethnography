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
	$(shell yq -o='shell' '.env_variables' config/testing.toml \
	| tr '\n' ' ' \
	| sed 's|$$|./$(VENV)/bin/python3 -m pytest|')

# Use `yq` to parse config/testing.toml and set the env variables. Then run coverage.
coverage: venv
	touch .gitignore  # used to force make to run test every time 
	$(shell yq -o='shell' '.env_variables' config/testing.toml \
	| tr '\n' ' ' | \
	sed 's|$$|./$(VENV)/bin/coverage run -m pytest|')
	./$(VENV)/bin/coverage report --show-missing --fail-under=100

run: venv
	touch .gitignore  # used to force make to run command every time 
	$(shell yq -o='shell' '.env_variables' config/local.toml \
	| tr '\n' ' ' \
	| sed 's|$$|./$(VENV)/bin/python3 serve.py|')

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete


setup-db:
	$(shell yq -o='shell' '.env_variables.SQLITE_FILE' config/local.toml \
	| tr '\n' ' ' \
	| sed "s|value='\(.*\)'|sqlite3 '\1' < data/setup.sql|")

.PHONY: all test venv run clean coverage


