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

    def get(self, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users_user')
        users = cursor.fetchall()
        users_list = []
        for user in users:
            users_list.append(convert_to_dict(user))
        return Response(users_list)

    def post(self, request, *args, **kwargs):
        # copy search from products
        pass


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
        user = cursor.fetchall()
        user = convert_to_dict(user)
        if len(user) > 0:
            return JsonResponse(user, safe=False)

        return Response({'details': 'invalid email or password'}, safe=False, status=status.HTTP_400_BAD_REQUEST)