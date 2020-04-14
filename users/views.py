from rest_framework import generics, status
from rest_framework.response import Response
from django.db import connection
from .serializer import UserSerializer
from django.http import JsonResponse


def convert_to_dict(user):
    user_dict = {
        'id': user[0][0],
        'name': user[0][1],
        'email': user[0][2],
    }
    return user_dict


class UserAPIView(generics.GenericAPIView):

    serializer_class = UserSerializer

    def get(self, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users_user WHERE id=' + str(kwargs['id']))
        user = cursor.fetchall()
        print(user)
        user_dict = convert_to_dict(user)
        return Response(user_dict)

    def get_queryset(self):
        pass


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

    def get_queryset(self):
        pass


class LoginUserAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users_user WHERE email="' + request.data['email'] +
                       '" AND password="' + request.data['password'] + '"')
        user = cursor.fetchall()
        user = convert_to_dict(user)
        print(user)
        if len(user) > 0:
            return JsonResponse(user, safe=False)

        return Response({'details': 'invalid email or password'}, safe=False, status=status.HTTP_400_BAD_REQUEST)