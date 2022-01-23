import datetime
import io
import json
import logging
import pathlib
import random
import sys

import appdirs
import diskcache
import humanfriendly
import requests


def js1(cache_path, fcn_refresh) -> str:
    with diskcache.Cache(cache_path) as reference:
        result = reference.get("clinepunk.words")
        if not result:
            logging.debug("setting cache")
            js = fcn_refresh()
            reference.set(
                "clinepunk.words",
                io.BytesIO(js),
                expire=datetime.timedelta(days=365 * 2).total_seconds(),
            )
        else:
            logging.debug("cache is still fresh, using it")
            reader = result
            js = reader.read().decode()

        return js
