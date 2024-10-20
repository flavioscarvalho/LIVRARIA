import factory
from product.models import Category, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("word")  # Gera uma palavra aleatória
    slug = factory.Faker("slug")  # Gera um slug único
    description = factory.Faker("sentence")  # Gera uma frase aleatória
    active = factory.Iterator([True, False])

    class Meta:
        model = Category


class ProductFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("pystr")
    price = factory.Faker("pyint")
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        # Se categorias forem passadas no momento da criação, adicione-as
        if extracted:
            for category in extracted:
                self.category.add(category)

    class Meta:
        model = Product
        skip_postgeneration_save = True
