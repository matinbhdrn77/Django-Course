from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from datetime import date

from django.views.generic.base import View
from .models import *
from django.views.generic import ListView, DetailView
from .forms import CommentForm

# Create your views here.

# sorted_post = Post.objects.all().order_by("date")[0:3]


class StartingPageView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    ordering = ["-date"]

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class PostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    context_object_name = "all_posts"
    ordering = ["-date"]


# def posts(request):
#     return render(request, "blog/all-posts.html", {"all_posts": sorted_post})


class PostDetailView(View):
    def get_context(self, request, post):
        stored_post = request.session.get("stored_post")
        print(stored_post)
        print(post.id)
        if stored_post is not None:
            is_saved_for_later = post.id in stored_post
            print(is_saved_for_later)
        else:
            is_saved_for_later = False

        context = {
            "post": post,
            "post_tag": post.tags.all(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": is_saved_for_later
        }

        return context

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        
        context = self.get_context(request, post)
        context["comment_form"] =  CommentForm()

        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = get_object_or_404(Post, slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detial", args=[slug]))

        context = self.get_context(request, post) 
        context["comment_form"] = comment_form

        return render(request, "blog/post-detail.html", context)



# class PostDetailView(DetailView):
#     template_name = "blog/post-detail.html"
#     model = Post

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         form = CommentForm()
#         context["comment_form"] = form
#         context["post_tag"] = self.object.tags.all()
#         return context


def post_detail(request, slug):
    # identified_post = Post.objects.get(slug = slug)
    identified_post = get_object_or_404(Post, slug=slug)
    return render(
        request,
        "blog/post-detail.html",
        {"post": identified_post, "post_tag": identified_post.tags.all()},
    )


class ReadLaterView(View):
    def get(self, request):
        stored_post = request.session.get("stored_post")

        context = {}

        if stored_post is None or len(stored_post) == 0:
            context["posts"] = []
            context["has_post"] = False
        
        else:
            posts = Post.objects.filter(id__in=stored_post)
            context["posts"] = posts
            context["has_post"] = True
        
        return render(request, "blog/stored-post.html", context)


    def post(self, request):
        stored_post = request.session.get("stored_post")

        if stored_post is None:
            stored_post = []
        
        post_id = int(request.POST["post_id"])

        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)
        request.session["stored_post"] = stored_post

        return HttpResponseRedirect("/")