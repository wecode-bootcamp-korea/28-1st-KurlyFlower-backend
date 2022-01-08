import json
from json.decoder import JSONDecodeError

from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from django.views import View
from django.db.models import Q
from django.utils.decorators import method_decorator

from products.models import Category, Product
from users.models import Cart
from users.decorators import login_required


class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        result = [
            {
                "id": category.id,
                "name": category.name,
                "subcategories": [sub for sub in category.subcategory_set.values()],
            }
            for category in categories
        ]
        return JsonResponse({"result": result}, status=200)


class ProductListView(View):
    def get(self, request):
        category_id = request.GET.get("category_id")
        subcategory_id = request.GET.get("subcategory_id")
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 20))
        sorting = request.GET.get("sort", "추천순")

        sort = {
            "낮은가격순": "price",
            "신상품순": "-created_at",
            "판매량순": "-sales_quantity",
            "높은가격순": "-price",
            "추천순": "id",
        }

        q = Q()

        if category_id:
            q &= Q(category_id=category_id)
        if subcategory_id:
            q &= Q(subcategory_id=subcategory_id)

        products = Product.objects.filter(q).order_by(sort[sorting])[
            offset : offset + limit
        ]

        result = {
            "total": products.count(),
            "data": [
                {
                    "id": product.id,
                    "category_id": product.category_id,
                    "subcategory_id": product.subcategory_id,
                    "name": product.name,
                    "description": product.description,
                    "price": int(product.price),
                    "thumbnail_url": product.thumbnail_url,
                    "sales_quantity": product.sales_quantity,
                }
                for product in products
            ],
        }
        return JsonResponse({"result": result}, status=200)


class CollectionView(View):
    def get(self, request, collection_id):
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 20))

        COLLECTION_CODE = {
            1: {
                "title": "놓칠 수 없는 최저가",
                "subtitle": "최저가 할인만 모음",
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

        title = COLLECTION_CODE.get(collection_id)["title"]
        subtitle = COLLECTION_CODE.get(collection_id)["subtitle"]
        sorting = COLLECTION_CODE.get(collection_id)["sorting"]

        products = Product.objects.order_by(sorting)[offset : offset + limit]

        result = {
            "collection_id": collection_id,
            "total": products.count(),
            "title": title,
            "subtitle": subtitle,
            "data": [
                {
                    "id": product.id,
                    "category_id": product.category_id,
                    "subcategory_id": product.subcategory_id,
                    "name": product.name,
                    "description": product.description,
                    "price": int(product.price),
                    "thumbnail_url": product.thumbnail_url,
                    "sales_quantity": product.sales_quantity,
                }
                for product in products
            ],
        }

        return JsonResponse({"result": result}, status=200)


class ProductDetailView(View):
    def get(self, request, product_id):

        try:
            product = Product.objects.get(id=product_id)
            images = product.image_set.all()

            data = {
                "name": product.name,
                "description": product.description,
                "price": int(product.price),
                "units": product.units,
                "weights": product.weights,
                "shipping_type": product.shipping_type,
                "origin": product.origin,
                "packaging": product.packaging.first().name,
                "detail_images": [image.url for image in images],
                "thumbnail_url": product.thumbnail_url,
            }
            return JsonResponse({"product_detail": data}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"message": "Product_DoesNotExist"}, status=404)


class CartView(View):
    @login_required
    def get(self, request):
        try:
            items = Cart.objects.filter(user_id=request.user.id)

            results = [
                {
                    "product_id": item.product.id,
                    "name": item.product.name,
                    "price": item.product.price,
                    "quantity": item.quantity,
                    "packaging": item.product.packaging.first().name,
                    "address": request.user.address,
                    "thumbnail_url": item.product.thumbnail_url,
                }
                for item in items
            ]

            return JsonResponse({"result": results}, status=200)

        except Cart.DoesNotExist:
            return JsonResponse({"message": "Cart_DoesNotExist"}, status=404)

    def post_input_validator(self, quantity):
        if quantity <= 0:
            raise ValidationError("INVALID_QUANTITY")

    def patch_input_validator(self, quantity):
        SIGNIFICANT_FIGURES = (-1, 1)
        if quantity not in SIGNIFICANT_FIGURES:
            raise ValidationError("INVALID_QUANTITY")

    @login_required
    def post(self, request):
        try:
            data = json.loads(request.body)

            product_id = data["product_id"]
            quantity = data["quantity"]

            self.post_input_validator(quantity)

            product = Product.objects.get(id=product_id)

            item, is_created = Cart.objects.get_or_create(
                user=request.user, product=product, defaults={"quantity": quantity}
            )

            if not is_created:  # 장바구니에 이미 상품이 담겨있는 경우
                item.quantity += quantity
                item.save()

            result = {"product_id": item.product_id, "quantity": item.quantity}

            http_status_code = 201 if is_created else 200

            return JsonResponse({"result": result}, status=http_status_code)

        except JSONDecodeError:
            return JsonResponse({"message": "INVALID_JSON"}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"message": "PRODUCT_DOES_NOT_EXIST"}, status=400)

    @login_required
    def patch(self, request):
        try:
            data = json.loads(request.body)

            product_id = data["product_id"]
            quantity = data["quantity"]

            self.patch_input_validator(quantity)

            product = Product.objects.get(id=product_id)
            item = Cart.objects.get(product_id=product.id, user=request.user)

            if item.quantity == 1 and quantity == -1:
                return JsonResponse({"message": "NO_CHANGE"}, status=200)

            item.quantity += quantity
            item.save()

            result = {"product_id": item.product_id, "quantity": item.quantity}

            return JsonResponse({"result": result}, status=200)

        except JSONDecodeError:
            return JsonResponse({"message": "INVALID_JSON"}, status=400)

        except ValidationError as e:
            return JsonResponse({"message": e.message}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"message": "INVALID_PRODUCT"}, status=400)

        except Cart.DoesNotExist:
            return JsonResponse({"message": "ITEM_DOES_NOT_EXIST"}, status=400)

    @login_required
    def delete(self, request):
        try:
            data = json.loads(request.body)
            product_id_list = data["product_id_list"]

            cart_items = Cart.objects.filter(product__id__in=product_id_list)

            result = [
                {
                    "deleted_id": item.product_id,
                    "deleted_quantity": item.quantity,
                }
                for item in cart_items
            ]

            cart_items.delete()

            return JsonResponse({"result": result}, status=200)

        except JSONDecodeError:
            return JsonResponse({"message": "INVALID_JSON"}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"message": "PRODUCT_DOES_NOT_EXIST"}, status=400)
