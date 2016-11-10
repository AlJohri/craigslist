# craigslist

Python wrapper for craigslist.

**NOTE**: This library is a WIP. The API is not stable.

## Disclaimer

- This library is not associated with Craigslist.
- Please read the Craigslist [terms of use](https://www.craigslist.org/about/terms.of.use.en).

## Install
```
pip3 install --upgrade git+https://github.com/AlJohri/craigslist.git
```

## API

See the [examples](./examples) folder.

```python
from craigslist import search

for post in search('washingtondc', 'apa', postal=20071, search_distance=1):
    print(post)
```

## CLI

```
usage: craigslist search area category [options]

positional arguments:
  area
  category

optional arguments:
  -h, --help            show this help message and exit
  --parking [{carport,street_parking,detached_garage,no_parking,attached_garage,off_street_parking,valet_parking} [{carport,street_parking,detached_garage,no_parking,attached_garage,off_street_parking,valet_parking} ...]]
  --is_internship
  --srchType
  --employment_type [{part_time,employees_choice,contract,full_time} [{part_time,employees_choice,contract,full_time} ...]]
  --laundry [{w_d_hookups,laundry_in_bldg,laundry_on_site,w_d_in_unit,no_laundry_on_site} [{w_d_hookups,laundry_in_bldg,laundry_on_site,w_d_in_unit,no_laundry_on_site} ...]]
  --search_distance SEARCH_DISTANCE
  --min_price MIN_PRICE
  --max_price MAX_PRICE
  --searchNearby
  --sale_date SALE_DATE
  --wheelchaccess
  --pets_dog
  --no_smoking
  --postal POSTAL
  --is_furnished
  --postedToday
  --is_telecommuting
  --availabilityMode {within_30_days,all_dates,beyond_30_days}
  --housing_type [{condo,manufactured,house,duplex,townhouse,assisted_living,loft,land,in_law,apartment,flat,cottage_cabin} [{condo,manufactured,house,duplex,townhouse,assisted_living,loft,land,in_law,apartment,flat,cottage_cabin} ...]]
  --bathrooms {8plus_bathrooms,5plus_bathrooms,6plus_bathrooms,1plus_bathrooms,4plus_bathrooms,2plus_bathrooms,7plus_bathrooms,3plus_bathrooms}
  --hasPic
  --pets_cat
  --is_nonprofit
  --bedrooms {3plus_bedrooms,1plus_bedrooms,8plus_bedrooms,6plus_bedrooms,4plus_bedrooms,7plus_bedrooms,2plus_bedrooms,5plus_bedrooms}
  --maxSqft MAXSQFT
  --condition [{new,fair,excellent,salvage,like_new,good} [{new,fair,excellent,salvage,like_new,good} ...]]
  --minSqft MINSQFT
  --verbose
  --detail
  --executor_class EXECUTOR_CLASS
  --cachedir CACHEDIR   Cache directory. Defaults to ~/.craigslist
  --nocache
```

## Development

### Setup

```
make virtualenv install
```

### Test

```
workon craigslist
py.test
```