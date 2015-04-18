.PHONY: install upgrade coverage travis docs

install:
		pip install -r requirements.txt
		python setup.py develop

upgrade:
		pip install --upgrade -r requirements.txt
		python setup.py develop --upgrade

coverage:
		py.test --cov-report term-missing --cov precise_bbcode

travis: install coverage

docs:
	cd docs && make html