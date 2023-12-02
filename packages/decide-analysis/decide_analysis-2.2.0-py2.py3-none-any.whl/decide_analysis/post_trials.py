# -*- coding: utf-8 -*-
# -*- mode: python -*-
""" Script to post trials to the django-decide-host server """

import sys
import argparse
import logging
import json
import datetime
from pathlib import Path

import httpx

from decide_analysis import __version__
from decide_analysis import core

log = logging.getLogger("decide-analysis")  # root logger


def main(argv=None):
    p = argparse.ArgumentParser(
        description="""Post trial records to decide-host. Reads line-delimited json from standard input.""",
        epilog="""Example: %(prog)s -r http://pholia.lab:4000/decide/api/
        --name gng --addr beagle-1 < C291_gng.jsonl""",
    )
    p.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )
    p.add_argument("--debug", help="show verbose log messages", action="store_true")
    p.add_argument(
        "-r",
        dest="host_url",
        help="URL of the decide-host service. "
        "Default is to use the environment variable '%s'" % core.env_host,
        default=core.default_host(),
    )
    p.add_argument("-n", "--name", help="name of procedure (required)", required=True)
    p.add_argument("-a", "--addr", help="controller name (required)", required=True)
    args = p.parse_args(argv)
    core.setup_log(log, args.debug)
    log.debug(args)

    fixed_params = {"addr": args.addr, "name": args.name}

    if args.host_url is None:
        p.error("host URL not specified as argument or environment variable")
    with httpx.Client(headers={"Accept": "application/json"}) as session:
        try:
            r = session.head(args.host_url, follow_redirects=True)
            r.raise_for_status()
            trial_url = r.links["trials"]["url"]
        except httpx.HTTPStatusError as e:
            p.error(e)
        except KeyError:
            p.error("unable to determine URL for posting trials subject")
        log.info("Posting records to %s", trial_url)

        n = 0
        for i, line in enumerate(sys.stdin):
            data = json.loads(line.strip())
            r = session.post(trial_url, json=(data | fixed_params))
            if r.status_code == 400:
                # this is usually because the record is already in the database
                log.debug("%skipped %d: server replied %s", i, r.text)
            else:
                n += 1
        log.info("Posted %d/%d record(s)", n, i + 1)


if __name__ == "__main__":
    main()
