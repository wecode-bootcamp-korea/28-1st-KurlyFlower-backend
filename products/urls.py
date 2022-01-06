from django.urls import path

from products.views import CategoryView, CollectionView, ProductListView, ProductDetailView, CartView

urlpatterns = [
    path("/categories", CategoryView.as_view()),
    path("", ProductListView.as_view()),
    path("/collection/<int:collection_id>", CollectionView.as_view()),
    path("/<int:product_id>", ProductDetailView.as_view()),
    path("/cart", CartView.as_view()),
]
