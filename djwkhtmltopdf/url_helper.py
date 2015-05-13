import re

from django.core.exceptions import ViewDoesNotExist
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.conf import settings


def extract_views_from_urlpatterns(urlpatterns, base='', namespace=None):
    """
    Return a list of views from a list of urlpatterns.

    Each object in the returned list is a two-tuple: (view_func, regex)
    :param: urlpatterns: It will take url patterns.
    :type: list
    :param: base: string
    :type: base: str or unicode
    :param: namespace: namespace will doesn't allow collision.
    :type: namespace: str or unicode
    :returns: (view_func, regex)
    :raise: ViewDoesNotExist: if view doesn't exists
    :raise: ImportError: I can't help you
    """
    views = []
    for p in urlpatterns:
        if isinstance(p, RegexURLPattern):
            try:
                if not p.name:
                    name = p.name
                elif namespace:
                    name = '{0}:{1}'.format(namespace, p.name)
                else:
                    name = p.name
                views.append((p.callback, base + p.regex.pattern, name))
            except ViewDoesNotExist:
                continue
        elif isinstance(p, RegexURLResolver):
            try:
                patterns = p.url_patterns  # Hi there
            except ImportError:
                continue
            views.extend(extract_views_from_urlpatterns(
                patterns,
                base + p.regex.pattern,
                namespace=(namespace or p.namespace)))
        elif hasattr(p, '_get_callback'):
            try:
                views.append(
                    (p._get_callback(),
                     base + p.regex.pattern,
                     p.name))
            except ViewDoesNotExist:
                continue
        elif hasattr(p, 'url_patterns') or hasattr(p, '_get_url_patterns'):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            views.extend(extract_views_from_urlpatterns(
                patterns, base + p.regex.pattern,
                namespace=namespace))
        else:
            raise TypeError("%s does not appear to be a urlpattern object" % p)
    return views


def get_all_views():
    """
        Collecting all views from top level project
    """
    views = []
    try:
        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
    except Exception as e:
        print e
        pass
    view_functions = extract_views_from_urlpatterns(urlconf.urlpatterns)
    for (func, regex, url_name) in view_functions:
        if hasattr(func, '__name__'):
            func_name = func.__name__
        elif hasattr(func, '__class__'):
            func_name = '%s()' % func.__class__.__name__
        else:
            func_name = re.sub(r' at 0x[0-9a-f]+', '', repr(func))
        module = '{0}.{1}'.format(func.__module__, func_name)
        views.append((module, module))
    return views
