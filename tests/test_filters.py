import pathlib
import textwrap

import jiml
import pytest


DATA_DIR = pathlib.Path(__file__).absolute().parent / 'data'


def test_str_filters():
    t = jiml.load_template(textwrap.dedent(
        '''
        # options
        undefined: undefined
        ---
        var_with_qstr: {{ var | qstr }}
        var_with_str: "prefix_{{ var | str }}"
        '''
    ))
    f = jiml.testlib.TestFile(t, DATA_DIR / 'str_filters.test.yaml')
    f.run()


def test_yaml_escape_undefined():
    t = jiml.load_template(textwrap.dedent(
        '''
        # options
        undefined: undefined
        ---
        key: {{ value }}
        '''
    ))
    assert t({'another_value': '1'}) == {'key': None}


def test_yaml_escape_strictundefined():
    with pytest.raises(jiml.exceptions.RenderTemplateError):
        t = jiml.load_template(textwrap.dedent(
            '''
            key: {{ value }}
            '''
        ))
        t({'another_value': '1'})


def test_yaml_escape_custom_undefined():
    t = jiml.load_template(textwrap.dedent(
        '''
        # options
        undefined: jiml.common.Undefined
        ---
        key: {{ value }}
        '''
    ))
    t({'another_value': '1'})
