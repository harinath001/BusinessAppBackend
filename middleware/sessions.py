from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
import re
from api.models import User
from middleware.models import Sessions

class SessionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.cookie_setter_urls = ["/api/login/?"]
        self.cookie_not_required_uris = ["/api/login/?", "/api/register/?"]
        self.cookie_failure_redirection = []
        self.token_name = "classictoken"
        self.response = None
        self.request = None
        self.uri = None
        self.token_exists = False

    def __call__(self, request):
        self.request = request
        self.uri = str(request.META["PATH_INFO"])
        self.response = None
        self.check_if_token_present()
        self.disable_csrf_token()

        if not self.is_cookie_not_required():
            if not self.validate_cookie():
                if self.is_redirect_required():
                    self.redirect()
                    self.response = HttpResponseBadRequest("URL redirected")
                else:
                    self.response = HttpResponseBadRequest("Session verification failed")
                return self.response
            else:  # cookie validated
                self.run()
        else:
            self.run()

        if self.is_setting_cookie_required():
            if self.is_loggedin():
                token = self.generate_token_for_user()
                self.set_cookie_in_response(token)
            else:
                self.response = HttpResponseBadRequest("Unable to log in")
                return self.response
        return self.response

    def disable_csrf_token(self):
        attr = '_dont_enforce_csrf_checks'
        if not getattr(self.request, attr, False):
            setattr(self.request, attr, True)

    def check_if_token_present(self):
        token = self.request.COOKIES.get(self.token_name, None)
        self.token_exists = True if token is not None else False
        return self.token_exists

    def run(self):
        m = self.get_response
        self.response = m(self.request)

    def is_cookie_not_required(self):
        for each_regex in self.cookie_not_required_uris:
            if self.is_regex_match(each_regex, self.uri):
                return True
        return False

    def is_regex_match(self, regex, given_string):
        r = re.match(regex, given_string, re.IGNORECASE)

        if r:
            s = r.span()
            if s[0]==0 and s[1]>(len(given_string)-1):
                return True
            return False
        else:
            return False

    def redirect(self):
        for each_pair in self.cookie_failure_redirection:
            if self.is_regex_match(each_pair[0], self.uri):
                HttpResponseRedirect(each_pair[1])
                break



    def is_loggedin(self):
        if self.response.get("loggedin", None) and self.response["loggedin"]:
            return True
        return False

    def set_cookie_in_response(self, token):
        # response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)
        self.response.set_cookie(self.token_name, token, max_age=365*24*60*60)

    def validate_cookie(self):
        token = self.request.COOKIES.get(self.token_name)
        self.request.user = None
        try:
            sess = Sessions.objects.get(id=token)
            if sess.is_active:
                self.request.user = sess.user
                return True

            return False
        except Exception as ex:
            return False

    def is_redirect_required(self):
        for each_pair in self.cookie_failure_redirection:
            if self.is_regex_match(each_pair[0], self.uri):
                return True
        return False

    def is_setting_cookie_required(self):
        for each in self.cookie_setter_urls:
            if self.is_regex_match(each, self.uri):
                return True
        return False

    def generate_token_for_user(self):
        user = self.response["phone"]
        self.expire_cookies(user)
        sess = Sessions.objects.create(**{"user": User.objects.get(phone=user)})
        print("session generated")
        return sess.id

    def expire_cookies(self, user):
        sess = Sessions.objects.filter(**{"user": User.objects.get(phone=user)})
        for each in sess:
            each.delete()

