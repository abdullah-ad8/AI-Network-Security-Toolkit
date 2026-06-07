from scapy.all import IP, TCP, sr1
import logging

# إيقاف رسائل التحذير الخاصة بمكتبة Scapy لتنظيف المخرجات
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def scan_port(target_ip, port):
    
   # تقوم هذه الدالة بفحص منفذ معين على جهاز محدد 
   # وإرجاع True إذا كان مفتوحاً، و False إذا كان مغلقاً.
    
    print(f"[*] Scanning {target_ip} on port {port}...")
    
    # بناء حزمة البيانات: طبقة IP + طبقة TCP مع تفعيل علامة SYN
    packet = IP(dst=target_ip) / TCP(dport=port, flags="S")
    
    # إرسال الحزمة وانتظار رد واحد (timeout=1 حتى لا ننتظر للأبد)
    response = sr1(packet, timeout=1, verbose=0)
    
    # تحليل الرد
    if response is None:
        return False # لا يوجد رد (غالباً المنفذ مفلتر أو الجهاز مغلق)
    elif response.haslayer(TCP):
        # 0x12 تعني أن الأعلام هي SYN و ACK
        if response.getlayer(TCP).flags == 0x12:
            # إرسال حزمة RST لإغلاق الاتصال بأمان
            sr1(IP(dst=target_ip)/TCP(dport=port, flags="R"), timeout=1, verbose=0)
            return True
    return False

# ----- تجربة الكود -----
if __name__ == "__main__":
    # يمكنك وضع الـ IP الخاص بجهازك المحلي (localhost) للتجربة
    target = "127.0.0.1" 
    ports_to_scan = [21, 22, 80, 443, 8080, 5432] # قائمة منافذ شائعة
    
    open_ports = []
    
    print(f"--- Starting Scan on {target} ---")
    for p in ports_to_scan:
        if scan_port(target, p):
            print(f"[+] Port {p} is OPEN")
            open_ports.append(p)
        else:
            print(f"[-] Port {p} is CLOSED or FILTERED")
            
    print("\n--- Scan Completed ---")
    print(f"Open Ports: {open_ports}")





