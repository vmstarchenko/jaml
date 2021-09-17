import textwrap
import pathlib
import jiml

import pytest


DATA_DIR = pathlib.Path(__file__).absolute().parent / 'data'


def test_load_template_broken():
    with pytest.raises(jiml.exceptions.TemplateSyntaxError):
        jiml.load_template(textwrap.dedent(
            '''
            key: {{ value
            '''
        ))

    with pytest.raises(jiml.exceptions.TemplateOptionsSyntaxError):
        jiml.load_template(textwrap.dedent(
            '''
            # options
            a: b: c
            ---
            key: {{ value }}
            '''
        ))

    with pytest.raises(jiml.exceptions.TemplateOptionsSyntaxError):
        jiml.load_template(textwrap.dedent(
            '''
            # options
            a: b: c
            '''
        ))




def test_load_template():
    t = jiml.load_template(textwrap.dedent(
        '''
        # options
        input_schema:
            properties:
                value: { type: string }
        ---
        key: {{ value }}
        '''
    ))
    f = jiml.testlib.TestFile(t, DATA_DIR / 'simple_template.test.yaml')
    f.run()


def test_render_template():
    assert jiml.render('key: {{ value }}', {'value': 'v'}) == 'key: "v"'
