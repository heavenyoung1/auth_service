from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
print(BASE_DIR)

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "core" / "_certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "core" / "_certs" / "jwt-public.pem"
    def __repr__(self):
        return f"AuthJWT(private_key_path={self.private_key_path})"

# Создаем экземпляр класса
auth_jwt_instance = AuthJWT()

# Выводим значение private_key_path
print(f"private_key_path: {auth_jwt_instance.private_key_path}")

# Вызываем метод __repr__
print(repr(auth_jwt_instance))