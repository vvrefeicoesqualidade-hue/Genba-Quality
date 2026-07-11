import streamlit as st
import pandas as pd
from datetime import date
import json

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Genba Quality Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #F5FAF6 !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] > .main { background: #F5FAF6; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: #0F2D1A; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Top bar ── */
.topbar {
    background: #0F2D1A;
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
}
.topbar-logo { font-size: 17px; font-weight: 600; color: #EAFBF0; letter-spacing: -0.3px; }
.topbar-logo span { color: #7DC65A; }
.topbar-user { font-size: 12px; color: #5DAF78; }

/* ── Cards ── */
.metric-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; padding: 20px 24px 0; }
.metric-card {
    background: #fff;
    border-radius: 12px;
    padding: 14px 16px;
    border: 0.5px solid #D6EDD9;
}
.metric-label { font-size: 11px; color: #6B8F72; margin-bottom: 4px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; }
.metric-value { font-size: 26px; font-weight: 600; color: #0F2D1A; }
.metric-value.green { color: #1D6B35; }
.metric-value.red   { color: #9C0006; }
.metric-sub { font-size: 11px; color: #6B8F72; margin-top: 2px; }

/* ── Section title ── */
.section-title {
    font-size: 11px; font-weight: 600; color: #6B8F72;
    text-transform: uppercase; letter-spacing: 0.07em;
    padding: 20px 24px 8px;
}

/* ── Item row ── */
.item-card {
    background: #fff;
    border: 0.5px solid #D6EDD9;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.item-card.c  { border-color: #1D9E75; background: #EAF5ED; }
.item-card.nc { border-color: #E24B4A; background: #FFF0F0; }
.item-name { font-size: 13px; color: #0F2D1A; font-weight: 400; }
.item-card.nc .item-name { color: #501313; }

/* ── Badges ── */
.badge {
    font-size: 11px; font-weight: 600;
    padding: 3px 10px; border-radius: 99px;
    display: inline-block;
}
.badge-c  { background: #1D9E75; color: #fff; }
.badge-nc { background: #E24B4A; color: #fff; }
.badge-p  { background: #E8F0E9; color: #6B8F72; border: 0.5px solid #D6EDD9; }

/* ── Progress ── */
.progress-wrap { padding: 0 24px; margin-top: 4px; }
.progress-bar-bg {
    height: 5px; background: #D6EDD9; border-radius: 99px; overflow: hidden;
}
.progress-bar-fill {
    height: 100%; background: #7DC65A; border-radius: 99px;
    transition: width 0.3s;
}
.progress-label { font-size: 12px; color: #6B8F72; margin-top: 4px; display: flex; justify-content: space-between; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    border: none !important;
    padding: 10px 20px !important;
}
.btn-primary > button {
    background: #0F2D1A !important;
    color: #EAFBF0 !important;
}
.btn-wa > button {
    background: #25D366 !important;
    color: #fff !important;
    width: 100% !important;
}
.btn-nc > button {
    background: #E24B4A !important;
    color: #fff !important;
    width: 100% !important;
}
.btn-secondary > button {
    background: #fff !important;
    color: #0F2D1A !important;
    border: 0.5px solid #D6EDD9 !important;
}

/* ── Form card ── */
.form-card {
    background: #fff;
    border-radius: 14px;
    padding: 24px;
    border: 0.5px solid #D6EDD9;
    margin: 20px 24px;
}
.form-title { font-size: 18px; font-weight: 600; color: #0F2D1A; margin-bottom: 4px; }
.form-sub   { font-size: 13px; color: #6B8F72; margin-bottom: 20px; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] label { font-size: 12px !important; font-weight: 500 !important; color: #6B8F72 !important; text-transform: uppercase; letter-spacing: 0.04em; }
[data-testid="stSelectbox"] > div > div {
    border-radius: 10px !important;
    border-color: #D6EDD9 !important;
    background: #F5FAF6 !important;
}

/* ── Radio ── */
[data-testid="stRadio"] label { font-size: 13px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] .stSelectbox label { color: #5DAF78 !important; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: #EAFBF0; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0F2D1A;
    gap: 0;
    border-radius: 0;
    padding: 0 24px;
}
.stTabs [data-baseweb="tab"] {
    color: #5DAF78 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 12px 16px !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #7DC65A !important;
    border-bottom: 2px solid #7DC65A !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; background: #F5FAF6; }

/* ── Divider ── */
hr { border-color: #D6EDD9 !important; margin: 8px 0 !important; }

/* ── Summary chips ── */
.summary-row { display: flex; gap: 10px; padding: 12px 24px 0; }
.chip { flex: 1; border-radius: 10px; padding: 10px 14px; text-align: center; }
.chip-c  { background: #EAF5ED; }
.chip-nc { background: #FFF0F0; }
.chip-label { font-size: 10px; color: #6B8F72; font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; }
.chip-val { font-size: 24px; font-weight: 600; }
.chip-c .chip-val  { color: #1D6B35; }
.chip-nc .chip-val { color: #9C0006; }

/* ── Scrollable items ── */
.items-wrap { padding: 12px 24px; max-height: 60vh; overflow-y: auto; }

/* ── Alert ── */
.alert-nc {
    background: #FFF0F0; border: 0.5px solid #E24B4A;
    border-radius: 10px; padding: 12px 16px;
    font-size: 13px; color: #501313;
    margin: 0 24px 12px;
}
</style>
""", unsafe_allow_html=True)

# ── Dados ────────────────────────────────────────────────────
ITENS = {
    "Turno 1": {
        "Todos": [
            "Controle de Higiene e Saúde dos Colaboradores",
            "Checklist Diário de Higienização dos Ralos e Piso",
            "Controle de Sanitização dos Hortifrutis",
            "Controle de Cocção",
            "Controle de Troca de Óleo de Fritura",
            "Controle de Coleta de Amostras",
            "Controle de Temperatura de Alimentos na Distribuição",
            "Controle de Temperatura de Equipamentos de Apoio de Distribuição",
            "Controle de Temperatura dos Equipamentos no Armazenamento",
            "Checklist de Condições de Armazenamento",
            "Controle de Vetores e Pragas",
            "Ficha de Rastreabilidade",
            "Checklist de Entrega de Garrafas",
            "Controle de Limpeza",
            "Controle ASOS",
        ],
        "R1": ["Planilha de Monitoramento de Saída de Refeições"],
    },
    "Turno 2": {
        "Todos": [
            "Controle de Higiene e Saúde dos Colaboradores",
            "Checklist Diário de Higienização dos Ralos e Piso",
            "Controle de Sanitização dos Hortifrutis",
            "Controle de Cocção",
            "Controle de Coleta de Amostras",
            "Controle de Temperatura de Alimentos na Distribuição",
            "Controle de Temperatura de Equipamentos de Apoio de Distribuição",
            "Controle de Temperatura dos Equipamentos no Armazenamento",
            "Checklist de Condições de Armazenamento",
            "Controle de Vetores e Pragas",
            "Ficha de Rastreabilidade",
            "Checklist de Entrega de Garrafas",
            "Controle ASOS",
        ],
        "R1": ["Planilha de Monitoramento de Saída de Refeições"],
    },
    "Turno 3": {
        "Todos": [
            "Controle de Higiene e Saúde dos Colaboradores",
            "Checklist Diário de Higienização dos Ralos e Piso",
            "Controle de Sanitização dos Hortifrutis",
            "Controle de Cocção",
            "Controle de Coleta de Amostras",
            "Controle de Temperatura de Alimentos na Distribuição",
            "Controle de Temperatura de Equipamentos de Apoio de Distribuição",
            "Controle de Temperatura dos Equipamentos no Armazenamento",
            "Checklist de Condições de Armazenamento",
            "Controle de Vetores e Pragas",
            "Checklist de Entrega de Garrafas",
            "Enzilimp",
            "Controle ASOS",
        ],
        "R1": ["Planilha de Monitoramento de Saída de Refeições"],
    },
    "Turno Comercial": {
        "Sala VIP": [
            "Controle de Higiene e Saúde dos Colaboradores",
            "Checklist Diário de Higienização dos Ralos e Piso",
            "Controle de Sanitização dos Hortifrutis",
            "Controle de Cocção",
            "Controle de Troca de Óleo de Fritura",
            "Controle de Coleta de Amostras",
            "Controle de Temperatura de Alimentos na Distribuição",
            "Controle de Temperatura de Equipamentos de Apoio de Distribuição",
            "Controle de Temperatura dos Equipamentos no Armazenamento",
            "Checklist de Condições de Armazenamento",
            "Controle de Vetores e Pragas",
            "Ficha de Rastreabilidade",
            "Planilha de Monitoramento de Saída de Refeições",
            "Controle ASOS",
        ],
    },
}

FISCAIS = ["Adriele Ferreira","Luanna Mattos","Victoria Lucena","Karoline Teles","Tailândia","Larissa Brito"]
LOCAIS  = ["R1","R2","R3","R5","Sala VIP"]
TURNOS  = ["Turno 1","Turno 2","Turno 3","Turno Comercial"]

def get_itens(turno, local):
    if turno not in ITENS:
        return []
    grupos = ITENS[turno]
    itens = list(grupos.get("Todos", []))
    if local in grupos:
        itens += grupos[local]
    if "Sala VIP" in grupos and local == "Sala VIP":
        itens = list(grupos["Sala VIP"])
    return itens

# ── Session state ─────────────────────────────────────────────
if "tela" not in st.session_state:
    st.session_state.tela = "inicio"
if "respostas" not in st.session_state:
    st.session_state.respostas = {}
if "conf" not in st.session_state:
    st.session_state.conf = {}
if "historico" not in st.session_state:
    st.session_state.historico = []

# ── Top bar ───────────────────────────────────────────────────
fiscal_logado = st.session_state.get("fiscal", "Fiscal")
st.markdown(f"""
<div class="topbar">
    <div class="topbar-logo">Genba <span>Quality</span> Analytics</div>
    <div class="topbar-user">👤 {fiscal_logado}</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TELAS
# ═══════════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs(["📋  Nova Conferência", "📊  Histórico", "⚡  NCs Pendentes"])

# ── TAB 1: NOVA CONFERÊNCIA ────────────────────────────────────
with tab1:
    if st.session_state.tela == "inicio":
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">Nova Conferência</div>', unsafe_allow_html=True)
        st.markdown('<div class="form-sub">Selecione a unidade, turno e fiscal responsável</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            local  = st.selectbox("Unidade", LOCAIS)
        with col2:
            # filtrar turnos disponíveis para Sala VIP
            turnos_disp = ["Turno Comercial"] if local == "Sala VIP" else ["Turno 1","Turno 2","Turno 3"]
            turno  = st.selectbox("Turno", turnos_disp)

        fiscal = st.selectbox("Fiscal", FISCAIS)
        data_conf = st.date_input("Data", value=date.today())

        st.markdown("</div>", unsafe_allow_html=True)

        col_a, col_b = st.columns([3,1])
        with col_a:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("▶  Iniciar conferência", use_container_width=True):
                itens = get_itens(turno, local)
                st.session_state.conf = {
                    "local": local, "turno": turno,
                    "fiscal": fiscal, "data": str(data_conf),
                    "itens": itens
                }
                st.session_state.fiscal = fiscal
                st.session_state.respostas = {it: None for it in itens}
                st.session_state.tela = "conferencia"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.tela == "conferencia":
        conf = st.session_state.conf
        resp = st.session_state.respostas
        itens = conf["itens"]

        total   = len(itens)
        total_c  = sum(1 for v in resp.values() if v == "C")
        total_nc = sum(1 for v in resp.values() if v == "NC")
        avaliados = total_c + total_nc
        pct = int((avaliados / total) * 100) if total else 0

        # Header conferência
        st.markdown(f"""
        <div style="background:#0F2D1A;padding:12px 24px;">
            <div style="font-size:11px;color:#5DAF78;margin-bottom:4px;">← voltar</div>
            <div style="font-size:15px;font-weight:600;color:#EAFBF0;">{conf['local']} · {conf['turno']}</div>
            <div style="font-size:11px;color:#5DAF78;">{conf['data']} · {conf['fiscal']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Barra de progresso
        st.markdown(f"""
        <div class="progress-wrap">
            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{pct}%"></div></div>
            <div class="progress-label"><span>{avaliados} de {total} avaliados</span><span>{pct}%</span></div>
        </div>
        """, unsafe_allow_html=True)

        # Chips resumo
        st.markdown(f"""
        <div class="summary-row">
            <div class="chip chip-c"><div class="chip-label">Conformes</div><div class="chip-val">{total_c}</div></div>
            <div class="chip chip-nc"><div class="chip-label">Não Conformes</div><div class="chip-val">{total_nc}</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Itens
        st.markdown('<div class="items-wrap">', unsafe_allow_html=True)
        for item in itens:
            status = resp.get(item)
            card_cls = "item-card c" if status == "C" else "item-card nc" if status == "NC" else "item-card"
            badge = f'<span class="badge badge-c">C</span>' if status == "C" else f'<span class="badge badge-nc">NC</span>' if status == "NC" else f'<span class="badge badge-p">—</span>'
            st.markdown(f"""
            <div class="{card_cls}">
                <div class="item-name">{item}</div>
                {badge}
            </div>
            """, unsafe_allow_html=True)

            col_c, col_nc, col_r = st.columns([1,1,2])
            with col_c:
                if st.button("✔ C", key=f"c_{item}"):
                    st.session_state.respostas[item] = "C"
                    st.rerun()
            with col_nc:
                if st.button("✖ NC", key=f"nc_{item}"):
                    st.session_state.respostas[item] = "NC"
                    st.rerun()
            with col_r:
                if st.button("↺ Limpar", key=f"r_{item}"):
                    st.session_state.respostas[item] = None
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<hr>', unsafe_allow_html=True)

        # Botões de ação
        col_fin, col_wa = st.columns(2)

        with col_fin:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("✓ Finalizar conferência", use_container_width=True):
                registro = {
                    **conf,
                    "respostas": dict(resp),
                    "total_c": total_c,
                    "total_nc": total_nc,
                    "pct": pct,
                }
                st.session_state.historico.append(registro)
                st.session_state.tela = "inicio"
                st.success("Conferência finalizada e salva!")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        if total_nc > 0:
            ncs_texto = "\n".join([f"• {it}" for it, v in resp.items() if v == "NC"])
            msg = (
                f"🔍 *NCs — Genba Quality Analytics*\n"
                f"📍 {conf['local']} · {conf['turno']}\n"
                f"📅 {conf['data']}\n"
                f"👤 Fiscal: {conf['fiscal']}\n\n"
                f"❌ *Itens Não Conformes:*\n{ncs_texto}\n\n"
                f"✅ C: {total_c}  |  ❌ NC: {total_nc}  |  📊 {pct}% conformidade"
            )
            import urllib.parse
            wa_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
            with col_wa:
                st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background:#25D366;color:#fff;border:none;border-radius:10px;padding:10px 20px;font-size:13px;font-weight:500;width:100%;cursor:pointer;">📲 Enviar {total_nc} NCs via WhatsApp</button></a>', unsafe_allow_html=True)

        col_back = st.columns(1)[0]
        if st.button("← Voltar ao início"):
            st.session_state.tela = "inicio"
            st.rerun()

# ── TAB 2: HISTÓRICO ──────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">Conferências realizadas</div>', unsafe_allow_html=True)
    hist = st.session_state.historico
    if not hist:
        st.markdown("""
        <div style="text-align:center;padding:60px 24px;color:#6B8F72;">
            <div style="font-size:32px;margin-bottom:12px;">📋</div>
            <div style="font-size:15px;font-weight:500;color:#0F2D1A;">Nenhuma conferência ainda</div>
            <div style="font-size:13px;margin-top:4px;">As conferências finalizadas aparecerão aqui</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, h in enumerate(reversed(hist)):
            with st.expander(f"📍 {h['local']} · {h['turno']} · {h['data']} — {h['pct']}% conformidade"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Fiscal", h['fiscal'])
                col2.metric("✅ Conformes", h['total_c'])
                col3.metric("❌ Não Conformes", h['total_nc'])
                if h['total_nc'] > 0:
                    st.markdown("**Itens NC:**")
                    for it, v in h['respostas'].items():
                        if v == "NC":
                            st.markdown(f"- ❌ {it}")

# ── TAB 3: NCs PENDENTES ──────────────────────────────────────
with tab3:
    st.markdown('<div class="section-title">Não conformidades registradas</div>', unsafe_allow_html=True)
    hist = st.session_state.historico
    ncs_total = [(h, it) for h in hist for it, v in h['respostas'].items() if v == "NC"]

    if not ncs_total:
        st.markdown("""
        <div style="text-align:center;padding:60px 24px;color:#6B8F72;">
            <div style="font-size:32px;margin-bottom:12px;">✅</div>
            <div style="font-size:15px;font-weight:500;color:#1D6B35;">Nenhuma NC registrada</div>
            <div style="font-size:13px;margin-top:4px;">Todas as conferências estão conformes</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-nc">⚠️ {len(ncs_total)} não conformidade(s) registrada(s)</div>', unsafe_allow_html=True)
        st.markdown('<div class="items-wrap">', unsafe_allow_html=True)
        for h, it in ncs_total:
            st.markdown(f"""
            <div class="item-card nc">
                <div>
                    <div class="item-name">{it}</div>
                    <div style="font-size:11px;color:#888;margin-top:3px;">{h['local']} · {h['turno']} · {h['data']}</div>
                </div>
                <span class="badge badge-nc">NC</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
