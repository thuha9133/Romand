
from django.shortcuts import render, get_object_or_404, redirect
from .models import SanPham, TaiKhoan, KhachHang, DonHang, LoaiHang
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import check_password, make_password
from .models import KhachHang  
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def logout(request):
    auth_logout(request)  # Gọi hàm logout chính xác của Django
    return redirect('login')
def xoa_donhang(request, ma_dh):
    don_hang = get_object_or_404(DonHang, ma_dh=ma_dh)
    don_hang.delete()
    return redirect('donhang_list')
def xoa_khachhang(request, ma_kh):
    khachhang = get_object_or_404(KhachHang, ma_kh=ma_kh)
    khachhang.delete()
    return redirect('khachhang_list')
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required(login_url='login_staff')
def trang_chu(request):
    sanpham_list = SanPham.objects.all()
    taikhoan_list = TaiKhoan.objects.all()
    khachhang_list = KhachHang.objects.all()

    context = {
        'sanpham_list': sanpham_list,
        'taikhoan_list': taikhoan_list,
        'khachhang_list': khachhang_list,
    }
    return render(request, 'quantri/trang_chu.html', context)

def them_san_pham(request):
    if request.method == 'POST':
        ma_sp = request.POST['ma_sp']
        ten = request.POST['ten']
        ten_loai = request.POST['ten_loai']
        mo_ta = request.POST['mo_ta']
        gia = request.POST['gia']
        so_luong = request.POST['so_luong']
        hinh_anh = request.FILES.get('hinh_anh')

        SanPham.objects.create(
            ma_sp=ma_sp,
            ten_san_pham=ten,
            ten_loai = ten_loai,
            mo_ta=mo_ta,
            gia=gia,
            so_luong=so_luong,
            hinh_anh=hinh_anh
        )
        return redirect('sanpham_list')
    ds_loai = LoaiHang.objects.all()        
    return render(request, 'quantri/them_san_pham.html', {'ds_loai': ds_loai})


def sua_san_pham(request, ma_sp):
    san_pham = get_object_or_404(SanPham, ma_sp=ma_sp)
    if request.method == 'POST':
        san_pham.ma_sp = request.POST['ma_sp']
        san_pham.ten_san_pham = request.POST['ten']
        san_pham.ten_loai = request.POST['ten_loai']
        san_pham.mo_ta = request.POST['mo_ta']
        san_pham.gia = request.POST['gia']
        san_pham.so_luong = request.POST['so_luong']
        # Nếu người dùng có upload hình mới, thì cập nhật
        if 'hinh_anh' in request.FILES:
            san_pham.hinh_anh = request.FILES['hinh_anh']

        san_pham.save()
        return redirect('sanpham_list')
    ds_loai = LoaiHang.objects.all()        

    return render(request, 'quantri/sua_san_pham.html', {'sp': san_pham, 'ds_loai': ds_loai})


def xoa_san_pham(request, ma_sp):
    san_pham = get_object_or_404(SanPham, ma_sp=ma_sp)
    san_pham.delete()
    return redirect('sanpham_list')



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import TaiKhoan

from django.contrib.auth.models import User  # ✅ dùng model User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from .models import TaiKhoan


def sua_taikhoan(request, id):  # đổi tên biến
    user = get_object_or_404(User, id=id)
    taikhoan = get_object_or_404(TaiKhoan, user=user)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        ho_ten = request.POST.get('hoTen')
        password = request.POST.get('password')

        # ✅ Cập nhật User
        if user:
            user.username = username
            user.email = email
            if password:
                user.set_password(password)
            user.save()

        # ✅ Cập nhật TaiKhoan
        taikhoan.tenTK = username
        taikhoan.email = email
        taikhoan.hoTen = ho_ten
        if password:
            taikhoan.matKhau = password  # ❗nếu có mã hóa mật khẩu, cần xử lý thêm
        taikhoan.save()

        return redirect('taikhoan_list')

    return render(request, 'quantri/sua_taikhoan.html', {'taikhoan': taikhoan})



def xoa_taikhoan(request, id):
    taikhoan = get_object_or_404(User, id=id)
    taikhoan.delete()
    return redirect('taikhoan_list')




