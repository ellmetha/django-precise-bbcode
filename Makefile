.PHONY: init install qa lint tests spec coverage docs


init:
	poetry install


# DEVELOPMENT
# ~~~~~~~~~~~
# The following rules can be used during development in order to compile generate locales, build
# documentation, etc.
# --------------------------------------------------------------------------------------------------

# Generate the project's .po files.
messages:
	cd precise_bbcode && poetry run python -m django makemessages -a

# Compiles the project's .po files.
compiledmessages:
	cd precise_bbcode && poetry run python -m django compilemessages

# Builds the documentation.
docs:
	cd docs && rm -rf _build && poetry run make html


# QUALITY ASSURANCE
# ~~~~~~~~~~~~~~~~~
# The following rules can be used to check code quality, import sorting, etc.
# --------------------------------------------------------------------------------------------------

qa: lint isort

# Code quality checks (eg. flake8, eslint, etc).
lint:
	poetry run flake8

# Import sort checks.
isort:
	poetry run isort --check-only --diff precise_bbcode tests


# TESTING
# ~~~~~~~
# The following rules can be used to trigger tests execution and produce coverage reports.
# --------------------------------------------------------------------------------------------------

# Just runs all the tests!
tests:
	poetry run py.test

# Collects code coverage data.
coverage:
	poetry run py.test --cov-report term-missing --cov precise_bbcode

# Run the tests in "spec" mode.
spec:
	poetry run py.test --spec -p no:sugar
