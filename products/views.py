from django.http.response import JsonResponse
from django.views import View

from products.models import Category

class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()

        result = []
        for category in categories:
            subcategories = category.subcategory_set.filter(category_id=category.id).values()
            result.append(
                {
                    "id": category.id,
                    "name": category.name,
                    "subcategories": [sub for sub in subcategories]
                }
            )
        return JsonResponse({"result":result}, status=200)
