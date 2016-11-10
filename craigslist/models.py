from collections import namedtuple

class BasePost:
    __slots__ = ()

    def __new__(cls, **kwargs):
        return super().__new__(cls, *[kwargs[k] for k in cls._fields])

BaseJSONSearchPost = namedtuple('RegularSearchPost', [
    'id',
    'title',
    'url',
    'longitude',
    'latitude',
    'price',
    'bedrooms',
    'date',
    'thumbnail',
    'category_id'])

class JSONSearchPost(BaseJSONSearchPost, BasePost):
    pass

BaseJSONSearchCluster = namedtuple('BaseJSONSearchCluster', [
    'id',
    'url',
    'longitude',
    'latitude',
    'posting_ids',
    'num_posts',
    'date'])

class JSONSearchCluster(BaseJSONSearchCluster, BasePost):
    pass

BaseRegularSearchPost = namedtuple('RegularSearchPost', [
    'id',
    'title',
    'url',
    'repost_id',
    'price',
    'bedrooms',
    'date',
    'area'])

class RegularSearchPost(BaseRegularSearchPost, BasePost):
    pass

BaseDetailPost = namedtuple('BaseDetailPost', [
    'id',
    'title',
    'url',
    # 'longitude',
    # 'latitude',
    # 'price',
    # 'bedrooms',
    # 'date',
    # 'thumbnail',
    # 'category_id'
])

class DetailPost(BaseDetailPost, BasePost):
    pass
