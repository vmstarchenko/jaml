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
```
