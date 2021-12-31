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

class CollectionView(View):
    def get(self, request, collection_id):
        offset = request.GET.get('offset')
        limit  = request.GET.get('limit')

        COLLECTION_CODE = {
            1: ("놓칠 수 없는 최저가", "최저가 할인만 모음"),
            2: ("인기 신상품 랭킹", "가장 먼저 만나보는 인기 신상품"),
            3: ("지금 가장 핫한 상품", "재구매율 높은 상품"),
            4: ("프리미엄 상품 대전", "컬리플라워가 추천하는 프리미엄 상품"),
        }
        if collection_id == 1:
            query = Product.objects.order_by("price","id")
        elif collection_id == 2:
            query = Product.objects.order_by("-created_at","id")
        elif collection_id == 3:
            query = Product.objects.order_by("-sales_quantity","id")
        else:
            query = Product.objects.order_by("-price","id")

        title    = COLLECTION_CODE.get(collection_id)[0]
        subtitle = COLLECTION_CODE.get(collection_id)[1]

        products = query[offset:limit].values(
            "id",
            "category_id",
            "subcategory_id",
            "name",
            "description",
            "price",
            "thumbnail_url",
            "sales_quantity"
        )

        result = {
            "collection_id": collection_id,
            "title"        : title,
            "subtitle"     : subtitle,
            "products"     : [product for product in products]
        }

        return JsonResponse({"result": result}, status=200)
