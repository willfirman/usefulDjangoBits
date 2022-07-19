# Useful Django Bits

A collection of code snippets and examples that I've found useful working with Django. This is very much a work in
progress and I have plenty more to add to it.

At some point in the future I intend to make it into an installable Django app and publish on PyPI, but for now it's a
full-blown Django project so to use any of the useful bits, you'll need to copy them into your own source files.

The only files of interest are:
- `useful_django_bits/templatetags/useful_django_tags.py` - a collection of template tags that might be helpful. If you
  run the Django project, you can see usage examples at `/demos/useful_django_tags`.
- `usefulDjangoBits/settings/` - using a Python module instead of a simple `settings.py` file to configure Django
  settings. This is inspired by the way Wagtail CMS does things. It's great for ensuring your different environments
  have the right settings - e.g. making sure `DEBUG` stays on in dev mode, and off in production. You'll need to
  set your `DJANGO_SETTINGS_MODULE` environment variable, or call `manage.py` commands with the `--settings=` flag.
  See https://docs.djangoproject.com/en/4.0/topics/settings/#designating-the-settings for help.
