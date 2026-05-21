from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, LoginForm, ApplicationForm, ReviewForm
from .models import User, Application, Review


SLIDER_IMAGES = [
    'slider/bus.jpg',
    'slider/electrobus.jpg',
    'slider/tram.jpg',
    'slider/road.jpg',
]


def get_current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        return User.objects.filter(id=user_id).first()
    return None


def index(request):
    reviews = Review.objects.select_related('user', 'application').order_by('-created_at')[:3]
    return render(request, 'index.html', {'reviews': reviews, 'slider_images': SLIDER_IMAGES})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно. Теперь можно войти.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            admin_user = authenticate(request, username=login, password=password)
            if admin_user and admin_user.is_superuser:
                auth_login(request, admin_user)
                request.session['is_admin'] = True
                messages.success(request, 'Вы вошли как администратор')
                return redirect('admin_panel')
            user = User.objects.filter(login=login, password=password).first()
            if user:
                request.session['user_id'] = user.id
                request.session['is_admin'] = False
                messages.success(request, 'Вы вошли в личный кабинет')
                return redirect('cabinet')
            form.add_error(None, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    messages.info(request, 'Вы вышли из системы')
    return redirect('index')


def cabinet(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    applications = Application.objects.filter(user=user).order_by('-created_at')
    return render(request, 'cabinet.html', {'current_user': user, 'applications': applications})


def new_application(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = user
            application.save()
            messages.success(request, 'Заявка создана')
            return redirect('cabinet')
    else:
        form = ApplicationForm()
    return render(request, 'application_form.html', {'form': form})


def add_review(request, application_id):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    application = get_object_or_404(Application, id=application_id, user=user)
    if application.status != 'finished':
        messages.error(request, 'Отзыв можно оставить только после завершения обучения')
        return redirect('cabinet')
    if Review.objects.filter(application=application).exists():
        messages.info(request, 'Вы уже оставили отзыв по этой заявке')
        return redirect('cabinet')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user
            review.application = application
            review.save()
            messages.success(request, 'Спасибо за отзыв')
            return redirect('cabinet')
    else:
        form = ReviewForm()
    return render(request, 'review_form.html', {'form': form, 'application': application})


def admin_panel(request):
    if not request.session.get('is_admin'):
        return redirect('login')

    applications = Application.objects.select_related('user').all()
    status = request.GET.get('status')
    course = request.GET.get('course')
    sort = request.GET.get('sort', '-created_at')

    if status:
        applications = applications.filter(status=status)
    if course:
        applications = applications.filter(course_type=course)
    if sort in ['created_at', '-created_at', 'preferred_date', '-preferred_date', 'status']:
        applications = applications.order_by(sort)
    else:
        applications = applications.order_by('-created_at')

    paginator = Paginator(applications,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_panel.html',{
        'page_obj': page_obj,
        'status_choices': Application.STATUS_CHOICES,
        'course_choices': Application.COURSE_CHOICES,
    })


def change_status(request, application_id):
    if not request.session.get('is_admin'):
        return redirect('login')
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        application.status = request.POST.get('status', application.status)
        application.save()
        messages.success(request, 'Статус обновлен')
    return redirect('admin_panel')
