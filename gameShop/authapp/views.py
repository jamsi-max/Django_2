from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.contrib import auth
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserChangePassword
from authapp.models import ShopUser

def login(request):
    if request.is_ajax():
        login_form = ShopUserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            
            user = auth.authenticate(username=username, password=password)

            if user and user.is_active:
                auth.login(request, user)

                content = {
                    'user': request.user,
                    'basket': request.user.basket.all(),
                }

                result = render_to_string('includes/inc__main_menu.html', context=content)
                return JsonResponse({'result': result})

        else:
            return JsonResponse({'result': 0, 'error': login_form.errors})

@login_required
def logout(request):
    if request.is_ajax():
        auth.logout(request)
        result = render_to_string('includes/inc__main_menu.html') #, context={'result': result.request})
        return JsonResponse({'result': result})


def reg(request):
    if request.method == 'POST':
        reg_form = ShopUserRegisterForm(request.POST, request.FILES)
        if reg_form.is_valid():
            user = reg_form.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('main'))
            else:
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('main'))
    else:
        reg_form = ShopUserRegisterForm()

    content={
        'page_title': 'registration',
        'reg_form': reg_form,
    }
    return render(request, 'authapp/reg.html', context=content)


@login_required
def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
    
    content = {
        'page_title': 'edit',
        'edit_form': edit_form,
        'mediaURL': settings.MEDIA_URL,
    }

    return render(request, 'authapp/edit.html', context=content)


@login_required
def chpassword(request):
    if request.method == 'POST':
        form = ShopUserChangePassword(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        form = ShopUserChangePassword(user=request.user)

    content = {
        'page_title': 'Change Password',
        'form': form,
    }
    return render(request, 'authapp/password.html', context=content)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', 
    kwargs={
        'email': user.email, 
        'activation_key': user.activation_key
        })

    title = f'Account confirmation {user.username}'
    message = f'To confirm your account {user.username} on the portal' \
              f'{settings.DOMAIN_NAME} follow the link: \n' \
              f'{settings.DOMAIN_NAME}{verify_link}'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = get_object_or_404(ShopUser, email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
        else:
            print(f'error activation user: {user}')
        return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main'))