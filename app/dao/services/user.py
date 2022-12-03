import base64
import hashlib
import hmac

from app.dao.user import UserDAO
from app.helpers.constants import PWD_SALT, PWD_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, did):
        return self.dao.get_one(did)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_data):
        user_data["password"] = self.generate_password(user_data["password"])
        return self.dao.create(user_data)

    def update_partial(self, data):
        uid = data.get('id')
        user = self.get_one(uid)

        if 'name' in data:
            user.name = data.get('name')
        if 'surname' in data:
            user.surname = data.get('surname')
        if 'favorite_genre' in data:
            user.favorite_genre = data.get('favorite_genre')

        self.dao.update(user)

    def update_password(self, data):
        uid = data.get('id')
        user = self.get_one(uid)

        user.email = user.email
        if user.password == data['password']:
            data["password"] = data["new_password"]
            data["password"] = self.generate_password(data["password"])
            user.password = data.get('password')
        self.dao.update(user)

    def delete(self, uid):
        self.dao.delete(uid)

    def generate_password(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode('utf-8'),
            PWD_SALT,
            PWD_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def compare_passwords(self, password_hash, other_password) -> bool:
        decoded_digest = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_SALT,
            PWD_ITERATIONS
        )

        return hmac.compare_digest(decoded_digest, hash_digest)
