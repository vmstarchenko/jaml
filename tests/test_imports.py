import pathlib
import textwrap

import jiml
import pytest


def test_imports():
    t = jiml.load_template(textwrap.dedent(
        '''
        # options
        globals:
            - urllib
        ---
        host: {{ urllib.parse.urlparse(url).hostname }}
        '''
    ))
    assert t({'url': 'https://example.com/hello'}) == {'host': 'example.com'}

    t = jiml.load_template(textwrap.dedent(
        '''
        # options
        globals:
            - urllib.parse.urlparse
        ---
        host: {{ urlparse(url).hostname }}
        '''
    ))
    assert t({'url': 'https://example.com/hello'}) == {'host': 'example.com'}


