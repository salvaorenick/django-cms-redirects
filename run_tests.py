"""Allows running tests from setup.py"""
#!/usr/bin/env python
from unittest import TestSuite
import os


class RunTests(object):
    """Used to run tests from setup.py"""
    def loadTestsFromNames(self, *args, **kwargs):
        """Calls django's test command and returns an empty test suite.

        Django knows how to run its own tests, we'll let it do its thing, then
        return an empty testsuite so setup.py doesn't panic.
        """
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testsettings')
        # call_command has to be imported here for django to find our tests
        from django.core.management import call_command
        call_command('test')
        return TestSuite()
