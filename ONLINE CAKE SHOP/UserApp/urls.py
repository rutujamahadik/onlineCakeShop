from django.urls import path
from UserApp import views
urlpatterns = [
    path('', views.home),
    path('ShowCakes/<cid>',views.showCakes),
    path('ViewDetails/<cakeid>',views.ViewDetails),
    path('SignUp',views.SignUp),
    path('Login',views.Login),
    path('Logout',views.logout),
    path('addToCart',views.addToCart),
    path('showAllCartItems',views.showAllCartItems),
    path('MakePayment',views.MakePayment),
]
