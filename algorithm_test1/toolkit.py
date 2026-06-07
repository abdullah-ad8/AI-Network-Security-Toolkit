import customtkinter as ctk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import threading
import logging
from google import genai
import subprocess
import os
import sys

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import ARP, Ether, srp, IP, TCP, sr1

# ==========================================
# 1. Network Scanner Module (LIVE SCAN ENABLED)
# ==========================================
class NetworkScanner:
    def __init__(self, target_network, gateway_ip):
        self.target_network = target_network
        self.gateway_ip = gateway_ip
        # قائمة بأهم المنافذ التي نبحث عنها
        self.ports_to_scan = {21: 40, 22: 20, 80: 30, 443: 15, 3389: 50, 5432: 45, 8080: 25}

    def run_full_scan(self):
        print(f"\n[*] Initiating LIVE scan on network: {self.target_network}...")
        
        # 1. اكتشاف الأجهزة عبر بروتوكول ARP
        arp = ARP(pdst=self.target_network)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        result = srp(ether/arp, timeout=2, verbose=0)[0]

        live_hosts = []
        for sent, received in result:
            live_hosts.append(received.psrc)
            
        print(f"[+] Discovered {len(live_hosts)} active devices.")

        network_data = []

        # 2. فحص المنافذ لكل جهاز تم اكتشافه
        for ip in live_hosts:
            print(f"[*] Scanning ports for host: {ip} ...")
            open_ports = []
            for port in self.ports_to_scan:
                packet = IP(dst=ip) / TCP(dport=port, flags="S")
                response = sr1(packet, timeout=0.5, verbose=0)
                
                if response and response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
                    # إرسال حزمة RST لإغلاق الاتصال بأمان
                    sr1(IP(dst=ip)/TCP(dport=port, flags="R"), timeout=0.5, verbose=0)
                    open_ports.append(port)

            # 3. بناء هيكل الاتصال (بافتراض أن كل الأجهزة متصلة بالراوتر المحلي)
            if ip != self.gateway_ip:
                network_data.append({
                    "source": self.gateway_ip,
                    "target": ip,
                    "target_ports": open_ports
                })

        return network_data

# ==========================================
# 2. Topology Mapper Module (UPDATED WITH VISUALIZATION)
# ==========================================
class TopologyMapper:
    def __init__(self):
        self.graph = nx.Graph()

    def build_graph(self, network_data):
        print("[*] Building Network Topology Graph...")
        for connection in network_data:
            node_a = connection["source"]
            node_b = connection["target"]
            open_ports_b = connection["target_ports"]
            
            self.graph.add_node(node_a)
            self.graph.add_node(node_b, ports=open_ports_b)
            
            base_resistance = 100 
            vulnerability_discount = len(open_ports_b) * 20
            attack_weight = max(5, base_resistance - vulnerability_discount)
            
            self.graph.add_edge(node_a, node_b, weight=attack_weight)
        return self.graph

    def visualize_network(self, attack_path=None):
        """
        Draws the network graph and highlights the attack path if provided.
        """
        print("\n[*] Generating Network Topology Visualization...")
        plt.figure(figsize=(10, 7))
        
        # تحديد طريقة توزيع العقد في الرسم
        pos = nx.spring_layout(self.graph, seed=42) 
        
        # تلوين العقد بناءً على موقعها في مسار الهجوم
        node_colors = []
        for node in self.graph.nodes():
            if attack_path and node == attack_path[0]:
                node_colors.append('red') # المهاجم
            elif attack_path and node == attack_path[-1]:
                node_colors.append('green') # الهدف (الخادم الحساس)
            elif attack_path and node in attack_path:
                node_colors.append('orange') # أجهزة وسيطة مخترقة
            else:
                node_colors.append('skyblue') # أجهزة عادية
                
        # رسم العقد والروابط الأساسية
        nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, 
                node_size=3000, font_size=10, font_weight="bold", edge_color="gray")
        
        # رسم أوزان الروابط (درجة صعوبة الاختراق)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_color='red')
        
        # تحديد مسار الهجوم بخط عريض أحمر إذا تم اكتشافه
        if attack_path:
            path_edges = list(zip(attack_path, attack_path[1:]))
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, edge_color='red', width=2.5)
            
        plt.title("Network Topology & Vulnerability Attack Path", fontsize=14, fontweight='bold')
        plt.show() # عرض النافذة التي تحتوي على الرسم   

