import pathlib
import textwrap

import jiml
import pytest


def test_autoescape_disabled():
    t = jiml.load_template(textwrap.dedent(
        '''
        # options
        autoescape: false
        ---
        key: {{ value | e }}
        '''
    ))
    assert t({'value': 'some:strange\n{string'}) == {'key': 'some:strange\n{string'}

    with pytest.raises(jiml.exceptions.LoadResultsError):
        t = jiml.load_template(textwrap.dedent(
            '''
            # options
            autoescape: false
            ---
            key: {{ value }}
            '''
        ))
        t({'value': 'some:strange\n{string'})


def test_custom_filter():
    t = jiml.load_template(textwrap.dedent(
        '''
        key: {{ value | test_lower }}
        '''
    ), env={'filters': {**jiml.FILTERS, 'test_lower': str.lower}})
    assert t({'value': 'LOWER'}) == {'key': 'lower'}

    with pytest.raises(jiml.exceptions.TemplateSyntaxError):
        t = jiml.load_template(textwrap.dedent(
            '''
            key: {{ value | qstr }}
            '''
        ), env={'filters': {'test_lower': str.lower}})
        assert t({'value': 'LOWER'}) == {'key': 'lower'}
