from django.urls import path

from .views import (
    MakeupProductCreateView,
    MakeupProductDeleteView,
    MakeupProductDetailView,
    MakeupProductGetAllView,
    MakeupProductSingleView,
    MakeupProductUpdateView,
)

urlpatterns = [
    path("products/", MakeupProductGetAllView.as_view(), name="product-list-all"),
    path("products/create/", MakeupProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/", MakeupProductSingleView.as_view(), name="product-single"),
    path("products/<int:pk>/detail/", MakeupProductDetailView.as_view(), name="product-detail"),
    path("products/<int:pk>/update/", MakeupProductUpdateView.as_view(), name="product-update"),
    path("products/<int:pk>/delete/", MakeupProductDeleteView.as_view(), name="product-delete"),
]