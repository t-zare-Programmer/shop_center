from itertools import product
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from apps.comment_scoring_favorites.forms import CommentForm
from apps.comment_scoring_favorites.models import Comment
from apps.products.models import Product
from django.db.models import Q
#___________________________________________________________________________________________________

class CommentView(View):
    def get(self, request, *args, **kwargs):
        productId = request.GET.get('productId')
        commentId = request.GET.get('commentId')
        slug = request.GET.get('slug')
        initial_dict = {'productId': productId, 'commentId': commentId}
        form = CommentForm(initial=initial_dict)
        return render(request,"csf_app/partials/create_comment.html", {'form': form,'slug':slug})

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            parent = None
            if (cd['comment_id']):
                parentId = cd['comment_id']
                parent = Comment.objects.get(id=parentId)

            Comment.objects.create(
                product=product,
                commenting_user=request.user,
                comment_text=cd['comment_text'],
                comment_parent=parent,
            )
            messages.success(request, "نظر شما با موفقیت ثبت شد")
            return redirect("products:product_details",product.slug)
        messages.error(request, "خطا در ارسال نظر",'danger')
        return redirect("products:product_details",product.slug)
