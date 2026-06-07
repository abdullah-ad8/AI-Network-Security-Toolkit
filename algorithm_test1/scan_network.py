from scapy.all import ARP, Ether, srp

def scan_network(ip_range):
    """
    تقوم هذه الدالة بإرسال طلب ARP لاكتشاف الأجهزة المتصلة بالشبكة
    """
    print(f"\n[*] Scanning network range: {ip_range} ...")
    
    # إنشاء طلب ARP لمدى الـ IPs المحدد
    arp = ARP(pdst=ip_range)
    # إنشاء حزمة إيثرنت (Broadcast) لتصل للجميع
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # دمج الحزمتين
    packet = ether/arp
    
    # إرسال الحزمة واستقبال الردود (timeout قليل لسرعة الفحص)
    result = srp(packet, timeout=2, verbose=0)[0]
    
    devices = []
    # استخراج الـ IP والـ MAC Address من ردود الأجهزة
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
        
    return devices

# ----- تجربة الدالة الجديدة -----
if __name__ == "__main__":
    # ضع هنا المدى الخاص بشبكتك (غالباً يكون بهذا الشكل للراوترات المنزلية)
    # يمكنك معرفة مدى شبكتك من خلال كتابة ipconfig في موجه الأوامر
    target_network = "192.168.1.1/24" 
    
    active_devices = scan_network(target_network)
    
    print("\n--- Active Devices Found ---")
    for device in active_devices:
        print(f"IP: {device['ip']}\t MAC: {device['mac']}")