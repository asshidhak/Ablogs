from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

register = template.Library()


@register.simple_tag(takes_context=True)
def paginate(context, object_list, page_count):
    paginator = Paginator(object_list, page_count)
    page = context['request'].GET.get('page')
    pages = []
    for i in range(1,paginator.num_pages+1):
        pages.append(i)
    try:
        context['current_page'] = int(page)
        context['article_list'] = paginator.page(page).object_list

    except TypeError:
        context['current_page'] = 1
        context['article_list'] = paginator.page(1).object_list

    except PageNotAnInteger:
        context['current_page'] = 1
        context['article_list'] = paginator.page(1).object_list
    except EmptyPage:
        context['current_page'] = 1
        context['article_list'] = paginator.page(1).object_list
    context['pages']  = pages
    return ''