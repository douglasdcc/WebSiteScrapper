import pytest
import requests
import logging
from unittest.mock import patch, Mock
from websitescraping.scrape import is_valid_website, scrape_website, thread_scrape

from home.log_config import configure_logger
logger = configure_logger(__name__)

@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get

def test_is_valid_website_success(mock_requests_get, caplog):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response

    with caplog.at_level(logging.CRITICAL):
        valid, _ = is_valid_website('http://example.com')
        assert valid == True

def test_is_valid_website_failure(mock_requests_get, caplog):
    mock_requests_get.side_effect = requests.exceptions.RequestException

    with caplog.at_level(logging.CRITICAL):
        valid, _ = is_valid_website('http://example.com')
        assert valid == False

def test_scrape_website_valid(mock_requests_get, caplog):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '<html><body><a href="/link1">Link 1</a></body></html>'
    mock_requests_get.return_value = mock_response

    result = []
    with caplog.at_level(logging.CRITICAL):
        scrape_website('http://example.com', result)

    assert 'http://example.com/link1' in result

def test_scrape_website_invalid(mock_requests_get, caplog):
    mock_requests_get.return_value.status_code = 404

    result = []
    with caplog.at_level(logging.CRITICAL):
        scrape_website('http://example.com', result)

    assert len(result) == 0 or 'Error: http://example.com is not a valid website' in result

def test_thread_scrape(mock_requests_get, caplog):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '<html><body><a href="/link1">Link 1</a></body></html>'
    mock_requests_get.return_value = mock_response

    urls = ['http://example.com', 'http://example.org']
    with caplog.at_level(logging.CRITICAL):
        results = thread_scrape(urls)

    assert 'http://example.com/link1' in results
    assert 'http://example.org/link1' in results