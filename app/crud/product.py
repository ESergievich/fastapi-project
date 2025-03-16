from crud import BaseCRUD
from models import Product
from schemas import ProductCreate, ProductUpdate


class ProductCRUD(BaseCRUD[Product, ProductCreate, ProductUpdate]):
    pass


product_crud = ProductCRUD(Product)
