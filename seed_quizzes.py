import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'informatik22.settings')
django.setup()

from core.models import DailyTest
from django.contrib.auth.models import User

# Adminni topamiz
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'admin1234')

print("Oldingi qiyin testlar o'chirib tashlanmoqda...")
DailyTest.objects.all().delete()

quizzes_data = []

# --- 5-11 SINFLAR UCHUN MAKTAB DASTURIDAN SAVOLLARI ---
maktab_questions = [
    # 5-sinf
    {"q": "Axborotning eng kichik o'lchov birligi nima?", "a": "Bayt", "b": "Bit", "c": "Kilobayt", "d": "Megabayt", "ans": "B"},
    {"q": "1 Bayt necha bitga teng?", "a": "8", "b": "10", "c": "1024", "d": "16", "ans": "A"},
    {"q": "Kompyuterning 'miyasi' qaysi qurilma hisoblanadi?", "a": "Monitor", "b": "Klaviatura", "c": "Protsessor", "d": "Sichqoncha", "ans": "C"},
    {"q": "Axborot kiritish qurilmasini toping.", "a": "Monitor", "b": "Printer", "c": "Klaviatura", "d": "Kalonka", "ans": "C"},
    {"q": "Matn kiritishda bosh harf yozish uchun qaysi tugma ishlatiladi?", "a": "Enter", "b": "Space", "c": "Shift", "d": "Esc", "ans": "C"},
    {"q": "Paint qanday turdagi dastur?", "a": "Matn muharriri", "b": "Grafik muharrir", "c": "Brauzer", "d": "Antivirus", "ans": "B"},
    
    # 6-sinf
    {"q": "MS Word dasturida hujjatni saqlash klaviatura tugmasi?", "a": "Ctrl + S", "b": "Ctrl + C", "c": "Ctrl + V", "d": "Ctrl + P", "ans": "A"},
    {"q": "Fayl va papkalarni nusxalash tugmasi qaysi?", "a": "Ctrl + X", "b": "Ctrl + Z", "c": "Ctrl + C", "d": "Shift + Delete", "ans": "C"},
    {"q": "Scratch dasturlash tilida qahramonlar nima deb ataladi?", "a": "Blok", "b": "Spreyt (Sprite)", "c": "Sahnadagi aktyor", "d": "Kadr", "ans": "B"},
    {"q": "WWW so'zining to'liq ma'nosi nima?", "a": "World Wide Web", "b": "World Web Wide", "c": "Wide Web World", "d": "Web World Wide", "ans": "A"},
    {"q": "Antivirusning asosiy vazifasi nima?", "a": "Kino ko'rish", "b": "Matn yozish", "c": "Viruslardan himoya qilish", "d": "Rasm chizish", "ans": "C"},

    # 7-sinf
    {"q": "MS Excel qanday dasturlar sirasiga kiradi?", "a": "Matn muharriri", "b": "Elektron jadval", "c": "Taqdimot yaratuvchi", "d": "Brauzer", "ans": "B"},
    {"q": "MS PowerPoint dasturi nima uchun kerak?", "a": "Taqdimotlar (Prezentatsiya) tayyorlash uchun", "b": "Jadval chizish uchun", "c": "Kino ko'rish uchun", "d": "Musiqa eshitish uchun", "ans": "A"},
    {"q": "Excel'da formulalar qaysi belgi bilan boshlanadi?", "a": "+", "b": "-", "c": "=", "d": "*", "ans": "C"},
    {"q": "Algoritm nima?", "a": "Kompyuterning qismi", "b": "Maqsadga erishish uchun bajariladigan ketma-ket harakatlar qoidasi", "c": "O'yin", "d": "Internet brauzer", "ans": "B"},
    {"q": "Chiziqli algoritm qanday bo'ladi?", "a": "Savol so'raydi", "b": "Birma-bir, ketma-ket bajariladi", "c": "Qayta-qayta ishlaydi", "d": "Ishlamaydi", "ans": "B"},

    # 8-sinf
    {"q": "Sanoq sistemalarining qanday turlari mavjud?", "a": "Katta va kichik", "b": "Pozitsiyali va pozitsiyasiz", "c": "Oson va qiyin", "d": "Birlik va o'nlik", "ans": "B"},
    {"q": "Mantiqiy KOPAYTIRISH (AND) amali qanday ataladi?", "a": "Dizyunksiya", "b": "Kon’yunksiya", "c": "Inversiya", "d": "Implikatsiya", "ans": "B"},
    {"q": "Mantiqiy QOSHISH (OR) amali qanday ataladi?", "a": "Kon’yunksiya", "b": "Dizyunksiya", "c": "Inversiya", "d": "Implikatsiya", "ans": "B"},
    {"q": "1 KB (Kilobayt) necha baytga teng?", "a": "1000 bayt", "b": "1024 bayt", "c": "10 bayt", "d": "8 bayt", "ans": "B"},
    {"q": "O'nlik sanoq sistemasidagi 5 soni ikkilikda qanday yoziladi?", "a": "101", "b": "110", "c": "111", "d": "100", "ans": "A"},

    # 9-11 sinflar (Python asoslari)
    {"q": "Python dasturlash tilida ekranga yozuv chiqaruvchi funksiya qaysi?", "a": "echo", "b": "print()", "c": "cout", "d": "write()", "ans": "B"},
    {"q": "Pythonda foydalanuvchidan ma'lumot kiritishni so'rash funksiyasi qaysi?", "a": "output()", "b": "get()", "c": "input()", "d": "scan()", "ans": "C"},
    {"q": "Python'da butun sonlar (integer) qaysi turga tegishli?", "a": "float", "b": "int", "c": "str", "d": "bool", "ans": "B"},
    {"q": "Shart operatori qaysi?", "a": "for", "b": "while", "c": "if", "d": "def", "ans": "C"},
    {"q": "Tsikl (takrorlanish) operatorlarini toping.", "a": "if, else", "b": "for, while", "c": "and, or", "d": "def, return", "ans": "B"},
    {"q": "a = 5, b = 2 bo'lsa, a ** b natijasi nima bo'ladi?", "a": "10", "b": "7", "c": "25", "d": "3", "ans": "C"},
    {"q": "a = 5, b = 2 bo'lsa, a // b natijasi qanday?", "a": "2.5", "b": "2", "c": "1", "d": "3", "ans": "B"},
    {"q": "Python'da bo'sh ro'yxat (list) qanday e'lon qilinadi?", "a": "[]", "b": "{}", "c": "()", "d": "list{}", "ans": "A"},
    {"q": "x = 'Salom' matnining uzunligini qanday bilish mumkin?", "a": "size(x)", "b": "len(x)", "c": "length(x)", "d": "count(x)", "ans": "B"},
    {"q": "Ro'yxatning oxiriga element qo'shish uchun qaysi metod ishlatiladi?", "a": "insert()", "b": "add()", "c": "append()", "d": "push()", "ans": "C"},
    {"q": "Lug'at (dictionary) qanday qavs bilan e'lon qilinadi?", "a": "[]", "b": "()", "c": "{}", "d": "<>", "ans": "C"},
    {"q": "Tenglikni tekshirish uchun qaysi belgi ishlatiladi?", "a": "=", "b": "==", "c": "===", "d": "!=", "ans": "B"},
    {"q": "Pythonda funksiya qaysi so'z bilan yaratiladi?", "a": "function", "b": "def", "c": "create", "d": "fun", "ans": "B"},
    {"q": "Python'da izoh (comment) qaysi belgi bilan yoziladi?", "a": "//", "b": "/*", "c": "#", "d": "<!--", "ans": "C"},
    {"q": "HTML kengaytmasi qanday ma'noni anglatadi?", "a": "HyperText Markup Language", "b": "HighText Machine Language", "c": "HyperLoop Machine Language", "d": "Hech qanday", "ans": "A"},
    {"q": "Veb-sahifaga rasm qo'yish uchun qaysi HTML tegi ishlatiladi?", "a": "<pic>", "b": "<image>", "c": "<img>", "d": "<photo>", "ans": "C"},
    {"q": "Eng katta sarlavha qaysi HTML tegida yoziladi?", "a": "<h6>", "b": "<head>", "c": "<title>", "d": "<h1>", "ans": "D"},
    {"q": "Matnni qalin (bold) qilish uchun qaysi HTML tegi ishlatiladi?", "a": "<i>", "b": "<b>", "c": "<u>", "d": "<s>", "ans": "B"},
    {"q": "Tarmoqning qanday turlari mavjud?", "a": "Katta va kichik", "b": "Global va lokal", "c": "Tez va sekin", "d": "Uzun va qisqa", "ans": "B"},
    {"q": "Lokal tarmoq qisqartmasi nima?", "a": "WAN", "b": "LAN", "c": "MAN", "d": "PAN", "ans": "B"},
]

