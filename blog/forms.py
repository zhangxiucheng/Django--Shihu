from django import forms
from .models import Post, Answer
from mdeditor.fields import MDTextFormField


class ArticlePostForm(forms.Form):
    title = forms.CharField()
    body = MDTextFormField()
    category = forms.ChoiceField()
    tags = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        # 执行父类构造方法
        super(ArticlePostForm, self).__init__(*args, **kwargs)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'tags')


class AnswerForm(forms.Form):
    title = forms.CharField()
    body = MDTextFormField()
    tags = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        # 执行父类构造方法
        super(AnswerForm, self).__init__(*args, **kwargs)


class AnswerPostForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('title', 'body', 'tags')
