from django.http.response   import JsonResponse
from django.views           import View
from django.db.models       import Q

from products.models import Category, Product, Packaging

class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        result = [{
            "id"           : category.id,
            "name"         : category.name,
            "subcategories": [sub for sub in category.subcategory_set.values()]
        } for category in categories]
        return JsonResponse({"result":result}, status=200)

class ProductListView(View):
    def get(self, request):
        category_id    = request.GET.get("category_id")
        subcategory_id = request.GET.get("subcategory_id")
        offset         = int(request.GET.get("offset", 0))
        limit          = int(request.GET.get("limit", 20))
        sorting        = request.GET.get("sort", "추천순")

        sort = {
            "낮은가격순":"price",
            "신상품순":"-created_at",
            "판매량순":"-sales_quantity",
            "높은가격순":"-price",
            "추천순": "id",
        }

        q = Q()

        if category_id:
            q &= Q(category_id=category_id)
        if subcategory_id:
            q &= Q(subcategory_id=subcategory_id)

        products = Product.objects.filter(q).order_by(sort[sorting])[offset:offset+limit]

        result = {
            "total": products.count(),
            "data":[{
                "id"            : product.id,
                "category_id"   : product.category_id,
                "subcategory_id": product.subcategory_id,
                "name"          : product.name,
                "description"   : product.description,
                "price"         : int(product.price),
                "thumbnail_url" : product.thumbnail_url,
                "sales_quantity": product.sales_quantity
            } for product in products]
        }
        return JsonResponse({"result": result}, status=200)

class CollectionView(View):
    def get(self, request, collection_id):
        offset = int(request.GET.get("offset", 0))
        limit  = int(request.GET.get("limit", 20))

        COLLECTION_CODE = {
            1: {
                "title": "놓칠 수 없는 최저가",
                "subtitle":"최저가 할인만 모음",
                "sorting": "price",
            },
            2: {
                "title": "인기 신상품 랭킹",
                "subtitle": "가장 먼저 만나보는 인기 신상품",
                "sorting": "-created_at",
            },
            3: {
                "title": "지금 가장 핫한 상품",
                "subtitle": "재구매율 높은 상품",
                "sorting": "-sales_quantity",

            },
            4: {
                "title": "프리미엄 상품 대전",
                "subtitle": "컬리플라워가 추천하는 프리미엄 상품",
                "sorting": "-price",
            },
        }

        title    = COLLECTION_CODE.get(collection_id)["title"]
        subtitle = COLLECTION_CODE.get(collection_id)["subtitle"]
        sorting  = COLLECTION_CODE.get(collection_id)["sorting"]

        products = Product.objects.order_by(sorting)[offset:offset+limit]

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

class ProductDetailView(View):
    def get(self, request, product_id):

        try:
            product   = Product.objects.get(id=product_id)
            images    = product.image_set.all()

            data = {
                "name"          : product.name,
                "description"   : product.description,
                "price"         : int(product.price),
                "units"         : product.units,
                "weights"       : product.weights,
                "shipping_type" : product.shipping_type,
                "origin"        : product.origin,
                "packaging"     : product.packaging.first().name,
                "detail_images" : [image.url for image in images],
                "thumbnail_url" : product.thumbnail_url
            }
            return JsonResponse({"product_detail":data}, status = 200)

        except Product.DoesNotExist:
            return JsonResponse({"message":"Product_DoesNotExist"}, status=404)
