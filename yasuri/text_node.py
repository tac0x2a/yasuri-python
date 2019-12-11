import requests
from bs4 import BeautifulSoup


class TextNode:
    def __init__(self, path: str):
        self.path = path

    def inject(self, html):
        bs = BeautifulSoup(html, 'html.parser')
        return " ".join([t.text for t in bs.select(self.path)])
