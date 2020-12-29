from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('register', views.register),
    path('quotes', views.quotes_list),
    path('addQuote', views.add_quote),
    path('user/<int:userId>', views.all_their_quotes),
    path('like/<int:quoteId>', views.like),
    path('delete/<int:quoteId>', views.delete),
    path('edit/<int:userId>', views.edit),
    path('edit/update/<int:thisUserId>', views.update),
]
