from django.shortcuts import redirect
from system.config import GlobalConfig
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import resolve
from django.conf import settings


class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated

        no_auth_url_list = GlobalConfig.no_auth_url_list()
        # print('no_auth_url_list : ', no_auth_url_list)
        # print(f'auth: {request.user.is_authenticated}|||anoynymous : {request.user.is_anonymous}')
        if request.user.is_authenticated and not request.user.is_anonymous:
            response = self.get_response(request)
            if request.session.get('logged_in_pass'):
                return response
            else:
                logout(request)
                return redirect('login')

        else:
            url = resolve(request.path)
            print('custome auth middleware url else: ', url) 
            if url.url_name in no_auth_url_list:
                # The requested URL is the login URL, pass the request on to the next middleware
                # print(f'{url.url_name} || {no_auth_url_list}')
                response = self.get_response(request)

            else:
                # Redirect the user to the login page
                response = redirect('login')

        return response
