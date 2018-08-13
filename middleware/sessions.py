from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
import re
from api.models import User
from middleware.models import Sessions
import uuid

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

        self.session_action = self.response.get("session_action", None)
        if self.session_action:
            getattr(self, self.session_action)()
        return self.response

    def delete_session(self):
        try:
            token = self.request.COOKIES.get(self.token_name,  None)
            sess = Sessions.objects.get(id=token)
            sess.delete()
        except Exception as ex:
            print(ex)

    def delete_all_sessions(self):
        if self.response.get("user_id", None) and self.response["user_id"]:
            sess = Sessions.objects.filter(user_id=self.response["user_id"])
            for each in sess:
                each.delete()

    def set_token(self):
        self.delete_session()
        token = self.generate_token_for_user()
        self.response.set_cookie(self.token_name, token, max_age=365 * 24 * 60 * 60)

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

    def validate_cookie(self):
        token = self.request.COOKIES.get(self.token_name)
        self.request.user = None
        try:
            sess = Sessions.objects.get(id=token)
            if sess.is_active:
                self.request.user = sess.user
                self.request.is_admin = sess.user.is_admin
                return True

            return False
        except Exception as ex:
            return False

    def is_redirect_required(self):
        for each_pair in self.cookie_failure_redirection:
            if self.is_regex_match(each_pair[0], self.uri):
                return True
        return False

    def generate_token_for_user(self):
        user = self.response["phone"]
        sess = Sessions(user=User.objects.get(phone=user), id=str(uuid.uuid4()))
        sess.save()
        return sess.id


