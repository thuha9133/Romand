from django.shortcuts import render, redirect
from quantri.models import SanPham 
from django.shortcuts import render, redirect, get_object_or_404
from quantri.models import DonHang, ChiTietDonHang, SanPham, KhachHang, TaiKhoan
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from .forms import UserForm, CustomerForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from customers.models import Customer
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from quantri.models import KhachHang
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_POST
import random
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def lich_su_don_hang(request):
    # Tìm mã khách hàng từ tài khoản hiện tại
    tai_khoan = TaiKhoan.objects.get(user=request.user)
    khach_hang = KhachHang.objects.get(tai_khoan=tai_khoan)
    don_hangs = DonHang.objects.filter(khach_hang=khach_hang).order_by('-ngay_dat')

    return render(request, 'customers/lichsu_donhang.html', {'don_hangs': don_hangs})


@login_required
def chi_tiet_don_hang(request, ma_dh):
    don_hang = get_object_or_404(DonHang, ma_dh=ma_dh)
    return render(request, 'customers/chitiet_donhang.html', {
        'don_hang': don_hang,
        'chi_tiets': don_hang.chi_tiet.all()  # sử dụng related_name
    })


def tim_kiem_san_pham(request):
    tu_khoa = request.GET.get('q', '')
    if tu_khoa:
        ket_qua = SanPham.objects.filter(ten_san_pham__icontains=tu_khoa)
        if ket_qua.exists():
            if ket_qua.count() == 1:
                return redirect('chitiet_sanpham', ma_sp=ket_qua.first().ma_sp)
            else:
                return render(request, 'customers/tim_kiem_ket_qua.html', {
                    'danh_sach_ket_qua': ket_qua,
                    'tu_khoa': tu_khoa,
                    'khong_tim_thay': not ket_qua.exists(),  # biến báo có kết quả
                })
        else:
            # Không tìm thấy sản phẩm nào
            return render(request, 'customers/tim_kiem_ket_qua.html', {
                'danh_sach_ket_qua': [],
                'tu_khoa': tu_khoa,
                'khong_tim_thay': True,   # biến báo không có kết quả
            })
    return redirect('sanpham')




def chitiet_sanpham(request, ma_sp):
    sp = get_object_or_404(SanPham, ma_sp=ma_sp)  
    return render(request, 'customers/chitiet_sanpham.html', {'sp': sp})


def sanpham(request):
    danh_sach_san_pham = SanPham.objects.all()
    khach_hang = None

    if request.user.is_authenticated:
        try:
            tai_khoan_obj = TaiKhoan.objects.get(user=request.user)  # dùng user của Django để lấy TaiKhoan
            khach_hang = KhachHang.objects.get(tai_khoan=tai_khoan_obj)
        except (TaiKhoan.DoesNotExist, KhachHang.DoesNotExist):
            khach_hang = None

    return render(request, 'customers/sanpham.html', {
        'danh_sach_san_pham': danh_sach_san_pham,
        'khach_hang': khach_hang,
    })
@login_required(login_url='login')
def giohang(request):
    return render(request, 'customers/giohang.html')
def index(request):
    return render(request, 'customers/index.html')

def gioithieu(request):
    return render(request, 'customers/gioithieu.html')

def chitiet(request, id):
    return render(request, 'customers/chitiet.html')

def romand23(request):
    return render(request, 'customers/romand23.html')
def cart(request):
    return render(request, 'customers/cart.html')

def lienhe(request):
    return render(request, 'customers/lienhe.html')


def generate_ma_kh():
    while True:
        ma_kh = 'KH' + ''.join(random.choices('0123456789', k=6))
        if not KhachHang.objects.filter(ma_kh=ma_kh).exists():
            return ma_kh



from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Customer
from quantri.models import TaiKhoan, KhachHang
import random
import re
from django.db.models import Q

def is_password_strong(password):
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )
@csrf_exempt
def register(request):
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        email = email.strip().lower()

        # Kiểm tra trùng email hoặc username
        if User.objects.filter(Q(username=email) | Q(email=email)).exists():
            return render(request, 'customers/login.html', {
                'register_error': 'Email đã tồn tại!',
                'next': '/profile/',
            })

        # ✅ Kiểm tra mật khẩu mạnh
        if not is_password_strong(password):
            return render(request, 'customers/login.html', {
                'register_error': 'Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt.',
                'next': '/profile/',
            })

        # ✅ Tạo user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        tai_khoan = TaiKhoan.objects.create(
            user=user,
            ma_tk='TK' + ''.join(random.choices('0123456789', k=6)),
            tenTK=email,
            matKhau=make_password(password),
            hoTen=name,
            email=email
        )

        khachhang = KhachHang.objects.create(
            tai_khoan=tai_khoan,
            ten_kh=name,
            email=email,
            mat_khau=make_password(password),
            so_dien_thoai=phone,
            dia_chi=address
        )

        Customer.objects.create(
            user=user,
            address=address,
            phone=phone,
            ma_kh=khachhang.ma_kh
        )

        return render(request, 'customers/login.html', {
            'register_success': 'Tạo tài khoản thành công! Bạn có thể đăng nhập.',
            'next': next_url,
        })




def qa(request):
    return render(request, 'customers/qa.html')



