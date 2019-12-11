#!/usr/bin/env python

import pytest
from yasuri import text_node as tn
import requests
from bs4 import BeautifulSoup

import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

# ---------------------------------------------------------------------
@pytest.fixture(scope='function', autouse=True)
def scope_function():
    yield


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


def test_scrape_text_hello_yasuri():
    """
    'scrape text text <p>Hello,Yasuri</p>'
    """

    url = "http://localhost:8888/tests/htdocs/index.html"
    html = requests.get(url)

    node = tn.TextNode(path='p:nth-child(1)')
    actual = node.inject(html.text)
    assert "Hello,Yasuri" == actual
