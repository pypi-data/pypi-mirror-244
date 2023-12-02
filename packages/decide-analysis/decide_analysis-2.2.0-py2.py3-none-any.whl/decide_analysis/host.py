# -*- coding: utf-8 -*-
# -*- mode: python -*-
"""Functions to retrieve data from a decide-host http server

Copyright (C) 2015 Dan Meliza <dmeliza@gmail.com>
Created Sat May 30 17:41:56 2015
"""

# python 3 compatibility
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

from decide_analysis.core import logger
import requests as rq
import posixpath as path

log = logger('host')
HTTPError = rq.exceptions.HTTPError

def json(url, **params):
    """Retrieve json data from server and return as a dictionary, or None if no data"""
    r = rq.get(url, params=params, headers={'Accept': 'application/json'}, verify=False)
    log.debug("GET %s", r.url)
    r.raise_for_status()
    return r.json()


def json_stream(url, **params):
    """Retrieve json objects from a streaming response; returns an iterator"""
    import json
    r = rq.get(url, params=params, headers={'Accept': 'application/json'},
               verify=False, stream=True)
    log.debug("GET %s", r.url)
    r.raise_for_status()
    for line in r.iter_lines(decode_unicode=True, delimiter="\n"):
        if line: yield json.loads(line)


def timestamp(dt):
    """
    Converts datetime object to ms since the epoch. If dt is not a datetime
    object, returns it without alteration.
    """
    import time
    from datetime import date
    if isinstance(dt, date):
        return int(time.mktime(dt.timetuple()) * 1000)
    try:
        return int(time.mktime(dt.timetuple()) * 1000 + dt.microsecond / 1000)
    except AttributeError:
        return dt

def convert_req_times(params):
    """Replaces any datetime values in params with long timestamps"""
    return {k: timestamp(v) for k,v in params.items()}


def find_events(base_url, controller, **kwargs):
    params = convert_req_times(kwargs)
    url = path.join(base_url, "api", "controllers", controller, "events")
    return json_stream(url, **params)


def find_controllers(base_url, **params):
    url = path.join(base_url, "api", "controllers")
    return json_stream(url, **params)


def find_one_subject(base_url, subject):
    return json(path.join(base_url, "api", "subjects", subject))


def find_subjects(base_url, **params):
    return json_stream(path.join(base_url, "api", "subjects"), **params)


def find_trials(base_url, subject, **kwargs):
    params = convert_req_times(kwargs)
    url = path.join(base_url, "api","subjects", subject, "trials")
    return json_stream(url, **params)

# Variables:
# End:
