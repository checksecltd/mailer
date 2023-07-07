#!/usr/bin/env python
# encoding: utf-8

import sys

try:
	from setuptools.core import setup, find_packages
except ImportError:
	from setuptools import setup, find_packages

assert sys.version_info >= (3, 8), "Python 3.8 or later is required."

version = "4.2.1"
author = "Alice Bevan-McGregor"
author_email = "alice@gothcandy.com"
description = "A light-weight modular mail delivery framework for 3.8+, Pypy, and Pypy3."
url = "https://github.com/checksecltd/mailer"

tests_require = [
	'pytest',
	'pytest-cov',
	'pytest-spec',
	'pytest-flakes',
	'coverage',
	'transaction',
	'py3dns',
]


# # Entry Point

setup(
		name = "marrowmailer",
		version = version,
		
		description = description,
		long_description = "",
		url = url,
		
		author = author,
		author_email = author_email,
		
		license = 'MIT',
		keywords = '',
		classifiers = [
				"Development Status :: 5 - Production/Stable",
				"Environment :: Console",
				"Intended Audience :: Developers",
				"License :: OSI Approved :: MIT License",
				"Operating System :: OS Independent",
				"Programming Language :: Python",
				"Programming Language :: Python :: 3.8",
				"Programming Language :: Python :: 3.9",
				"Programming Language :: Python :: 3.10",
				"Programming Language :: Python :: 3.11",
				"Topic :: Software Development :: Libraries :: Python Modules",
				"Topic :: Utilities",
			],
		
		packages = find_packages(exclude=['example', 'test', 'test.*']),
		include_package_data = True,
		package_data = {'': ['README.textile', 'LICENSE.txt']},
		
		# ## Dependency Declaration
		
		install_requires = ['python-magic'],
		
		extras_require = {
				":python_version<'3.0.0'": ['futures'],
				'develop': tests_require,
				'requests': ['requests'],
			},
		
		tests_require = tests_require,
		
		setup_requires = ['pytest-runner'] if {'pytest', 'test', 'ptr'}.intersection(sys.argv) else [],
		
		# ## Plugin Registration
		
		entry_points = {
				'marrow.mailer.manager': [
						'immediate = marrow.mailer.manager.immediate:ImmediateManager',
						'futures = marrow.mailer.manager.futures:FuturesManager',
						'dynamic = marrow.mailer.manager.dynamic:DynamicManager',
						# 'transactional = marrow.mailer.manager.transactional:TransactionalDynamicManager'
					],
				'marrow.mailer.transport': [
						'amazon = marrow.mailer.transport.ses:AmazonTransport',
						'mock = marrow.mailer.transport.mock:MockTransport',
						'smtp = marrow.mailer.transport.smtp:SMTPTransport',
						'mbox = marrow.mailer.transport.mbox:MailboxTransport',
						'mailbox = marrow.mailer.transport.mbox:MailboxTransport',
						'maildir = marrow.mailer.transport.maildir:MaildirTransport',
						'sendmail = marrow.mailer.transport.sendmail:SendmailTransport',
						'imap = marrow.mailer.transport.imap:IMAPTransport',
						'appengine = marrow.mailer.transport.gae:AppEngineTransport',
						'logging = marrow.mailer.transport.log:LoggingTransport',
						'postmark = marrow.mailer.transport.postmark:PostmarkTransport',
						'sendgrid = marrow.mailer.transport.sendgrid:SendgridTransport',
						'mailgun = marrow.mailer.transport.mailgun:MailgunTransport[requests]',
					]
			},
		
		zip_safe = False,
	)
