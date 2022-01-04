from django.http      import JsonResponse
from django.views     import View
from products.models  import Product


class ProductDetailView(View):
    def get(self, request, product_id):

        try:
            product   = Product.objects.get(id=product_id)
            packaging = product.packaging.get(product=product_id)
            images    = product.image_set.all()
                        #product - 중간테이블(product_id, pakaging_id) - pakaging테이블
            data = {
                "name"          : product.name,
                "description"   : product.description,
                "price"         : int(product.price),
                "units"         : product.units,
                "weights"       : product.weights,
                "shipping_type" : product.shipping_type,
                "origin"        : product.origin,
                "packaging"     : packaging.name,
                "detail_images" : [image.url for image in images],
                "thumbnail_url" : product.thumbnail_url
            }
            return JsonResponse({"product_detail":data}, status = 201)

        except Product.DoesNotExist:
            return JsonResponse({"message":"Product_DoesNotExist"}, status=404)
