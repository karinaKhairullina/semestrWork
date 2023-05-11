from django import forms
from .models import ClothingItem, Subcategory


class ClothingItemForm(forms.ModelForm):
    image = forms.ImageField(label='Изображение')
    description = forms.CharField(label='Описание', widget=forms.Textarea)

    class Meta:
        model = ClothingItem
        fields = ['image', 'category', 'subcategory', 'description']
        labels = {
            'category': 'Категория',
            'subcategory': 'Подкатегория',
        }
        widgets = {
            'subcategory': forms.Select(attrs={'disabled': 'disabled'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].required = True
        self.fields['category'].widget.attrs.update({'onchange': 'this.form.submit();'})
        if self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')
        else:
            self.fields['subcategory'].queryset = Subcategory.objects.none()
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')
                self.fields['subcategory'].widget.attrs.pop('disabled')
            except(ValueError, TypeError):
                pass








