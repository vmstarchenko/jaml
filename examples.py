import jiml

context = {
    'simple_string_var': 'some_text',
    'complex_string_var': 'some text:\"with\nstrange\'symbols',
    'int_var': 42,
    'int_string_var': '42',
    'null': None,
    'some_object': {'a': 1, 3: (1, 2, 3) },
    'simple_list': [1, 2],
}

# use simple string as object value
template = '''key: {{ simple_string_var | qstr }}'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use complex string as object value
template = '''key: {{ complex_string_var | qstr }}'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use complex string as object value
template = '''{{ complex_string_var | qstr }}: value'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use empty string by qstr
template = '''key: {{ "" | qstr }}'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use number as string value
template = '''key: {{ int_var | qstr }}'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use None as string value
template = '''key: {{ None | qstr }}'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use optional as string value
template = '''\
optional_not_empty: {{ (simple_string_var | qstr) if simple_string_var is not none else 'null' }}
optional_empty:     {{ (null | qstr)              if null              is not none else 'null' }}
optional_not_empty_with_default: {{ (simple_string_var if simple_string_var is not none else 'default') | qstr }}
optional_empty_with_default:     {{ (null              if null              is not none else 'default') | qstr }}
'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use variable as part of result string by str
template = '''key: "some prefix {{ simple_string_var | str }}"'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use number variable as int value
template = '''key: {{ int_var | int }}'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use number in string var as int value
template = '''key: {{ int_string_var | int }}'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use None as int value
template = '''key: {{ None | int }}'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use complex object as inserted value
template = '''key: {{ some_object | json.dumps }}'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use dicts in yaml or json form
template = '''\
as_json: {
    k1: {{ simple_string_var | qstr }},
    k2: v2,
}
as_yaml:
    k1: {{ simple_string_var | qstr }}
    k2: v2
'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use lists in yaml or json form
template = '''\
as_json: [
    {{ simple_string_var | qstr }},
    { a: 1},
    1,
]
as_yaml:
    - {{ simple_string_var | qstr }}
    - { a: 1}
    - 1
'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use jinja or yaml comments
template = '''\
key1: "test.{# jinja cut this text #}.comment"
key2: "test.comment"  # yaml cut this text
'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use jinja as loops value
template = '''\
key1:
    {% for x in simple_list %}
        - {
            k1: {{ x }},
            v1: v1,
        }
    {% endfor %}
key2:
    {% for x in simple_list %}
        - k1: {{ x }}
          v1: v1
    {% endfor %}
'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use inline conditional keys and values
template = '''\
{{ 'in_key' if True else 'oops' }}: value1
key2: {{ 'oops' if False else 'in_value' }}
{{ 'both: both' if True else 'oops: oops' }}
'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use block conditional keys
template = '''\
{% if True %}key2{% else %}oops{% endif %}: value2
# use '-' for same result but multiline format
{% if True -%}
    key1
{%- else -%}
    oops
{%- endif %}: value1
'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use block conditional values
template = '''\
key1: {% if False -%}
    value1
{%- else -%}
    {{ simple_string_var | qstr }}
{%- endif %}
'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

# use block condition for key value pair
template = '''\
key1: value1
{% if True -%}
    key2: value2
{%- else -%}
    key3: value3
{%- endif %}
key4: value4
'''
print(jiml.render(template, context))
print(jiml.convert(template, context))

