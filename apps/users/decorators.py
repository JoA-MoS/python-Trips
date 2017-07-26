from functools import wraps
# from urllib.parse import urlparse

from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from .models import User
import base64


def user_passes_test(test_func, login_url=None, next_url=None):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            print kwargs
            if 'user_id' in request.session:
                user = User.objects.get_user(request.session['user_id'])
                if user:
                    if test_func(user):
                        return view_func(request, *args, **kwargs)
            b64_resolved_next_url = base64.urlsafe_b64encode(resolve_url(next_url or request.path))
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            return redirect(resolved_login_url + '?next=%s' % (b64_resolved_next_url))
        return _wrapped_view
    return decorator


def user_login_required(function=None, login_url=None, next_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        next_url=next_url, 
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def anonymous_only(function=None, next_url=None):
    """
    Decorator for views that that should not be shown if not logged in.
    """
    actual_decorator = inner_annonymous_only(
        True,
        next_url=next_url, 
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# needed to allow you to call the function with out parenthesis
def inner_annonymous_only(function=None, next_url=None):
    """
    Decorator for views that that should not be shown if not logged in.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            print kwargs
            # resolved_next_url = resolve_url(next_url or settings.HOME_URL)
            if 'user_id' in request.session:
                user = User.objects.get_user(request.session['user_id'])
                if user:
                    return redirect(resolve_url(next_url or settings.HOME_URL))
                else:
                    return view_func(request, *args, **kwargs)
            else:
                return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator




def user_is_obj_owner(function):
    def wrap(request, *args, **kwargs):
        #get the object from the parameter in the route
        #entry = Entry.objects.get(pk=kwargs['obj_id'])
        # if entry.created_by == request.user:
        #     return function(request, *args, **kwargs)
        # else:
        #     raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap


# def user_is_owner(function=None, login_url=None, next_url=None):
#     """
#     Decorator for views that checks that the user is logged in, redirecting
#     to the log-in page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: u.is_authenticated,
#         login_url=login_url,
#         next_url=next_url, 
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator
        
