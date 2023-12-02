# -*- coding: utf-8 -*-
# -*- mode: python -*-
""" Script to bulk retrieve data from the django-decide-host server """

import sys
import argparse
import logging
import csv
import datetime

import httpx

from decide_analysis import __version__
from decide_analysis import core

log = logging.getLogger("decide-analysis")  # root logger


class ParseKeyVal(argparse.Action):
    def parse_value(self, value):
        import ast

        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value

    def __call__(self, parser, namespace, arg, option_string=None):
        kv = getattr(namespace, self.dest)
        if kv is None:
            kv = dict()
        if not arg.count("=") == 1:
            raise ValueError("-k %s argument badly formed; needs key=value" % arg)
        else:
            key, val = arg.split("=")
            kv[key] = self.parse_value(val)
        setattr(namespace, self.dest, kv)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="""Retrieve trial records from decide-host and ouput them as
        a CSV. Optional arguments allow filtering of the records to specific
        date ranges or on any of the fields of the records.""",
        epilog="""Example: %(prog)s -r http://pholia.lab:4000/decide/api/
        --from-date 2022-03-01 --to-date 2022-03-09 -k experiment=2ac-config-segmented10 C14""",
    )
    p.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )
    p.add_argument(
        "-r",
        dest="host_url",
        help="URL of the decide-host service. "
        "Default is to use the environment variable '%s'" % core.env_host,
        default=core.default_host(),
    )
    p.add_argument(
        "--output",
        "-o",
        help="the file to write the records to. If not set, outputs to stdout",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )
    p.add_argument(
        "--fields",
        help="specify which fields to store in the output as a comma-delimited list. "
        " If not set, uses the fields in the first record",
        type=lambda val: val.split(","),
    )
    p.add_argument("--debug", help="show verbose log messages", action="store_true")
    p.add_argument(
        "--max-records", "-N", type=int, help="maximum number of records to retrieve"
    )
    p.add_argument(
        "--from-date",
        "-f",
        help="only retrieve records on or after %(metavar)s",
        metavar="DATE",
        type=datetime.date.fromisoformat,
    )
    p.add_argument(
        "--to-date",
        "-t",
        help="only retrieve records up to (and not including) %(metavar)s",
        metavar="DATE",
        type=datetime.date.fromisoformat,
    )
    p.add_argument(
        "--exclude-date",
        "-e",
        help="exclude records on %(metavar)s",
        action="append",
        default=list(),
        metavar="DATE",
        type=datetime.date.fromisoformat,
    )
    p.add_argument(
        "-k",
        help="only retrieve records with %(metavar)s (use multiple -k for multiple values)",
        action=ParseKeyVal,
        default=dict(),
        metavar="KEY=VALUE",
        dest="data_params",
    )
    p.add_argument(
        "--name",
        "-n",
        help="only retrieve records with name=%(metavar)s",
        metavar="NAME",
    )
    p.add_argument("subject", help="retrieve records for this subject")

    args = p.parse_args(argv)
    core.setup_log(log, args.debug)
    log.debug(args)

    if args.host_url is None:
        p.error("host URL not specified as argument or environment variable")
    with httpx.Client(headers={"Accept": "application/json"}) as session:
        try:
            r = session.head(args.host_url, follow_redirects=True)
            r.raise_for_status()
            subjects_url = r.links["subjects"]["url"]
            r = session.head(f"{subjects_url}{args.subject}/")
            r.raise_for_status()
            trial_url = r.links["trials"]["url"]
        except httpx.HTTPStatusError as e:
            p.error(e)
        except KeyError:
            p.error(f"unable to look up trial URL for subject {args.subject}")
    log.info("Retrieving records from %s", trial_url)

    params = {
        "name": args.name,
        "date_after": args.from_date,
        "date_before": args.to_date,
    }
    for k, v in args.data_params.items():
        params[f"data__{k}"] = v
    query_params = {k: v for k, v in params.items() if v is not None}
    log.debug("query parameters: %s", query_params)

    writer = None
    for i, record in enumerate(core.iter_records(trial_url, **query_params)):
        rectime = datetime.datetime.fromisoformat(record["time"])
        if rectime.date() in args.exclude_date:
            continue
        if writer is None:
            if args.fields is None:
                args.fields = record.keys()
            writer = csv.DictWriter(
                args.output, fieldnames=args.fields, extrasaction="ignore"
            )
            writer.writeheader()
        writer.writerow(record)
        if args.max_records is not None and i > args.max_records:
            break


if __name__ == "__main__":
    main()
