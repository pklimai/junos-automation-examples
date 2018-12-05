#! /usr/bin/python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))

my_template = env.get_template("hello.j2")

result = my_template.render({"user": "lab"})

print(result)
