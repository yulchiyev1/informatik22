from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .models import TeacherMaterial, StudentPost, DailyTest, Profile
from .forms import RegisterForm, LoginForm, ProfileForm, StudentPostForm


# --------------------------------------------------------------------------- #
#  Authentication Views                                                        #
# --------------------------------------------------------------------------- #

def register_page(request):
    """
    Handles new user registration.
    On success, redirects to login page.
    """
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz! Iltimos, tizimga kiring.")
            return redirect('login')
        else:
            messages.error(request, "Xato yuz berdi. Iltimos, ma'lumotlarni tekshiring.")

    context = {'form': form}
    return render(request, 'core/register.html', context)


def login_page(request):
    """
    Handles user login with Django's authenticate().
    """
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri.")

    context = {'form': form}
    return render(request, 'core/login.html', context)


def logout_user(request):
    """
    Logs out the current user and redirects to login.
    """
    logout(request)
    return redirect('login')


# --------------------------------------------------------------------------- #
#  Main Views                                                                  #
# --------------------------------------------------------------------------- #

def home(request):
    """
    Homepage: shows materials, leaderboard, latest quiz, and student posts.
    """
    materials = TeacherMaterial.objects.all()[:5]

    top_students = Profile.objects.filter(
        is_approved=True
    ).order_by('-points')[:5]

    latest_quiz = DailyTest.objects.first()  # Already ordered by -created_at

    posts = StudentPost.objects.all()  # Already ordered by -created_at

    context = {
        'materials': materials,
        'top_students': top_students,
        'latest_quiz': latest_quiz,
        'posts': posts,
    }
    return render(request, 'core/home.html', context)


@login_required
def profile_page(request):
    """
    Allows the logged-in user to view and update their profile
    (full name, class). Displays current points and approval status.
    """
    # get_or_create ensures safety for any older accounts without a profile
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profilingiz muvaffaqiyatli yangilandi!")
            return redirect('profile')

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'core/profile.html', context)


@login_required
def create_post(request):
    """
    Allows approved students to create a learning post.
    - Checks approval status before allowing post creation.
    - Awards 4 points upon successful submission.
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # Security gate: only approved students may post
    if not profile.is_approved:
        return HttpResponse(
            "<div style='font-family:sans-serif;text-align:center;margin-top:80px;"
            "color:#1e4b82;'>"
            "<h2>⚠️ Kechirasiz!</h2>"
            "<p>Ustoz hali profilingizni tasdiqlamagan. Iltimos kuting!</p>"
            "<a href='/' style='color:#1e4b82;'>← Bosh sahifaga qaytish</a>"
            "</div>",
            status=403
        )

    form = StudentPostForm()

    if request.method == 'POST':
        form = StudentPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Gamification: add 4 points for successfully creating a post
            profile.points += 4.0
            profile.save()

            messages.success(request, "Postingiz muvaffaqiyatli joylashtirildi! +4 ball qo'shildi 🎉")
            return redirect('home')
        else:
            messages.error(request, "Xato yuz berdi. Iltimos, formani to'g'ri to'ldiring.")

    context = {'form': form}
    return render(request, 'core/create_post.html', context)
