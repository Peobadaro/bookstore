import factory
from django.contrib.auth.models import User

from order.models import Order


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"usuario{n}")
    email = factory.Faker("email")

    class Meta:
        model = User


class OrderFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def product(self, create, extracted, **kwargs):
        if create and extracted:
            self.product.set(extracted)

    class Meta:
        model = Order
        skip_postgeneration_save = True
