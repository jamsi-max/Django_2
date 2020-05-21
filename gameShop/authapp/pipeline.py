from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile, ShopUser
from gameShop.settings import MEDIA_ROOT

def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(dict(fields=','.join(('bdate', 'sex', 'about')),
                                                access_token=response['access_token'],
                                                v='5.92')),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data.get('sex'):
        user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

    if data.get('about'):
        user.shopuserprofile.aboutMe = data['about']

    if data.get('bdate'):
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        user.age = age
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if response.get('email'):
        user.email = response['email']

    if response.get('user_photo'): 
        ava = requests.get(response.get('user_photo'))
        file_name = response.get('user_photo').split('?')[0].split('/')[-1]
        file_path = MEDIA_ROOT + '/users_avatar/' + file_name
        if file_path != (MEDIA_ROOT + str(user.avatar)):
            with open(file_path, 'wb') as f:
                f.write(ava.content)
            user.avatar = '/users_avatar/' + file_name

    user.save()
    