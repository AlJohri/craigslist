#!/usr/bin/env python3

import csv
import json
import arrow
from geopy.distance import vincenty

with open("posts.json") as f:
	posts = json.load(f)

print(posts)