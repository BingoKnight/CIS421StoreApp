from rest_framework import generics
from rest_framework.response import Response
from django.db import connection
from .serializer import UserSerializer
from .models import User


class UserAPIView(generics.GenericAPIView):

    serializer_class = UserSerializer

    @staticmethod
    def convert_to_dict(users_list):
        new_list = []
        for user in users_list:
            new_list.append({
                'id': user[0],
                'name': user[1],
                'email': user[2],
            })
        print(new_list)
        return new_list

    def get(self, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users_user')
        users = cursor.fetchall()
        print(users)
        usersList = self.convert_to_dict(users)
        return Response(usersList)


class AddUserAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        print('request NAME: ', request.data['name'])

        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO users_user (name, email, password) VALUES (%s, %s, %s)',
                           (request.data['name'], request.data['email'], request.data['password']))

            cursor.execute('SELECT * FROM users_user WHERE name = %s AND email = %s AND password = %s',
                           (request.data['name'], request.data['email'], request.data['password']))

            data = list(cursor.fetchall()[0])

        response = {
            'id': data[0],
            'name': data[1],
            'email': data[2]
        }

        return Response(response)
