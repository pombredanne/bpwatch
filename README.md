Logplex-Instrument
==================

This is a simple CLI for instrumenting buildpacks.

You should be able to just stick it in a directory and go:

    $ git clone git@github.com:kennethreitz/logplex-instrument.git
    $ cd logplex-instrument
    $ make
    $ ./lplex

You can then move `lp` and `lp.zip` wherever you like.


Usage
-----

Configure logplex with the disired prefix and token:

    $ lp init python secretlogplextoken

Log something:

    $ lplex log life 42

Start a timer:

    $ lplex start dance

End a timer:

    $ $ lplex stop dance

Logplex output of all above:

    2013-07-16T07:44:15+00:00 app[python-logplex]: measure.python.life=42
    2013-07-16T07:44:21+00:00 app[python-logplex]: measure.python.dance.start=2013-07-16T07:44:21.550399+00:00
    2013-07-16T07:44:24+00:00 app[python-logplex]: measure.python.dance.end=2013-07-16 07:44:24.246280
    2013-07-16T07:44:24+00:00 app[python-logplex]: measure.python.dance.duration=2.695881

Configuration
-------------

By default, `lplex` stores its data in `lplex.json`. This is configurable with the `LP_STORE_PATH` environment variable.

    $ export LP_STORE_PATH=/tmp/somefile

By default, `lplex` requires that its distro (`lplex.zip`) is next to the executable. This is configurable with the `LP_DISTRO_PATH` environment variable.

    $ export LP_DISTRO_PATH=/tmp/lplex.zip

