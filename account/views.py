from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from .models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str

from app.decorators import user_not_authenticated
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token

@user_not_authenticated
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save(commit = False)
			user.is_active = False
			user.save()
			activateEmail(request, user, form.cleaned_data.get('email'))
			return redirect("home")
		for error in list(form.errors.values()):
			messages.error(request, error)
	form = NewUserForm()
	return render (request=request, template_name="account/register.html", context={"register_form":form})

@user_not_authenticated
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Você fez login como {username}.")
				return redirect(request.GET.get('next', '/menu/'))
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
		else:
			for error in list(form.errors.values()):
				messages.error(request, error)
	form = AuthenticationForm()
	return render(request=request, template_name="account/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "Você fez logout.") 
	return redirect("home")

@user_not_authenticated
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Redefinição de Senha"
					email_template_name = "account/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':get_current_site(request).domain,
					'site_name': 'AuxGrade',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user.username,
					'token': default_token_generator.make_token(user),
					'protocol': 'https' if request.is_secure() else 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'auxgrade.noreply@gmail.com', ['auxgrade.noreply@gmail.com'], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					messages.success(request, 'Uma mensagem com informações para redefinir a senha foi enviado para seu e-mail.')
					return redirect ("home")
			messages.error(request, 'Um email inválido foi inserido.')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="account/password_reset.html", context={"password_reset_form":password_reset_form})

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('account/activate_account_email.txt', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })
    email = EmailMessage(mail_subject, message, 'auxgrade.noreply@gmail.com', ['auxgrade.noreply@gmail.com'])
    if email.send():
        messages.success(request, f'Usuário {user} criado. Por favor vá para a caixa de entrada do seu email {to_email} e clique no \
            link de ativação recebido para completar o registro. Verifique a caixa de spam.')
    else:
        messages.error(request, f'Erro ao enviar email para {to_email}, verifique se digitou corretamente.')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Obrigado por confirmar seu email. Agora você pode entrar em sua conta.')
        return redirect('login')
    else:
        messages.error(request, 'Link de ativação inválido.')
    
    return redirect('home')
