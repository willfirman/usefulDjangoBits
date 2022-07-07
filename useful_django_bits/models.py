from django.db import models


class TemplateTagsDemo(models.Model):
    """A model used for demonstrating the template tags in useful_django_tags.py"""
    DEMO_CHOICES = (
        (1, 'one'),
        (2, 'two'),
        (3, 'three')
    )

    demo_integer = models.IntegerField(choices=DEMO_CHOICES, verbose_name='Demo Integer Field with Choices')
    demo_char = models.CharField(max_length=100)

    @staticmethod
    def return_hello():
        return 'hello'
