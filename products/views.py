from django.http.response import JsonResponse
from django.views import View

from products.models import Category, Product

class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()

        result = []
        for category in categories:
            subcategories = category.subcategory_set.filter(category_id=category.id).values()
            result.append(
                {
                    "id"           : category.id,
                    "name"         : category.name,
                    "subcategories": [sub for sub in subcategories]
                }
            )
        return JsonResponse({"result":result}, status=200)

class ProductListView(View):
    def get(self, request):
        query = Product.objects.order_by("id")

        category_id    = request.GET.get("category_id")
        subcategory_id = request.GET.get("subcategory_id")

        if category_id:
            category_id = int(category_id)
            query = query.filter(category_id=category_id)
        if category_id and subcategory_id:
            category_id = int(category_id)
            subcategory_id = int(subcategory_id)
            query = query.filter(category_id=category_id, subcategory_id=subcategory_id)

        products = query[:20]

        result = [
            {
                "id"            : product.id,
                "category_id"   : product.category_id,
                "subcategory_id": product.subcategory_id,
                "name"          : product.name,
                "description"   : product.description,
                "price"         : product.price,
                "thumbnail_url" : product.thumbnail_url
            }
            for product in products
        ]
        return JsonResponse({"result": result}, status=200)
