# encoding: utf-8

'''

from __future__ import unicode_literals

import logging
import sys
import pytest

from unittest import TestCase

from marrow.mailer.interfaces import IManager, ITransport

if sys.version_info[:2] >= (3, 10):
    from importlib.metadata import entry_points
else:
    from importlib_metadata import entry_points

log = logging.getLogger('tests')



def test_managers():
	def closure(plugin):
		try:
			plug = plugin.load()
		except ImportError as e:
			pytest.skip("Skipped {name} manager due to ImportError:\n{err}".format(name=plugin.name, err=str(e)))
		
		assert isinstance(plug, IManager), "{name} does not conform to the IManager API.".format(name=plugin.name)
	
	entrypoint = None
	for entrypoint in entry_points(group='marrow.mailer.manager'):
		yield closure, entrypoint
	
	if entrypoint is None:
		pytest.skip("No managers found, have you run `setup.py develop` yet?")


def test_transports():
	def closure(plugin):
		try:
			plug = plugin.load()
		except ImportError as e:
			pytest.skip("Skipped {name} transport due to ImportError:\n{err}".format(name=plugin.name, err=str(e)))
		
		assert isinstance(plug, ITransport), "{name} does not conform to the ITransport API.".format(name=plugin.name)
	
	entrypoint = None
	for entrypoint in entry_points(group='marrow.mailer.transport'):
		yield closure, entrypoint
	
	if entrypoint is None:
		pytest.skip("No transports found, have you run `setup.py develop` yet?")

'''