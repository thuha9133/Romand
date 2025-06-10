from django.urls import path
from . import views

urlpatterns = [
    path('sanpham/', views.sanpham, name='sanpham'),
    path('', views.index, name='index'), # Trang chủ
    path('gioithieu/', views.gioithieu, name='gioithieu'), # Giới thiệu
    path('san-pham/<str:ma_sp>/', views.chitiet_sanpham, name='chitiet_sanpham'),
    path('tim-kiem/', views.tim_kiem_san_pham, name='tim_kiem_san_pham'),
    path('lienhe/', views.lienhe, name='lienhe'), # Liên hệ
    path('register/', views.register, name='register'), # Đăng ký
    path('login/', views.login, name='login'), # Đăng nhập
    path('profile/', views.profile, name='profile'), # Thông tin người dùng
    path('cart/', views.cart, name='cart'),
    path('them-vao-gio/<int:id>/', views.them_vao_gio, name='them_vao_gio'),
    path('giohang/thanhtoan/', views.thanhtoan, name='thanhtoan'),
    path('yeuthich/', views.yeuthich, name='yeuthich'),
    path('qa/', views.qa, name='qa'),
    path('profile/', views.yeuthich, name='profile'),
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout, name='logout'),
    path('profile/delete-account/', views.delete_account, name='delete_account'),
    path('them-gio-hang/', views.them_gio_hang, name='them_gio_hang'),
    path('giohang/', views.giohang, name='giohang'),
    path('lich-su-don-hang/', views.lich_su_don_hang, name='lich_su_don_hang'),
    path('don-hang/<str:ma_dh>/', views.chi_tiet_don_hang, name='chi_tiet_don_hang'),
    
]
