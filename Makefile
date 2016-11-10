.PHONY: data virtualenv install clean cleandata

data: craigslist/data/areas.json craigslist/data/arguments.json

craigslist/data/areas.json:
	./scripts/get_areas.py > craigslist/data/areas.json

craigslist/data/arguments.json:
	./scripts/get_arguments.py > craigslist/data/arguments.json

cleandata:
	rm -f craigslist/data/areas.json
	rm -f craigslist/data/arguments.json

clean:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete

virtualenv:
	mkvirtualenv craigslist -p python3

install:
	pip install --editable .
	pip install -r requirements-dev.txt
