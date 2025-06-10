from django.db import models
from django.contrib.auth.models import User

# Create your models here.

import random
import string
#Tài khoản
class  TaiKhoan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    ma_tk = models.CharField(max_length=10, primary_key=True, unique=True, null=False, blank=False)
    tenTK =models.CharField(max_length=30)
    matKhau=models.CharField(max_length=50)
    hoTen=models.CharField(max_length=35)
    email=models.CharField(max_length=50)
    create_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.tenTK
class KhachHang(models.Model):
    tai_khoan = models.ForeignKey(TaiKhoan, on_delete=models.CASCADE, null=True, blank=True)
    ma_kh = models.CharField(max_length=10, unique=True, editable=False)
    ten_kh = models.CharField(max_length=100)
    # các trường còn lại ...

    email = models.EmailField(unique=True)
    mat_khau = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(max_length=15)
    dia_chi = models.TextField()

    def __str__(self):
        return f"{self.ma_kh} - {self.ten_kh}"

    def save(self, *args, **kwargs):
        if not self.ma_kh:
            self.ma_kh = self._generate_unique_ma_kh()
        super().save(*args, **kwargs)

    def _generate_unique_ma_kh(self):
        while True:
            new_ma = 'KH' + ''.join(random.choices(string.digits, k=6))
            if not KhachHang.objects.filter(ma_kh=new_ma).exists():
                return new_ma

# Sản phẩm mỹ phẩm
class SanPham(models.Model):
    ma_sp = models.CharField(max_length=20, null=False, blank=True, unique=True,)
    ten_san_pham = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    ten_loai = models.CharField(max_length=100, verbose_name="Tên loại", null=True, blank=True)
    mo_ta = models.TextField(verbose_name="Mô tả sản phẩm")
    gia = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá bán")
    so_luong = models.PositiveIntegerField(verbose_name="Số lượng trong kho")
    hinh_anh = models.ImageField(upload_to='img/', null=True, blank=True, verbose_name="Hình ảnh")
    def __str__(self):
        return self.ten_san_pham
    
#Loại hàng
class LoaiHang(models.Model):
    ma_loai = models.CharField(max_length=10, primary_key=True, verbose_name="Mã loại", unique=True, null=False, blank=False)
    ten_loai = models.CharField(max_length=100, verbose_name="Tên loại")
    mo_ta = models.TextField(blank=True, verbose_name="Mô tả")

    def __str__(self):
        return self.ten_loai
    

    


# Đơn hàng
class DonHang(models.Model):
    ma_dh = models.CharField(max_length=10, primary_key=True, unique=True, null=False, blank=False)
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE)
    ngay_dat = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt hàng")
    ghi_chu = models.TextField(blank=True, verbose_name="Ghi chú")
    tong_tien = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Tổng tiền")  # ✅ KHÔNG có dấu phẩy
 # <--- thêm dòng này
    phuong_thuc = models.CharField(max_length=20, choices=[('cod', 'Thanh toán khi nhận hàng'), ('bank', 'Chuyển khoản ngân hàng')], default='cod', verbose_name='Phương thức thanh toán')
    PHUONG_THUC_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng'),
        ('bank', 'Chuyển khoản ngân hàng'),
    ]
    TRANG_THAI_CHOICES = [
    ('cho_xu_ly', 'Chờ xử lý'),
    ('dang_giao', 'Đang giao'),
    ('da_giao', 'Đã giao'),
    ('da_bi_xoa', 'Đã bị xóa'),

    ]
    trang_thai = models.CharField(
        max_length=20,
        choices=TRANG_THAI_CHOICES,
        default='cho_xu_ly'
    )
    def __str__(self):
        return f"Đơn hàng #{self.ma_dh} - {self.khach_hang.ten_kh}"
    import random
import string

def generate_unique_ma_dh():
    while True:
        new_ma = 'DH' + ''.join(random.choices(string.digits, k=6))
        if not DonHang.objects.filter(ma_dh=new_ma).exists():
            return new_ma

# Chi tiết đơn hàng
class ChiTietDonHang(models.Model):
    don_hang = models.ForeignKey(DonHang, on_delete=models.CASCADE, related_name="chi_tiet", verbose_name="Đơn hàng")
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE, verbose_name="Sản phẩm")
    so_luong = models.PositiveIntegerField(verbose_name="Số lượng")

    def __str__(self):
        return f"{self.so_luong} x {self.san_pham.ten_san_pham}"
