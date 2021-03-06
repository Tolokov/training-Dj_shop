from django.forms import Textarea, ModelForm, CharField

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from Blog.models import Comment, News


class AddCommentForm(ModelForm):
    """Добавление комментария к новости"""

    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {'text': Textarea(attrs={"id": "commentator", "placeholder": "Оставить комментарий ..."})}


class NewsAdminForm(ModelForm):
    """CKEditor"""
    description_ru = CharField(label="Описание [ru]", widget=CKEditorUploadingWidget())
    description_en = CharField(label="Description [en]", widget=CKEditorUploadingWidget())
    description_de = CharField(label="Beschreibung [de]", widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'

