from django import template
from recipes.models import Tag


register = template.Library()


@register.filter
def get_tags(request):
    return request.getlist("tag")


@register.filter
def tag_link(request, tag):
    request_copy = request.GET.copy()
    request_copy["page"] = "1"
    tags = request_copy.getlist("tag")
    if tag.display_name in tags:
        tags.remove(tag.display_name)
        request_copy.setlist("tag", tags)
    else:
        request_copy.appendlist("tag", tag.display_name)
    return request_copy.urlencode()


@register.filter
def all_tags(value):
    return Tag.objects.all()


@register.filter
def pagination(request, page):
    request_copy = request.GET.copy()
    request_copy["page"] = page
    return request_copy.urlencode()
