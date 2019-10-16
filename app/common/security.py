from werkzeug.security import safe_str_cmp
from models.user import AdminModel


def authenticate(phone_no, password):
    admin = AdminModel.find_by_phone_no(phone_no)
    if admin and safe_str_cmp(admin.password, password):
        return admin


def identity(payload):
    user_id = payload['identity']
    return AdminModel.find_by_id(user_id)
