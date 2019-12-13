#!/usr/bin/env python

import pytest
from yasuri.text import TextNode
import requests
from bs4 import BeautifulSoup

import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

# ---------------------------------------------------------------------
URL = "http://localhost:8888/tests/htdocs/index.html"


@pytest.fixture(scope='function')
def index_html():
    html = requests.get(URL)
    return html


def start_server(server):
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Ignored KeyboardInterrupt")
        pass
    finally:
        server.server_close()


@pytest.fixture(scope='session', autouse=True)
def scope_session():
    server = HTTPServer(("localhost", 8888), SimpleHTTPRequestHandler)
    thread = threading.Thread(None, lambda: start_server(server))
    thread.start()

    yield

    server.server_close()
    server.shutdown()
    thread.join()


# ---------------------------------------------------------------------
def test_scrape_text_hello_yasuri(index_html):
    """
    'scrape text text <p>Hello,Yasuri</p>'
    """

    node = TextNode(path='p:nth-child(1)')
    actual = node.inject(index_html.text)
    assert "Hello,Yasuri" == actual


def test_return_empty_text_if_no_match_node(index_html):
    """
    return empty text if no match node
    """

    node = TextNode(path='no_match_node')
    actual = node.inject(index_html.text)
    assert "" == actual


def test_fail_if_invalid_selector(index_html):
    """
    fail if invalid selector
    """
    node = TextNode(path='p:nth-child[1]')
    # with pytest.raises(ValueError):
    with pytest.raises(Exception):
        node.inject(index_html.text)
