#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.viewsets import ModelViewSet
from product.models import Product
from product.serializers.product_serializer import ProductSerializer
# from rest_framework.authentication import (
#     SessionAuthentication,
#     BasicAuthentication,
#     TokenAuthentication,
# )
# from rest_framework.permissions import IsAuthenticated


class ProductViewSet(ModelViewSet):
    # authentication_classes = [
    #     SessionAuthentication,
    #     BasicAuthentication,
    #     TokenAuthentication,
    # ]
    # permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by("id")
