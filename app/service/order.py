from crud import order_crud
from models import Order
from schemas import OrderCreate, OrderUpdate
from service import BaseService


class OrderService(BaseService[Order, OrderCreate, OrderUpdate]):
    pass


order_service = OrderService(order_crud, Order)
