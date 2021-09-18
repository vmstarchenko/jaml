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

  >>> import jiml
  >>> template = {'v


For lists use jinja loops
::

  >>> import jiml


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
