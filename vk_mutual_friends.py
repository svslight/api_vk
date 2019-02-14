import requests
import json
from pprint import pprint
from urllib.parse import urlencode

# id-приложения
APP_ID = 6854454

# Авторизация
AUTH_URL = 'https://oauth.vk.com/authorize'
auth_data = {
    'client_id': APP_ID,
    'display': 'page',
    'scope': 'status,friends',
    'response_type': 'token',
    'v': '5.92',
    }

TOKEN = '9570e65128ca5ef049f7acb08267f6e21262f07c600583e8aa09add5eff22eeb196a2d13fd27b6d606ce8'
user_id = 435315664

# Получение ссылки на адрес Токен
# print('?'.join((AUTH_URL, urlencode(auth_data))))

class User:
    def __init__(self, token):
        self.token = token

    def get_params(self):
        return{
            'v': '5.92',
            'access_token': TOKEN,
            'user_id': user_id,
        }

    def get_friends(self, usr):
        # params = self.get_params()
        response = requests.get('https://api.vk.com/method/friends.get', params={'access_token': TOKEN,
                                                                                 'user_id': usr,
                                                                                 'v': '5.92'
                                                                                 })

        resp_json = response.json()
        return resp_json

    def get_users(self, usr):
        response = requests.get('https://api.vk.com/method/users.get', params={'access_token': TOKEN,
                                                                               'user_id': usr,
                                                                               'first_name': 'Имя',
                                                                               'last_name': 'Фамилия',
                                                                               'v': '5.92'
                                                                               })

        resp_json = response.json()
        return resp_json


user = User(TOKEN)

friends_response = user.get_friends(user_id)
my_friends_list = set(friends_response['response']['items'])

print('Наши общие друзья с:')
for id_my_friend in my_friends_list:
    resp = user.get_friends(id_my_friend)
    each_friend_list = set(resp['response']['items'])

    intersection_friends = set.intersection(my_friends_list, each_friend_list)

    info_my_friend_resp = user.get_users(id_my_friend)
    info_my_friend_list = info_my_friend_resp['response']

    if len(intersection_friends):
        for info_my_friend in info_my_friend_list:
            p_info_my_friend = str(info_my_friend['id']) + ' ' + info_my_friend['first_name'] + ' ' + info_my_friend['last_name']
            print(' {}: '.format(p_info_my_friend))

            for mutual_friends in intersection_friends:
                info_mutual_friends_resp = user.get_users(mutual_friends)
                info_mutual_friends_list = info_mutual_friends_resp['response']
                for info_mutual_friends in info_mutual_friends_list:
                    p_info_mutual_friends = info_mutual_friends['first_name'] + ' ' + \
                                       info_mutual_friends['last_name']
                    print('     {} {} '.format(mutual_friends, p_info_mutual_friends))





