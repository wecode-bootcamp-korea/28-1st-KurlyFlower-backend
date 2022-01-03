from django.http.response   import HttpResponseNotFound, JsonResponse
from django.views           import View
from django.db.models       import Q

from products.models import Category, Product

class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        result = [
            {
                "id"           : category.id,
                "name"         : category.name,
                "subcategories": [sub for sub in category.subcategory_set.values()]
            }
            for category in categories
        ]
        return JsonResponse({"result":result}, status=200)

class ProductListView(View):
    def get(self, request):
        category_id    = request.GET.get("category_id")
        subcategory_id = request.GET.get("subcategory_id")
        offset         = request.GET.get("offset", 0)
        limit          = request.GET.get("limit", 20)

        q = Q()

        if category_id:
            q &= Q(category_id=category_id)
        if subcategory_id:
            q &= Q(subcategory_id=subcategory_id)

        products = Product.objects.order_by('id').filter(q)[int(offset):int(offset)+int(limit)]

        result = {
            "total": products.count(),
            "data":[
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
        }
        return JsonResponse({"result": result}, status=200)

class CollectionView(View):
    def get(self, request, collection_id):
        COLLECTION_CODE = {
            1: ("놓칠 수 없는 최저가", "최저가 할인만 모음", "price"),
            2: ("인기 신상품 랭킹", "가장 먼저 만나보는 인기 신상품", "-created_at"),
            3: ("지금 가장 핫한 상품", "재구매율 높은 상품", "-sales_quantity"),
            4: ("프리미엄 상품 대전", "컬리플라워가 추천하는 프리미엄 상품", "-price"),
        }

        title    = COLLECTION_CODE.get(collection_id)[0]
        subtitle = COLLECTION_CODE.get(collection_id)[1]
        sorting  = COLLECTION_CODE.get(collection_id)[2]

        offset = request.GET.get("offset", 0)
        limit  = request.GET.get("limit", 20)

        products = Product.objects.order_by(sorting)[int(offset):int(offset)+int(limit)].values(
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
            "total"        : products.count(),
            "title"        : title,
            "subtitle"     : subtitle,
            "products"     : [product for product in products]
        }

        return JsonResponse({"result": result}, status=200)
