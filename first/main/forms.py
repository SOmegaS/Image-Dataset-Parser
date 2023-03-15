from django import forms


class PostForm(forms.Form):
    list_of_names = forms.CharField(label="Список классов изображений")
    count_image = forms.IntegerField(label="Количество изображений")
