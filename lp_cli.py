#!/usr/bin/env python

"""
Logplex instrumentation.

Usage:
  lp init <language> [<token>]
  lp start <event>
  lp stop <event>
  lp log <event> <value>
  lp -h | --help
  lp --debug

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import json
import sys
import os
from datetime import datetime, timedelta

# Path hack
sys.path.insert(0, os.path.abspath('../vendor'))

from logplex import Logplex
from docopt import docopt

def dispatch_cli(args):

    if args.get('init'):
        init(args.get('<language>'), args.get('<token>'))

    if args.get('--debug'):
        print get_state()


    if args.get('log'):
        log(args.get('<event>'), args.get('<value>'))

    if args.get('start'):
        start(args.get('<event>'))

    if args.get('stop'):
        stop(args.get('<event>'))


def get_state():
    try:
        with open('lp.json', 'r') as f:
            return json.loads(f.read())
    except IOError:
      with open('lp.json', 'w') as f:
        f.write(json.dumps(dict()))
        return get_state()

def set_state(state):
    with open('lp.json', 'w') as f:
        f.write(json.dumps(state))

def get_logplex(state):
    return Logplex(token=state.get('token'))

def format_entry(state, event, value=None):

    lang = state.get('language')
    return 'measure.{lang}.{event}={value}'.format(lang=lang, event=event, value=value)


def to_timestamp(dt=None):
    if dt is None:
        dt = datetime.utcnow()
    return '{}+00:00'.format(dt.isoformat())

def from_timestamp(ts):

    ts = ts.split('+', 1)[0]
    dt_s, _, us= ts.partition(".")
    dt= datetime.strptime(dt_s, "%Y-%m-%dT%H:%M:%S")
    us= int(us.rstrip("Z"), 10)
    return dt + timedelta(microseconds=us)


def init(language, token=None):
    state = get_state()
    state['language'] = language
    state['token'] = token

    set_state(state)

def start(event):
    state = get_state()
    now = to_timestamp()

    if 'starts' not in state:
        state['starts'] = {}

    state['starts'][event] = now

    set_state(state)

    log('{}.start'.format(event), now)

def stop(event):
    state = get_state()

    now = datetime.utcnow()
    try:
        then = from_timestamp(state['starts'][event])
        delta = (now - then).total_seconds()
    except KeyError:
        # Stopping an event that never started.
        delta = None

    log('{}.end'.format(event), now)
    if delta:
        log('{}.duration'.format(event), delta)


def log(event, value):
    state = get_state()
    logplex = get_logplex(state)
    entry = format_entry(state, event, value)
    logplex.puts(entry)

def main():
    arguments = docopt(__doc__, version='Logplex')
    try:
        dispatch_cli(arguments)
    except Exception:
        exit()

if __name__ == '__main__':
    main()
