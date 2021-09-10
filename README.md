# jiml

Convert json to json using [jinja2 templates](https://jinja.palletsprojects.com/en/3.0.x/templates/)
and [yaml](https://pyyaml.org/wiki/PyYAMLDocumentation). 

This package demonstrates an approach for converting input json to output json without using python code directly.
The conversion is done by Jinja library. Input json used as context for rendered template. Conversion rules are specified in template.
Due to the fact that the json format has too strict syntax, the templates written to produce yaml as an alternative. 

jiml defines a couple of jinja filters specialized for yaml templates writing:
- `qstr`: escape context variable before insert to template. Result is always valid json string.
- `str`: same as qstr but cut prefix and suffix quotes.
- `json.dump`: escape object variable before insert to template. Result is always valid json.

## Examples
```
>>> import jiml
>>> 
>>> context = {
...     'simple_string_var': 'some_text',
...     'complex_string_var': 'some text:\"with\nstrange\'symbols',
...     'int_var': 42,
...     'int_string_var': '42',
...     'null': None,
...     'some_object': {'a': 1, 3: (1, 2, 3) },
...     'simple_list': [1, 2],
... }
```
- use simple string as object value
```python
>>> template = '''key: {{ simple_string_var }}'''
>>> print(jiml.render(template, context))
key: "some_text"
>>> print(jiml.convert(template, context))
{'key': 'some_text'}
```
- use complex string as object value
```python
>>> template = '''key: {{ complex_string_var }}'''
>>> print(jiml.render(template, context))
key: "some text:\"with\nstrange'symbols"
>>> print(jiml.convert(template, context))
{'key': 'some text:"with\nstrange\'symbols'}
```
- use complex string as object value
```python
>>> template = '''{{ complex_string_var }}: value'''
>>> print(jiml.render(template, context))
"some text:\"with\nstrange'symbols": value
>>> print(jiml.convert(template, context))
{'some text:"with\nstrange\'symbols': 'value'}
```
- use empty string by qstr
```python
>>> template = '''key: {{ "" }}'''
>>> print(jiml.render(template, context))
key: ""
>>> print(jiml.convert(template, context))
{'key': ''}
```
- use number as string value
```python
>>> template = '''key: {{ int_var | qstr }}'''
>>> print(jiml.render(template, context))
key: "42"
>>> print(jiml.convert(template, context))
{'key': '42'}
```
- use None as string value
```python
>>> template = '''key: {{ None | qstr }}'''
>>> print(jiml.render(template, context))
key: ""
>>> print(jiml.convert(template, context))
{'key': ''}
```
- use optional as string value
```python
>>> template = '''\
... optional_not_empty: {{ simple_string_var if simple_string_var is not none else None }}
... optional_empty:     {{ null              if null              is not none else None }}
... optional_not_empty_with_default: {{ simple_string_var if simple_string_var is not none else 'default' }}
... optional_empty_with_default:     {{ null              if null              is not none else 'default' }}
... '''
>>> print(jiml.render(template, context))
optional_not_empty: "some_text"
optional_empty:     !!null "null"
optional_not_empty_with_default: "some_text"
optional_empty_with_default:     "default"
>>> print(jiml.convert(template, context))
{'optional_not_empty': 'some_text', 'optional_empty': None, 'optional_not_empty_with_default': 'some_text', 'optional_empty_with_default': 'default'}
```
- use variable as part of result string by str
```python
>>> template = '''key: "some prefix {{ simple_string_var | str }}"'''
>>> print(jiml.render(template, context))
key: "some prefix some_text"
>>> print(jiml.convert(template, context))
{'key': 'some prefix some_text'}
```
- use number variable as int value
```python
>>> template = '''key: {{ int_var }}'''
>>> print(jiml.render(template, context))
key: !!int "42"
>>> print(jiml.convert(template, context))
{'key': 42}
```
- use number in string var as int value
```python
>>> template = '''key: {{ int_string_var | int }}'''
>>> print(jiml.render(template, context))
key: !!int "42"
>>> print(jiml.convert(template, context))
{'key': 42}
```
- use None as int value
```python
>>> template = '''key: {{ None | int }}'''
>>> print(jiml.render(template, context))
key: !!int "0"
>>> print(jiml.convert(template, context))
{'key': 0}
```
- use complex object as inserted value
```python
>>> template = '''key: {{ some_object | json.dumps }}'''
>>> print(jiml.render(template, context))
key: {"a": 1, "3": [1, 2, 3]}
>>> print(jiml.convert(template, context))
{'key': {'a': 1, '3': [1, 2, 3]}}
```
- use dicts in yaml or json form
```python
>>> template = '''\
... as_json: {
...     k1: {{ simple_string_var }},
...     k2: v2,
... }
... as_yaml:
...     k1: {{ simple_string_var }}
...     k2: v2
... '''
>>> print(jiml.render(template, context))
as_json: {
    k1: "some_text",
    k2: v2,
}
as_yaml:
    k1: "some_text"
    k2: v2
>>> print(jiml.convert(template, context))
{'as_json': {'k1': 'some_text', 'k2': 'v2'}, 'as_yaml': {'k1': 'some_text', 'k2': 'v2'}}
```
- use lists in yaml or json form
```python
>>> template = '''\
... as_json: [
...     {{ simple_string_var }},
...     { a: 1},
...     1,
... ]
... as_yaml:
...     - {{ simple_string_var }}
...     - { a: 1}
...     - 1
... '''
>>> print(jiml.render(template, context))
as_json: [
    "some_text",
    { a: 1},
    1,
]
as_yaml:
    - "some_text"
    - { a: 1}
    - 1
>>> print(jiml.convert(template, context))
{'as_json': ['some_text', {'a': 1}, 1], 'as_yaml': ['some_text', {'a': 1}, 1]}
```
- use jinja or yaml comments
```python
>>> template = '''\
... key1: "test.{# jinja cut this text #}.comment"
... key2: "test.comment"  # yaml cut this text
... '''
>>> print(jiml.render(template, context))
key1: "test..comment"
key2: "test.comment"  # yaml cut this text
>>> print(jiml.convert(template, context))
{'key1': 'test..comment', 'key2': 'test.comment'}
```
- use jinja as loops value
```python
>>> template = '''\
... key1:
...     {% for x in simple_list %}
...         - {
...             k1: {{ x }},
...             v1: v1,
...         }
...     {% endfor %}
... key2:
...     {% for x in simple_list %}
...         - k1: {{ x }}
...           v1: v1
...     {% endfor %}
... '''
>>> print(jiml.render(template, context))
key1:
    
        - {
            k1: !!int "1",
            v1: v1,
        }
    
        - {
            k1: !!int "2",
            v1: v1,
        }
    
key2:
    
        - k1: !!int "1"
          v1: v1
    
        - k1: !!int "2"
          v1: v1
    
>>> print(jiml.convert(template, context))
{'key1': [{'k1': 1, 'v1': 'v1'}, {'k1': 2, 'v1': 'v1'}], 'key2': [{'k1': 1, 'v1': 'v1'}, {'k1': 2, 'v1': 'v1'}]}
```
- use inline conditional keys and values
```python
>>> template = '''\
... {{ 'in_key' if True else 'oops' }}: value1
... key2: {{ 'oops' if False else 'in_value' }}
... {{ ('both: both' if True else 'oops: oops') | safe }}
... '''
>>> print(jiml.render(template, context))
"in_key": value1
key2: "in_value"
both: both
>>> print(jiml.convert(template, context))
{'in_key': 'value1', 'key2': 'in_value', 'both': 'both'}
```
- use block conditional keys
```python
>>> template = '''\
... {% if True %}key2{% else %}oops{% endif %}: value2
... # use '-' for same result but multiline format
... {% if True -%}
...     key1
... {%- else -%}
...     oops
... {%- endif %}: value1
... '''
>>> print(jiml.render(template, context))
key2: value2
# use '-' for same result but multiline format
key1: value1
>>> print(jiml.convert(template, context))
{'key2': 'value2', 'key1': 'value1'}
```
- use block conditional values
```python
>>> template = '''\
... key1: {% if False -%}
...     value1
... {%- else -%}
...     {{ simple_string_var }}
... {%- endif %}
... '''
>>> print(jiml.render(template, context))
key1: "some_text"
>>> print(jiml.convert(template, context))
{'key1': 'some_text'}
```
- use block condition for key value pair
```python
>>> template = '''\
... key1: value1
... {% if True -%}
...     key2: value2
... {%- else -%}
...     key3: value3
... {%- endif %}
... key4: value4
... '''
>>> print(jiml.render(template, context))
key1: value1
key2: value2
key4: value4
>>> print(jiml.convert(template, context))
{'key1': 'value1', 'key2': 'value2', 'key4': 'value4'}
```

