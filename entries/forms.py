from django import forms
from .models import Entry, Tag

class EntryForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Entry
        fields = ['title', 'content', 'tags', 'image', 'is_private']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError("Заголовок должен быть не короче 3 символов")
        return title
