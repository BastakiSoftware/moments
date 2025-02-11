from django import forms
from .models import TextPost, ImagePost, VideoPost, VoicePost, Comment


class BasePostForm(forms.ModelForm):
    """
    Base form for all post types with common fields
    """

    class Meta:
        abstract = True
        fields = ["title", "content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Write your post content..."}
            ),
            "title": forms.TextInput(attrs={"placeholder": "Enter title"}),
        }


class TextPostForm(BasePostForm):
    """
    Form for text-only posts
    """

    class Meta(BasePostForm.Meta):
        model = TextPost
        fields = BasePostForm.Meta.fields  # Using same fields as base form


class ImagePostForm(BasePostForm):
    """
    Form for image posts
    """

    class Meta(BasePostForm.Meta):
        model = ImagePost
        fields = BasePostForm.Meta.fields + ["image", "caption"]
        widgets = {
            **BasePostForm.Meta.widgets,
            "caption": forms.TextInput(
                attrs={"placeholder": "Add a caption for your image"}
            ),
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            # Add image validation if needed
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
        return image


class VideoPostForm(BasePostForm):
    """
    Form for video posts
    """

    class Meta(BasePostForm.Meta):
        model = VideoPost
        fields = BasePostForm.Meta.fields + ["video", "thumbnail"]
        widgets = {
            **BasePostForm.Meta.widgets,
            "thumbnail": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }

    def clean_video(self):
        video = self.cleaned_data.get("video")
        if video:
            # Add video validation if needed
            if video.size > 50 * 1024 * 1024:  # 50MB limit
                raise forms.ValidationError("Video file too large ( > 50MB )")
        return video


class VoicePostForm(BasePostForm):
    """
    Form for voice posts
    """

    class Meta(BasePostForm.Meta):
        model = VoicePost
        fields = BasePostForm.Meta.fields + ["audio"]

    def clean_audio(self):
        audio = self.cleaned_data.get("audio")
        if audio:
            # Add audio validation if needed
            if audio.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError("Audio file too large ( > 10MB )")
        return audio


class CommentForm(forms.ModelForm):
    """
    Form for comments
    """

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Write a comment...",
                    "class": "form-control",
                }
            )
        }
