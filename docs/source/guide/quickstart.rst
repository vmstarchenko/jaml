.. highlight:: python

===============
Quick start
===============

Jiml use yaml and jinja templates
if you dont familiar with it's syntax check tutorials:

* `yaml <https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started>`_
* `jinja <https://ultraconfig.com.au/blog/jinja2-a-crash-course-for-beginners/>`_
* `jinja more <https://jinja.palletsprojects.com/en/3.0.x/templates/>`_

Для начала необходимо задать правила перекладывания json в json. Эти правила задаются с помощью
Jinja шаблона. By design jinja используется для рендеринга HTML формата, но может использоваться
и для других форматов. Мы можем использовать их и для рендеринга json, но из-за того, что json
имеет слишком строгий и не гибкий синтаксис, мы используем формат yaml. Таким обрахом схема
преобразований заключается в следующем:

* Шаблон описывает правила преобразования входного json в выходной yaml
* Входной json используется в качестве контекста для jinja шаблона.
* Jinja преобразует шаблон и контекст в валидный результирующий yaml
* Yaml загружается  обратно из текстового представления внуть питона

Давайте начнем с простого примера использования. Точкой входа является функция load_template
которая возвращает объект Template кастомизированный для отрисовки yaml.
Так как результат - это текст, то вложенность и сложность входного и выходного жсона не
играют роли 
.. First template template as plain text so no difference between nested and structures
::

  >>> convert = jiml.load_template('''
  ... author: {{ author.name }}
  ... permissions:
  ...   authenticated: {{ authenticated }}
  ... ''')
  >>> convert({'author': {'name': 'John' }, 'authenticated': True})
  {'author': 'John', 'permissions': {'authenticated': True}}

Шаблоны джинджи кастомизированы для вывода в формате ямл, так что перед вставкой переменных используется
экранирование. Например, урл не может вставляться как есть из за того что содержит сомвол двоеточия
но автоматическое экранирование решает эту проблему.
Если строчку нужно встачить в качестве части другой строчки, можно использовать фильтр str,
окружив переменные кавычками.
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

Для обработки однотипных элементов можно использовать цикл из джинджи. при использовании
циклов и объектов есть 2 варианта: отображение в json стиле и yaml стиле:
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

Условные конструкции так же используют jinja синтаксис. Для использования значений по
умолчанию можно использовать тернарные операторы внутри if или default фильтр из джинджи
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

Jiml шаблоны могут состоять из двух секций. Кроме самого шаблона в начале может идти секция
которая описывает дополнительные опции шаблона. Эта секция обязательно начинается с последовательности
# options и заканчивается последовательностью \n---\n
Один из параметров является globals. Глобалс служит для того чтобы внести в глобальное пространство
имен джинджи дополнительные переменные и модули. Это оказывается полезно при необходимости
использовать какую-то функцию из стандартной библиотеки или стороннего модуля.
::

  >>> convert = jiml.load_template('''
  ... # options
  ... globals: [urllib]
  ... ---
  ... url: {{ urllib.parse.urljoin(base_url, suffix) }}
  ... ''')
  >>> convert({'base_url': 'https://example.com/test/old.html', 'suffix': 'new.html'})
  {'url': 'https://example.com/test/new.html'}