# ==========================================
# 3. Path Analyzer Module (UPDATED WITH BFS)
# ==========================================
class PathAnalyzer:
    def __init__(self, graph):
        self.graph = graph

    def find_shortest_attack_path(self, attacker_node, target_node):
        print("\n[*] Analyzing Attack Paths using Dijkstra's Algorithm...")
        try:
            path = nx.dijkstra_path(self.graph, source=attacker_node, target=target_node, weight='weight')
            cost = nx.dijkstra_path_length(self.graph, source=attacker_node, target=target_node, weight='weight')
            return path, cost
        except nx.NetworkXNoPath:
            return None, None

    def analyze_connectivity_bfs(self, start_node):
        """
        Connectivity Analysis using BFS to find reachable, 
        highly connected, and isolated nodes.
        """
        print(f"\n[*] Running BFS Connectivity Analysis starting from: {start_node}...")
        
        # 1. Discover all reachable devices using BFS
        reachable_nodes = list(nx.bfs_tree(self.graph, source=start_node).nodes())
        
        highly_connected = []
        isolated_devices = []

        # 2. Analyze network connectivity (Degree of nodes)
        for node in self.graph.nodes():
            degree = self.graph.degree(node) # Number of connections
            
            # If a device is connected to 3 or more devices, it's a central/hub node
            if degree >= 3: 
                highly_connected.append(node)
            # If a device has only 1 connection, it's an edge/isolated device
            elif degree <= 1: 
                isolated_devices.append(node)

        return {
            "reachable": reachable_nodes,
            "highly_connected": highly_connected,
            "isolated": isolated_devices
        }



