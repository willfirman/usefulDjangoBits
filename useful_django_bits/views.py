from django.shortcuts import render
from useful_django_bits.models import TemplateTagsDemo


def useful_django_tags(request):
    context = {
        'tags_demo': TemplateTagsDemo(
            demo_integer=2,
            demo_char='An example value'
        ),
        'get_attr_fields': ['demo_integer', 'demo_char', 'return_hello'],
    }
    return render(request, 'useful_django_bits/useful_django_tags.html', context=context)

