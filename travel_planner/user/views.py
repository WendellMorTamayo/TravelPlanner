from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.db import connection
from django.shortcuts import render, redirect
from django.views import View
from .form import UserRegistrationForm
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


class UserLoginView(View):
    template_name = 'user_login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        try:
            cursor = connection.cursor()
            cursor.callproc('ValidateLogin', [username, password])
            result = cursor.fetchall()
            print(result[0][0])
            cursor.close()
        except Exception as e:
            logger.error("Database error: %s", e)
            return HttpResponseServerError("Internal Server Error", e)

        logger.debug("Validation Result: %s", result)

        if result and result[0][0] > 0:
            user_id = result[0][0]
            request.session['username'] = username
            request.session['user_id'] = user_id
            print("User ID from session: ", request.session.get('user_id'))
            return redirect('index')
        else:
            messages.warning(request, 'Invalid login credentials.')

        return render(request, self.template_name, {'error_message': 'Invalid login credentials'})


class UserRegistrationView(View):
    template_name = 'user_registration.html'

    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, self.template_name, {'register_form': user_form})

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            pUsername = user_form.cleaned_data['username']
            pEmail = user_form.cleaned_data['email']
            pPassword = user_form.cleaned_data['password']
            pFirstname = user_form.cleaned_data['first_name']
            pLastname = user_form.cleaned_data['last_name']
            pDateOfBirth = user_form.cleaned_data['date_of_birth']
            pContactNumber = user_form.cleaned_data['contact_number']

            # Execute stored procedure
            with connection.cursor() as cursor:
                cursor.callproc('UserRegister',
                                [pUsername, pEmail, pPassword, pFirstname, pLastname, pDateOfBirth, pContactNumber])
                result = cursor.fetchone()

            if 'User registered successfully' in result:
                return redirect('/account/login')
            else:
                # Handle error case, you can modify this based on your needs
                return render(request, self.template_name, {'register_form': user_form, 'error_message': result})
        else:
            return render(request, self.template_name, {'register_form': user_form})
