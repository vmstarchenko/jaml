.. highlight:: python

===============
Quick start
===============

Jiml use yaml and jinja templates
if you dont familiar with it's syntax check tutorials:

* `yaml <https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started>`_
* `jinja <https://ultraconfig.com.au/blog/jinja2-a-crash-course-for-beginners/>`_
* `jinja more <https://jinja.palletsprojects.com/en/3.0.x/templates/>`_

To begin with, you must set the rules of convention input json into output json. These rules
are set with a Jinja template. By design, Jinga is used for rendering HTML-documents,
but it can be also used for other formats. It is possible to use it for rendering json as well,
but as json has too strict and inflexible syntax, yaml-format is more sutable. Thus, the full
workflow is as follows:
* The template describes the rules of the conversion the input json into the output yaml
* The input json gets used as a context for Jinja template
* Jinja converts the template and the context into a valid resulting yaml
* Yaml is then loaded back from the text representation to the Python code

Let's continue with a simple usage example. An entry point is the function ``load_template``
that returns the ``Template`` object, customized for rendering yaml. As the result is a text,
depth and complexity of the input and output jsons doesn't matter. 
::

  >>> convert = jiml.load_template('''
  ... author: {{ author.name }}
  ... permissions:
  ...   authenticated: {{ authenticated }}
  ... ''')
  >>> convert({'author': {'name': 'John' }, 'authenticated': True})
  {'author': 'John', 'permissions': {'authenticated': True}}

Jinga templates are customized for output in the yaml-format, so variables are escaped before
substitution. For example, one can't insert a URL as is because it contains the colon mark,
but the automatic escaping solves the problem. If it is required to insert the string
as a part of some other string, you can use the ``str`` filter, while surrounding the
variables with quotation marks.
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

To process similar objects you can use Jinja loops. There are two ways for representing
lists and objects:
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

Conditional statements also use Jinja syntax. To set the defaults the ternary operators
can be used or the ``default`` filter (from Jinja library).
::

  >>> convert = jiml.load_template('''
  ... inline_if: {{ value if value is not none else 'default_value' }}
  ... multiline_if:
  ...   {% if value is not none -%}
  ...     {{ value }}
  ...   {%- else -%}
  ...     {{ other_value }}
  ...   {%- endif %}
  ... {% if value -%}
  ...     whole_block_inside_if: {{ value }}
  ... {%- else -%}
  ...     error_message: bad_value
  ... {%- endif %}
  ... ''')
  >>> pprint(convert({'value': 'Good value.', 'other_value': 'Other value'}))
  {'inline_if': 'Good value.',
   'multiline_if': 'Good value.',
   'whole_block_inside_if': 'Good value.'}

Jiml templates can have two sections. Besides the template itself, the section
that describes its additional options can precede it. This section must begin
with the sequence ``# options\n`` and ends with ``\n---\n``. One of the possible
parameters is ``globals``. It serves for adding the extra variables and modules
to the global scope of Jinga template. It is useful if it is needed to use some
function from the standard library or a third-party modules.
::

  >>> convert = jiml.load_template('''
  ... # options
  ... globals: [urllib]
  ... ---
  ... url: {{ urllib.parse.urljoin(base_url, suffix) }}
  ... ''')
  >>> convert({'base_url': 'https://example.com/test/old.html', 'suffix': 'new.html'})
  {'url': 'https://example.com/test/new.html'}
