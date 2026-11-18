import factory

from product.models import Category, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("word")
    slug = factory.Sequence(lambda n: f"categoria-{n}")
    description = factory.Faker("sentence")
    active = True

    class Meta:
        model = Category


class ProductFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("sentence")
    price = factory.Faker("pyint", min_value=1, max_value=500)
    active = True

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if create and extracted:
            self.category.set(extracted)

    class Meta:
        model = Product
        skip_postgeneration_save = True
