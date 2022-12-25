import datetime
from django.views import generic
from django.db.models import Q
from django.views.generic.edit import UpdateView

from product.models import Variant, ProductVariantPrice, ProductVariant


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    paginate_by = 10

    def get_queryset(self):
        filter_string = {}
        print(self.request.GET)
        if self.request.GET.get('price_from') and self.request.GET.get('price_to'):
            return ProductVariantPrice.objects.filter(
                price__range=(int(self.request.GET.get('price_from')), int(self.request.GET.get('price_to'))),
                product__title__icontains=self.request.GET.get('product__title__icontains')
            )
        elif self.request.GET.get('variant'):
            print("self.request.GET.get('variant')", self.request.GET.get('variant'))
            return ProductVariantPrice.objects.filter(
                Q(product_variant_one__variant_title=str(self.request.GET.get('variant'))) |
                Q(product_variant_two__variant_title=str(self.request.GET.get('variant'))) |
                Q(product_variant_three__variant_title=str(self.request.GET.get('variant')))
            )
        else:
            print("data else")
            for key in self.request.GET:
                if self.request.GET.get(key):
                    filter_string[key] = self.request.GET.get(key)
            return ProductVariantPrice.objects.filter(**filter_string)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = True
        context['product_variant_list'] = ProductVariant.objects.values('variant_title').distinct()
        context['request'] = ''
        if self.request.GET:
            context['request'] = self.request.GET['product__title__icontains']
            context['request'] = self.request.GET['created_at']
        return context


class UpdateProductView(UpdateView):
    model = ProductVariantPrice
    fields = [
        'product',
        'price',
        'stock',
        'product_variant_one',
        'product_variant_two',
        'product_variant_three',
    ]
    template_name = 'products/edit.html'
    success_url = "/product/list"
