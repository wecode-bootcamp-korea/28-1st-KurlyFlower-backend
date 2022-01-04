from django.urls import path

from products.views import CategoryView, CollectionView, ProductListView

urlpatterns = [
    path("/categories", CategoryView.as_view()),
    path("", ProductListView.as_view()),
    path("/collection/<int:collection_id>", CollectionView.as_view()),
]
