from crud import BaseCRUD
from models import Product


class ProductCRUD(BaseCRUD[Product]):
    pass


product_crud = ProductCRUD(Product)
