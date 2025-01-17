#!/usr/bin/env python
"""
This simple script checks the DNSSEC validity of a zone.

Copyright 2013 - Kumina B.V./Pieter Lexis
Copyright 2016 - Pieter Lexis
Licensed under the terms of the GNU GPL version 3 or higher
"""
# Import the classes needed
import argparse
from sys import exit, argv
try:
    import unbound
except ImportError:
    print("Please install the python-bindings for unbound")
    exit(1)

__version__ = '1.0.0'

# Define and initialize global variables
exit_ok = 0
exit_warn = 1
exit_crit = 2
exit_err = 3
msg = ""


def parse_args(args=None):
    args = args or argv[1:]

    parser = argparse.ArgumentParser(
        description=(
            "This script tests the zone for validation failures by looking "
            "up the SOA record. This script is meant to be invoked by "
            "nagios/icinga."
        ),
    )
    parser.add_argument(
        "--zone", "-z",
        action="store",
        metavar='ZONE',
        help="The zone to be checked",
        required=True,
    )
    parser.add_argument(
        "--insecure-is-ok",
        action="store_true",
        dest="insecureOK",
        help=(
            "When the result of the check is insecure, the state is "
            "OK and not WARNING."
        ),
    )
    parser.add_argument(
        "--trust-anchor-file",
        metavar='PATH',
        help=(
            "Pick alternate path to trust anchor file "
            "(default: /var/lib/icinga2/root.key)"
        ),
        default='/var/lib/icinga2/root.key',
    )

    return parser.parse_args(args)


def quit(state):
    print(msg)
    exit(state)


def addToMsg(newString):
    global msg
    if msg != "":
        msg += " %s" % newString
    else:
        msg += "%s" % newString


def main():
    args = parse_args()

    ctx = unbound.ub_ctx()

    # This key-file should be created once using unbound-anchor(8)
    ctx.set_option('auto-trust-anchor-file:', args.trust_anchor_file)

    status, result = ctx.resolve(args.zone, rrtype=unbound.RR_TYPE_SOA)

    if status != 0:
        addToMsg("UNKNOWN: resolver failure.")
        quit(exit_err)

    if result.secure:
        addToMsg("OK %s: the chain of trust is valid." % args.zone)
        quit(exit_ok)

    if result.bogus:
        addToMsg("CRITICAL %s: %s" % (args.zone, result.why_bogus))
        quit(exit_crit)

    # The result is insecure
    if args.insecureOK:
        addToMsg("OK %s: is insecure." % args.zone)
        quit(exit_ok)

    addToMsg("WARNING %s: Result not secure (but not bogus)" % args.zone)
    quit(exit_warn)


if __name__ == '__main__':
    main()
