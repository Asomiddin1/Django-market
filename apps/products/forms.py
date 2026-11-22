from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Mahsulot yaratish va tahrirlash uchun ModelForm.
    """
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl bg-[#F4F4F6] border border-black/5 focus:border-[#8B5CF6] focus:bg-white focus:outline-hidden transition text-xs sm:text-sm font-medium',
                'placeholder': 'Mahsulot nomi (masalan, iPhone 15 Pro)'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl bg-[#F4F4F6] border border-black/5 focus:border-[#8B5CF6] focus:bg-white focus:outline-hidden transition text-xs sm:text-sm font-medium'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl bg-[#F4F4F6] border border-black/5 focus:border-[#8B5CF6] focus:bg-white focus:outline-hidden transition text-xs sm:text-sm font-medium',
                'placeholder': 'Narxi ($)',
                'step': '0.01'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl bg-[#F4F4F6] border border-black/5 focus:border-[#8B5CF6] focus:bg-white focus:outline-hidden transition text-xs sm:text-sm font-medium',
                'placeholder': 'Mavjud soni (dona)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-2xl bg-[#F4F4F6] border border-black/5 focus:border-[#8B5CF6] focus:bg-white focus:outline-hidden transition text-xs sm:text-sm font-medium',
                'placeholder': 'Mahsulot haqida batafsil ma’lumot...',
                'rows': 4
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full text-xs text-neutral-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-bold file:bg-[#8B5CF6] file:text-white hover:file:bg-[#7c4dff] file:cursor-pointer'
            }),
        }
        labels = {
            'name': 'Mahsulot nomi',
            'category': 'Kategoriya',
            'price': 'Narxi ($)',
            'stock': 'Ombordagi soni',
            'description': 'Tavsif',
            'image': 'Mahsulot rasmi',
        }
