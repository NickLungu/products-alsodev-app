# custom_filters.py

from django import template

register = template.Library()

@register.filter
def slice_list(my_list, num_elements):
    return my_list[:num_elements]