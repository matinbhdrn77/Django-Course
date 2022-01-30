from typing import List
from django.db import models
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, FormView
from .forms import ReviewForm
from .models import Review
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.urls import reverse

# Create your views here.


class ReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review.html"
    success_url = "/thank-you"


# class ReviewView(FormView):
#     form_class = ReviewForm
#     template_name = "reviews/review.html"
#     success_url = "/thank-you"

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

# class ReviewView(View):
#     def get(self, request):
#         form = ReviewForm()
#         return render(request, "reviews/review.html", {
#         "form": form
#     })

#     def post(self, request):
#         form = ReviewForm(request.POST)
#         if form.is_valid():

#             ### Simple Form ###
#             # review = Review(
#             #     user_name=form.cleaned_data["user_name"], review_text=form.cleaned_data["review_text"], rating=form.cleaned_data["rating"])
#             # review.save()

#             ### ModelForm ###
#             form.save()

#             return HttpResponseRedirect("/thank-you")

#         return render(request, "reviews/review.html", {
#         "form": form
#     })


# def review(request):

# if request.method == 'POST':
#     form = ReviewForm(request.POST)
#     if form.is_valid():

#         ### Simple Form ###
#         # review = Review(
#         #     user_name=form.cleaned_data["user_name"], review_text=form.cleaned_data["review_text"], rating=form.cleaned_data["rating"])
#         # review.save()

#         ### ModelForm ###
#         form.save()

#         return HttpResponseRedirect("/thank-you")

# else:
#     form = ReviewForm()

# return render(request, "reviews/review.html", {
#     "form": form
# })


def thank_you(request):
    return render(request, "reviews/thank-you.html")


class Thank_youView(TemplateView):
    template_name = "reviews/thank-you.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "This Work"
        return context


# class ReviewListView(TemplateView):
#     template_name = "reviews/review-list.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         reviews = Review.objects.all()
#         print(reviews)
#         context["reviews"] = reviews
#         return context


class ReviewListView(ListView):
    template_name = "reviews/review-list.html"
    model = Review
    context_object_name = "reviews"

    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query.filter(rating__gt=1)
        return data


# Auto matically fetch data (with id) and return single review
# use {{ review }} in html
class ReviewDetailView(DetailView):
    template_name = "reviews/detail-review.html"
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_review = self.object
        request = self.request
        favourite_id = request.session["favourite_reviews"]
        context["is_favourite"] = favourite_id == str(loaded_review.id)
        return context


class AddFavouriteView(View):
    def post(self, request):
        review_id = request.POST["review_id"]

        # we can't store object in session
        # request.session["favourite_reviews"] = fav_review
        # fav_review = Review.objects.get(pk=review_id)
        # we have to store int,string,bool or dictionart
        request.session["favourite_reviews"] = review_id

        return HttpResponseRedirect(reverse("review-detail", args=[review_id]))
        # return HttpResponseRedirect("/reviews/" + review_id)
