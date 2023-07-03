# encoding: utf-8

"""Release information about Marrow Mailer."""

from collections import namedtuple

VersionInfo = namedtuple(
	'Version', (
		'major',
		'minor',
		'micro',
		'releaselevel',
		'serial',
	),
)

AuthorInfo = namedtuple(
	'Author', (
		'name',
		'email',
	),
)

info = VersionInfo(4, 1, 3, 'dev', 0)
release = f"{info.releaselevel[0]}{info.serial}" if info.releaselevel != "final" else ""
version = f"{info.major}.{info.minor}.{info.micro}{release}"

author = AuthorInfo("Alice Bevan-McGregor", 'alice@gothcandy.com')

description = "A light-weight modular mail delivery framework for Python 2.7+, 3.3+, Pypy, and Pypy3."
url = "https://github.com/checksecltd/mailer"
