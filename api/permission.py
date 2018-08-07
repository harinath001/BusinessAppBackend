from rest_framework.permissions import BasePermission
from middleware.models import GeneralPermissions
import re

class AdminPermissions(BasePermission):

    def __init__(self):
        super(AdminPermissions, self).__init__()

    def has_permission(self, request, view):
        if request.user and request.user.is_admin:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_admin:
            return True
        return False


class ClassicPermission(BasePermission):
    def __init__(self):
        super(ClassicPermission, self).__init__()

    def is_regex_match(self, regex, given_string):
        r = re.match(regex, given_string, re.IGNORECASE)
        if r:
            s = r.span()
            if s[0]==0 and s[1]>(len(given_string)-1):
                return True
            return False
        else:
            return False

    def has_permission(self, request, view):
        return self.determine_permit(request, view)

    def has_object_permission(self, request, view, obj):
        return self.determine_permit(request, view, obj)

    def determine_permit(self, request, view, obj=None):
        if request.user and request.user.is_admin:
            return True
        if obj:
            if hasattr(request, 'user') and request.user:
                if obj.created_by.id != request.user.id:
                    return False
            else:
                return False
        allowed_actions = view.custom_allowed_actions if hasattr(view, 'custom_allowed_actions') else ['create', 'update',
                                                                                                       'list', 'retrieve']
        if str(view.action).lower() not in allowed_actions:
            return False
        if hasattr(view, 'allow_all') and view.allow_all:
            return True
        if request.user:
            all_restrictions = GeneralPermissions.objects.filter(user=request.user, is_active=True,
                                                                 method=str(view.action).lower())
            for each in all_restrictions:
                if self.is_regex_match(each.uri_regex, str(request.META["PATH_INFO"])) and (not each.is_allowed):
                    return False
            return True
        return False