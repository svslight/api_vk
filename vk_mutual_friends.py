import requests
import json
from pprint import pprint
from urllib.parse import urlencode
import time

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
# Получить Токен
# print('?'.join((AUTH_URL, urlencode(auth_data))))

# TOKEN = '9b0ba4bb04f6f34dbddb6b38d74ad3257fcdf7a67f17965cac880644ed6bdc4610438512aa1875ceb08d9'
user_id = 435315664

class User:
    api_url = 'https://api.vk.com/method/'
    params = {
        'access_token': '9b0ba4bb04f6f34dbddb6b38d74ad3257fcdf7a67f17965cac880644ed6bdc4610438512aa1875ceb08d9',
        'v': '5.92',
        'user_id': 435315664,
    }

    def __init__(self, user_id, friend=None, mutual=None, friends_list=None, each_friend_list=None):
        self.user_id = user_id
        self.friend = friend
        self.mutual = mutual
        self.friends_list = friends_list
        self.each_friend_list = each_friend_list

    # Фрматирование пути url-method ( https://api.vk.com/method//friends.get )
    def format_url(self, method_name):
        return f'{self.api_url}/{method_name}'

    # Выполнение запроса методов
    def make_request_method(self, method_name, user_id=None):
        method_url = self.format_url(method_name)

        params = self.params.copy()
        params['user_id'] = user_id or self.user_id

        result = requests.get(method_url, params=params).json()
        time.sleep(0.35)

        return result

    # def __add__(self):
    #     inter = self.friends_list & self.each_friend_list
    #     return inter


    def get_friends(self, user_id=None):
        return self.make_request_method('friends.get', user_id)

    def get_users(self, user_ids):
        method_url = self.format_url('users.get')
        params = self.params.copy()
        params['first_name'] = 'Имя'
        params['last_name'] = 'Фамилия'
        params['user_ids'] = user_ids

        result = requests.get(method_url, params=params).json()
        time.sleep(0.35)

        return result

    def friend_object_factory(self, friend):
        friend_info = friend['first_name'] + ' ' + friend['last_name'] + ' ' + str(friend['id'])
        return ' {}: '.format(friend_info)
        # return self.friend_info

    def mutual_object_factory(self, mutual):
        mutual_info = str(mutual['id']) + ' ' + mutual['first_name'] + ' ' + mutual['last_name']
        return '   - {} '.format(mutual_info)
        # return self.mutual_info

    # def __str__(self):
    #     if self.friend:
    #         rep = ' {}: '.format(self.friend_info)
    #     elif self.mutual:
    #         rep = '    {} '.format(self.mutual_info)
    #     return rep


def main():
    user = User(user_id)

    friends_response = user.get_friends()

    friends_list = set(friends_response['response']['items'])

    print('Наши общие друзья с:')
    # print(my_friends_list)
    for id_my_friend in friends_list:
        resp = user.get_friends(id_my_friend)

        each_friend_list = set(resp['response']['items'])

        # intersection = User(friends_list, each_friend_list)
        # intersection_add = intersection
        # print('intersection_add', intersection_add)

        intersection_friends = friends_list & each_friend_list
        # print('intersection_friends= ', intersection_friends)

        info_my_friend_resp = user.get_users(id_my_friend)
        info_my_friend_list = info_my_friend_resp['response']

        # print(info_my_friend_list)

        if len(intersection_friends):
            for friend in info_my_friend_list:
                friend_info = User(friend)
                friends_info = friend_info.friend_object_factory(friend)
                print(friends_info)

                for mutual_friends_id in intersection_friends:
                    mutual_friends_resp = user.get_users(mutual_friends_id)
                    mutual_friends_list = mutual_friends_resp['response']

                    for mutual in mutual_friends_list:
                        mutual_info = User(mutual)
                        mutual_friends_info = mutual_info.mutual_object_factory(mutual)
                        print(mutual_friends_info)


if __name__ == '__main__':
    main()

