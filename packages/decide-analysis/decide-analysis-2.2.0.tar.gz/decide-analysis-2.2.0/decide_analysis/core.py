# -*- coding: utf-8 -*-
# -*- mode: python -*-
"""Core functions for decide-analysis"""

import os
import logging
import httpx

# from tzlocal import get_localzone

# timezone = get_localzone()
env_host = "DECIDE_HOST"
log = logging.getLogger("decide-analysis")  # root logger


def setup_log(log, debug=False):
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    loglevel = logging.DEBUG if debug else logging.INFO
    log.setLevel(loglevel)
    ch.setLevel(loglevel)
    ch.setFormatter(formatter)
    log.addHandler(ch)


def default_host():
    """Return the URL associated with the default host environment variable"""
    return os.environ.get(env_host, None)


def iter_records(url, nocomment=True, **params):
    """Iterates over records from the database, sending additional requests as
    needed to retrieve multiple pages.

    url: the URL of the endpoint for the records you want (use get_endpoint to look this up)
    nocomment: whether to exclude comments from the query (true by default)

    Additional keyword arguments are passed to the server as query parameters.
    Note that the server may require certain query keys to be prefixed with
    "data__"

    Example:

    iter_records("http://pholia.lab:4000/decide/api/trials", subject="C14", date_after="2022-10-15")

    """
    params["nocomment"] = nocomment
    with httpx.Client(headers={"Accept": "application/json"}) as session:
        r = session.get(url, params=params)
        log.debug("GET %s", r.url)
        r.raise_for_status()
        for d in r.json():
            yield d
        while "next" in r.links:
            url = r.links["next"]["url"]
            r = session.get(url)
            log.debug("GET %s", r.url)
            r.raise_for_status()
            for d in r.json():
                yield d
