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

print("Eski oson testlar o'chirib tashlanmoqda...")
DailyTest.objects.all().delete()

quizzes_data = []

# --- 1. QIYIN ALGORITM VA MA'LUMOTLAR TUZILMASI SAVOLLARI ---
algo_questions = [
    {"q": "Qizil-qora daraxtda (Red-Black Tree) qo'shish va o'chirish amallarining o'rtacha vaqt murakkabligi qanday?", "a": "O(1)", "b": "O(log n)", "c": "O(n)", "d": "O(n log n)", "ans": "B"},
    {"q": "Dijkstra algoritmida manfiy vaznli qirralar qatnashsa nima bo'ladi?", "a": "Oddiy ishlaydi", "b": "Kutilmagan/noto'g'ri natija berishi mumkin", "c": "O(1) da tugaydi", "d": "Siklni topib beradi", "ans": "B"},
    {"q": "Bellman-Ford algoritmining vaqt murakkabligi qanday? (V - uchlar, E - qirralar)", "a": "O(V + E)", "b": "O(V * E)", "c": "O(V^2)", "d": "O(E log V)", "ans": "B"},
    {"q": "Kruskal algoritmida qaysi ma'lumotlar tuzilmasi asosiy rol o'ynaydi?", "a": "Stack", "b": "Disjoint-Set (Union-Find)", "c": "Hash Table", "d": "Trie", "ans": "B"},
    {"q": "Qaysi saralash (sort) algoritmi 'in-place' va o'rtacha O(n log n) vaqt oladi, lekin barqaror (stable) emas?", "a": "Merge Sort", "b": "Quick Sort", "c": "Bubble Sort", "d": "Radix Sort", "ans": "B"},
    {"q": "Grafda eng qisqa yo'lni barcha juftliklar orasida (All-Pairs Shortest Path) qaysi algoritm topadi?", "a": "Dijkstra", "b": "Floyd-Warshall", "c": "DFS", "d": "Prim", "ans": "B"},
    {"q": "A* (A-star) qidiruv algoritmida 'Heuristic' (evristika) funksiyasi qanday xususiyatga ega bo'lishi kerak?", "a": "Har doim 0 ga teng bo'lishi", "b": "Haqiqiy masofani ortiqcha baholamasligi (Admissible)", "c": "Faqat manfiy bo'lishi", "d": "O(n!) vaqt olishi", "ans": "B"},
    {"q": "Topologik saralash (Topological Sort) qanday graflarda qo'llaniladi?", "a": "Barcha graflarda", "b": "Aylanasiz yo'naltirilgan graflarda (DAG)", "c": "Daraxtlarda", "d": "Bog'lanmagan graflarda", "ans": "B"},
    {"q": "NP-Complete muammosini polinom vaqtda hal qiladigan algoritm topilsa nima bo'ladi?", "a": "P = NP deb e'lon qilinadi", "b": "Hech narsa bo'lmaydi", "c": "Kompyuterlar buziladi", "d": "O(1) vaqtli algoritm topilgan bo'ladi", "ans": "A"},
    {"q": "Trie (Prefix Tree) ma'lumotlar tuzilmasining asosiy maqsadi nima?", "a": "Sonlarni saralash", "b": "Stringlar (matnlar) ustida tez qidiruv", "c": "Grafda sikl topish", "d": "Matrisalarni ko'paytirish", "ans": "B"},
]

