#!/usr/bin/env python3
import os

def generate_svg():
    width = 860
    height = 660
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
    
    # CSS Styles for premium look
    svg.append("""  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap');
    
    svg {
      background-color: #0b1329;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
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
      font-size: 16px;
      font-weight: 700;
      fill: #38bdf8;
      letter-spacing: -0.01em;
    }
    
    .ns-card {
      fill: #111b36;
      stroke: #2a3a60;
      stroke-width: 1.5;
      rx: 16px;
      ry: 16px;
      transition: all 0.3s ease;
    }
    
    .ns-card-warning {
      fill: #191427;
      stroke: #991b1b;
      stroke-dasharray: 6,4;
    }
    
    .title {
      font-size: 24px;
      font-weight: 700;
      fill: #f8fafc;
      letter-spacing: -0.025em;
    }
    
    .subtitle {
      font-size: 13px;
      fill: #94a3b8;
      font-weight: 400;
    }
    
    .ns-title {
      font-size: 14px;
      font-weight: 700;
      fill: #f1f5f9;
      letter-spacing: -0.01em;
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
    
    /* Nodes */
    .node-bg-client {
      fill: #1e293b;
      stroke: #94a3b8;
      stroke-width: 1.5;
      filter: drop-shadow(0 2px 6px rgba(71, 85, 105, 0.15));
    }
    
    .node-bg-svc {
      fill: url(#grad-svc);
      stroke: #10b981;
      stroke-width: 1.5;
    }
    
    .node-bg-pod {
      fill: url(#grad-pod);
      stroke: #0ea5e9;
      stroke-width: 1.5;
    }
    
    .node-bg-cm {
      fill: url(#grad-cm);
      stroke: #eab308;
      stroke-width: 1.5;
    }
    
    .node-bg-warning {
      fill: url(#grad-warning);
      stroke: #ef4444;
      stroke-width: 2;
      filter: drop-shadow(0 4px 12px rgba(239, 68, 68, 0.25));
    }
    
    /* Hover micro-animations */
    .node-group {
      cursor: pointer;
    }
    .node-group:hover .node-bg-svc { stroke-width: 2.5; filter: drop-shadow(0 4px 12px rgba(16, 185, 129, 0.3)); }
    .node-group:hover .node-bg-pod { stroke-width: 2.5; filter: drop-shadow(0 4px 12px rgba(14, 165, 233, 0.3)); }
    .node-group:hover .node-bg-cm  { stroke-width: 2.5; filter: drop-shadow(0 4px 12px rgba(234, 179, 8, 0.25)); }
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
    
    .conn-broken {
      fill: none;
      stroke: #ef4444;
      stroke-width: 2;
      stroke-dasharray: 5,3;
    }
    
    /* Badges */
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
      font-size: 9px;
      font-weight: 600;
      fill: #f1f5f9;
      text-anchor: middle;
      font-family: 'JetBrains Mono', monospace;
    }
    
    .warning-label {
      font-size: 11px;
      font-weight: 600;
      fill: #f87171;
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
    
    <!-- Icon Shapes -->
    <!-- Client (Browser) -->
    <g id="icon-client">
      <rect x="-14" y="-12" width="28" height="18" rx="2" fill="none" stroke="#94a3b8" stroke-width="1.5" />
      <line x1="-16" y1="8" x2="16" y2="8" stroke="#94a3b8" stroke-width="2" />
      <line x1="-6" y1="6" x2="-10" y2="10" stroke="#94a3b8" stroke-width="1.5" />
      <line x1="6" y1="6" x2="10" y2="10" stroke="#94a3b8" stroke-width="1.5" />
      <circle cx="0" cy="-3" r="1.5" fill="#94a3b8" />
    </g>
    
    <!-- Service Icon -->
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
    
    <!-- Pod Icon -->
    <g id="icon-pod">
      <polygon points="0,-16 13.86,-8 13.86,8 0,16 -13.86,8 -13.86,-8" fill="none" stroke="#38bdf8" stroke-width="1.8" />
      <line x1="0" y1="-16" x2="0" y2="16" stroke="#38bdf8" stroke-width="1" opacity="0.4" />
      <line x1="0" y1="0" x2="13.86" y2="8" stroke="#38bdf8" stroke-width="1" opacity="0.4" />
      <line x1="0" y1="0" x2="-13.86" y2="8" stroke="#38bdf8" stroke-width="1" opacity="0.4" />
    </g>
    
    <!-- ConfigMap Icon -->
    <g id="icon-cm">
      <path d="M -9,-12 L 3,-12 L 9,-6 L 9,12 L -9,12 Z" fill="none" stroke="#facc15" stroke-width="1.5" />
      <path d="M 3,-12 L 3,-6 L 9,-6" fill="none" stroke="#facc15" stroke-width="1.5" />
      <line x1="-5" y1="-2" x2="5" y2="-2" stroke="#facc15" stroke-width="1.2" opacity="0.8" />
      <line x1="-5" y1="2" x2="5" y2="2" stroke="#facc15" stroke-width="1.2" opacity="0.8" />
      <line x1="-5" y1="6" x2="1" y2="6" stroke="#facc15" stroke-width="1.2" opacity="0.8" />
    </g>
    
    <!-- Warning Icon -->
    <g id="icon-warning">
      <polygon points="0,-14 14,10 -14,10" fill="#ef4444" stroke="#f87171" stroke-width="1.5" />
      <circle cx="0" cy="6" r="1.5" fill="#ffffff" />
      <line x1="0" y1="-6" x2="0" y2="2" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" />
    </g>
  </defs>
  
  <rect width="{width}" height="{height}" fill="url(#grid-pattern)" />
""")
    
    # Header
    svg.append(f"""  <!-- Header Section -->
  <g transform="translate(40, 50)">
    <text class="title" x="0" y="0">Incident: Payment Gateway Down (Section 02a)</text>
    <text class="subtitle" x="0" y="22">Tracing the upstream 503 error due to an unowned backend deployment scaled to 0 replicas.</text>
  </g>
""")

    # Legend
    svg.append(f"""  <!-- Legend Section -->
  <g transform="translate(560, 32)">
    <rect width="260" height="42" fill="#0f172a" stroke="#1e293b" stroke-width="1" rx="6" ry="6" />
    <g transform="translate(18, 21)">
      <line x1="0" y1="0" x2="25" y2="0" class="conn-line" />
      <text x="32" y="4" fill="#94a3b8" font-size="10" font-weight="600">Active Routing</text>
    </g>
    <g transform="translate(138, 21)">
      <line x1="0" y1="0" x2="25" y2="0" class="conn-broken" />
      <text x="32" y="4" fill="#f87171" font-size="10" font-weight="600">Broken Link (503)</text>
    </g>
  </g>
""")

    # Helper function to create namespace cards
    def create_namespace(name, x, y, w, h, style_class="ns-card"):
        ns_svg = []
        ns_svg.append(f'  <!-- Namespace: {name} -->')
        ns_svg.append(f'  <g transform="translate({x}, {y})">')
        ns_svg.append(f'    <rect class="ns-card {style_class}" width="{w}" height="{h}" />')
        ns_svg.append(f'    <path d="M 0 12 C 0 5.37 5.37 0 12 0 L 150 0 L 135 30 L 0 30 Z" fill="#1e293b" stroke="#2a3a60" stroke-width="1" />')
        ns_svg.append(f'    <text class="ns-title" x="12" y="19">{name}</text>')
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
        elif node_type == "client":
            node_svg.append('      <rect class="node-bg-client" x="-35" y="-35" width="70" height="70" rx="12" ry="12" />')
            
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

    # 1. User Zone (Outside K8s) - Browser
    svg.append("  <!-- User Browser -->")
    svg.append(create_node("client", "Local Browser", "localhost:8089", 75, 310))
    
    # 2. SINGLE KUBERNETES CLUSTER CONTAINER
    svg.append(f"""  <!-- Kubernetes Cluster Box -->
  <g transform="translate(160, 110)">
    <rect class="cluster-card" width="680" height="490" />
    <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 260 0 L 245 32 L 0 32 Z" fill="#1e3a8a" stroke="#38bdf8" stroke-width="1.5" />
    <text class="cluster-title" x="15" y="21">☸️ Kubernetes Cluster (finops-cluster)</text>
  </g>
""")

    # 3. payment Namespace container (inside cluster box)
    # Border styled as a warning boundary due to live incident & label failure
    svg.append(create_namespace(
        name="payment Namespace",
        x=190, y=175, w=620, h=400,
        style_class="ns-card-warning"
    ))

    # --- TOP SERVICE: payment-gateway (Frontend UI) ---
    svg.append("  <!-- Frontend UI Workload -->")
    svg.append(create_node("svc", "payment-gateway", "ClusterIP:80", 255, 265))
    svg.append(create_node("pod", "payment-gateway-*", "nginx:alpine", 435, 265, status_badge="1/1 Running"))
    svg.append(create_node("cm", "ui-config", "nginx.conf", 615, 265))
    
    # Connect Frontend components
    svg.append(f'  <path d="M {255+32} 265 L {435-32} 265" class="conn-line" />')
    svg.append(f'  <path d="M {435+32} 265 L {615-30} 265" class="conn-dashed" />')

    # Traffic from Browser to Frontend Service (Via Port-Forward)
    # Path from Outside (Browser cx=75, cy=310) to Inside (UI Service cx=255, cy=265)
    svg.append(f'  <path d="M {75+35} 310 C {130} 310, {150} 265, {255-32} 265" class="conn-line" />')
    svg.append(f"""  <g transform="translate(145, 275)">
    <rect x="-32" y="-9" width="64" height="18" fill="#1e293b" stroke="#475569" stroke-width="0.8" rx="4" ry="4" />
    <text text-anchor="middle" fill="#94a3b8" font-size="9" font-weight="600" y="3">Port Forward</text>
  </g>
""")

    # --- BOTTOM SERVICE: payment-gateway-api (Broken Backend) ---
    svg.append("  <!-- Backend API Workload -->")
    svg.append(create_node("svc", "payment-gateway-api", "ClusterIP:8080", 255, 425))
    
    # The API Deployment node (scaled to 0 - warning state!)
    svg.append(create_node(
        node_type="pod", 
        name="payment-gateway-api", 
        subtext="replicas: 0", 
        x=435, y=425, 
        warning=True, 
        status_badge="0/0 Desired:0"
    ))
    svg.append(create_node("cm", "api-config", "nginx.conf", 615, 425))

    # Connect Backend components
    svg.append(f'  <path d="M {435+32} 425 L {615-30} 425" class="conn-dashed" />')

    # Curved link from UI Pod to API Service (Frontend fetches Backend API)
    svg.append(f'  <path d="M {435} 297 C {435} 340, {255} 350, {255} 393" class="conn-line" />')
    svg.append(f"""  <g transform="translate(365, 345)">
    <text text-anchor="middle" fill="#94a3b8" font-size="10" font-weight="600">HTTP requests</text>
    <text text-anchor="middle" fill="#64748b" font-size="8" font-weight="500" y="10">payment-gateway-api:8080</text>
  </g>
""")

    # Broken routing connection from API Service to API Deployment pods
    svg.append(f'  <path d="M {255+32} 425 L {435-35} 425" class="conn-broken" />')
    
    # Broken routing warning indicators
    svg.append(f"""  <!-- Broken routing markers -->
  <g transform="translate(345, 425)">
    <circle cx="0" cy="0" r="14" fill="#450a0a" stroke="#ef4444" stroke-width="1.5" />
    <line x1="-6" y1="-6" x2="6" y2="6" stroke="#ef4444" stroke-width="2.5" />
    <line x1="6" y1="-6" x2="-6" y2="6" stroke="#ef4444" stroke-width="2.5" />
  </g>
  <g transform="translate(345, 453)">
    <rect x="-65" y="-9" width="130" height="18" fill="#7f1d1d" stroke="#f87171" stroke-width="0.8" rx="4" ry="4" />
    <text text-anchor="middle" fill="#ffffff" font-size="9" font-weight="700" y="3">503 Service Unavailable</text>
  </g>
""")

    # Ownership wall / metadata failure annotations inside namespace
    svg.append(f"""  <!-- Ownership Wall Annotation -->
  <g transform="translate(435, 525)">
    <rect x="-225" y="-20" width="450" height="40" fill="#1e1b29" stroke="#ef4444" stroke-width="1" rx="8" ry="8" />
    <!-- Alert Icon -->
    <polygon points="-205,-4 -195,12 -215,12" fill="#ef4444" stroke="#f87171" stroke-width="1" />
    <circle cx="-205" cy="9" r="1" fill="#ffffff" />
    <line x1="-205" y1="0" x2="-205" y2="6" stroke="#ffffff" stroke-width="2" stroke-linecap="round" />
    <text x="-185" y="4" class="warning-label">OWNERSHIP WALL: No owner, cost-center, or team labels found!</text>
    <text x="-185" y="15" fill="#94a3b8" font-size="9" font-weight="400">At 2 AM, the on-call engineer has no metadata to identify who owns this broken API.</text>
  </g>
""")

    # Footer
    svg.append(f"""  <!-- Footer Section -->
  <g transform="translate(40, {height - 25})">
    <text fill="#475569" font-size="10" font-weight="600">The browser accesses the payment-gateway UI over port 8089 (outside K8s), which calls payment-gateway-api:8080 (inside K8s). The API has 0 endpoints.</text>
  </g>
</svg>""")
    
    return "\n".join(svg)

def main():
    target_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(target_dir, "architecture.svg")
    print(f"Generating single-cluster incident architecture diagram to {output_path}...")
    
    svg_content = generate_svg()
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print("Successfully generated SVG incident diagram!")

if __name__ == "__main__":
    main()
