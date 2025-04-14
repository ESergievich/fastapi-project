from sqladmin import Admin

from .views import UserAdmin, ProductAdmin, OrderAdmin, OrderItemAdmin


def setup_admin(app, engine):
    admin = Admin(
        app,
        engine,
    )

    admin.add_view(UserAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(OrderItemAdmin)
