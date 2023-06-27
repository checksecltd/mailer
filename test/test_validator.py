# encoding: utf-8

"""Test the primary configurator interface, Delivery."""

import logging
import pytest

import DNS

from unittest import TestCase

from marrow.mailer.validator import ValidationException, BaseValidator, DomainValidator, EmailValidator, \
		EmailHarvester


log = logging.getLogger('tests')


class TestBaseValidator(TestCase):
	class MockValidator(BaseValidator):
		def validate(self, success=True):
			if success:
				return True, None

			return False, "Mock failure."

	def test_validator_success(self):
		mock = self.MockValidator()
		assert mock.validate_or_raise()

	def test_validator_failure(self):
		mock = self.MockValidator()
		with pytest.raises(ValidationException):
			mock.validate_or_raise(False)


def test_common_rules():
	mock = DomainValidator()
	dataset = [
			('valid@example.com', ''),
			('', 'It cannot be empty.'),
			('*' * 256, 'It cannot be longer than 255 chars.'),
			('.invalid@example.com', 'It cannot start with a dot.'),
			('invalid@example.com.', 'It cannot end with a dot.'),
			('invalid..@example.com', 'It cannot contain consecutive dots.'),
		]

	def closure(address, expect):
		assert mock._apply_common_rules(address, 255) == (address, expect)

	for address, expect in dataset:
		closure(address, expect)


def test_common_rules_fixed():
	mock = DomainValidator(fix=True)
	dataset = [
			('.fixme@example.com', ('fixme@example.com', '')),
			('fixme@example.com.', ('fixme@example.com', '')),
		]

	def closure(address, expect):
		assert mock._apply_common_rules(address, 255) == expect

	for address, expect in dataset:
		closure(address, expect)


def test_domain_validation_basic():
	mock = DomainValidator()
	dataset = [
			('example.com', ''),
			('xn--ls8h.la', ''), # IDN: (poop).la
			('', 'Invalid domain: It cannot be empty.'),
			('-bad.example.com', 'Invalid domain.'),
		]

	def closure(domain, expect):
		assert mock.validate_domain(domain) == (domain, expect)

	for domain, expect in dataset:
		closure(domain, expect)


def test_domain_lookup():
	validator = DomainValidator()
	dataset = [
			('thisdomainshouldnot.exist', 'a', False),
		]

	def closure(domain, kind, expect):
		try:
			got = validator.lookup_domain(domain, kind, server=['8.8.8.8'])
			assert got == expect, f"{domain=} {kind=} {got=} {expect=}"
		except DNS.DNSError:
			pytest.skip("Skipped due to DNS error.")

	for domain, kind, expect in dataset:
		closure(domain, kind, expect)


def test_bad_lookup_record_1():
	with pytest.raises(RuntimeError):
		DomainValidator(lookup_dns='cname')


def test_bad_lookup_record_2():
	mock = DomainValidator()
	
	with pytest.raises(RuntimeError):
		mock.lookup_domain('example.com', 'cname')


def test_email_validation():
	mock = EmailValidator()
	dataset = [
			('user@example.com', ''),
			('user@xn--ls8h.la', ''), # IDN: (poop).la
			('', 'The e-mail is empty.'),
			('user@user@example.com', 'An email address must contain a single @'),
			('user@-example.com', 'The e-mail has a problem to the right of the @: Invalid domain.'),
			('bad,user@example.com', 'The email has a problem to the left of the @: Invalid local part.'),
		]

	def closure(address, expect):
		assert mock.validate_email(address) == (address, expect)

	for address, expect in dataset:
		closure(address, expect)


def test_harvester():
	mock = EmailHarvester()
	dataset = [
			('', []),
			('test@example.com', ['test@example.com']),
			('lorem ipsum test@example.com dolor sit', ['test@example.com']),
		]

	def closure(text, expect):
		assert list(mock.harvest(text)) == expect

	for text, expect in dataset:
		closure(text, expect)
