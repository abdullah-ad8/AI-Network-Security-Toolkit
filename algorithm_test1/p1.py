from scapy.all import ARP, Ether, srp, IP, TCP, sr1
import logging

# إيقاف رسائل التحذير الخاصة بمكتبة Scapy
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def scan_network(ip_range):
    """اكتشاف الأجهزة المتصلة بالشبكة باستخدام ARP"""
    print(f"\n[*] Scanning network range: {ip_range} for active devices...")
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    
    # إرسال الحزمة واستقبال الردود
    result = srp(packet, timeout=2, verbose=0)[0]
    
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
        
    return devices

def scan_port(target_ip, port):
    """فحص منفذ معين على جهاز محدد"""
    packet = IP(dst=target_ip) / TCP(dport=port, flags="S")
    response = sr1(packet, timeout=0.5, verbose=0) # قللنا الوقت لتسريع الفحص
    
    if response is None:
        return False
    elif response.haslayer(TCP):
        if response.getlayer(TCP).flags == 0x12:
            sr1(IP(dst=target_ip)/TCP(dport=port, flags="R"), timeout=0.5, verbose=0)
            return True
    return False

if __name__ == "__main__":
    # ضع المدى الخاص بشبكتك المحلية هنا (مثل 192.168.1.1/24)
    target_network = "192.168.1.1/24" 
    
    # قائمة بأهم المنافذ الشائعة للبحث عنها
    ports_to_scan = [21, 22, 80, 443, 3389, 5432, 8080] 
    
    # 1. اكتشاف الأجهزة
    active_devices = scan_network(target_network)
    
    print("\n--- Active Devices & Open Ports ---")
    if not active_devices:
        print("No devices found. Check your network range.")
    else:
        # 2. فحص المنافذ لكل جهاز تم اكتشافه
        for device in active_devices:
            ip = device['ip']
            mac = device['mac']
            print(f"\n[+] Device Found: IP: {ip} | MAC: {mac}")
            
            open_ports = []
            for port in ports_to_scan:
                if scan_port(ip, port):
                    open_ports.append(port)
            
            if open_ports:
                print(f"    -> Open Ports: {open_ports}")
            else:
                print("    -> No open ports found from the given list.")
                
    print("\n--- Full Network Scan Completed ---")