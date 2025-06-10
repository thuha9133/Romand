from django.urls import path
from . import views
from .views import create_order
urlpatterns = [    
    path('sanpham/', views.sanpham_list, name='sanpham_list'),
    path('quantri/sanpham/them/', views.them_san_pham, name='them_san_pham'),
    path('quantri/sanpham/sua/<str:ma_sp>/', views.sua_san_pham, name='sua_san_pham'),
    path('quantri/sanpham/xoa/<str:ma_sp>/', views.xoa_san_pham, name='xoa_san_pham'),
    path('', views.trang_chu, name='trang_chu'),
    path('khachhang/', views.khachhang_list, name='khachhang_list'),
    path('register/', views.register_staff, name='register_staff'),
    path('login/', views.login_staff, name='login_staff'),


    path('logout/', views.logout_staff, name='logout_staff'),
    path('loaihang/', views.loaihang_list, name='loaihang_list'),
    path('loaihang/<str:ma_loai>/', views.loaihang_detail, name='loaihang_detail'),
    path('taikhoan/', views.taikhoan_list, name='taikhoan_list'),

    path('donhang/', views.donhang_list, name='donhang_list'),
    path('donhang/<str:ma_dh>/capnhattrangthai/', views.cap_nhat_trang_thai, name='cap_nhat_trang_thai'),
    path('quantri/donhang/xoa/<str:ma_dh>/', views.xoa_donhang, name='xoa_donhang'),
    path('donhang/<str:ma_dh>/', views.chi_tiet_don_hang, name='ct_don_hang'),

    
    path('quantri/taikhoan/sua/<str:id>/', views.sua_taikhoan, name='sua_taikhoan'),
    path('quantri/taikhoan/xoa/<str:id>/', views.xoa_taikhoan, name='xoa_taikhoan'),
    
    path('quantri/khachhang/xoa/<str:ma_kh>/', views.xoa_khachhang, name='xoa_khachhang'),
    path('quantri/loaihang/them/', views.them_loaihang, name='them_loaihang'),
    path('quantri/loaihang/sua/<str:ma_loai>/', views.sua_loaihang, name='sua_loaihang'),
    path('quantri/loaihang/xoa/<str:ma_loai>/', views.xoa_loaihang, name='xoa_loaihang'),
    path('order/create/', create_order, name='create_order'),
    path('thongke/doanhthu/', views.thongke_doanhthu, name='thongke_doanhthu'),
    path('thongke/sanphambanchay/', views.thongke_sanphambanchay, name='thongke_sanphambanchay'),
    path('thongke/tonkho/', views.thongke_tonkho, name='thongke_tonkho')
]
