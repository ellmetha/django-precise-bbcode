.PHONY: install upgrade lint coverage travis docs

install:
	pip install -r dev-requirements.txt
	pip install -e .

upgrade:
	pip install -r dev-requirements.txt -U
	pip install -e . -U

lint:
	flake8

isort:
	isort -sl --recursive --check-only --diff precise_bbcode tests -s migrations

coverage:
	py.test --cov-report term-missing --cov precise_bbcode

spec:
	py.test --spec -p no:sugar

travis: install lint coverage isort

docs:
	cd docs && make html
