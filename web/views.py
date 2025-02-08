from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from moments.models import TextPost, ImagePost, VideoPost, VoicePost
from itertools import chain

# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Home page view that displays recent posts and user activity
    """

    template_name = "web/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get recent posts from all types
        text_posts = TextPost.objects.select_related("author").all()[:5]
        image_posts = ImagePost.objects.select_related("author").all()[:5]
        video_posts = VideoPost.objects.select_related("author").all()[:5]
        voice_posts = VoicePost.objects.select_related("author").all()[:5]

        # Combine and sort all posts
        recent_posts = sorted(
            chain(text_posts, image_posts, video_posts, voice_posts),
            key=lambda post: post.created_at,
            reverse=True,
        )[
            :10
        ]  # Get top 10 most recent posts

        context["recent_posts"] = recent_posts
        context["post_types"] = [
            {"type": "text", "name": "Text Post", "icon": "fas fa-file-alt"},
            {"type": "image", "name": "Image Post", "icon": "fas fa-image"},
            {"type": "video", "name": "Video Post", "icon": "fas fa-video"},
            {"type": "voice", "name": "Voice Post", "icon": "fas fa-microphone"},
        ]
        return context
