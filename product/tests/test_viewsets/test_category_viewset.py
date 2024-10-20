import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from product.factories import CategoryFactory


class CategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="Technology")

    def test_get_all_category(self):
        response = self.client.get(
            reverse("category-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category_data = json.loads(response.content)

        # Verificar se a lista de categorias não está vazia
        self.assertGreater(len(category_data.get('results', [])), 0, "Nenhuma categoria encontrada na resposta")

        # Comparar o título da primeira categoria retornada com o título esperado
        self.assertEqual(category_data['results'][0]["title"], self.category.title)
