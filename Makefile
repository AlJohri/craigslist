.PHONY: data virtualenv install clean cleandata
.DELETE_ON_ERROR:

data: craigslist/data/arguments.json

craigslist/data/areas.json:
	./scripts/get_areas.py > $@

craigslist/data/categories.json:
	./scripts/get_categories.py > $@

craigslist/data/arguments.json: craigslist/data/areas.json craigslist/data/categories.json
	./scripts/get_arguments.py > $@

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
	pip install --editable .
	pip install -r requirements-dev.txt

test:
	python setup.py test

build:
	python setup.py sdist bdist_wheel

build-exe:
	python cxfreeze_setup.py build

upload:
	twine upload dist/*
