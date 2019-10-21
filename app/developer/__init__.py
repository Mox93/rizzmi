from functools import wraps
from flask import Blueprint, redirect, url_for
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_admin.contrib.mongoengine import ModelView
from flask_login import current_user
from wtforms.validators import ValidationError
from models.user import DeveloperModel
from models.form import FormTemplateModel, CollectionTemplateModel
from models.field import FieldModel
from app import app


class ExtendedModelView(ModelView):
    # create_modal = True
    # edit_modal = True
    can_export = True

    # column_searchable_list = ['name']

    create_template = 'dev/extended_create.html'
    list_template = 'dev/extended_list.html'
    edit_template = 'dev/extended_edit.html'

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("dev.login"))


def unique(form, field):
    user = DeveloperModel.find_one_by(field.id, field.data)
    if user:
        raise ValidationError(f"'{field.data}' already exists.")


def redirect_auth_user_to(endpoint):
    def auth_user_check(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            if current_user.is_authenticated:
                return redirect(url_for(endpoint))
            return func(*args, **kwargs)
        return func_wrapper
    return auth_user_check


dev_bp = Blueprint("dev", __name__, template_folder="templates")


from developer.views import registration, login
from developer.views.profile import DevProfileView
from developer.views.homepage import DevHomeView

# TODO figure out how to reference the urls using url_for
admin = Admin(app, name="Rizzmi Team", template_mode='bootstrap3',
              index_view=DevHomeView(url="/dev", template="dev/homepage.html"))

admin.add_view(ExtendedModelView(FormTemplateModel, name="Forms", endpoint="forms"))
admin.add_view(ExtendedModelView(CollectionTemplateModel, name="Collections", endpoint="collection"))
admin.add_view(ExtendedModelView(FieldModel, name="Fields", endpoint="fields"))
admin.add_view(DevProfileView(name="Profile", endpoint="profile", category="Go To"))

admin.add_sub_category(name="Custom", parent_name="Go To")
admin.add_link(MenuLink(name='Forms', url="/forms", category='Custom'))
admin.add_link(MenuLink(name='Collections', url="/collections", category='Custom'))
admin.add_link(MenuLink(name='Fields', url="/fields", category='Custom'))

admin.add_sub_category(name="Action", parent_name="Go To")
admin.add_link(MenuLink(name='Log Out', url="/dev/logout", category='Action'))
admin.add_link(MenuLink(name='Delete Account', url="/dev/delete", category='Action'))

