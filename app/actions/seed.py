import asyncio
import random

from faker import Faker
from fastapi_users.password import PasswordHelper
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper, settings
from models import User, Product, Order, OrderItem, AccessToken
from utils import RoleEnum

fake = Faker()
password_helper = PasswordHelper()

NUM_USERS = 5
NUM_PRODUCTS = 10
NUM_ORDERS = 15


async def seed(with_clean: bool = False):
    async with db_helper.session_factory() as session:
        if with_clean:
            await clear_data(session)

        users = [
            User(
                username=fake.user_name(),
                hashed_password=password_helper.hash("password"),
                email=fake.email(),
                role=RoleEnum.CUSTOMER,
            )
            for _ in range(NUM_USERS)
        ]
        session.add_all(users)

        products = [
            Product(
                name=fake.unique.word().capitalize(),
                description=fake.text(max_nb_chars=100),
                price=round(random.uniform(10, 200), 2),
            )
            for _ in range(NUM_PRODUCTS)
        ]
        session.add_all(products)

        await session.flush()

        for _ in range(NUM_ORDERS):
            user = random.choice(users)
            order = Order(user=user)
            session.add(order)
            await session.flush()

            items = random.sample(products, random.randint(1, 3))
            for product in items:
                quantity = random.randint(1, 5)
                order_item = OrderItem(
                    order_id=order.id, product_id=product.id, quantity=quantity
                )
                session.add(order_item)

        await session.commit()


async def clear_data(session: AsyncSession):
    for model in [OrderItem, Order, Product, User, AccessToken]:
        await session.execute(delete(model))
    await session.commit()


if __name__ == "__main__":
    asyncio.run(seed(with_clean=settings.initial_data.seed_with_clean))
