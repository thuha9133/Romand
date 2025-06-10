from django import forms
from .models import KhachHang, DonHang

class FormKhachHang(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = ['ma_kh','ten_kh', 'email','mat_khau', 'so_dien_thoai', 'dia_chi']

class FormDonHang(forms.ModelForm):
    class Meta:
        model = DonHang
        fields = ['ghi_chu']

