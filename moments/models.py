from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class BasePost(models.Model):
    """
    Abstract base class for all types of posts
    """

    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)ss",  # This will create different related names for each subclass
    )
    likes = models.ManyToManyField(User, related_name="liked_%(class)ss", blank=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    @property
    def post_type(self):
        return self._meta.model_name


class TextPost(BasePost):
    """
    Model for text-only posts
    """

    class Meta:
        verbose_name = _("Text Post")
        verbose_name_plural = _("Text Posts")


class ImagePost(BasePost):
    """
    Model for posts with images
    """

    image = models.ImageField(upload_to="posts/images/")
    caption = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = _("Image Post")
        verbose_name_plural = _("Image Posts")


class VideoPost(BasePost):
    """
    Model for posts with videos
    """

    video = models.FileField(upload_to="posts/videos/")
    thumbnail = models.ImageField(upload_to="posts/thumbnails/", blank=True)
    duration = models.DurationField(null=True, blank=True)

    class Meta:
        verbose_name = _("Video Post")
        verbose_name_plural = _("Video Posts")


class VoicePost(BasePost):
    """
    Model for posts with voice recordings
    """

    audio = models.FileField(upload_to="posts/audio/")
    duration = models.DurationField(null=True, blank=True)

    class Meta:
        verbose_name = _("Voice Post")
        verbose_name_plural = _("Voice Posts")


class Comment(models.Model):
    """
    Model for comments on posts
    """

    # Generic foreign key to allow comments on any post type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    post = GenericForeignKey("content_type", "object_id")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"
