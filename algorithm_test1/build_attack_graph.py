import networkx as nx

def build_attack_graph(network_data):
    """بناء خريطة الشبكة وتحديد أوزان الهجوم"""
    G = nx.Graph()
    
    # إضافة الأجهزة كعقد (Nodes) وتمثيل الاتصالات كحواف (Edges)
    for connection in network_data:
        node_a = connection["source"]
        node_b = connection["target"]
        open_ports_b = connection["target_ports"]
        
        G.add_node(node_a)
        G.add_node(node_b, ports=open_ports_b)
        
        # حساب المقاومة: كلما زادت المنافذ المفتوحة، قلّت المقاومة أمام المهاجم
        # وضعنا وزن افتراضي عالي (100) للأنظمة المغلقة
        base_resistance = 100 
        vulnerability_discount = len(open_ports_b) * 20
        
        # نضمن أن الوزن لا يصبح سالباً أو صفراً
        attack_weight = max(5, base_resistance - vulnerability_discount)
        
        # إضافة الرابط مع الوزن المحسوب
        G.add_edge(node_a, node_b, weight=attack_weight)
        
    return G

def find_shortest_attack_path(G, attacker_node, target_node):
    """استخدام خوارزمية ديكسترا لإيجاد أقصر مسار للمهاجم"""
    try:
        # خوارزمية ديكسترا المدمجة في NetworkX
        path = nx.dijkstra_path(G, source=attacker_node, target=target_node, weight='weight')
        path_cost = nx.dijkstra_path_length(G, source=attacker_node, target=target_node, weight='weight')
        return path, path_cost
    except nx.NetworkXNoPath:
        return None, None

if __name__ == "__main__":
    # محاكاة لبيانات تم جمعها من الشبكة (بدلاً من الفحص الحي لتسريع التجربة)
    # جهاز المهاجم متصل بجهازين، وهناك مسارات مختلفة للوصول إلى الخادم الحساس
    simulated_network = [
        {"source": "Attacker_PC", "target": "HR_Laptop", "target_ports": []}, # جهاز آمن
        {"source": "Attacker_PC", "target": "Dev_PC", "target_ports": [22, 80]}, # جهاز مطور فيه منافذ مفتوحة
        {"source": "HR_Laptop", "target": "Main_Server", "target_ports": [443, 5432]},
        {"source": "Dev_PC", "target": "Main_Server", "target_ports": [443, 5432]}
    ]

    print("[*] Building Network Topology Graph...")
    attack_graph = build_attack_graph(simulated_network)
    
    print("\n[*] Analyzing Attack Paths using Dijkstra's Algorithm...")
    start_point = "Attacker_PC"
    end_point = "Main_Server"
    
    # تحليل المسار الأقصر باستخدام خوارزمية ديكسترا
    best_path, total_difficulty = find_shortest_attack_path(attack_graph, start_point, end_point)
    
    if best_path:
        print(f"\n[!!!] VULNERABILITY DETECTED [!!!]")
        print(f"Most Efficient Attack Path: {' -> '.join(best_path)}")
        print(f"Total Attack Difficulty Score (Lower is worse): {total_difficulty}")
    else:
        print("\n[+] Network is secure. No direct path found to the target.")