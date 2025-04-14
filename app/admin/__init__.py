__all__ = ("UserAdmin", "ProductAdmin", "OrderAdmin", "OrderItemAdmin", "setup_admin")

from .views import UserAdmin, ProductAdmin, OrderAdmin, OrderItemAdmin
from .setup_admin import setup_admin
