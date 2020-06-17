from django import forms
from image.models import Image

class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="圖片"
    )
    description = forms.CharField(
        label="內容",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Image
        fields = ('description', 'image')
        