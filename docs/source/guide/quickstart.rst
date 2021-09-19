.. highlight:: python

===============
Quick start
===============

Jiml use yaml and jinja templates
if you dont familiar with it's syntax check tutorials:

* `yaml <https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started>`_
* `jinja <https://ultraconfig.com.au/blog/jinja2-a-crash-course-for-beginners/>`_
* `jinja more <https://jinja.palletsprojects.com/en/3.0.x/templates/>`_

First template
template as plain text so no difference between nested and structures
::

  >>> convert = jiml.load_template('''
  ... author: {{ author.name }}
  ... permissions:
  ...   authenticated: {{ authenticated }}
  ... ''')
  >>> convert({'author': {'name': 'John' }, 'authenticated': True})
  {'author': 'John', 'permissions': {'authenticated': True}}

Templates almost pure jinja but customized for yaml files.
Before values insert variables are escaped. For string parts use str filter
::

  >>> convert = jiml.load_template('''
  ... escaped_string: {{ url }}
  ... {{ url }}: escaped_string_as_key
  ... composite_string: "{{ name | str }} {{ lastname | str }}"
  ... ''')
  >>> pprint(convert({'url': 'https://example.com', 'name': 'John', 'lastname': 'Doe'}))
  {'composite_string': 'John Doe',
   'escaped_string': 'https://example.com',
   'https://example.com': 'escaped_string_as_key'}


For lists use jinja loops
::

  >>> convert = jiml.load_template('''
  ... json_style_list: [
  ...   {% for tag in tags %}
  ...     { name: {{ tag.key }}, id: {{ tag.id }} },
  ...   {% endfor %}
  ... ]
  ... yaml_style_list:
  ...   {% for tag in tags %}
  ...     - name: {{ tag.key }}
  ...       id: {{ tag.id }}
  ...   {% endfor %}
  ... ''')
  >>> pprint(convert({'tags': [{'key': 'tag1', 'id': 1}, {'key': 'tag2', 'id': 2}]}))
  {'json_style_list': [{'id': 1, 'name': 'tag1'}, {'id': 2, 'name': 'tag2'}],
   'yaml_style_list': [{'id': 1, 'name': 'tag1'}, {'id': 2, 'name': 'tag2'}]}

Ifs are also available
::

  >>> import jiml


For default values use ternar operator in jinja variables
::

  >>> import jiml


jiml template can have two sections first is template options.
if first line has comment #options then everything till \n---\n
used as template options.
::

  >>> import jiml


globals are used for adding functions and modules to jinja global scope

You can enable input and output json validation. Use jsonschema for this
link to jsonschema guide
