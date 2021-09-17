import pathlib
import textwrap

import jiml
import pytest


DATA_DIR = pathlib.Path(__file__).absolute().parent / 'data'


def test_input_schema_syntax():
    with pytest.raises(jiml.exceptions.InputSchemaSyntaxError):
        jiml.load_template(textwrap.dedent(
            '''
            # options
            input_schema:
                properties:
                    value: { type: str }
            ---
            key: {{ value }}
            '''
        ))


def test_output_schema_syntax():
    with pytest.raises(jiml.exceptions.OutputSchemaSyntaxError):
        jiml.load_template(textwrap.dedent(
            '''
            # options
            output_schema:
                properties:
                    value: asdf
            ---
            key: {{ value }}
            '''
        ))


def test_input_schema_validation():
    t = jiml.load_template(textwrap.dedent(
        '''
        # options
        input_schema:
          properties:
            value: { type: number }
          required: [value]
          additionalProperties: false
        ---
        key: {{ value }}
        '''
    ))
    f = jiml.testlib.TestFile(t, DATA_DIR / 'input_schema_validation.test.yaml')
    f.run()


def test_output_schema_validation():
    t = jiml.load_template(textwrap.dedent(
        '''
        # options
        output_schema:
          properties:
            key: { type: number }
          required: [value]
          additionalProperties: false
        ---
        {{ value | safe }}
        '''
    ))
    f = jiml.testlib.TestFile(t, DATA_DIR / 'output_schema_validation.test.yaml')
    f.run()


def test_schema_draft():
    with pytest.raises(jiml.exceptions.InputSchemaSyntaxError):
        jiml.load_template(textwrap.dedent(
            '''
            # options
            input_schema:
              draft: test_unk_draft
              properties:
                key: { type: number }
              required: [value]
              additionalProperties: false
            ---
            key: value
            '''
        ))