for q in maktab_questions:
    quizzes_data.append(q)

# --- PROGRAMMATIK OSON/O'RTA SAVOLLAR GENERATSIYASI ---
def shuffle_options(question_dict, correct_answer_text):
    opts = [question_dict["a"], question_dict["b"], question_dict["c"], question_dict["d"]]
    random.shuffle(opts)
    letters = ["A", "B", "C", "D"]
    correct_letter = "A"
    
    for i in range(4):
        question_dict[letters[i].lower()] = opts[i]
        if opts[i] == correct_answer_text:
            correct_letter = letters[i]
            
    question_dict["ans"] = correct_letter
    return question_dict

# 1. Excel formulalari (7-sinf)
for _ in range(20):
    a = random.randint(2, 10)
    b = random.randint(2, 10)
    c = random.randint(2, 10)
    ans = a + b * c
    q = {
        "q": f"MS Excel dasturida = {a} + {b} * {c} formulasi qanday natija beradi?",
        "a": str(ans),
        "b": str((a + b) * c),
        "c": str(ans + 1),
        "d": str(ans - 2)
    }
    quizzes_data.append(shuffle_options(q, str(ans)))

# 2. Sanoq sistemalari (8-sinf)
for n in range(2, 22):
    bin_str = bin(n)[2:]
    q = {
        "q": f"O'nlik sanoq sistemasidagi {n} soni ikkilik sanoq sistemasida qanday yoziladi?",
        "a": bin_str,
        "b": bin(n+1)[2:],
        "c": bin(n-1)[2:],
        "d": bin(n+2)[2:]
    }
    quizzes_data.append(shuffle_options(q, bin_str))

