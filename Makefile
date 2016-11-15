.PHONY: data virtualenv install clean cleandata
.DELETE_ON_ERROR:

data: craigslist/data/areas.json craigslist/data/categories.json craigslist/data/arguments.json

craigslist/data/areas.json:
	./scripts/get_areas.py > $@

craigslist/data/categories.json:
	./scripts/get_categories.py > $@

craigslist/data/arguments.json:
	./scripts/get_arguments.py > $@

cleandata:
	rm -f craigslist/data/areas.json
	rm -f craigslist/data/categories.json
	rm -f craigslist/data/arguments.json

clean:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete

virtualenv:
	mkvirtualenv craigslist -p python3.6

install:
	pip install --editable .
	pip install -r requirements-dev.txt

register:
	python setup.py register

upload:
	python setup.py sdist upload