# Thêm loại hàng
def them_loaihang(request):
    if request.method == 'POST':
        ma_loai = request.POST.get('ma_loai')
        ten_loai = request.POST.get('ten_loai')
        mo_ta = request.POST.get('mo_ta')
        
        if ma_loai and ten_loai and mo_ta:
            LoaiHang.objects.create(
                ma_loai = ma_loai,
                ten_loai=ten_loai,
                mo_ta = mo_ta
                
            )
            return redirect('loaihang_list')
        else:
            messages.error(request, 'Vui lòng nhập đầy đủ thông tin!')
    return render(request, 'quantri/them_loaihang.html')

# Sửa loại hàng
def sua_loaihang(request, ma_loai):
    loaihang = get_object_or_404(LoaiHang, ma_loai=ma_loai)
    
    if request.method == 'POST':
        loaihang.ma_loai = request.POST.get('ma_loai')
        loaihang.ten_loai = request.POST.get('ten_loai')
        loaihang.mo_ta = request.POST.get('mo_ta')
        loaihang.save()
        return redirect('loaihang_list')  # hoặc tên URL của danh sách

    return render(request, 'quantri/sua_loaihang.html', {'loaihang': loaihang})


def xoa_loaihang(request, ma_loai):
    loaihang = get_object_or_404(LoaiHang, ma_loai=ma_loai)
    loaihang.delete()
    return redirect('loaihang_list')


def khachhang_list(request):
    khach_hang_list = KhachHang.objects.all()
    return render(request, 'quantri/khachhang_list.html', {'khach_hang_list': khach_hang_list})


def sanpham_list(request):
    san_pham_list = SanPham.objects.all()
    return render(request, 'quantri/sanpham_list.html', {'san_pham_list': san_pham_list})
def loaihang_list(request):
    loaihangs = LoaiHang.objects.all().order_by('ten_loai')
    return render(request, 'quantri/loaihang_list.html', {'loaihangs': loaihangs})

from django.contrib.auth.models import User
from django.shortcuts import render

def taikhoan_list(request):
    # Lấy user là staff hoặc superuser
    tai_khoan_list = User.objects.filter(is_staff=True)  # hoặc is_superuser=True tùy yêu cầu

    # Nếu bạn muốn lấy cả staff và superuser:
    # tai_khoan_list = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)

    return render(request, 'quantri/taikhoan_list.html', {
        'tai_khoan_list': tai_khoan_list,
    })


def donhang_list(request):
    don_hang_list = DonHang.objects.all()
    return render(request, 'quantri/donhang_list.html', {'don_hang_list': don_hang_list})

def loaihang_detail(request, ma_loai):
    loai = get_object_or_404(LoaiHang, ma_loai=ma_loai)
    sanphams = SanPham.objects.filter(ten_loai=loai.ten_loai)
    return render(request, 'quantri/loaihang_detail.html', {'loai': loai, 'sanphams': sanphams})
from django.contrib.auth.models import User
from .models import TaiKhoan

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import TaiKhoan
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TaiKhoan

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from quantri.models import TaiKhoan, KhachHang
import random
import re