# 3. Python mantiqiy elementlari (9-sinf)
for _ in range(20):
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    is_greater = a > b
    ans = "True" if is_greater else "False"
    wrong = "False" if is_greater else "True"
    q = {
        "q": f"Python dasturida print({a} > {b}) qanday natija chiqaradi?",
        "a": ans,
        "b": wrong,
        "c": "Error",
        "d": "0"
    }
    quizzes_data.append(shuffle_options(q, ans))

# 4. Axborot hajmi (5-sinf)
for n in range(2, 12):
    q = {
        "q": f"{n} Kilobayt (KB) qancha Baytga teng?",
        "a": str(n * 1024),
        "b": str(n * 1000),
        "c": str(n * 10),
        "d": str((n+1) * 1024)
    }
    quizzes_data.append(shuffle_options(q, str(n * 1024)))

print(f"Jami {len(quizzes_data)} ta maktab dasturi savollari tayyorlandi.")

count = 0
for data in quizzes_data:
    DailyTest.objects.create(
        author=admin_user,
        question=data["q"],
        option_a=data["a"],
        option_b=data["b"],
        option_c=data["c"],
        option_d=data["d"],
        correct_answer=data["ans"]
    )
    count += 1

print(f"Muvaffaqiyatli {count} ta maktab quizlari bazaga saqlandi!")
