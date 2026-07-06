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

    top_students = Profile.objects.all().order_by('-points')[:5]

    if request.user.is_authenticated:
        latest_quiz = DailyTest.objects.exclude(solved_by=request.user).order_by('?').first()
    else:
        latest_quiz = DailyTest.objects.order_by('?').first()

    posts = StudentPost.objects.all()[:2]  # Show only top 2 latest posts

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

    from django.utils import timezone
    today = timezone.localdate()
    if StudentPost.objects.filter(author=request.user, created_at__date=today).exists():
        return HttpResponse(
            "<div style='font-family:sans-serif;text-align:center;margin-top:80px;"
            "color:#1e4b82;'>"
            "<h2>⚠️ Kechirasiz!</h2>"
            "<p>Siz bugun allaqachon post yuklagansiz. Kuniga faqat bitta post joylash mumkin!</p>"
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


def submit_quiz(request, quiz_id):
    """
    Handles quiz submission. Awards 1 point if correct and tracks that the user solved it (for logged-in users).
    Guests can solve but get no points.
    """
    if request.method == 'POST':
        try:
            quiz = DailyTest.objects.get(id=quiz_id)
        except DailyTest.DoesNotExist:
            messages.error(request, "Quiz topilmadi.")
            return redirect('home')

        selected_answer = request.POST.get('quiz_answer')
        
        if not selected_answer:
            messages.warning(request, "Iltimos, javob variantini tanlang!")
            return redirect('home')

        if request.user.is_authenticated:
            # Check if already solved
            if request.user in quiz.solved_by.all():
                messages.warning(request, "Siz bu quizni allaqachon yechgansiz.")
                return redirect('home')

            if selected_answer == quiz.correct_answer:
                profile, _ = Profile.objects.get_or_create(user=request.user)
                profile.points += 1.0
                profile.save()
                
                quiz.solved_by.add(request.user)
                messages.success(request, f"✅ To'g'ri javob! Sizga 1 ball qo'shildi. (To'g'ri javob: {quiz.correct_answer})")
            else:
                messages.error(request, f"❌ Noto'g'ri javob. To'g'ri javob '{quiz.correct_answer}' edi. Boshqa quizlarda omadingizni sinab ko'ring!")
                quiz.solved_by.add(request.user)
        else:
            # Guest user logic
            if selected_answer == quiz.correct_answer:
                messages.success(request, f"✅ To'g'ri javob! (Siz tizimga kirmaganingiz uchun ball qo'shilmadi)")
            else:
                messages.error(request, f"❌ Noto'g'ri javob. To'g'ri javob '{quiz.correct_answer}' edi.")

    return redirect('home')


def post_list(request):
    """
    Displays a full list of all student posts (titles only).
    """
    posts = StudentPost.objects.all()
    context = {'posts': posts}
    return render(request, 'core/post_list.html', context)


def post_detail(request, pk):
    """
    Displays a single student post in full screen.
    """
    from django.shortcuts import get_object_or_404
    post = get_object_or_404(StudentPost, pk=pk)
    context = {'post': post}
    return render(request, 'core/post_detail.html', context)
