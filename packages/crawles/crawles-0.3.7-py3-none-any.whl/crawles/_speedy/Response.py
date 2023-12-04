from re import findall
from lxml import etree
from requests import models


class Response(models.Response):
    def __init__(self, response):
        self.response = response

    def xpath(self, pattern):
        html = etree.HTML(self.response.text)
        return html.xpath(pattern)

    def findall(self, pattern, flags=0):
        if isinstance(flags, str) and str(flags).lower() == 's':
            flags = 16
        return findall(pattern, self.response.text, flags=flags)

    def save(self, file_name, encoding='utf-8'):
        with open(file_name, 'w+', encoding=encoding) as file:
            file.write(self.response.text)
