from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("itemadd", views.itemadd, name="itemadd"),
    path("itempage/<int:item_id>", views.item_page, name="itempage"),
    path("itemmod/<int:item_id>", views.itemmod, name="itemmod"),
    path("itemdel/<int:item_id>", views.itemdel, name="itemdel"),
]