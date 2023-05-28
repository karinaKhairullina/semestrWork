from django import forms
from myClothes.models import Image
from subscribe.models import Post,Subscriber


class CreatePostForm(forms.ModelForm):
    """
    Форма для создания поста.
    """

    selected_images = forms.ModelMultipleChoiceField(
        queryset=Image.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Post
        fields = ['selected_images', 'title', 'text']


class CommentForm(forms.Form):
    """
    Форма для добавления комментария к посту.
    """

    post_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=forms.Textarea, label="Комментарий")


class SearchForm(forms.Form):
    """
    Форма для поиска постов по имени пользователя.
    """

    username = forms.CharField(max_length=30, label='Найти пользователя')

    class Meta:
        model = Post
        fields = ['username']



class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = [ 'email']