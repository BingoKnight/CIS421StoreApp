from rest_framework import generics, status
from rest_framework.response import Response
from django.db import connection
from .serializer import ProductSerializer
from .models import Product


def product_select_query_builder(validated_dict):
    query = 'SELECT * FROM products_product WHERE '
    # first_itr = True
    # for key in validated_dict:
    #     if first_itr and key != 'csrfmiddlewaretoken':
    #         query += key.lower()
    #         first_itr = False
    #     elif key != 'csrfmiddlewaretoken':
    #         query += ', ' + key.lower()

    # query += ' FROM products_product WHERE '
    first_itr = True
    for key, value in validated_dict.items():
        if first_itr and key != 'csrfmiddlewaretoken':
            query += key.lower() + '="' + value.lower() + '"'
            first_itr = False
        elif key != 'csrfmiddlewaretoken':
            query += ' AND ' + key.lower() + '="' + value.lower() + '"'

    query += ';'
    print(query)

    return query


def convert_to_dict(products_list):
    new_list = []
    for product in products_list:
        new_list.append({
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'category': product[3],
            'price': product[4],
            'quantity': product[5]
        })

    return new_list


def get_validated_list(product_dict, is_post):
    valid_keys_list = ['name', 'description', 'category', 'price', 'quantity', 'csrfmiddlewaretoken']

    del product_dict['csrfmiddlewaretoken']

    keys_to_delete = [key for key, value in product_dict.items() if value is None or value is '']
    for key in keys_to_delete:
        del product_dict[key]

    if not product_dict:
        raise ValueError('empty object')

    for key in product_dict.keys():
        if key not in valid_keys_list:
            raise ValueError('invalid product object key')

    if is_post:
        for key in valid_keys_list:
            if key not in product_dict:
                raise ValueError('invalid object format')

    return product_dict


class ProductAPIView(generics.GenericAPIView):

    serializer_class = ProductSerializer

    @staticmethod
    def product_insert_query_builder(validated_dict):
        query = 'INSERT INTO products_product ('

        first_itr = True
        for key in validated_dict:
            if first_itr and key != 'csrfmiddlewaretoken':
                query += key.lower().strip()
                first_itr = False
            elif key != 'csrfmiddlewaretoken':
                query += ', ' + key.lower().strip()

        query += ') VALUES ('
        first_itr = True
        for key, value in validated_dict.items():
            if first_itr and key != 'csrfmiddlewaretoken':
                query += '"' + value.lower().strip() + '"'
                first_itr = False
            elif key != 'csrfmiddlewaretoken':
                query += ',"' + value.lower().strip() + '"'

        query += ');'
        return query

    def post(self, request, *args, **kwargs):
        try:
            validated_dict = get_validated_list(request.data.copy(), True)
        except ValueError as error:
            return Response({'details': format(error)}, status=status.HTTP_400_BAD_REQUEST)

        query = self.product_insert_query_builder(validated_dict)
        cursor = connection.cursor()
        cursor.execute(query)
        return Response({'details': 'success'})

    def get(self, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM products_product')
        products_list = cursor.fetchall()

        products_list = convert_to_dict(products_list)
        return Response(products_list)

    def put(self, request):
        pass

    def get_queryset(self):
        pass


class ProductSearchAPIView(generics.GenericAPIView):

    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        search_query = request.data.copy()
        try:
            search_query = get_validated_list(search_query, False)
        except ValueError as error:
            return Response({'details': format(error)}, status=status.HTTP_400_BAD_REQUEST)

        print(search_query)
        cursor = connection.cursor()

        query = product_select_query_builder(search_query)
        print(query)
        cursor.execute(query)
        result = convert_to_dict(cursor.fetchall())

        return Response(result)

    def get_queryset(self):
        pass
