.PHONY: clean

all: posts.json stations.json ranked_posts.csv

posts.json:
	./scrape.py washingtondc --postal 20071 --distance 2 --min_price 900 --max_price 1500 --has_picture --availability within_30_days > posts.json

stations.json:
	curl -s -H 'api_key: ${WMATA_API_KEY}' https://api.wmata.com/Rail.svc/json/jStations | jsonpp > stations.json

ranked_posts.csv:
	./rank.py > ranked_posts.csv

clean:
	rm -f posts.json
	rm -f stations.json
	rm -f ranked_posts.csv
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete