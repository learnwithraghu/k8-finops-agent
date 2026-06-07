#!/usr/bin/env python3
import os

def generate_svg():
    width = 1050
    height = 1030
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
    
    svg.append("""  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap');
    
    svg {
      background-color: #0b1329;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Grid background */
    .grid {
      fill: none;
      stroke: #1e293b;
      stroke-width: 1;
      opacity: 0.15;
    }
    
    /* Cluster enclosing box */
    .cluster-card {
      fill: #0c152b;
      stroke: #38bdf8;
      stroke-width: 2.5;
      rx: 20px;
      ry: 20px;
    }
    
    .cluster-title {
      font-size: 18px;
      font-weight: 700;
      fill: #38bdf8;
      letter-spacing: -0.01em;
    }
    
    /* Card design with glassmorphism values */
    .ns-card {
      fill: #111b36;
      stroke: #2a3a60;
      stroke-width: 1.5;
      rx: 16px;
      ry: 16px;
      transition: all 0.3s ease;
    }
    
    .ns-card:hover {
      stroke: #3b528c;
    }
    
    .ns-card-warning {
      fill: #1a1527;
      stroke: #7f1d1d;
      stroke-dasharray: 6,4;
    }
    
    .ns-card-warning:hover {
      stroke: #b91c1c;
    }
    
    /* Typography styling */
    .title {
      font-size: 26px;
      font-weight: 700;
      fill: #f8fafc;
      letter-spacing: -0.025em;
    }
    
    .subtitle {
      font-size: 14px;
      fill: #94a3b8;
      font-weight: 400;
    }
    
    .ns-title {
      font-size: 15px;
      font-weight: 700;
      fill: #f1f5f9;
      letter-spacing: -0.01em;
    }
    
    .ns-tag {
      font-size: 10px;
      font-weight: 600;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: 0.05em;
    }
    
    .node-text {
      font-size: 12px;
      font-weight: 600;
      fill: #e2e8f0;
      text-anchor: middle;
    }
    
    .node-subtext {
      font-size: 9px;
      font-weight: 500;
      fill: #64748b;
      text-anchor: middle;
      font-family: 'JetBrains Mono', monospace;
    }
    
    /* Node styling */
    .node-bg-svc {
      fill: url(#grad-svc);
      stroke: #10b981;
      stroke-width: 1.5;
      filter: drop-shadow(0 2px 8px rgba(16, 185, 129, 0.15));
    }
    
    .node-bg-pod {
      fill: url(#grad-pod);
      stroke: #0ea5e9;
      stroke-width: 1.5;
      filter: drop-shadow(0 2px 8px rgba(14, 165, 233, 0.15));
    }
    
    .node-bg-cm {
      fill: url(#grad-cm);
      stroke: #eab308;
      stroke-width: 1.5;
      filter: drop-shadow(0 2px 8px rgba(234, 179, 8, 0.1));
    }
    
    .node-bg-pvc {
      fill: url(#grad-pvc);
      stroke: #a855f7;
      stroke-width: 1.5;
      filter: drop-shadow(0 2px 8px rgba(168, 85, 247, 0.1));
    }
    
    .node-bg-warning {
      fill: url(#grad-warning);
      stroke: #ef4444;
      stroke-width: 2;
      filter: drop-shadow(0 4px 12px rgba(239, 68, 68, 0.2));
    }
    
    /* Interactive nodes */
    .node-group {
      cursor: pointer;
    }
    .node-group:hover .node-bg-svc { stroke-width: 2.5; filter: drop-shadow(0 4px 12px rgba(16, 185, 129, 0.3)); }
    .node-group:hover .node-bg-pod { stroke-width: 2.5; filter: drop-shadow(0 4px 12px rgba(14, 165, 233, 0.3)); }
    .node-group:hover .node-bg-cm  { stroke-width: 2.5; filter: drop-shadow(0 4px 12px rgba(234, 179, 8, 0.25)); }
    .node-group:hover .node-bg-pvc { stroke-width: 2.5; filter: drop-shadow(0 4px 12px rgba(168, 85, 247, 0.25)); }
    .node-group:hover .node-bg-warning { stroke-width: 3; filter: drop-shadow(0 6px 16px rgba(239, 68, 68, 0.4)); }
    
    /* Connections */
    .conn-line {
      fill: none;
      stroke: #475569;
      stroke-width: 1.5;
      stroke-linecap: round;
      marker-end: url(#arrow);
    }
    
    .conn-dashed {
      fill: none;
      stroke: #64748b;
      stroke-width: 1.5;
      stroke-dasharray: 4,4;
      marker-end: url(#arrow-dashed);
    }
    
    .conn-storage {
      fill: none;
      stroke: #64748b;
      stroke-width: 1.5;
      marker-end: url(#arrow-storage);
    }
    
    /* Badge styling */
    .badge-bg {
      fill: #1e293b;
      stroke: #475569;
      stroke-width: 1;
      rx: 6px;
      ry: 6px;
    }
    
    .badge-warning-bg {
      fill: #7f1d1d;
      stroke: #f87171;
      stroke-width: 1;
      rx: 6px;
      ry: 6px;
    }
    
    .badge-text {
      font-size: 10px;
      font-weight: 600;
      fill: #f1f5f9;
      text-anchor: middle;
      font-family: 'JetBrains Mono', monospace;
    }
  </style>
  
  <defs>
    <!-- Background grid -->
    <pattern id="grid-pattern" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" class="grid" />
    </pattern>
    
    <!-- Gradients -->
    <linearGradient id="grad-svc" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#064e3b" />
      <stop offset="100%" stop-color="#022c22" />
    </linearGradient>
    
    <linearGradient id="grad-pod" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0c4a6e" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    
    <linearGradient id="grad-cm" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#78350f" />
      <stop offset="100%" stop-color="#451a03" />
    </linearGradient>
    
    <linearGradient id="grad-pvc" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4c1d95" />
      <stop offset="100%" stop-color="#2e1065" />
    </linearGradient>
    
    <linearGradient id="grad-warning" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#991b1b" />
      <stop offset="100%" stop-color="#450a0a" />
    </linearGradient>
    
    <!-- Markers -->
    <marker id="arrow" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#10b981" />
    </marker>
    
    <marker id="arrow-dashed" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#eab308" />
    </marker>
    
    <marker id="arrow-storage" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#a855f7" />
    </marker>
    
    <!-- Icon Shapes -->
    <g id="icon-svc">
      <circle cx="0" cy="0" r="14" fill="none" stroke="#34d399" stroke-width="1.5" />
      <circle cx="0" cy="0" r="3" fill="#34d399" />
      <circle cx="-6" cy="-6" r="2" fill="#34d399" />
      <circle cx="-6" cy="6" r="2" fill="#34d399" />
      <circle cx="7" cy="0" r="2" fill="#34d399" />
      <line x1="0" y1="0" x2="-6" y2="-6" stroke="#34d399" stroke-width="1" />
      <line x1="0" y1="0" x2="-6" y2="6" stroke="#34d399" stroke-width="1" />
      <line x1="0" y1="0" x2="7" y2="0" stroke="#34d399" stroke-width="1" />
    </g>
    
    <g id="icon-pod">
      <polygon points="0,-16 13.86,-8 13.86,8 0,16 -13.86,8 -13.86,-8" fill="none" stroke="#38bdf8" stroke-width="1.8" />
      <line x1="0" y1="-16" x2="0" y2="16" stroke="#38bdf8" stroke-width="1" opacity="0.4" />
      <line x1="0" y1="0" x2="13.86" y2="8" stroke="#38bdf8" stroke-width="1" opacity="0.4" />
      <line x1="0" y1="0" x2="-13.86" y2="8" stroke="#38bdf8" stroke-width="1" opacity="0.4" />
    </g>
    
    <g id="icon-cm">
      <path d="M -9,-12 L 3,-12 L 9,-6 L 9,12 L -9,12 Z" fill="none" stroke="#facc15" stroke-width="1.5" />
      <path d="M 3,-12 L 3,-6 L 9,-6" fill="none" stroke="#facc15" stroke-width="1.5" />
      <line x1="-5" y1="-2" x2="5" y2="-2" stroke="#facc15" stroke-width="1.2" opacity="0.8" />
      <line x1="-5" y1="2" x2="5" y2="2" stroke="#facc15" stroke-width="1.2" opacity="0.8" />
      <line x1="-5" y1="6" x2="1" y2="6" stroke="#facc15" stroke-width="1.2" opacity="0.8" />
    </g>
    
    <g id="icon-pvc">
      <path d="M -10,-8 A 10,4 0 0,1 10,-8 L 10,6 A 10,4 0 0,1 -10,6 Z" fill="none" stroke="#c084fc" stroke-width="1.5" />
      <ellipse cx="0" cy="-8" rx="10" ry="4" fill="none" stroke="#c084fc" stroke-width="1.5" />
      <path d="M -10,-1 A 10,4 0 0,0 10,-1" fill="none" stroke="#c084fc" stroke-width="1.5" opacity="0.8" />
      <path d="M -10,6 A 10,4 0 0,0 10,6" fill="none" stroke="#c084fc" stroke-width="1.5" opacity="0.8" />
    </g>
    
    <g id="icon-warning">
      <polygon points="0,-14 14,10 -14,10" fill="#ef4444" stroke="#f87171" stroke-width="1.5" />
      <circle cx="0" cy="6" r="1.5" fill="#ffffff" />
      <line x1="0" y1="-6" x2="0" y2="2" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" />
    </g>
  </defs>
  
  <!-- Background Grid -->
  <rect width="{width}" height="{height}" fill="url(#grid-pattern)" />
""")
    
    # ----------------------------------------------------
    # Header Section
    # ----------------------------------------------------
    svg.append(f"""  <!-- Header Section -->
  <g transform="translate(40, 50)">
    <text class="title" x="0" y="0">Airline Workload Architecture Diagram</text>
    <text class="subtitle" x="0" y="22">Visualizing deployed Kubernetes resources inside the cluster boundaries.</text>
  </g>
""")
    
    # ----------------------------------------------------
    # Legend Section (Top Right)
    # ----------------------------------------------------
    svg.append(f"""  <!-- Legend Section -->
  <g transform="translate(560, 32)">
    <rect width="440" height="56" fill="#0f172a" stroke="#1e293b" stroke-width="1" rx="8" ry="8" />
    <g transform="translate(25, 28)">
      <circle cx="0" cy="0" r="10" fill="#022c22" stroke="#10b981" stroke-width="1.5" />
      <circle cx="0" cy="0" r="2.5" fill="#10b981" />
      <text x="16" y="4" fill="#94a3b8" font-size="11" font-weight="600">Service</text>
    </g>
    <g transform="translate(110, 28)">
      <polygon points="0,-9 7.79,-4.5 7.79,4.5 0,9 -7.79,4.5 -7.79,-4.5" fill="#0f172a" stroke="#0ea5e9" stroke-width="1.5" />
      <text x="16" y="4" fill="#94a3b8" font-size="11" font-weight="600">Pod</text>
    </g>
    <g transform="translate(245, 28)">
      <rect x="-7" y="-9" width="14" height="18" rx="2" fill="#451a03" stroke="#eab308" stroke-width="1.5" />
      <line x1="-3" y1="-3" x2="3" y2="-3" stroke="#eab308" stroke-width="1" />
      <line x1="-3" y1="1" x2="3" y2="1" stroke="#eab308" stroke-width="1" />
      <text x="16" y="4" fill="#94a3b8" font-size="11" font-weight="600">ConfigMap</text>
    </g>
    <g transform="translate(355, 28)">
      <rect x="-7" y="-7" width="14" height="14" rx="2" fill="#2e1065" stroke="#a855f7" stroke-width="1.5" />
      <line x1="-7" y1="-2" x2="7" y2="-2" stroke="#a855f7" stroke-width="1" />
      <line x1="-7" y1="2" x2="7" y2="2" stroke="#a855f7" stroke-width="1" />
      <text x="16" y="4" fill="#94a3b8" font-size="11" font-weight="600">Storage (PVC)</text>
    </g>
  </g>
""")

    # ----------------------------------------------------
    # SINGLE KUBERNETES CLUSTER CONTAINER
    # ----------------------------------------------------
    svg.append(f"""  <!-- Kubernetes Cluster Box -->
  <g transform="translate(20, 110)">
    <rect class="cluster-card" width="1010" height="880" />
    <!-- Cluster Label -->
    <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 360 0 L 340 36 L 0 36 Z" fill="#1e3a8a" stroke="#38bdf8" stroke-width="1.5" />
    <text class="cluster-title" x="20" y="23">☸️ Kubernetes Cluster (finops-cluster)</text>
  </g>
""")

    # Helper function to generate namespace cards
    def create_namespace(name, x, y, w, h, style_class="ns-card", labels_list=None):
        ns_svg = []
        ns_svg.append(f'  <!-- Namespace: {name} -->')
        ns_svg.append(f'  <g transform="translate({x}, {y})">')
        ns_svg.append(f'    <rect class="ns-card {style_class}" width="{w}" height="{h}" />')
        
        # Namespace label banner (top-left)
        ns_svg.append(f'    <path d="M 0 12 C 0 5.37 5.37 0 12 0 L 150 0 L 135 30 L 0 30 Z" fill="#1e293b" stroke="#2a3a60" stroke-width="1" />')
        ns_svg.append(f'    <text class="ns-title" x="12" y="19">{name}</text>')
        
        # Display tags if present
        if labels_list:
            lx = 165
            for label in labels_list:
                lbl_txt = f"{label[0]}={label[1]}"
                text_len = len(lbl_txt) * 6.5
                ns_svg.append(f'    <g transform="translate({lx}, 6)">')
                ns_svg.append(f'      <rect width="{text_len}" height="18" rx="4" ry="4" fill="#1e293b" stroke="#334155" stroke-width="1" />')
                ns_svg.append(f'      <text x="{text_len/2}" y="12" fill="#94a3b8" class="ns-tag" text-anchor="middle">{lbl_txt}</text>')
                ns_svg.append(f'    </g>')
                lx += text_len + 8
        ns_svg.append(f'  </g>')
        return "\n".join(ns_svg)

    # Helper function to create resource nodes
    def create_node(node_type, name, subtext, x, y, warning=False, status_badge=None):
        node_svg = []
        node_svg.append(f'    <!-- Node: {name} -->')
        node_svg.append(f'    <g class="node-group" transform="translate({x}, {y})">')
        
        if warning:
            node_svg.append('      <rect class="node-bg-warning" x="-35" y="-35" width="70" height="70" rx="12" ry="12" />')
        elif node_type == "svc":
            node_svg.append('      <rect class="node-bg-svc" x="-32" y="-32" width="64" height="64" rx="32" ry="32" />')
        elif node_type == "pod":
            node_svg.append('      <rect class="node-bg-pod" x="-32" y="-32" width="64" height="64" rx="14" ry="14" />')
        elif node_type == "cm":
            node_svg.append('      <rect class="node-bg-cm" x="-30" y="-30" width="60" height="60" rx="8" ry="8" />')
        elif node_type == "pvc":
            node_svg.append('      <rect class="node-bg-pvc" x="-30" y="-30" width="60" height="60" rx="8" ry="8" />')
            
        node_svg.append(f'      <use href="#icon-{node_type if not warning else "warning"}" x="0" y="-8" />')
        node_svg.append(f'      <text class="node-text" x="0" y="16">{name}</text>')
        node_svg.append(f'      <text class="node-subtext" x="0" y="27">{subtext}</text>')
        
        if status_badge:
            badge_class = "badge-warning-bg" if warning else "badge-bg"
            node_svg.append(f'      <g transform="translate(0, -32)">')
            b_width = len(status_badge) * 6 + 10
            node_svg.append(f'        <rect class="{badge_class}" x="{-b_width/2}" y="-8" width="{b_width}" height="15" />')
            node_svg.append(f'        <text class="badge-text" x="0" y="3">{status_badge}</text>')
            node_svg.append(f'      </g>')
            
        node_svg.append('    </g>')
        return "\n".join(node_svg)

    # Coordinates for grid rows (inside cluster box)
    # Row 1: y=170
    # Row 2: y=440
    # Row 3: y=710
    # All namespaces have w=460, h=245

    # 1. booking-api Namespace
    svg.append(create_namespace(
        name="booking-api", 
        x=45, y=170, w=460, h=245,
        labels_list=[("tier", "backend"), ("cost-center", "booking-engine"), ("env", "prod")]
    ))
    svg.append(create_node("svc", "booking-api", "ClusterIP:8080", 45 + 75, 170 + 140))
    svg.append(create_node("pod", "booking-api-*", "nginx:alpine", 45 + 200, 170 + 140))
    svg.append(create_node("cm", "booking-api-config", "2 keys", 45 + 355, 170 + 85))
    svg.append(create_node("pvc", "booking-api-data", "10Gi", 45 + 355, 170 + 195))
    
    svg.append(f'  <path d="M {45+107} {170+140} L {45+168} {170+140}" class="conn-line" />')
    svg.append(f'  <path d="M {45+232} {170+140} C {45+280} {170+140}, {45+280} {170+85}, {45+325} {170+85}" class="conn-dashed" />')
    svg.append(f'  <path d="M {45+232} {170+140} C {45+280} {170+140}, {45+280} {170+195}, {45+325} {170+195}" class="conn-storage" />')


    # 2. flight-search Namespace
    svg.append(create_namespace(
        name="flight-search", 
        x=545, y=170, w=460, h=245,
        labels_list=[("tier", "backend"), ("env", "prod")]
    ))
    svg.append(create_node("svc", "flight-search-svc", "ClusterIP:80", 545 + 75, 170 + 140))
    svg.append(create_node("pod", "flight-search-*", "nginx:alpine", 545 + 200, 170 + 140, status_badge="Missing Owner"))
    svg.append(create_node("cm", "flight-search-config", "2 keys", 545 + 355, 170 + 85))
    svg.append(create_node("pvc", "flight-search-data", "2Gi", 545 + 355, 170 + 195))
    
    svg.append(f'  <path d="M {545+107} {170+140} L {545+168} {170+140}" class="conn-line" />')
    svg.append(f'  <path d="M {545+232} {170+140} C {545+280} {170+140}, {545+280} {170+85}, {545+325} {170+85}" class="conn-dashed" />')
    svg.append(f'  <path d="M {545+232} {170+140} C {545+280} {170+140}, {545+280} {170+195}, {545+325} {170+195}" class="conn-storage" />')


    # 3. inventory Namespace
    svg.append(create_namespace(
        name="inventory", 
        x=45, y=440, w=460, h=245,
        labels_list=[("tier", "backend"), ("cost-center", "inventory"), ("owner", "inventory-team")]
    ))
    svg.append(create_node("svc", "inventory-service", "ClusterIP:80", 45 + 75, 440 + 140))
    svg.append(create_node("pod", "inventory-svc-*", "nginx:alpine", 45 + 200, 440 + 140))
    svg.append(create_node("cm", "inventory-config", "2 keys", 45 + 355, 440 + 85))
    svg.append(create_node("pvc", "inventory-data", "20Gi", 45 + 355, 440 + 195))
    
    svg.append(f'  <path d="M {45+107} {440+140} L {45+168} {440+140}" class="conn-line" />')
    svg.append(f'  <path d="M {45+232} {440+140} C {45+280} {440+140}, {45+280} {440+85}, {45+325} {440+85}" class="conn-dashed" />')
    svg.append(f'  <path d="M {45+232} {440+140} C {45+280} {440+140}, {45+280} {440+195}, {45+325} {440+195}" class="conn-storage" />')


    # 4. payment Namespace
    svg.append(create_namespace(
        name="payment", 
        x=545, y=440, w=460, h=245,
        labels_list=[("env", "prod"), ("owner", "payments-team")]
    ))
    svg.append(create_node("svc", "payment-processor", "ClusterIP:80", 545 + 75, 440 + 140))
    svg.append(create_node("pod", "payment-proc-*", "nginx:alpine", 545 + 200, 440 + 140))
    svg.append(create_node("cm", "payment-config", "2 keys", 545 + 355, 440 + 85))
    svg.append(create_node("pvc", "payment-proc-data", "5Gi", 545 + 355, 440 + 195))
    
    svg.append(f'  <path d="M {545+107} {440+140} L {545+168} {440+140}" class="conn-line" />')
    svg.append(f'  <path d="M {545+232} {440+140} C {545+280} {440+140}, {545+280} {440+85}, {545+325} {440+85}" class="conn-dashed" />')
    svg.append(f'  <path d="M {545+232} {440+140} C {545+280} {440+140}, {545+280} {440+195}, {545+325} {440+195}" class="conn-storage" />')


    # 5. airline Namespace (Orphaned storage)
    svg.append(create_namespace(
        name="airline", 
        x=45, y=710, w=460, h=245,
        style_class="ns-card-warning",
        labels_list=[("audit", "failed")]
    ))
    svg.append(create_node("pvc", "orphaned-data-pvc", "Capacity: 5Gi", 45 + 230, 710 + 125, warning=True, status_badge="ORPHANED"))
    svg.append(f"""  <g transform="translate({45 + 230}, {710 + 195})">
    <text text-anchor="middle" fill="#f87171" font-size="11" font-weight="600">No active Pod mounts this PVC.</text>
    <text text-anchor="middle" fill="#64748b" font-size="9" font-weight="400" y="12">Cost leak: Storage is provisioned but unused.</text>
  </g>
""")


    # 6. default Namespace (Misplaced workload)
    svg.append(create_namespace(
        name="default (Shared/System)", 
        x=545, y=710, w=460, h=245,
        style_class="ns-card-warning",
        labels_list=[("owner", "unknown"), ("cost-center", "unallocated")]
    ))
    svg.append(create_node("svc", "analytics-coll", "ClusterIP:80", 545 + 65, 710 + 155))
    svg.append(create_node("pod", "analytics-coll-*", "nginx:alpine", 545 + 165, 710 + 155, status_badge="Misplaced"))
    svg.append(create_node("cm", "analytics-config", "2 keys", 545 + 275, 710 + 95))
    svg.append(create_node("pvc", "analytics-data", "1Gi", 545 + 275, 710 + 195))
    svg.append(create_node("cm", "untracked-config", "unlabelled", 545 + 385, 710 + 155, warning=True, status_badge="UNTRACKED"))
    
    svg.append(f'  <path d="M {545+97} {710+155} L {545+133} {710+155}" class="conn-line" />')
    svg.append(f'  <path d="M {545+197} {710+155} C {545+230} {710+155}, {545+230} {710+95}, {545+245} {710+95}" class="conn-dashed" />')
    svg.append(f'  <path d="M {545+197} {710+155} C {545+230} {710+155}, {545+230} {710+195}, {545+245} {710+195}" class="conn-storage" />')

    svg.append(f"""  <g transform="translate({545 + 230}, {710 + 230})">
    <text text-anchor="middle" fill="#f87171" font-size="9" font-weight="600">Misplaced workload in default namespace without tags!</text>
  </g>
""")

    # ----------------------------------------------------
    # Footer Section
    # ----------------------------------------------------
    svg.append(f"""  <!-- Footer Section -->
  <g transform="translate(40, {height - 20})">
    <text fill="#475569" font-size="10" font-weight="600">Solid lines (—) denote service traffic routing. Dashed lines (---) represent configuration linkages. Purple lines represent PV storage mounts.</text>
  </g>
</svg>""")
    
    return "\n".join(svg)

def main():
    target_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(target_dir, "architecture.svg")
    print(f"Generating single-cluster architecture diagram to {output_path}...")
    
    svg_content = generate_svg()
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print("Successfully generated SVG diagram!")

if __name__ == "__main__":
    main()
