from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from accounts.api_service import emailvalidation
from accounts.models import Address, Follower
from customer_service.mails import send_mail_activation_user
from publication.models import Post, PostMedia

User = get_user_model()


def follow_hint(following: object, followed: object):
    try:
        Follower.objects.get(followed=followed, following=following)
        return False
    except:
        return True


def profile(request, username: str):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    followers = Follower.objects.filter(followed=user)
    followings = Follower.objects.filter(following=user)

    following = request.user  # suiveur
    context = {
        'user_profile': user,
        'posts': posts,
        'followers': followers,
        'followings': followings,
        'follow_hint': follow_hint(following=following, followed=user),
    }
    return render(request, 'accounts/profile.html', context=context)


@login_required
def follow(request, username: str):
    following = request.user  # suiveur
    followed = User.objects.get(username=username)  # suivi
    
    if follow_hint(following=following, followed=followed):
        Follower.objects.create(followed=followed, following=following)
    else:
        follower = Follower.objects.get(followed=followed, following=following)
        follower.delete()
    """if not followed == following:
        try:
            follower = Follower.objects.get(followed=followed, following=following)
            follower.delete()
        except:
            Follower.objects.create(followed=followed, following=following)"""

    return redirect(reverse('accounts:profile', kwargs={'username': followed.username}))


def welcome_message(request):
    return render(request, 'accounts/welcome_message.html')


@login_required
def set_address(request):
    user = request.user
    context = {}
    if user.address:
        context = {
            'city': user.address.city,
            'zip_code': user.address.zip_code,
            'neighborhood': user.address.neighborhood,
            'street': user.address.street,
            'number': user.address.number
        }

    if request.method == "POST":
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code').lower()
        neighborhood = request.POST.get('neighborhood').lower()
        street = request.POST.get('street').lower()
        number = request.POST.get('number').lower()

        if not user.address:
            address = Address.objects.create(city=city,
                                             zip_code=zip_code,
                                             neighborhood=neighborhood,
                                             street=street,
                                             number=number)
            user.address = address
            user.save()
        else:
            user.address.city = city
            user.address.zip_code = zip_code
            user.address.neighborhood = neighborhood
            user.address.street = street
            user.address.number = number
            user.address.save()

        return redirect('accounts:profile')

    return render(request, 'accounts/set_address.html', context)


def signup(request):
    context = {}

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # retun value if errors
        context = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'password1': password1,
            'password2': password2,
        }
        if not emailvalidation(email):
            context['email_error'] = "Cette adresse est hors d'atteinte."
        elif password1 != password2:
            context['password_error'] = 'Les deux mots de passe ne correspondent pas.'
        else:
            try:
                user = User.objects.create_user(username=username,
                                                password=password1,
                                                first_name=first_name,
                                                last_name=last_name,
                                                email=email,
                                                is_active=False
                                                )
                # login(request, user)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                send_mail_activation_user(
                    user=user,
                    uid=uid,
                    token=token
                )

                return redirect('accounts:welcome-message')  # welcome message
            except Exception as ex:
                # print(f'erreur de caca: {ex}')
                if str(ex) == 'UNIQUE constraint failed: accounts_customeruser.username':
                    context['username_error'] = "Un autre compte utilise déjà ce pseudo."
                elif str(ex) == 'UNIQUE constraint failed: accounts_customeruser.email':
                    context['email_error'] = "Un autre compte utilise déjà cette adresse email."
                else:
                    context['error'] = "Vérifiez que vos informations sont exactes."

    return render(request, 'accounts/signup.html', context)


def activation_user(request, uidb64, token):
    uidb64 = uidb64
    token = token

    if uidb64 is not None and token is not None:
        uid = urlsafe_base64_decode(uidb64)
        try:
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token) and user.is_active == False:
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('accounts:profile')
        except:
            pass

    return redirect('accounts:login')


def login_user(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        context = {'email': email}

        if User.objects.filter(email=email, is_active=False).exists():
            context['error'] = 'Merci de confirmer votre adresse électronique.'

        elif user := authenticate(email=email, password=password):
            login(request, user)
            return redirect('home:index')
        else:
            context['error'] = 'Informations non reconnues, reassayer!'

    return render(request, 'accounts/login.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('accounts:login')
