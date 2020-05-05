"""
This file is part of famafrench.
Copyright (c) 2020, Christian Jauregui <chris.jauregui@berkeley.edu>
See file LICENSE.txt for license information.

This file must be kept very simple, because it is consumed from several places.
It is imported by famafrench/__init__.py, execfile'd by setup.py, etc.

I use a simple scheme: 1.0.0 -> 1.0.0+dev -> 1.1.0 -> 1.1.0+dev
where the +dev versions are never publicly released - they are just what I
stick into the VCS in between releases.

This is compatible with PEP 440:
   http://legacy.python.org/dev/peps/pep-0440/
via the use of the "local suffix" "+dev", which is disallowed on index
servers and causes 1.0.0+dev to sort after plain 1.0.0, which is what I
want. (Contrast with the special suffix 1.0.0.dev, which sorts *before* 1.0.0.)

"""

__version__ = "0.1.3"
