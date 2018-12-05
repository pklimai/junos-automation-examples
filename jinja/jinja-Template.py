#! /usr/bin/python

from jinja2 import Template

template_string = "Hello {{ user }}"
my_template = Template(template_string)
result = my_template.render(
    {"user": "lab"}
)
print(result)
