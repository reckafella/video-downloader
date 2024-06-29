from random import randint
from django.core.mail import send_mail

""" contains functions to handle passwords """


class PasswordReset:
    """Class to handle password reset"""

    @staticmethod
    def generate_code() -> str:
        """Method to generate OTP code"""
        return str(randint(100000, 999999))

    @staticmethod
    def send_email(email: str, code: str) -> int:
        """Method to send OTP via email"""
        subject = 'Password Reset Code'
        message = f'Your Password reset code is: {code}'
        email_from = 'ethanmuthoni@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, email_from,
                  recipient_list, fail_silently=False)

'''
def password_reset_email(request):
    """ View to handle sending password reset tokens """
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                token = PasswordReset.generate_token()
                user.profile.reset_token = token
                user.profile.token_created_at = timezone.now()
                user.profile.token_expires_at = timezone.now() + timezone.timedelta(hours=2)
                user.profile.save()
                PasswordReset.send_reset_email(email, token)
                request.session['reset_email'] = email
                messages.success(request, 'Password reset token sent')
                return redirect('password_reset_token')
            except User.DoesNotExist:
                messages.error(request, 'No user found with that email')
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset_email.html', {'form': form})


def password_reset_token(request):
    """ View to handle password reset token verification """
    if 'reset_email' not in request.session:
        return redirect('password_reset_email')
    
    email = request.session['reset_email']

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data.get('token')
            try:
                user = User.objects.get(email=email)
                if (user.profile.reset_token == token) and (user.profile.token_expires_at > timezone.now()):
                    return redirect('password_reset_confirm')
                else:
                    messages.error(request, 'Invalid token')
            except User.DoesNotExist:
                messages.error(request, 'An error occurred. Please try again.')
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset_token.html', {'form': form})


def password_reset_confirm(request):
    """ View to handle password reset """
    if 'reset_email' not in request.session:
        return redirect('password_reset_email')

    email = request.session['reset_email']

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password1 = form.cleaned_data.get('password')
            new_password2 = form.cleaned_data.get('password2')
            if new_password1 != new_password2:
                messages.error(request, 'Passwords do not match')
            else:
                try:
                    user = User.objects.get(email=email)
                    user.set_password(new_password1)
                    user.save()

                    # Keeps the user logged in after password change
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Password reset successfully')
                    return redirect('login')
                except User.DoesNotExist:
                    messages.error(request, 'An error occurred. Please try again.')
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset_confirm.html', {'form': form})
'''

""" def generate_code() -> str:
    ''' function to generate and return a 6-digit code'''
    return str(randint(100000, 999999))
 """
