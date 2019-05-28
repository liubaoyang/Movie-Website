from flask import Blueprint
admin=Blueprint('adminhtml',__name__,template_folder="templates",static_folder='static')

from app.admin import views,views_admin
