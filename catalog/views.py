from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from .models import (
    Item, OrderItem, Order,Address,Category,ProductReview)
from .forms import AddressForm,ReviewForm
class HomeView(ListView):
    # model=Item
    # template_name='index.html'

    def get(self, *args, **kwargs):
        categories = Category.objects.all()[0:3]
        item=Item.objects.all()[0:3]
        shirts = Item.objects.filter(status="NEW")
        # new_products = Item.objects.filter(category__name="New Products")
        context = {
            'categories': categories,
            'product':item,
            'shirts': shirts,
            # 'new_products': new_products
        }
        return render(self.request, 'index.html', context)

# class ProductDetail(DetailView):
#     model=Item
#     template_name='product.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'items': Item.objects.all().order_by('id')[0:3],
#             'review':ProductReview.objects.all()[0:3],
#         })
#         return context
#     def get(self, *args, **kwargs):

def ProductDetail(request, slug):
    items = get_object_or_404(Item, slug=slug)
    review=ProductReview.objects.filter(item=items.id)
    context={
        'object':items,
        'items': Item.objects.all().order_by('id')[0:3],
        'review':review
    }

    return render(request,'product.html',context)


def addProductReview(request, slug):
    items = get_object_or_404(Item, slug=slug)
    review=ProductReview.objects.filter(item=items.id)
    form = ReviewForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name=form.cleaned_data.get('name')
            message=form.cleaned_data.get('message')
            email=form.cleaned_data.get('email')
            ratting=form.cleaned_data.get('ratting')
        productReview=ProductReview(item=items,email=email,name=name,message=message,ratting=ratting)
        productReview.save()
        form = ReviewForm()
    context={
        'object':items,
        'items': Item.objects.all().order_by('id')[0:3],
        'review':review
    }
    return HttpResponseRedirect(reverse('add_productReview_success', args=(slug,)))
    # return render(request,'product.html',context)

def home(request):
    return render(request,'index.html')


def checkout(request):
    return render(request,'checkout.html')


def product(request):
    return render(request,'product.html')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            # address = Address.objects.get(user=self.request.user,default=True)
            form = AddressForm()
            context={
                'form':form,
                # 'address':address,
                'order': order,
            }
            return render(self.request,'checkout.html',context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You don't have an active order")
            return redirect('order_summary')
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = AddressForm(self.request.POST or None)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            use_default = form.cleaned_data.get('use_default')
            payment_option=form.cleaned_data.get('payment_option')
            save_info = form.cleaned_data.get('save_info')
            address = Address(
                user=self.request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                zip=zip,
                use_default=use_default,
                payment_option=payment_option,
                save_info=save_info
            )
            address.save()
            # order.address = address
            # order.save()

            if save_info:
                address.default = True
                address.save()
            order.address = address
            order.save()

            use_default = form.cleaned_data.get('use_default')
            if use_default:
                address_qs = Address.objects.get(user=self.request.user,default=True)
                if address_qs.exists():
                    address = address_qs[0]
                    order.address = address
                    order.save()
            return redirect('checkout')
        else :
            return redirect('checkout')



@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, f"{item}'s quantity was updated")
            return redirect('order_summary')
        else:
            order.items.add(order_item)
            messages.success(request, f"{item} was added to your cart")
            return redirect('product',slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered=False , ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, f"{item} was added to your cart")
        return redirect('product',slug=slug)


@login_required
def remove_single_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
                order.save()
            messages.success(request, f"{item}'s quantity was updated!")
            return redirect('order_summary')

        else:
            messages.success(request, f"{item} was not in your cart")
            return redirect('detail', slug=slug)
    else:
        messages.success(request, "You do not have an active order")
        return redirect('detail', slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]

            order.items.remove(order_item)
            order_item.delete()
            messages.success(request, f"{item} was removed from your cart!")
            return redirect('order_summary')

        else:
            messages.success(request, f"{item} was not in your cart")
            return redirect('order_summary')
    else:
        messages.success(request, "You do not have an active order")
        return redirect('order_summary')


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context={
            'order':order
        }
        return render(self.request,'order_summary.html',context)


# class login_user(View):
#     def get(self, *args, **kwargs):
#         context={
#         }
#         return render(self.request,'account/login.html',context)
