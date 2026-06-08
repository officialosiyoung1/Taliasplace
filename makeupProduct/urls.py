from django.urls import path
from .views import MakeupProductCreateView, MakeupProductDetailView, MakeupProductGetAllView, MakeupProductUpdateView, MakeupProductDeleteView, MakeupProductSingleView

urlpatterns = [

 path("products/", MakeupProductGetAllView.as_view(), name="product-list-all"),
 path("create-products/", MakeupProductCreateView.as_view(), name="product-detail"),
 path("update-products/", MakeupProductUpdateView.as_view(), name="product-update"),
 path("delete-products/", MakeupProductDeleteView.as_view(), name="product-delete"),
 path("single-products/", MakeupProductSingleView.as_view(), name="product-single")
]