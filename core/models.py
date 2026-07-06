from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Extended user profile linked one-to-one with Django's built-in User.
    Created automatically via post_save signal when a new User is registered.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150, blank=True, verbose_name="To'liq ism")
    student_class = models.CharField(max_length=50, blank=True, verbose_name="Sinf")
    is_approved = models.BooleanField(default=False, verbose_name="Tasdiqlangan")
    points = models.FloatField(default=0.0, verbose_name="Ballar")

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"

    def __str__(self):
        return f"{self.user.username} – {self.points} ball"


class TeacherMaterial(models.Model):
    """
    Material uploaded by a teacher (admin) for students to download.
    """
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    file = models.FileField(upload_to='materials/', verbose_name="Fayl")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuklangan vaqt")

    class Meta:
        verbose_name = "O'qituvchi materiali"
        verbose_name_plural = "O'qituvchi materiallari"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


class StudentPost(models.Model):
    """
    A student's daily learning post (what they learned, their experience).
    Worth 4 points each time successfully submitted.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Muallif")
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    photo = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name="Rasm")
    learned_today = models.TextField(verbose_name="Bugun nimani o'rgandim")
    experience = models.TextField(verbose_name="Tajribam")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "O'quvchi ishi"
        verbose_name_plural = "O'quvchilar ishlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username}: {self.title}"


class DailyTest(models.Model):
    """
    A daily quiz question with 4 multiple-choice options (A, B, C, D).
    """
    ANSWER_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes', verbose_name="Muallif")
    question = models.TextField(verbose_name="Savol")
    option_a = models.CharField(max_length=300, verbose_name="A variant")
    option_b = models.CharField(max_length=300, verbose_name="B variant")
    option_c = models.CharField(max_length=300, verbose_name="C variant")
    option_d = models.CharField(max_length=300, verbose_name="D variant")
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, verbose_name="To'g'ri javob")
    solved_by = models.ManyToManyField(User, related_name='solved_quizzes', blank=True, verbose_name="Yechgan o'quvchilar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Kunlik test"
        verbose_name_plural = "Kunlik testlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Savol: {self.question[:60]}..."
