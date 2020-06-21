from django import forms
from post.models import Post, Comment

class PostForm(forms.ModelForm):
    image = forms.ImageField(
        label="圖片"
    )
    body = forms.CharField(
        label="內容",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Post
        fields = ('body', 'image')

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        label="評論",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Comment
        fields = ('body',)
