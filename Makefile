.PHONY: data virtualenv install clean cleandata
.DELETE_ON_ERROR:

data: craigslist/data/arguments.json

craigslist/data/areas.json:
	pipenv run ./scripts/get_areas.py > $@

craigslist/data/categories.json:
	pipenv run ./scripts/get_categories.py > $@

craigslist/data/arguments.json: craigslist/data/areas.json craigslist/data/categories.json
	pipenv run ./scripts/get_arguments.py > $@

cleandata:
	rm -f craigslist/data/areas.json
	rm -f craigslist/data/categories.json
	rm -f craigslist/data/arguments.json

clean:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf build
	rm -rf dist

install:
	pip install --upgrade -q pipenv
	pipenv install
	pipenv run pip install -e .

test:
	pipenv run python -m pytest

build:
	pipenv run python setup.py sdist bdist_wheel

build-exe:
	pipenv run python cxfreeze_setup.py build

upload:
	pipenv run twine upload dist/*