# ==========================================
# 4. Threat Intelligence Module (AI) - UPDATED
# ==========================================
class ThreatIntelligence:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-3.1-flash-lite'

    def generate_report(self, attack_path, difficulty_score, network_data):
        print("[*] Generating AI Security Report...")
        prompt = f"""
        You are a cybersecurity expert. You have just analyzed a network using Dijkstra's algorithm to discover attack paths.
        
        Current Network Data:
        {network_data}
        
        Most dangerous attack path discovered: {' -> '.join(attack_path)}
        Penetration difficulty score (lower means easier to hack): {difficulty_score}
        
        Based on this data:
        1. Explain the threat simply and readably for management.
        2. State why this path is dangerous (based on open ports).
        3. Suggest two practical steps to close this vulnerability.
        
        Write the response entirely in English and in a professional tone.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"[-] Error with AI Module: {e}"
        


class ConsoleRedirector:
    """
    هذا الكلاس يصطاد مخرجات الـ Print ويوجهها إلى مربع النص في الواجهة.
    """
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert("end", string)
        self.text_widget.see("end") # التمرير التلقائي للأسفل لرؤية أحدث سطر

    def flush(self):
        pass
        



class SecurityDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Network Security & Auto-Mitigation Toolkit")
        self.geometry("1250x850")
        ctk.set_appearance_mode("dark")

        # إخبار البرنامج بتشغيل دالة الإغلاق الآمن عند الضغط على (X)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # إعدادات تقنية
        self.api_key = "AIzaSyDidTWweGP6-TzfwW9xHYdRg3WnJWlVS0Y"
        self.target_subnet = "192.168.1.1/24"
        self.gateway_ip = "192.168.1.1"
        self.detected_vulnerability = None # لتخزين بيانات الثغرة المكتشفة

       # تقسيم الواجهة (Sidebar & Main Area)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- القائمة الجانبية ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="Network Security Toolkit", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.pack(pady=30, padx=10)

        self.scan_btn = ctk.CTkButton(self.sidebar, text="Scan & Analyze", command=self.start_scan_thread, height=40)
        self.scan_btn.pack(pady=10, padx=20)

        self.fix_btn = ctk.CTkButton(self.sidebar, text="🛡️ Fix Vulnerability", 
                                     command=self.apply_mitigation, 
                                     fg_color="#28a745", hover_color="#218838",
                                     state="disabled")
        self.fix_btn.pack(pady=10, padx=20)

        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Waiting", text_color="gray")
        self.status_label.pack(side="bottom", pady=20)

        # --- المنطقة الرئيسية ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=3) # قسم الرسم والتقرير يأخذ مساحة أكبر
        self.main_frame.grid_rowconfigure(1, weight=1) # قسم التيرمينال يأخذ مساحة أقل

        # 1. عرض الخريطة (أعلى اليسار)
        self.graph_frame = ctk.CTkFrame(self.main_frame)
        self.graph_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # 2. عرض التقرير (أعلى اليمين)
        self.report_text = ctk.CTkTextbox(self.main_frame, font=("Consolas", 13))
        self.report_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.report_text.insert("0.0", "System ready. Click 'Scan' to begin...")

        # 3. شاشة التيرمينال المباشرة (الأسفل)
        self.console_frame = ctk.CTkFrame(self.main_frame)
        self.console_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.console_label = ctk.CTkLabel(self.console_frame, text=">_ Live Terminal Output", font=ctk.CTkFont(weight="bold"))
        self.console_label.pack(anchor="w", padx=10, pady=(5, 0))
        
        # تصميم التيرمينال (أسود وأخضر)
        self.console_text = ctk.CTkTextbox(self.console_frame, font=("Consolas", 12), text_color="#00FF00", fg_color="#1e1e1e")
        self.console_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.console_text.insert("end", "Initialize Engine...\n")

        # ربط مخرجات النظام (print) بمربع التيرمينال الجديد
        sys.stdout = ConsoleRedirector(self.console_text)
        sys.stderr = ConsoleRedirector(self.console_text)

    def start_scan_thread(self):
        self.scan_btn.configure(state="disabled")
        self.fix_btn.configure(state="disabled")
        self.status_label.configure(text="Status: Scanning Network...", text_color="orange")
        self.console_text.insert("end", "\n" + "="*40 + "\n[*] NEW SCAN INITIATED...\n" + "="*40 + "\n")
        threading.Thread(target=self.run_full_operation, daemon=True).start()

    

    def on_closing(self):
        """
        تعمل هذه الدالة عند إغلاق البرنامج للتأكد من قتل كل 
        العمليات التي تعمل في الخلفية ومنع أخطاء الـ Terminal
        """
        print("[*] Shutting down AI Toolkit and background threads safely...")
        self.destroy()  # تدمير الواجهة الرسومية
        os._exit(0)     # إجبار النظام على إنهاء البايثون وكل الـ Threads فوراً



    def run_full_operation(self):
        try:
            # 1. الفحص الحي (نستخدم الكلاسات السابقة)
            scanner = NetworkScanner(self.target_subnet, self.gateway_ip)
            live_data = scanner.run_full_scan()

            if not live_data:
                self.update_status("No devices found", "red")
                return

            mapper = TopologyMapper()
            graph = mapper.build_graph(live_data)
            analyzer = PathAnalyzer(graph)

            best_path, path_cost = self.find_weakest_link(analyzer, live_data)
            
            if best_path and len(best_path) > 1:
                target_ip = best_path[-1]
                for d in live_data:
                    if d["target"] == target_ip and d["target_ports"]: 
                        self.detected_vulnerability = {"ip": target_ip, "port": d["target_ports"][0]}
                        break

            ai_module = ThreatIntelligence(self.api_key)
            report = ai_module.generate_report(best_path, path_cost, live_data)

            self.after(0, lambda: self.update_ui(graph, best_path, report))

        except Exception as e:
            print(f"\n[-] SYSTEM ERROR: {e}\n") # هذه الـ print ستظهر في واجهة التيرمينال الجديدة
            self.after(0, lambda: messagebox.showerror("System Error", str(e)))
            self.update_status("Error", "red")

    def find_weakest_link(self, analyzer, data):
        lowest_cost = float('inf')
        best_path = None
        for device in data:
            path, cost = analyzer.find_shortest_attack_path(self.gateway_ip, device["target"])
            if cost is not None and cost < lowest_cost:
                lowest_cost = cost
                best_path = path
        return best_path, lowest_cost

    def apply_mitigation(self):
        if not self.detected_vulnerability: return
        ip = self.detected_vulnerability["ip"]
        port = self.detected_vulnerability["port"]
        
        print(f"[*] Attempting to block Port {port} on {ip}...")
        rule_name = f"Block_Vulnerable_Port_{port}"
        cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block protocol=TCP localport={port}'
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"[+] SUCCESS: Firewall rule applied. Port {port} secured.")
            messagebox.showinfo("Success", f"Security Mitigation Applied!\nPort {port} has been blocked to secure {ip}.")
            self.fix_btn.configure(state="disabled", text="🛡️ Protected")
        except:
            print("[-] FAILED: Insufficient privileges. Please run as Administrator.")
            messagebox.showerror("Permission Denied", "Please run this app as Administrator to fix vulnerabilities.")

    def update_ui(self, graph, best_path, report):
        self.report_text.delete("0.0", "end")
        self.report_text.insert("0.0", report)

        # حذف الرسم القديم قبل إضافة الجديد
        for widget in self.graph_frame.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg): widget.get_tk_widget().destroy()

        # إعداد خلفية الرسم
        fig, ax = plt.subplots(figsize=(10, 5), facecolor="#2b2b2bac")
        ax.set_facecolor("#2b2b2ba5")
        pos = nx.spring_layout(graph)

        # 1. رسم العقد (الأجهزة) وأرقام الـ IP
        # تم تغيير font_color إلى 'yellow' (أصفر) ليكون واضحاً جداً
        # تم إضافة node_size=2500 لتكبير الدائرة الزرقاء حتى تسع النص
        nx.draw(graph, pos, ax=ax, with_labels=True, node_color='#1f538d', 
                edge_color='gray', font_color='yellow', font_size=10, 
                font_weight='bold', node_size=4000)
        
        # 2. رسم الأوزان (Weights) على الروابط
        # تم إضافتها للواجهة الرسومية بلون أحمر فاتح '#ff4d4d'
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, 
                                     font_color="#4dff684c", font_size=20, ax=ax)
        
        # رسم مسار الهجوم باللون الأحمر العريض إذا وُجد
        if best_path:
            path_edges = list(zip(best_path, best_path[1:]))
            nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='#e74c3c', width=3, ax=ax)
            self.fix_btn.configure(state="normal") # تفعيل زر الإصلاح

        # عرض الرسمة على الواجهة
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.scan_btn.configure(state="normal")
        self.status_label.configure(text="Status: Safe / Analysis Complete", text_color="green")


    def update_status(self, text, color):
        self.status_label.configure(text=f"Status: {text}", text_color=color)
        self.scan_btn.configure(state="normal")



# ==========================================
# Main Execution Flow
# ==========================================
def main():
    """
    API_KEY = "AIzaSyDidTWweGP6-TzfwW9xHYdRg3WnJWlVS0Y" # ضع مفتاحك الحقيقي هنا
    
    # 1. إعدادات الشبكة المحلية (تأكد من مطابقتها لشبكتك، استخدم ipconfig لمعرفتها)
    # عادة ما يكون الراوتر 192.168.1.1 أو 192.168.0.1
    target_subnet = "192.168.1.1/24"
    gateway_ip = "192.168.1.1" 
    
    # 2. تشغيل الفحص الحي
    scanner = NetworkScanner(target_subnet, gateway_ip)
    live_network_data = scanner.run_full_scan()
    
    # التحقق مما إذا تم اكتشاف أجهزة
    if not live_network_data:
        print("[-] No devices found or scan failed. Check your network range and permissions.")
        return

    # 3. بناء الخريطة باستخدام البيانات الحقيقية
    mapper = TopologyMapper()
    attack_graph = mapper.build_graph(live_network_data)
    
    analyzer = PathAnalyzer(attack_graph)
    
    # نطلب من الخوارزمية البحث عن مسار من الراوتر إلى أي جهاز آخر التقطناه
    # يمكنك تغيير الهدف لاحقاً لأي IP محدد التقطته الأداة
    start_point = gateway_ip
    # ---------------------------------------------------------
    # NEW LOGIC: Automatically find the absolute weakest target 
    # (The one with the lowest path cost from the attacker)
    # ---------------------------------------------------------
    start_point = gateway_ip
    
    best_path = None
    lowest_cost = float('inf') # نبدأ بقيمة لا نهائية
    weakest_target = None
    
    # Loop through all discovered devices to find the most vulnerable one
    for device in live_network_data:
        target = device["target"]
        path, cost = analyzer.find_shortest_attack_path(start_point, target)
        
        # If this target is easier to hack (lower cost), update our target
        if cost is not None and cost < lowest_cost:
            lowest_cost = cost
            weakest_target = target
            best_path = path

    path_cost = lowest_cost
    # ---------------------------------------------------------
    

    # تشغيل تحليل BFS الجديد
    connectivity_results = analyzer.analyze_connectivity_bfs(start_point)
    
    print("\n--- BFS Connectivity Analysis Results ---")
    print(f"Reachable Devices: {connectivity_results['reachable']}")
    print(f"Highly Connected Nodes (Critical Hubs): {connectivity_results['highly_connected']}")
    print(f"Isolated/Edge Devices: {connectivity_results['isolated']}")
    print("-----------------------------------------")
    
    if best_path:
        print(f"\n[!] VULNERABLE PATH DETECTED: {' -> '.join(best_path)}")
        print(f"[!] Path Difficulty Cost: {path_cost}\n")
        
        ai_module = ThreatIntelligence(API_KEY)
        # PASS THE LIVE DATA INSTEAD OF THE SIMULATED DATA
        report = ai_module.generate_report(best_path, path_cost, live_network_data)
        
        print("================ AI SECURITY REPORT ================")
        print(report)
        print("====================================================")
        
        # DRAW THE GRAPH AND HIGHLIGHT THE ATTACK PATH
        mapper.visualize_network(best_path)
    else:
        print("\n[+] Network is secure. No direct path found.")
        # YOU CAN STILL DRAW THE NETWORK EVEN IF SECURE
        mapper.visualize_network()
        """


if __name__ == "__main__":
    app = SecurityDashboard()
    app.mainloop()