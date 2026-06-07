import google.generativeai as genai

# ستحتاج إلى وضع مفتاح الـ API الخاص بك هنا
# يمكنك الحصول عليه مجاناً من منصة Google AI Studio
API_KEY = "AIzaSyDidTWweGP6-TzfwW9xHYdRg3WnJWlVS0Y" 
genai.configure(api_key=API_KEY)

def generate_security_report(attack_path, difficulty_score, simulated_network):
    """
    هذه الدالة تأخذ نتائج التحليل والخوارزميات 
    وترسلها لنموذج Gemini لتوليد تقرير أمني مقروء باللغة الإنجليزية.
    """
    print("[*] Sending data to Gemini AI Module for analysis...\n")
    
    # تجهيز الـ Prompt باللغة الإنجليزية لضمان أن المخرجات ستكون بالإنجليزية فقط
    prompt = f"""
    You are a cybersecurity expert. You have just analyzed a network using Dijkstra's algorithm to discover attack paths.
    
    Current Network Data:
    {simulated_network}
    
    Most dangerous attack path discovered: {' -> '.join(attack_path)}
    Penetration difficulty score (lower means easier to hack): {difficulty_score}
    
    Based on this data:
    1. Explain the threat simply and readably for management.
    2. State why this path is dangerous (based on open ports).
    3. Suggest two practical steps to close this vulnerability.
    
    Write the response entirely in English and in a professional tone.
    """
    
    try:
        # إعداد واستدعاء نموذج Gemini (استخدمنا النموذج المستقر)
        model = genai.GenerativeModel('gemini-3.1-flash-lite')
        response = model.generate_content(prompt)
        
        # استخراج النص من الرد
        return response.text
        
    except Exception as e:
        return f"[-] Error communicating with Gemini AI: {e}"

# ----- تجربة الكود -----
if __name__ == "__main__":
    best_path = ['Attacker_PC', 'Dev_PC', 'Main_Server']
    total_difficulty = 65
    simulated_network = [
        {"source": "Attacker_PC", "target": "HR_Laptop", "target_ports": []},
        {"source": "Attacker_PC", "target": "Dev_PC", "target_ports": [22, 80]},
        {"source": "HR_Laptop", "target": "Main_Server", "target_ports": [443, 5432]},
        {"source": "Dev_PC", "target": "Main_Server", "target_ports": [443, 5432]}
    ]
    
    final_report = generate_security_report(best_path, total_difficulty, simulated_network)
    
    print("================ SECURITY REPORT ================")
    print(final_report)
    print("=================================================")