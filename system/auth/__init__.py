from apps.user.models import User
from django.contrib import messages
# from system.utils import verify_password
from django.contrib.auth.hashers import check_password

# def authenticate_user(request, email, password):
#     context = {}
#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         context['errors'] = 'email not found'
#         return None
    
#     if user and user.password != password:
#         context['errors'] = 'password wrong'
#         return None

#     return user

# def authenticate_user(request, email, password):
#     context = {}
#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         context['errors'] = 'email not found'
#         return None
#     try:
#         user = User.objects.get(email=email, password=password)
#     except Exception:
#         context['errors'] = 'password wrong'
#         messages.error(request, 'Cannot save. Please fill up the required inputs.')
    
#     return user

def authenticate_user(request, email, password):
    try:
        # Get the user by email
        user = User.objects.get(email=email)
        print('user passwrod : ', user.password)
        # Check the password
        if user.password == password:  # Securely compare hashed password
            return user
        else:
            messages.error(request, 'Incorrect password.')
            return None
    except User.DoesNotExist:
        messages.error(request, 'Email not found.')
        return None

def authenticate_user_by_id(id=None):
    try:
        user = User.objects.get(id=id)
        return user
    except User.DoesNotExist:
        return None

