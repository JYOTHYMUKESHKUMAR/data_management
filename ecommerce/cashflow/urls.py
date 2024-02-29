from django.urls import path
from . import views

app_name="cashflow"

urlpatterns = [
    path('',views.allProdcat,name="allProdcat"),
    path('<slug:c_slug>/',views.allProdcat,name="Products_by_categories"),
    path('<slug:c_slug>/<slug:product_slug>/',views.Product_Detail,name="productdetails"),
    
]