def is_password_strong(password):
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )
def register_staff(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            ho_ten = request.POST.get('ho_ten')

            # Kiểm tra dữ liệu
            if not all([username, password, email, ho_ten]):
                messages.error(request, 'Vui lòng nhập đầy đủ thông tin')
                return redirect('login_staff')  # về trang chung đăng nhập/đăng ký

            if not is_password_strong(password):
                messages.error(request, 'Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt.')
                return redirect('login_staff') 


            # Tạo User của Django
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_staff = True        # Cho phép vào /admin/
            user.is_superuser = False    # Toàn quyền admin (bạn có thể bỏ nếu không cần)
            user.is_active = True
            user.save()

            # Tạo bản ghi TaiKhoan mở rộng nếu cần
            ma_tk = 'TK' + str(user.id).zfill(4)
            TaiKhoan.objects.create(
                user=user,
                ma_tk=ma_tk,
                tenTK=username,
                matKhau=password,  # ❗ Bạn có thể mã hóa nếu cần
                hoTen=ho_ten,
                email=email
            )

            messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
            return redirect('login_staff')

        except Exception as e:
            messages.error(request, f'Đã xảy ra lỗi: {str(e)}')
            return redirect('login_staff')

    return redirect('login_staff')


def login_staff(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/quantri/')
        else:
            messages.error(request, 'Sai tài khoản hoặc mật khẩu hoặc không có quyền truy cập.')
            return redirect('login_staff')

    return render(request, 'quantri/login_staff.html')  # trang chứa cả đăng nhập và đăng ký


from django.contrib.auth import logout


def logout_staff(request):
    logout(request)
    return redirect('login_staff')

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DonHang, ChiTietDonHang

@csrf_exempt  # Nếu bạn chưa config CSRF
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart = data.get('cart', [])

            # Tạo đơn hàng
            donhang = DonHang.objects.create(
                # ví dụ: đặt tên khách hàng mặc định hoặc lấy từ user request.user
            )

            # Tạo chi tiết đơn hàng
            for item in cart:
                ChiTietDonHang.objects.create(
                    donhang=donhang,
                    ten_sanpham=item['title'],
                    so_luong=item['quantity'],
                    gia=item['price'],
                )
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid method'})

from django.shortcuts import render
from .models import DonHang, ChiTietDonHang
from django.db.models import Sum, F, FloatField, ExpressionWrapper

def thongke_doanhthu(request):
    # Tổng doanh thu toàn bộ
    doanhthu = ChiTietDonHang.objects.annotate(
        tong=ExpressionWrapper(F('so_luong') * F('san_pham__gia'), output_field=FloatField())
    ).aggregate(tong_doanhthu=Sum('tong'))['tong_doanhthu'] or 0

    # Thống kê doanh thu và số lượng theo đơn hàng
    donhang_data = (
        ChiTietDonHang.objects
        .values('don_hang__ma_dh', 'don_hang__ngay_dat')
        .annotate(
            tong_so_luong=Sum('so_luong'),
            tong_doanhthu=Sum(ExpressionWrapper(F('so_luong') * F('san_pham__gia'), output_field=FloatField()))
        )
        .order_by('-don_hang__ngay_dat')
    )

    context = {
        'tong_doanhthu': doanhthu,
        'donhang_data': donhang_data,
    }
    return render(request, 'quantri/thongke_doanhthu.html', context)
def thongke_sanphambanchay(request):
    top_sanpham = (
        ChiTietDonHang.objects
        .values('san_pham__ten_san_pham')
        .annotate(tong_sl=Sum('so_luong'))
        .order_by('-tong_sl')[:5]
    )

    context = {
        'top_sanpham': top_sanpham
    }
    return render(request, 'quantri/thongke_sanphambanchay.html', context)
def thongke_tonkho(request):
    danh_sach_sp = SanPham.objects.all()

    ton_kho = []
    for sp in danh_sach_sp:
        da_ban = ChiTietDonHang.objects.filter(san_pham=sp).aggregate(tong=Sum('so_luong'))['tong'] or 0
        con_lai = sp.so_luong - da_ban

        ton_kho.append({
            'ma_sp': sp.ma_sp,
            'ten_san_pham': sp.ten_san_pham,
            'gia': sp.gia,
            'so_luong_con_lai': con_lai
        })

    context = {
        'danh_sach_sp': ton_kho
    }
    return render(request, 'quantri/thongke_tonkho.html', context)
    return render(request, 'quantri/thongke_tonkho.html', context)
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import DonHang
from .models import TaiKhoan

@login_required
def cap_nhat_trang_thai(request, ma_dh):
    don_hang = get_object_or_404(DonHang, ma_dh=ma_dh)

    try:
        tai_khoan = TaiKhoan.objects.get(user=request.user)
    except TaiKhoan.DoesNotExist:
        return HttpResponseForbidden("Bạn không có quyền cập nhật trạng thái đơn hàng.")

    if request.method == "POST":
        trang_thai_moi = request.POST.get('trang_thai')
        if trang_thai_moi in dict(DonHang.TRANG_THAI_CHOICES).keys():
            don_hang.trang_thai = trang_thai_moi
            don_hang.save()
    
    return redirect('donhang_list')

def chi_tiet_don_hang(request, ma_dh):
    don_hang = get_object_or_404(DonHang, ma_dh=ma_dh)
    return render(request, 'quantri/chitiet_donhang.html', {
        'don_hang': don_hang,
        'chi_tiets': don_hang.chi_tiet.all()  # sử dụng related_name
    })