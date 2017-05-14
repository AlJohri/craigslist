class CraigslistException(Exception):
    pass

class CraigslistValueError(CraigslistException, ValueError):
    pass
