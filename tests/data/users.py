from faker import Faker

fake = Faker()


class FakeUser:
    """Класс для генерации фейкового пользователя"""

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.id = None
        self.is_active = True
        self.is_verified = False
        self.is_superuser = False
        self.access_token = None
        self.verify_token = None
        self.reset_password_token = None

    @classmethod
    def random(cls):
        """Создаёт случайного пользователя"""
        return cls(email=fake.email(), password=fake.password())
