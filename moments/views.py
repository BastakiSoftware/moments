from django.db.models import Q
from itertools import chain
from .models import TextPost, ImagePost, VideoPost, VoicePost, Comment
from django.views.generic import DetailView, ListView, CreateView
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import (
    TextPostForm,
    ImagePostForm,
    VideoPostForm,
    VoicePostForm,
    CommentForm,
)
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
        post = self.get_object()  # Get the post object

        # Get comments using the correct Generic Foreign Key lookup
        content_type = ContentType.objects.get_for_model(post)
        context["comments"] = Comment.objects.filter(
            content_type=content_type, object_id=post.pk
        )
        context["comment_form"] = CommentForm()
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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        # Get the post type and ID from the URL and store them
        self.post_type = self.kwargs["post_type"]
        self.post_id = self.kwargs["post_id"]

        # Pre-fetch the content type to avoid repeated lookups
        self.content_type = ContentType.objects.get_for_model(
            {
                "text": TextPost,
                "image": ImagePost,
                "video": VideoPost,
                "voice": VoicePost,
            }[self.post_type]
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user  # Use 'author' not 'user'
        form.instance.object_id = self.post_id
        form.instance.content_type = self.content_type
        return super().form_valid(form)

    def get_success_url(self):
        # Correctly reverse the URL using post_type and post_id
        return reverse(
            "post_detail",
            kwargs={"post_type": self.post_type, "pk": self.post_id},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add post_type and post_id to the form's hidden input fields
        context["post_type"] = self.post_type
        context["post_id"] = self.post_id
        return context