# --- 2. ADVANCED PYTHON SAVOLLARI ---
python_questions = [
    {"q": "Python'da GIL (Global Interpreter Lock) nima vazifa bajaradi?", "a": "Dasturni tezlashtiradi", "b": "Bir vaqtda faqat bitta thread ishlashini ta'minlaydi", "c": "Xatolarni ushlaydi", "d": "Xotirani tozalaydi", "ans": "B"},
    {"q": "Python'da generator bilan oddiy funksiyaning asosiy farqi nima?", "a": "Generator return ishlatadi", "b": "Generator yield ishlatadi va xotirani tejaydi", "c": "Generator sekinroq ishlaydi", "d": "Generator faqat raqamlar qaytaradi", "ans": "B"},
    {"q": "Decorator (Dekorator) Pythonda qanday ishlaydi?", "a": "Sintaksis xatolarini to'g'irlaydi", "b": "Funksiyani o'zgartirmasdan uning imkoniyatlarini kengaytiradi", "c": "Faqat class ichida yoziladi", "d": "Ma'lumotlar bazasiga ulanish uchun", "ans": "B"},
    {"q": "@staticmethod va @classmethod o'rtasidagi farq nima?", "a": "Farqi yo'q", "b": "@classmethod o'zining birinchi argumenti sifatida class ni oladi (cls), @staticmethod umuman olmaydi", "c": "@staticmethod faqat obyektlarda ishlaydi", "d": "@classmethod tezroq ishlaydi", "ans": "B"},
    {"q": "Python'da memory management qanday amalga oshiriladi?", "a": "Faqat Garbage Collector", "b": "Reference Counting va Garbage Collector orqali", "c": "C++ kabi qo'lda (malloc/free)", "d": "OS tomonidan bajariladi", "ans": "B"},
    {"q": "Dunder (magic) metodlar nima?", "a": "Xavfli metodlar", "b": "Ikki marta pastki chiziq bilan boshlanuvchi va tugaydigan metodlar (masalan __init__)", "c": "Faqat raqam qaytaruvchi metodlar", "d": "C tilidagi metodlar", "ans": "B"},
    {"q": "*args va **kwargs vazifasi?", "a": "Faqat stringlar uchun", "b": "Noma'lum miqdordagi pozitsion va nomli argumentlarni qabul qilish", "c": "Xotirani tozalash", "d": "Global o'zgaruvchilarni chaqirish", "ans": "B"},
    {"q": "List Comprehension o'rniga generator expression ishlatish qachon foydali?", "a": "Qisqa ro'yxatlarda", "b": "Katta hajmdagi ma'lumotlarda, xotirani tejash uchun", "c": "Sonlarni ko'paytirishda", "d": "Matnlar bilan ishlashda", "ans": "B"},
    {"q": "Pythonda 'deepcopy' va 'shallow copy' ning farqi nima?", "a": "Ikkalasi bir xil", "b": "Deepcopy barcha ichma-ich tuzilmalarni ham mustaqil nusxalaydi", "c": "Shallow copy xotirada ko'p joy oladi", "d": "Deepcopy faqat stringlarni nusxalaydi", "ans": "B"},
    {"q": "MRO (Method Resolution Order) Pythonda nimani anglatadi?", "a": "Xotira bo'shatish tartibini", "b": "Ko'p karra vorislikda klass metodlarini izlash ketma-ketligini", "c": "Modullarni yuklash ketma-ketligini", "d": "Funksiya ishlash tezligini", "ans": "B"},
]

for q in algo_questions + python_questions:
    quizzes_data.append(q)

# --- 3. GENERATED ADVANCED ALGORITHMIC SCENARIOS ---
# Recursion, Dynamic Programming, Big O, Graph theory
# We will generate programmatic variations of hard questions

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

# Generate 50 DP / Recurrence questions
for n in range(10, 60):
    val = n * (n - 1) // 2
    q = {
        "q": f"To'liq grafda (Complete Graph) {n} ta uch bo'lsa, jami qancha qirra (edge) bo'ladi?",
        "a": str(val - n),
        "b": str(val),
        "c": str(n * n),
        "d": str(val + n),
    }
    quizzes_data.append(shuffle_options(q, str(val)))

# Generate 50 Time Complexity specific questions
for k in range(5, 55):
    q = {
        "q": f"O(n^{k}) vaqt murakkabligi polinom (polynomial) vaqtmi yoki eksponensial?",
        "a": "Eksponensial",
        "b": "Polinom",
        "c": "Ikkalasi ham",
        "d": "Logarifmik",
    }
    quizzes_data.append(shuffle_options(q, "Polinom"))

for m in range(2, 42):
    ans = 2 ** m
    q = {
        "q": f"Balandligi {m} ga teng bo'lgan to'liq Binar Daraxtda (Full Binary Tree) eng ko'pi bilan nechta barg (leaf node) bo'lishi mumkin?",
        "a": str(ans - 1),
        "b": str(ans),
        "c": str(ans * 2),
        "d": str(ans // 2),
    }
    quizzes_data.append(shuffle_options(q, str(ans)))

print(f"Jami {len(quizzes_data)} ta qiyin savollar tayyorlandi.")

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

print(f"Muvaffaqiyatli {count} ta qiyin quiz bazaga saqlandi!")
