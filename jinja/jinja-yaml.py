#! /usr/bin/python
from jinja2 import Environment, FileSystemLoader
from yaml import load

env = Environment(loader=FileSystemLoader("templates"))
my_template = env.get_template("hello.j2")

with open("variables/data.yml") as f:
    data = load(f)

result = my_template.render(data)
print(result)
