from sqladmin import ModelView
from models import User, Product, Order, OrderItem


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.role, User.orders]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name, Product.price, Product.created_at]
    form_columns = [Product.name, Product.description, Product.price]
    column_searchable_list = [Product.name]


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.user_id, Order.created_at, Order.order_items]


class OrderItemAdmin(ModelView, model=OrderItem):
    column_list = [OrderItem.order_id, OrderItem.product_id, OrderItem.quantity]
