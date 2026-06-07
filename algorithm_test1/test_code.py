import google.generativeai as genai

# ضع المفتاح الخاص بك هنا
API_KEY = "AIzaSyDidTWweGP6-TzfwW9xHYdRg3WnJWlVS0Y"
genai.configure(api_key=API_KEY)

print("--- النماذج المتاحة التي تدعم توليد النصوص ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)