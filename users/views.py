from rest_framework import generics, status
from rest_framework.response import Response
from django.db import connection
from .serializer import UserSerializer
from django.http import JsonResponse


def convert_to_dict(user):
    user_dict = {
        'id': user[0],
        'name': user[1],
        'email': user[2],
    }
    return user_dict


class UserAPIView(generics.GenericAPIView):

    serializer_class = UserSerializer

    def user_select_query_builder(self, validated_dict):
        query = 'SELECT * FROM users_user WHERE '

        first_itr = True
        for key, value in validated_dict.items():
            if first_itr and key != 'csrfmiddlewaretoken':
                if isinstance(value, int):
                    query += key + ' LIKE "%' + str(value) + '%"'
                else:
                    query += key + ' LIKE "%' + value.lower().strip() + '%"'
                first_itr = False
            elif key != 'csrfmiddlewaretoken':
                if isinstance(value, int):
                    query += ' AND ' + key + ' LIKE "%' + str(value) + '%"'
                else:
                    query += ' AND ' + key + ' LIKE "%' + value.lower().strip() + '%"'

        query += ';'

        return query

    def get_validated_dict(self, user_dict):
        valid_keys_list = ['id', 'name', 'email']

        if 'csrfmiddlewaretoken' in user_dict:
            del user_dict['csrfmiddlewaretoken']

        keys_to_delete = [key for key, value in user_dict.items() if value is None or value is '']
        for key in keys_to_delete:
            del user_dict[key]

        if not user_dict:
            raise ValueError('empty object')

        # for key in product_dict.keys():
        #     if key not in valid_keys_list:
        #         raise ValueError('invalid product object key')

        return user_dict

    def get(self, *args, **kwargs):

        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users_user')
        print('SELECT * FROM users_user')
        users = cursor.fetchall()
        print(users)
        users_list = []
        for user in users:
            users_list.append(convert_to_dict(user))
        return Response(users_list)

    def post(self, request, *args, **kwargs):
        search_query = request.data.copy()
        print('user search query: ', search_query)
        try:
            search_query = self.get_validated_dict(search_query)
        except ValueError as error:
            return Response({'details': format(error)}, status=status.HTTP_400_BAD_REQUEST)

        cursor = connection.cursor()

        query = self.user_select_query_builder(search_query)
        print('user search post query: ', query)
        cursor.execute(query)
        user_list = []
        result_users = cursor.fetchall()
        for user in result_users:
            user_list.append(convert_to_dict(user))

        print(user_list)
        return Response(user_list)


class AddUserAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        print('request NAME: ', request.data['name'])

        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        with connection.cursor() as cursor:
            print('request ', request.data)
            query = 'INSERT INTO users_user (name, email, password) VALUES ("' + request.data['name'] \
                    + '", "' + request.data['email'] + '", "' + request.data['password'] + '")'
            cursor.execute(query)
            print('add user post insert query: ', query)

            query = 'SELECT * FROM users_user WHERE name = "' + request.data['name'] + '" AND email = "' \
                    + request.data['email'] + '" AND password = "' + request.data['password'] + '"'
            cursor.execute(query)
            print('add user post select query: ', query)

            data = list(cursor.fetchall()[0])

        response = {
            'id': data[0],
            'name': data[1],
            'email': data[2]
        }

        return Response(response)

    def get_queryset(self):
        pass


class LoginUserAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        cursor = connection.cursor()
        query = 'SELECT * FROM users_user WHERE email="' + request.data['email'] + \
                '" AND password="' + request.data['password'] + '"'
        cursor.execute(query)
        print('login user post query: ', query)
        user = cursor.fetchall()[0]
        user = convert_to_dict(user)
        if len(user) > 0:
            return JsonResponse(user, safe=False)

        return Response({'details': 'invalid email or password'}, safe=False, status=status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users_user WHERE id=' + str(kwargs['id']))
        user = cursor.fetchall()[0]
        print(user)
        return Response([convert_to_dict(user)])
