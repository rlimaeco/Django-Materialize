{% comment "This comment section will be deleted in the generated project" %}

**A Django project starter with .**

## Quick start:

1. `$ django-admin.py startproject --template=https://github.com/geraud42/Django-Materialize/archive/master.zip --extension=py,md,html,conf my_proj`

Rest of this README will be copied to the generated project.

--------------------------------------------------------------------------------------------

{% endcomment %}

# {{ project_name }}

{{ project_name }} is a _short description_. It is built with Python using the Django Web Framework.

This project has the following basic apps:

* App1 (short desc)
* App2 (short desc)
* App3 (short desc)

## Installation

### Quick start

To set up the project, you will need fabric and virtualenv:

`$ fab deploy:production=False,start_app=False`

To run the server, just use:

`$ fab runserver:production=False`
