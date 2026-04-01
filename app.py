import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO

st.set_page_config(
    page_title="🔗 ReFi Token Flow",
    page_icon="🌿",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400&display=swap');
    .main-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #10B981, #14B8A6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #94A3B8;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(145deg, #1E293B, #334155);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 600;
        color: #10B981;
    }
    .metric-label {
        color: #94A3B8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.3rem;
    }
    .info-box {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .transparency-badge {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Datos embebidos directamente (no necesita archivo externo)
DATA_CSV = """Date,Type,From,To,Amount,Ser
18/3/2026 16:35:32,Transfer,0x4da4d627949923125018C06441A74D5995b70642,0xdAab558078eC5E828cee28433BB3bE67c6f34693,16,Más Compost
18/3/2026 16:35:24,Transfer,0xba1523aAD313dDC94b3259b7a3a4B44D65E35620,0xdAab558078eC5E828cee28433BB3bE67c6f34693,15,Más Compost
18/3/2026 16:34:52,Transfer,0x7F611F9282947401450F3D9d630C2c72CFa478d9,0xdAab558078eC5E828cee28433BB3bE67c6f34693,16,Más Compost
18/3/2026 16:34:42,Transfer,0xb89c9ff9fe440750688225258397F243ff4f1948,0xdAab558078eC5E828cee28433BB3bE67c6f34693,16,Más Compost
18/3/2026 16:34:33,Transfer,0x97E5386eDA1f1Ff771C97DbBdB7CF8f372D6b793,0xdAab558078eC5E828cee28433BB3bE67c6f34693,19,Más Compost
18/3/2026 16:37:29,Transfer,0x4da4d627949923125018C06441A74D5995b70642,0xa93c0Ab2508b0c7Ef4fea8D42E6E0FE8553EbC47,11,Ecocirco
18/3/2026 16:37:22,Transfer,0xba1523aAD313dDC94b3259b7a3a4B44D65E35620,0xa93c0Ab2508b0c7Ef4fea8D42E6E0FE8553EbC47,13,Ecocirco
18/3/2026 16:36:03,Transfer,0x7F611F9282947401450F3D9d630C2c72CFa478d9,0xa93c0Ab2508b0c7Ef4fea8D42E6E0FE8553EbC47,11,Ecocirco
18/3/2026 16:35:17,Transfer,0x97E5386eDA1f1Ff771C97DbBdB7CF8f372D6b793,0xa93c0Ab2508b0c7Ef4fea8D42E6E0FE8553EbC47,13,Ecocirco
18/3/2026 16:35:12,Transfer,0xb89c9ff9fe440750688225258397F243ff4f1948,0xa93c0Ab2508b0c7Ef4fea8D42E6E0FE8553EbC47,12,Ecocirco
18/3/2026 16:38:00,Transfer,0x4da4d627949923125018C06441A74D5995b70642,0xE1ad70A145C25804F8D0Ab7480C919625Af09C3c,15,ECCO
18/3/2026 16:37:49,Transfer,0xba1523aAD313dDC94b3259b7a3a4B44D65E35620,0xE1ad70A145C25804F8D0Ab7480C919625Af09C3c,15,ECCO
18/3/2026 16:36:28,Transfer,0x97E5386eDA1f1Ff771C97DbBdB7CF8f372D6b793,0xE1ad70A145C25804F8D0Ab7480C919625Af09C3c,18,ECCO
18/3/2026 16:36:23,Transfer,0xb89c9ff9fe440750688225258397F243ff4f1948,0xE1ad70A145C25804F8D0Ab7480C919625Af09C3c,20,ECCO
18/3/2026 16:32:42,Transfer,0x7F611F9282947401450F3D9d630C2c72CFa478d9,0xE1ad70A145C25804F8D0Ab7480C919625Af09C3c,16,ECCO
18/3/2026 16:37:13,Transfer,0xb89c9ff9fe440750688225258397F243ff4f1948,0x2A504e6eaF97c96321ec5F270bbF97f04Db5D869,14,Biodiversa
18/3/2026 16:37:03,Transfer,0x97E5386eDA1f1Ff771C97DbBdB7CF8f372D6b793,0x2A504e6eaF97c96321ec5F270bbF97f04Db5D869,15,Biodiversa
18/3/2026 16:34:48,Transfer,0x4da4d627949923125018C06441A74D5995b70642,0x2A504e6eaF97c96321ec5F270bbF97f04Db5D869,12,Biodiversa
18/3/2026 16:34:44,Transfer,0xba1523aAD313dDC94b3259b7a3a4B44D65E35620,0x2A504e6eaF97c96321ec5F270bbF97f04Db5D869,13,Biodiversa
18/3/2026 16:33:14,Transfer,0x7F611F9282947401450F3D9d630C2c72CFa478d9,0x2A504e6eaF97c96321ec5F270bbF97f04Db5D869,14,Biodiversa
18/3/2026 16:40:00,Transfer,0x4da4d627949923125018C06441A74D5995b70642,0x998AE93A24266059a13aD5141943073aF11A4983,14,AAS
18/3/2026 16:37:39,Transfer,0x97E5386eDA1f1Ff771C97DbBdB7CF8f372D6b793,0x998AE93A24266059a13aD5141943073aF11A4983,13,AAS
18/3/2026 16:37:37,Transfer,0xb89c9ff9fe440750688225258397F243ff4f1948,0x998AE93A24266059a13aD5141943073aF11A4983,14,AAS
18/3/2026 16:36:04,Transfer,0xba1523aAD313dDC94b3259b7a3a4B44D65E35620,0x998AE93A24266059a13aD5141943073aF11A4983,16,AAS
18/3/2026 16:35:41,Transfer,0x7F611F9282947401450F3D9d630C2c72CFa478d9,0x998AE93A24266059a13aD5141943073aF11A4983,11,AAS
18/3/2026 14:30:47,Transfer,0xF3ec500C7bf62878aAe56D5B459eF2f3d7081849,0x4da4d627949923125018C06441A74D5995b70642,100,Ricardo Camargo (Ángel inversionista)
18/3/2026 14:29:36,Transfer,0x7F611F9282947401450F3D9d630C2c72CFa478d9,0x0C0C60800a19E25DD6C59B7fD6f414C80E5603e2,1,JJ
18/3/2026 14:27:53,Transfer,0x0C0C60800a19E25DD6C59B7fD6f414C80E5603e2,0x7F611F9282947401450F3D9d630C2c72CFa478d9,100,Sara Pulido (Fondo impacta)
18/3/2026 14:26:52,Transfer,0xF3ec500C7bf62878aAe56D5B459eF2f3d7081849,0x97E5386eDA1f1Ff771C97DbBdB7CF8f372D6b793,100,Germán Villegas (Fundación Avina)
18/3/2026 14:22:04,Transfer,0xF3ec500C7bf62878aAe56D5B459eF2f3d7081849,0xb89c9ff9fe440750688225258397F243ff4f1948,100,Carlos Casallas (Fondo acción)
18/3/2026 14:22:00,Transfer,0x0C0C60800a19E25DD6C59B7fD6f414C80E5603e2,0xba1523aAD313dDC94b3259b7a3a4B44D65E35620,100,Alexandra Baquero (Ángel inversionista)
18/3/2026 13:51:20,Transfer,reficollective.sarafu.eth,0xF3ec500C7bf62878aAe56D5B459eF2f3d7081849,300,Andrea
18/3/2026 13:45:14,Transfer,reficollective.sarafu.eth,0x0C0C60800a19E25DD6C59B7fD6f414C80E5603e2,200,JJ
18/3/2026 13:35:09,Mint,0x7102e091256Cb45DDfca79a4AC5323f8d885e67A,reficollective.sarafu.eth,500,ReFi"""

WALLET_ALIASES = {
    '0x4da4d627949923125018C06441A74D5995b70642': 'm1',
    '0xba1523aAD313dDC94b3259b7a3a4B44D65E35620': 'Alexandra',
    '0x7F611F9282947401450F3D9d630C2c72CFa478d9': 'Carlos',
    '0xb89c9ff9fe440750688225258397F243ff4f1948': 'm3',
    '0x97E5386eDA1f1Ff771C97DbBdB7CF8f372D6b793': 'm2',
    '0xF3ec500C7bf62878aAe56D5B459eF2f3d7081849': 'Andreita',
    '0x0C0C60800a19E25DD6C59B7fD6f414C80E5603e2': 'JJ',
    'reficollective.sarafu.eth': 'ReFi Pool',
    '0x7102e091256Cb45DDfca79a4AC5323f8d885e67A': 'Mint Contract',
    '0xdAab558078eC5E828cee28433BB3bE67c6f34693': 'Más Compost',
    '0xa93c0Ab2508b0c7Ef4fea8D42E6E0FE8553EbC47': 'Ecocirco',
    '0xE1ad70A145C25804F8D0Ab7480C919625Af09C3c': 'ECCO',
    '0x2A504e6eaF97c96321ec5F270bbF97f04Db5D869': 'Biodiversa',
    '0x998AE93A24266059a13aD5141943073aF11A4983': 'AAS'
}

WALLET_TYPES = {
    'Mint Contract': 'contract', 'ReFi Pool': 'pool',
    'JJ': 'liquidity', 'Andreita': 'liquidity',
    'm1': 'mentor', 'm2': 'mentor', 'm3': 'mentor', 'Alexandra': 'mentor', 'Carlos': 'mentor',
    'AAS': 'org', 'Biodiversa': 'org', 'ECCO': 'org', 'Ecocirco': 'org', 'Más Compost': 'org'
}

TYPE_COLORS = {'contract': '#6366F1', 'pool': '#8B5CF6', 'liquidity': '#EC4899', 'mentor': '#10B981', 'org': '#F59E0B'}
TYPE_LABELS = {'contract': '📜 Contrato', 'pool': '🏊 Pool', 'liquidity': '💧 Liquidez', 'mentor': '🎓 Mentor', 'org': '🌱 Organización'}

@st.cache_data
def load_data():
    df = pd.read_csv(StringIO(DATA_CSV))
    df['From_Alias'] = df['From'].map(WALLET_ALIASES).fillna(df['From'])
    df['To_Alias'] = df['To'].map(WALLET_ALIASES).fillna(df['Ser'])
    df['From_Type'] = df['From_Alias'].map(WALLET_TYPES).fillna('unknown')
    df['To_Type'] = df['To_Alias'].map(WALLET_TYPES).fillna('unknown')
    return df

def calculate_balances(df):
    balances = {}
    for _, row in df.iterrows():
        sender, receiver, amount = row['From_Alias'], row['To_Alias'], row['Amount']
        if row['Type'] == 'Mint':
            balances[receiver] = balances.get(receiver, 0) + amount
        else:
            balances[sender] = balances.get(sender, 0) - amount
            balances[receiver] = balances.get(receiver, 0) + amount
    return balances

def create_sankey(df):
    nodes = list(set(df['From_Alias'].tolist() + df['To_Alias'].tolist()))
    node_idx = {n: i for i, n in enumerate(nodes)}
    node_colors = [TYPE_COLORS.get(WALLET_TYPES.get(n, 'unknown'), '#64748B') for n in nodes]
    
    fig = go.Figure(go.Sankey(
        node=dict(pad=20, thickness=25, line=dict(color="#1E293B", width=1), label=nodes, color=node_colors),
        link=dict(
            source=[node_idx[r['From_Alias']] for _, r in df.iterrows()],
            target=[node_idx[r['To_Alias']] for _, r in df.iterrows()],
            value=df['Amount'].tolist(),
            color='rgba(16, 185, 129, 0.3)'
        )
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F1F5F9', family='Space Grotesk', size=12), height=450, margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig

def create_network_html(df, balances):
    import json
    edges = df.groupby(['From_Alias', 'To_Alias'])['Amount'].sum().reset_index()
    nodes_data = []
    for wallet in set(df['From_Alias'].tolist() + df['To_Alias'].tolist()):
        wtype = WALLET_TYPES.get(wallet, 'unknown')
        nodes_data.append({
            'id': wallet, 'label': wallet,
            'color': TYPE_COLORS.get(wtype, '#64748B'),
            'size': max(15, min(50, abs(balances.get(wallet, 0)) / 8 + 10)),
            'title': f"{wallet} | {TYPE_LABELS.get(wtype, '?')} | Balance: {balances.get(wallet, 0):+d}"
        })
    edges_data = [{'from': r['From_Alias'], 'to': r['To_Alias'], 'value': int(r['Amount']), 'title': f"{int(r['Amount'])} tokens"} for _, r in edges.iterrows()]
    
    nodes_json = json.dumps(nodes_data)
    edges_json = json.dumps(edges_data)
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style type="text/css">
        html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background: #0F172A;
        }}
        #mynetwork {{
            width: 100%;
            height: 500px;
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 12px;
            background: linear-gradient(145deg, #1E293B, #0F172A);
        }}
    </style>
</head>
<body>
    <div id="mynetwork"></div>
    <script type="text/javascript">
        var nodesArray = {nodes_json};
        var edgesArray = {edges_json};
        
        var nodes = new vis.DataSet(nodesArray);
        var edges = new vis.DataSet(edgesArray);
        
        var container = document.getElementById('mynetwork');
        var data = {{ nodes: nodes, edges: edges }};
        var options = {{
            nodes: {{
                shape: 'dot',
                font: {{ color: '#F1F5F9', size: 14, face: 'Space Grotesk, sans-serif' }},
                borderWidth: 3,
                shadow: true
            }},
            edges: {{
                arrows: {{ to: {{ enabled: true, scaleFactor: 0.8 }} }},
                color: {{ color: '#10B981', highlight: '#14B8A6', opacity: 0.7 }},
                smooth: {{ type: 'curvedCW', roundness: 0.2 }},
                width: 2
            }},
            physics: {{
                enabled: true,
                barnesHut: {{
                    gravitationalConstant: -3000,
                    centralGravity: 0.3,
                    springLength: 120,
                    springConstant: 0.04,
                    damping: 0.09
                }},
                stabilization: {{ iterations: 150 }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 100,
                zoomView: true,
                dragView: true
            }}
        }};
        
        var network = new vis.Network(container, data, options);
    </script>
</body>
</html>
"""

def main():
    st.markdown('<h1 class="main-header">🔗 ReFi Blockchain Flow</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Visualización transparente del flujo de tokens FCEA</p>', unsafe_allow_html=True)
    
    df = load_data()
    balances = calculate_balances(df)
    
    # Sidebar
    st.sidebar.markdown("## 🎛️ Filtros")
    type_filter = st.sidebar.multiselect("Tipo de wallet", list(TYPE_LABELS.keys()), default=list(TYPE_LABELS.keys()), format_func=lambda x: TYPE_LABELS[x])
    all_wallets = sorted(set(df['From_Alias'].tolist() + df['To_Alias'].tolist()))
    wallet_filter = st.sidebar.multiselect("Wallet específica", all_wallets)
    amount_range = st.sidebar.slider("Rango de tokens", int(df['Amount'].min()), int(df['Amount'].max()), (int(df['Amount'].min()), int(df['Amount'].max())))
    
    # Apply filters
    df_f = df[(df['Amount'] >= amount_range[0]) & (df['Amount'] <= amount_range[1])]
    if type_filter:
        df_f = df_f[(df_f['From_Type'].isin(type_filter)) | (df_f['To_Type'].isin(type_filter))]
    if wallet_filter:
        df_f = df_f[(df_f['From_Alias'].isin(wallet_filter)) | (df_f['To_Alias'].isin(wallet_filter))]
    
    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df_f)}</div><div class="metric-label">Transacciones</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card"><div class="metric-value">{int(df_f["Amount"].sum()):,}</div><div class="metric-label">Tokens</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card"><div class="metric-value">{len(set(df_f["From_Alias"].tolist() + df_f["To_Alias"].tolist()))}</div><div class="metric-label">Wallets</div></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="metric-card"><div class="metric-value">100%</div><div class="metric-label">Trazabilidad</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🕸️ Red de Nodos", "📊 Flujo Sankey", "💰 Balances", "📋 Transacciones"])
    
    with tab1:
        st.markdown('<div class="info-box"><strong>🔍 Red interactiva:</strong> Arrastra y explora las conexiones entre wallets. El tamaño representa el balance.</div>', unsafe_allow_html=True)
        cols = st.columns(5)
        for i, (t, l) in enumerate(TYPE_LABELS.items()):
            cols[i].markdown(f'<span class="transparency-badge" style="background:{TYPE_COLORS[t]}">{l}</span>', unsafe_allow_html=True)
        st.components.v1.html(create_network_html(df_f, balances), height=520)
    
    with tab2:
        st.markdown('<div class="info-box"><strong>📈 Diagrama Sankey:</strong> Visualiza cómo fluyen los tokens desde el origen hasta los destinatarios.</div>', unsafe_allow_html=True)
        st.plotly_chart(create_sankey(df_f), use_container_width=True)
    
    with tab3:
        st.markdown('<div class="info-box"><strong>💼 Estado actual:</strong> Balance de tokens en cada wallet después de todas las transacciones.</div>', unsafe_allow_html=True)
        bal_df = pd.DataFrame([{'Wallet': w, 'Tipo': TYPE_LABELS.get(WALLET_TYPES.get(w), '❓'), 'Balance': b} for w, b in sorted(balances.items(), key=lambda x: x[1], reverse=True)])
        c1, c2 = st.columns([2, 1])
        with c1:
            fig = px.bar(bal_df, x='Wallet', y='Balance', color='Balance', color_continuous_scale=['#EF4444', '#F59E0B', '#10B981'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#F1F5F9'), xaxis=dict(tickangle=45), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.dataframe(bal_df, hide_index=True, use_container_width=True)
    
    with tab4:
        st.markdown('<div class="info-box"><strong>🔐 Registro inmutable:</strong> Cada transacción con su hash verificable en blockchain.</div>', unsafe_allow_html=True)
        display_df = df_f[['Date', 'Type', 'From_Alias', 'To_Alias', 'Amount', 'From', 'To']].copy()
        display_df.columns = ['Fecha', 'Tipo', 'De', 'A', 'Tokens', 'Hash Origen', 'Hash Destino']
        st.dataframe(display_df, hide_index=True, use_container_width=True)
        st.download_button("📥 Descargar CSV", display_df.to_csv(index=False), "transacciones_blockchain.csv", "text/csv")
    
    # Footer
    st.markdown("""
    <div style="text-align:center;padding:1.5rem;background:rgba(16,185,129,0.1);border-radius:12px;margin-top:2rem;">
        <h4 style="color:#10B981;margin:0 0 0.5rem">🌿 Transparencia Total con Blockchain</h4>
        <p style="color:#94A3B8;font-size:0.9rem;margin:0">Cada transacción es inmutable, verificable y descentralizada.</p>
        <div style="margin-top:0.8rem">
            <span class="transparency-badge">✓ Inmutable</span>
            <span class="transparency-badge">✓ Verificable</span>
            <span class="transparency-badge">✓ Transparente</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
