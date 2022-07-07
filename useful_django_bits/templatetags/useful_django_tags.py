import json

from django import template
from django.core.exceptions import FieldDoesNotExist

register = template.Library()


@register.filter
def get_attr(obj: object, attr: str):
    """Given an object and its attribute (as a string), resolves the attribute and returns the result.

    This template tag allows you to access an object's attributes using the attribute name as a string. It takes the
    name of the attribute and uses Django's template variables system to resolve it into its value.

    Imagine your context has the following variables: `dog_breedss = {'rover': 'labrador', 'fido': 'spaniel'}` and
    `dogs = ['rover', 'fido']`. Django's template language only allows you to use dot notation, not brackets. So you
    can't do `{% for dog in dogs %} {{ dog_breeds.dog }} {% endfor %}` - you'll get an attribute error since
    `dog_breeds` has no `dog` key.

    Instead, you can use this template tag: `{% for dog in dogs %} {{ dog_breeds|get_attr:dog }} {% endfor %}`.
    `{{ dog_breeds|get_attr:'rover' }}` is roughly equivalent to `{{ dog_breeds.rover }}`.

    I've used a simple dict in that example, but it works just the same on an instance of a Django model. Since it uses
    Django's template resolution functions, passing the name of a function as a string will return the function's
    result, rather than the function itself.

    Note that passing the name of a choices field `foo` will return the result of `object.get_foo_display()` rather
    than just `object.foo`.

    :param obj: The object to check for an attribute
    :param attr: The attribute to retrieve
    :return: The value of obj.attr
    """
    local_context = {'obj': obj}

    # For choices fields, we want to return the result of Model.get_FOO_display() instead of Model.FOO
    # see https://docs.djangoproject.com/en/4.0/ref/models/instances/#django.db.models.Model.get_FOO_display
    if hasattr(obj, f"get_{attr}_display"):
        resolve_variable = f"obj.get_{attr}_display"
    else:
        resolve_variable = f"obj.{attr}"

    return template.Variable(resolve_variable).resolve(local_context)


@register.filter
def get_verbose_name(model, field: str):
    """Given a Django model and a field name, returns the field's verbose name.

    If you include the `verbose_name=` keyword when declaring your field, this tag will respect the case you use.
    Otherwise, it will convert the field's verbose_name into title case. So `id_number = IntegerField()` will return
    `'Id_Number`, whereas `id_number = IntegerField(verbose_name='ID number')` will return `'ID number'`.

    :param model: The Django model to check for `field`. Can be an instance of the model, or the model's class.
    :param field: The name of the field as a string
    :return: The verbose_name of the field
    """

    # Get the field instance from the provided 'field' string. If it's not a field (e.g. it's a function name, or a
    # class variable on the Model), just return it unchanged
    try:
        field_instance = model._meta.get_field(field)
    except FieldDoesNotExist:
        return field

    # If the field explicitly has a verbose_name set, it will be stored in _verbose_name, and don't want to override
    # it with title case. If it was not set explicitly, then _verbose_name is None, and we change the auto-generated
    # verbose_name to title case.
    display_name = field_instance._verbose_name or field_instance.verbose_name.title()

    return display_name


@register.filter
def make_range(number, start_index=0):
    """Returns a range from `start_index` up to `number`.

    Useful for iterating over a number, for example when using pagination, assuming there are 10 pages:

    {% for page_number in paginator.num_pages|make_range:"1" %}

    Will produce range(1, 11) - allowing you to use page numbers 1 to 10 in your template.
    :param number: the maximum number for the range (exclusive)
    :param start_index: the starting number for the range (inclusive)
    :return: a Python range object according to the given parameters
    """
    start_index = int(start_index)
    number = int(number)
    return range(start_index, number+start_index)
