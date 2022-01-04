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
        offset         = int(request.GET.get("offset", 0))
        limit          = int(request.GET.get("limit", 20))
        sorting        = request.GET.get("sort", "id")

        sort = {
            "낮은가격순":"price",
            "신상품순":"-created_at",
            "판매량순":"-sales_quantity",
            "높은가격순":"-price",
            "추천순": "-id"
        }

        q = Q()

        if category_id:
            q &= Q(category_id=category_id)
        if subcategory_id:
            q &= Q(subcategory_id=subcategory_id)

        products = Product.objects.order_by(sort[sorting]).filter(q)[offset:offset+limit]

        result = {
            "total": products.count(),
            "data":[
                {
                    "id"            : product.id,
                    "category_id"   : product.category_id,
                    "subcategory_id": product.subcategory_id,
                    "name"          : product.name,
                    "description"   : product.description,
                    "price"         : int(product.price),
                    "thumbnail_url" : product.thumbnail_url,
                    "sales_quantity": product.sales_quantity
                }
                for product in products
            ]
        }
        return JsonResponse({"result": result}, status=200)

class CollectionView(View):
    def get(self, request, collection_id):
        offset = int(request.GET.get("offset", 0))
        limit  = int(request.GET.get("limit", 20))

        COLLECTION_CODE = {
            1: ("놓칠 수 없는 최저가", "최저가 할인만 모음"),
            2: ("인기 신상품 랭킹", "가장 먼저 만나보는 인기 신상품"),
            3: ("지금 가장 핫한 상품", "재구매율 높은 상품"),
            4: ("프리미엄 상품 대전", "컬리플라워가 추천하는 프리미엄 상품"),
        }
        sort = {
            1: "price",
            2: "-created_at",
            3: "-sales_quantity",
            4: "-price"
        }

        title    = COLLECTION_CODE.get(collection_id)[0]
        subtitle = COLLECTION_CODE.get(collection_id)[1]

        products = Product.objects.order_by(sort[collection_id])[offset:offset+limit]

        result = {
            "collection_id": collection_id,
            "total"        : products.count(),
            "title"        : title,
            "subtitle"     : subtitle,
            "data"         : [
                {
                    "id"            : product.id,
                    "category_id"   : product.category_id,
                    "subcategory_id": product.subcategory_id,
                    "name"          : product.name,
                    "description"   : product.description,
                    "price"         : int(product.price),
                    "thumbnail_url" : product.thumbnail_url,
                    "sales_quantity": product.sales_quantity
                }
                for product in products
            ]
        }

        return JsonResponse({"result": result}, status=200)
