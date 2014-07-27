.PHONY: install upgrade coverage travis docs

install:
		pip install -r requirements.txt
		python setup.py develop

upgrade:
		pip install --upgrade -r requirements.txt
		python setup.py develop --upgrade

coverage:
		coverage run --source=precise_bbcode ./runtests.py
		coverage report -m

travis: install coverage

docs:
	cd docs && make html