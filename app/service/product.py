from crud import product_crud
from models import Product
from schemas import ProductCreate, ProductUpdate
from service import BaseService


class ProductService(BaseService[Product, ProductCreate, ProductUpdate]):
    pass


product_service = ProductService(product_crud, Product)
