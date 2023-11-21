from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path('selected_category', views.selected_category, name="selected_category"),
    path('listing_page/<int:id>', views.listing_page, name='listing_page'),
    path('category', views.category, name="category"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('add_watchlist/<int:id>', views.add_watchlist, name="add_watchlist"),
    path('remove_watchlist/<int:id>', views.remove_watchlist, name="remove_watchlist"),
    path('comment/<int:id>', views.comment, name="comment"),
    path('addbid/<int:id>', views.addbid, name="addbid"),
    path('closebid/<int:id>', views.closebid, name="closebid"),

]