# test_runner.py
from django.test.runner import DiscoverRunner
import logging

class NoLoggingTestRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        logging.disable(logging.CRITICAL)

    def teardown_test_environment(self, **kwargs):
        super().teardown_test_environment(**kwargs)
        logging.disable(logging.NOTSET)