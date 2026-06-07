import networkx as nx
import logging
import matplotlib.pyplot as plt # أضفنا مكتبة الرسم هنا
from google import genai # استخدام المكتبة الجديدة
# import scapy.all as scapy 

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
        # تهيئة العميل باستخدام المكتبة الجديدة
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
            # طريقة الاستدعاء الجديدة
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"[-] Error with AI Module: {e}"

# ==========================================
# Main Execution Flow
# ==========================================
def main():
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

if __name__ == "__main__":
    main()