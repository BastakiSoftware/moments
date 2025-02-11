from django.db.models import Q
from itertools import chain
from .models import TextPost, ImagePost, VideoPost, VoicePost
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import TextPostForm, ImagePostForm, VideoPostForm, VoicePostForm
from django.contrib.auth.mixins import LoginRequiredMixin


class PostDetailView(DetailView):
    """
    Generic view to display any type of post detail
    """

    template_name = "moments/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        # Get post type and ID from URL
        post_type = self.kwargs.get("post_type")
        post_id = self.kwargs.get("pk")

        # Map URL names to model classes
        post_types = {
            "text": TextPost,
            "image": ImagePost,
            "video": VideoPost,
            "voice": VoicePost,
        }

        # Get the appropriate model class
        model_class = post_types.get(post_type)
        if not model_class:
            raise Http404("Invalid post type")

        # Get the post object
        post = get_object_or_404(model_class, pk=post_id)
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get comments for the post
        content_type = ContentType.objects.get_for_model(self.object.__class__)
        # context["comments"] = self.object.comment_set.all()
        return context


def create_post(request, post_type):
    form_classes = {
        "text": TextPostForm,
        "image": ImagePostForm,
        "video": VideoPostForm,
        "voice": VoicePostForm,
    }

    FormClass = form_classes.get(post_type)
    if not FormClass:
        raise Http404("Invalid post type")

    if request.method == "POST":
        form = FormClass(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", post_type=post_type, pk=post.pk)
    else:
        form = FormClass()

    return render(request, "moments/post_form.html", {"form": form})


class PostListView(LoginRequiredMixin, ListView):
    """
    View to display all types of posts in a unified list
    """

    template_name = "moments/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        # Get all post types
        text_posts = TextPost.objects.select_related("author")
        image_posts = ImagePost.objects.select_related("author")
        video_posts = VideoPost.objects.select_related("author")
        voice_posts = VoicePost.objects.select_related("author")

        # Combine all posts and sort by creation date
        combined_posts = sorted(
            chain(text_posts, image_posts, video_posts, voice_posts),
            key=lambda post: post.created_at,
            reverse=True,
        )
        return combined_posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_types"] = [
            {"type": "text", "name": "Text Post"},
            {"type": "image", "name": "Image Post"},
            {"type": "video", "name": "Video Post"},
            {"type": "voice", "name": "Voice Post"},
        ]
        return context
