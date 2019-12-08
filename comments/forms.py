from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        # 表明该表单对应的数据库模型为Comment
        model = Comment
        # 必须为fields 需要显示的字段
        fields = ['text']

