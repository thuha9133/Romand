from django.contrib import admin

# Register your models here.

from .models import  SanPham, KhachHang, DonHang, ChiTietDonHang, TaiKhoan, LoaiHang
@admin.register(KhachHang)
class KhachHangAdmin(admin.ModelAdmin):
    list_display = ['ma_kh', 'ten_kh', 'email','mat_khau', 'so_dien_thoai', 'dia_chi']
@admin.register(TaiKhoan)
class TaiKhoanAdmin(admin.ModelAdmin):
    list_display = ['ma_tk','tenTK', 'matKhau', 'hoTen', 'email']

@admin.register(SanPham)
class SanPhamAdmin(admin.ModelAdmin):
    list_display = ['ma_sp', 'ten_san_pham', 'ten_loai','mo_ta', 'gia', 'so_luong']

class ChiTietDonHangInline(admin.TabularInline):
    model = ChiTietDonHang
    extra = 1

@admin.register(DonHang)
class DonHangAdmin(admin.ModelAdmin):
    list_display = ['ma_dh', 'khach_hang', 'ngay_dat']
    inlines = [ChiTietDonHangInline]
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return super().has_delete_permission(request, obj)


@admin.register(LoaiHang)
class LoaiHangAdmin(admin.ModelAdmin):
    list_display = ['ma_loai', 'ten_loai']
    search_fields = ['ten_loai']