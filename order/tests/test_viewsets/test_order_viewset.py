import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from order.factories import OrderFactory, UserFactory
from product.factories import CategoryFactory, ProductFactory


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100, category=[self.category]
        )
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)

        # Verificar se a lista de pedidos não está vazia
        self.assertGreater(
            len(order_data.get("results", [])),
            0,
            "Nenhum pedido encontrado na resposta",
        )

        # Verificar se o produto está presente no pedido
        order = order_data["results"][0]  # Acesso à lista de resultados paginados
        self.assertIn("product", order, "Produto não encontrado no pedido")

        # Convertendo o valor retornado para float para comparar com self.product.price
        self.assertEqual(float(order["product"][0]["price"]), float(self.product.price))
        self.assertEqual(order["product"][0]["title"], self.product.title)
        self.assertEqual(order["product"][0]["active"], self.product.active)
        self.assertEqual(
            order["product"][0]["category"][0]["title"],
            self.category.title,
        )
