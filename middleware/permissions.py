from django.http.response import HttpResponseForbidden
import re
from middleware.models import AdminPermissions, GeneralPermissions

class PermissionsMiddleware(object):
    def __init__(self, get_response):
        super(PermissionsMiddleware, self).__init__()
        self.get_response = get_response
        self.response = None
        self.uris_not_required_login = ["/api/login/?", "/api/regsiter/?"]

    def __call__(self, request):
        self.request = request
        self.response = None  # HttpResponseForbidden("You need permissions")
        self.uri = str(request.META["PATH_INFO"])
        self.method = request.method
        self.block_if_admin_url()
        self.block_if_url_requires_login_and_user_not_loggedin()
        self.block_if_user_not_allowed()
        self.run()
        return self.response

    def run(self):
        self.response = self.get_response(self.request)

    def block_if_admin_url(self):
        if self.response is not None:
            return
        if (self.request.user is None) or (not self.request.user.is_admin):
            rules = AdminPermissions.objects.filter(is_active=True)
            for each_rule in rules:
                if self.is_regex_match(each_rule.uri_regex, self.uri):
                    self.response = HttpResponseForbidden("You need admin permissions to do this operation")
                    break

    def block_if_url_requires_login_and_user_not_loggedin(self):
        if self.response is not None:
            return
        for each in self.uris_not_required_login:
            if self.is_regex_match(each, self.uri):
                return
        self.response = HttpResponseForbidden("Login required to access this url")

    def block_if_user_not_allowed(self):
        pass

    def is_regex_match(self, regex, given_string):
        r = re.match(regex, given_string, re.IGNORECASE)
        if r:
            s = r.span()
            if s[0]==0 and s[1]>(len(given_string)-1):
                return True
            return False
        else:
            return False