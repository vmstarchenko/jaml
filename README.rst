.. highlight:: python

Jiml
----

**Jiml**: just easy convertion json to json.

-------------------

Convert json data from one representation to another json representations.
Jiml use power of `jinja2 <https://jinja.palletsprojects.com/en/3.0.x/templates/>`_ templates
and flexibility of `yaml <https://pyyaml.org/wiki/PyYAMLDocumentation>`_ format.

**Short usage example**::

  >>> import jiml
  >>> template = '''
  ... # options
  ... globals: [urllib.parse.urlparse]
  ... ---
  ... title: {{ title }}
  ... site: {{ urlparse(author.url).hostname }}
  ... author:
  ...   name: "{{ author.first_name | str }} {{ author.last_name | str}}"
  ... year: {{ creation_date.year }}
  ... tags: [
  ...   {% for tag in tags %}
  ...     {{ tag.name }},
  ...   {% endfor %}
  ... ]
  ... '''
  >>> convert_film_for_responce = jiml.load_template(template)
  >>> print(json.dumps(convert_film_for_responce({
  ...     'title': 'Your favourite film',
  ...     'author': {
  ...         'first_name': 'John',
  ...         'last_name': 'Doe',
  ...         'url': 'https://example.com',
  ...     },
  ...     'creation_date': datetime.datetime(2021, 1, 1),
  ...     'tags': [{'id': 1, 'name': 'comedy'}, {'id': 5, 'name': 'drama'}]
  ... }), indent=4, sort_keys=True))
  {
      "author": {
          "name": "John Doe"
      },
      "site": "example.com",
      "tags": [
          "comedy",
          "drama"
      ],
      "title": "Your favourite film",
      "year": 2021
  }
