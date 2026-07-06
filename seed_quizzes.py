import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'informatik22.settings')
django.setup()

from core.models import DailyTest
from django.contrib.auth.models import User

# Adminni topamiz (yoki birinchi superuserni)
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'admin1234')

# Asosiy Python va Algoritm savollari
quizzes_data = [
    {"q": "Python'da ro'yxatning uzunligini qaysi funksiya orqali bilish mumkin?", "a": "size()", "b": "len()", "c": "length()", "d": "count()", "ans": "B"},
    {"q": "O'zgaruvchini butun son turiga aylantirish uchun nima ishlatiladi?", "a": "int()", "b": "str()", "c": "float()", "d": "bool()", "ans": "A"},
    {"q": "Python'da izoh (comment) qaysi belgi bilan boshlanadi?", "a": "//", "b": "/*", "c": "#", "d": "--", "ans": "C"},
    {"q": "Qaysi algoritm O(n log n) vaqtda ishlaydi?", "a": "Bubble Sort", "b": "Selection Sort", "c": "Merge Sort", "d": "Insertion Sort", "ans": "C"},
    {"q": "Stack qaysi prinsipda ishlaydi?", "a": "FIFO", "b": "LIFO", "c": "GIGO", "d": "Random", "ans": "B"},
    {"q": "Queue qaysi prinsipda ishlaydi?", "a": "LIFO", "b": "FIFO", "c": "LILO", "d": "Hech qaysi", "ans": "B"},
    {"q": "Binary Search uchun massiv qanday holatda bo'lishi kerak?", "a": "Tasodifiy", "b": "Teskari", "c": "Saralangan", "d": "Katta", "ans": "C"},
    {"q": "Python'da bo'sh ro'yxat qanday e'lon qilinadi?", "a": "[]", "b": "{}", "c": "()", "d": "list{}", "ans": "A"},
    {"q": "x = 5; y = 2; x // y natijasi nima?", "a": "2.5", "b": "2", "c": "3", "d": "1", "ans": "B"},
    {"q": "x = 5; y = 2; x % y natijasi nima?", "a": "2", "b": "1", "c": "2.5", "d": "0", "ans": "B"},
    {"q": "Python'da funksiya qaysi so'z bilan yaratiladi?", "a": "function", "b": "create", "c": "def", "d": "fun", "ans": "C"},
    {"q": "Listning oxiriga element qo'shish uchun qaysi metod ishlatiladi?", "a": "add()", "b": "append()", "c": "insert()", "d": "push()", "ans": "B"},
    {"q": "O(1) vaqt nima degani?", "a": "Vaqt n ga bog'liq", "b": "O'zgarmas vaqt", "c": "Eksponensial vaqt", "d": "Logarifmik", "ans": "B"},
    {"q": "Bubble sortning eng yomon holatdagi tezligi qanday?", "a": "O(n)", "b": "O(n log n)", "c": "O(n^2)", "d": "O(log n)", "ans": "C"},
    {"q": "Set nima maqsadda ishlatiladi?", "a": "Tartiblangan ro'yxat uchun", "b": "Takrorlanmas elementlar uchun", "c": "Lug'at uchun", "d": "Index orqali qidirish uchun", "ans": "B"},
    {"q": "Python'da dictionary qanday qavs bilan yaratiladi?", "a": "()", "b": "[]", "c": "{}", "d": "<>", "ans": "C"},
    {"q": "Recursion nima?", "a": "Tsiklning bir turi", "b": "Funksiyaning o'zini o'zi chaqirishi", "c": "Fayl yozish", "d": "Ma'lumotlar tuzilmasi", "ans": "B"},
    {"q": "Dynamic Programming nima?", "a": "Veb dasturlash", "b": "Muammoni kichik qismlarga bo'lib yechish", "c": "Obyektga yo'naltirilganlik", "d": "O'zgaruvchilarni dinamik tiplash", "ans": "B"},
    {"q": "Dasturlashda 'Bug' nima?", "a": "Hasharot", "b": "Dasturdagi xato", "c": "Yangi funksiya", "d": "Fayl turi", "ans": "B"},
    {"q": "Fibonacci ketma-ketligi qanday boshlanadi?", "a": "1, 2, 3...", "b": "0, 1, 1, 2...", "c": "2, 4, 6...", "d": "1, 3, 5...", "ans": "B"}
]

# Generate more programmatically to reach 100 questions
for i in range(1, 81):
    n1 = i % 10 + 2
    n2 = (i * 3) % 7 + 1
    op = "+" if i % 2 == 0 else "*"
    res = n1 + n2 if op == "+" else n1 * n2
    
    question = {
        "q": f"Algoritm: agar x = {n1} va y = {n2} bo'lsa, x {op} y ifodasi qanday natija beradi?",
        "a": str(res - 1),
        "b": str(res),
        "c": str(res + 1),
        "d": str(res * 2),
        "ans": "B"
    }
    
    # Shuffle options slightly so B is not always the answer
    import random
    options = [question["a"], question["b"], question["c"], question["d"]]
    ans_val = options[1] # "b" contains correct answer
    random.shuffle(options)
    
    correct_letter = "A"
    if options[0] == ans_val: correct_letter = "A"
    elif options[1] == ans_val: correct_letter = "B"
    elif options[2] == ans_val: correct_letter = "C"
    elif options[3] == ans_val: correct_letter = "D"
    
    quizzes_data.append({
        "q": question["q"],
        "a": options[0],
        "b": options[1],
        "c": options[2],
        "d": options[3],
        "ans": correct_letter
    })

print(f"Jami {len(quizzes_data)} ta savol tayyorlandi.")
print("Ma'lumotlar bazasiga yuklanmoqda...")

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

print(f"Muvaffaqiyatli {count} ta quiz bazaga saqlandi!")