from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
def login(request):
    next_url = request.GET.get('next') or 'index'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Kiểm tra User tồn tại
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'customers/login.html', {
                'error': 'Tài khoản không tồn tại.'
            })

        # ✅ Xác thực username/password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # ✅ Kiểm tra TaiKhoan & KhachHang còn tồn tại không
            try:
                tai_khoan = TaiKhoan.objects.get(user=user)
                khach_hang = KhachHang.objects.get(tai_khoan=tai_khoan)
            except (TaiKhoan.DoesNotExist, KhachHang.DoesNotExist):
                return render(request, 'customers/login.html', {
                    'error': 'Tài khoản không hợp lệ hoặc đã bị xóa.'
                })

            # ✅ Nếu mọi thứ hợp lệ → login
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'customers/login.html', {
                'error': 'Sai mật khẩu hoặc tài khoản bị khóa.'
            })

    return render(request, 'customers/login.html')

from django.contrib.auth import logout
from django.contrib.auth.models import User

class AutoLogoutIfUserDeletedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Nếu người dùng đã đăng nhập nhưng tài khoản bị xóa khỏi bảng User
        if request.user.is_authenticated:
            try:
                User.objects.get(pk=request.user.pk)
            except User.DoesNotExist:
                logout(request)  # tự động đăng xuất

        response = self.get_response(request)
        return response

def logout(request):
    auth_logout(request)  # Gọi hàm logout chính xác của Django
    return redirect('index')



@login_required
def profile(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    return render(request, 'customers/profile.html', {
        'user_full_name': request.user.get_full_name() or request.user.username,
        'customer': customer
    })

# views.py

def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('index')
@login_required
def edit_profile(request):
    user = request.user
    customer, _ = Customer.objects.get_or_create(user=user)

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, instance=customer)

        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        has_password_change = current_password or new_password or confirm_password
        password_valid = True

        if has_password_change:
            if not current_password:
                messages.error(request, "Vui lòng nhập mật khẩu hiện tại.")
                password_valid = False
            elif not user.check_password(current_password):
                messages.error(request, "Mật khẩu hiện tại không đúng.")
                password_valid = False
            elif new_password != confirm_password:
                messages.error(request, "Mật khẩu mới và xác nhận không khớp.")
                password_valid = False

        if customer_form.is_valid() and (not has_password_change or password_valid):
            # ✅ Lưu address + phone vào Customer
            customer_form.save()

            # ✅ Đồng bộ qua bảng KhachHang nếu tồn tại (theo email)
            try:
                kh = KhachHang.objects.get(email=user.email)
                kh.dia_chi = customer.address
                kh.so_dien_thoai = customer.phone
                kh.save()
            except KhachHang.DoesNotExist:
                pass  # không có thì bỏ qua

            # ✅ Nếu có đổi mật khẩu
            if has_password_change and password_valid:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Đổi mật khẩu và cập nhật thông tin thành công!")
            else:
                messages.success(request, "Cập nhật thông tin thành công!")

            return redirect('edit_profile')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")

    else:
        customer_form = CustomerForm(instance=customer)

    return render(request, 'customers/edit_profile.html', {
        'customer_form': customer_form
    })
import json
from django.http import JsonResponse
from quantri.models import KhachHang, SanPham, DonHang, ChiTietDonHang


import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from quantri.models import SanPham, DonHang, ChiTietDonHang, KhachHang


from django.utils.crypto import get_random_string
@csrf_exempt
def thanhtoan(request):
    if request.method == 'GET':
        return render(request, 'customers/thanhtoan.html')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart = data.get('cart', [])
            hinh_thuc = data.get('hinh_thuc', 'cod')
            ghi_chu = data.get('ghi_chu', '')
            subtotal = sum(item['price'] * item['quantity'] for item in cart)
            shipping_fee = 35000
            tong_tien = subtotal + shipping_fee

            # ✅ Kiểm tra giỏ hàng có sản phẩm không
            if not cart:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Giỏ hàng trống. Không thể thanh toán.'
                })

            # ✅ Lấy khách hàng từ user
            tai_khoan = TaiKhoan.objects.get(user=request.user)
            khach_hang = KhachHang.objects.get(tai_khoan=tai_khoan)

            ma_dh = 'DH' + get_random_string(length=6, allowed_chars='0123456789')

            don_hang = DonHang.objects.create(
                ma_dh=ma_dh,
                khach_hang=khach_hang,
                phuong_thuc=hinh_thuc,
                tong_tien = tong_tien,
                ghi_chu=ghi_chu

            )

            for item in cart:
                sp = SanPham.objects.get(id=int(item['id']))
                ChiTietDonHang.objects.create(
                    don_hang=don_hang,
                    san_pham=sp,
                    so_luong=int(item['quantity'])
                )

            return JsonResponse({'status': 'ok', 'ma_dh': ma_dh})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ'})



@login_required(login_url='login')
def yeuthich(request):
    return render(request, 'customers/yeuthich.html')

from django.http import JsonResponse

def them_gio_hang(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ request body (fetch gửi json)
        import json
        data = json.loads(request.body)
        san_pham_id = data.get('san_pham_id')
        so_luong = data.get('so_luong', 1)

        # Thực hiện thêm sản phẩm vào giỏ hàng (ví dụ dùng session)
        gio_hang = request.session.get('gio_hang', {})

        if san_pham_id in gio_hang:
            gio_hang[san_pham_id] += so_luong
        else:
            gio_hang[san_pham_id] = so_luong

        request.session['gio_hang'] = gio_hang

        return JsonResponse({'status': 'success', 'message': 'Đã thêm sản phẩm vào giỏ hàng'})

    return JsonResponse({'status': 'fail', 'message': 'Phương thức không hợp lệ'}, status=400)
def them_vao_gio(request, id):
    product = get_object_or_404(SanPham, id=id)
    cart = request.session.get('cart', {})

    if str(product.id) in cart:
        cart[str(product.id)]['quantity'] += 1
    else:
        cart[str(product.id)] = {'quantity': 1}

    request.session['cart'] = cart
    return redirect('sanpham')
