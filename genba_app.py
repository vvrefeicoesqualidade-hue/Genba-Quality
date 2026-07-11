import streamlit as st
import urllib.parse
from datetime import date

st.set_page_config(
    page_title="Genba Quality Analytics",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #F5FAF6 !important;
    font-family: 'Inter', sans-serif !important;
    max-width: 480px !important;
    margin: 0 auto !important;
}

[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }

.block-container {
    padding: 0 !important;
    max-width: 480px !important;
}

/* TOP BAR */
.topbar {
    background: #0F2D1A;
    padding: 16px 20px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
}
.topbar-brand { font-size: 16px; font-weight: 600; color: #EAFBF0; letter-spacing: -0.3px; }
.topbar-brand span { color: #7DC65A; }
.topbar-user { font-size: 11px; color: #5DAF78; display: flex; align-items: center; gap: 4px; }

/* CARDS */
.card {
    background: #fff;
    border-radius: 14px;
    border: 0.5px solid #D6EDD9;
    margin: 12px 16px;
    padding: 16px;
}
.card-title { font-size: 16px; font-weight: 600; color: #0F2D1A; margin-bottom: 4px; }
.card-sub   { font-size: 12px; color: #6B8F72; margin-bottom: 16px; }

/* LABELS */
[data-testid="stSelectbox"] label,
[data-testid="stDateInput"] label {
    font-size: 11px !important;
    font-weight: 600 !important;
    color: #6B8F72 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-bottom: 4px !important;
}
[data-testid="stSelectbox"] > div > div,
[data-testid="stDateInput"] > div > div {
    border-radius: 10px !important;
    border-color: #D6EDD9 !important;
    background: #F5FAF6 !important;
    font-size: 14px !important;
}

/* BUTTONS */
.stButton > button {
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 12px 20px !important;
    width: 100% !important;
    border: none !important;
    transition: opacity 0.15s !important;
}
.btn-green > button { background: #0F2D1A !important; color: #EAFBF0 !important; }
.btn-c > button     { background: #1D9E75 !important; color: #fff !important; font-size: 13px !important; padding: 8px !important; }
.btn-nc > button    { background: #E24B4A !important; color: #fff !important; font-size: 13px !important; padding: 8px !important; }
.btn-clear > button { background: #F0F4F1 !important; color: #6B8F72 !important; font-size: 12px !important; padding: 8px !important; }
.btn-wa > button    { background: #25D366 !important; color: #fff !important; }
.btn-back > button  { background: #F0F4F1 !important; color: #0F2D1A !important; }

/* PROGRESS */
.prog-wrap { margin: 8px 16px 0; }
.prog-bg { height: 6px; background: #D6EDD9; border-radius: 99px; overflow: hidden; }
.prog-fill { height: 100%; background: #7DC65A; border-radius: 99px; }
.prog-label { display: flex; justify-content: space-between; font-size: 11px; color: #6B8F72; margin-top: 4px; }

/* CHIPS */
.chips { display: flex; gap: 10px; margin: 10px 16px 0; }
.chip { flex: 1; border-radius: 12px; padding: 10px; text-align: center; }
.chip-c  { background: #EAF5ED; }
.chip-nc { background: #FFF0F0; }
.chip-lbl { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; color: #6B8F72; }
.chip-val { font-size: 22px; font-weight: 700; }
.chip-c .chip-val  { color: #1D6B35; }
.chip-nc .chip-val { color: #9C0006; }

/* ITEM ROW */
.item-wrap { margin: 12px 16px 0; }
.item-row {
    background: #fff;
    border: 0.5px solid #D6EDD9;
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 6px;
}
.item-row.c  { border-color: #1D9E75; background: #EAF5ED; }
.item-row.nc { border-color: #E24B4A; background: #FFF0F0; }
.item-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.item-name { font-size: 13px; font-weight: 500; color: #0F2D1A; line-height: 1.4; flex: 1; padding-right: 8px; }
.item-row.nc .item-name { color: #501313; }
.badge { font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 99px; flex-shrink: 0; }
.badge-c  { background: #1D9E75; color: #fff; }
.badge-nc { background: #E24B4A; color: #fff; }
.badge-p  { background: #E8F0E9; color: #6B8F72; border: 0.5px solid #D6EDD9; }

/* CONF HEADER */
.conf-header {
    background: #0F2D1A;
    padding: 12px 16px 14px;
}
.conf-back { font-size: 11px; color: #5DAF78; margin-bottom: 6px; cursor: pointer; }
.conf-title { font-size: 15px; font-weight: 600; color: #EAFBF0; }
.conf-meta  { font-size: 11px; color: #5DAF78; margin-top: 2px; }

/* SECTION */
.section-lbl {
    font-size: 10px; font-weight: 700; color: #6B8F72;
    text-transform: uppercase; letter-spacing: 0.06em;
    padding: 14px 16px 6px;
}

/* EMPTY */
.empty-state { text-align: center; padding: 48px 24px; color: #6B8F72; }
.empty-icon  { font-size: 40px; margin-bottom: 12px; }
.empty-title { font-size: 15px; font-weight: 600; color: #0F2D1A; }
.empty-sub   { font-size: 13px; margin-top: 4px; }

/* HIST CARD */
.hist-card {
    background: #fff; border-radius: 12px;
    border: 0.5px solid #D6EDD9; padding: 14px 16px;
    margin: 6px 16px;
}
.hist-title { font-size: 14px; font-weight: 600; color: #0F2D1A; }
.hist-meta  { font-size: 11px; color: #6B8F72; margin-top: 2px; }
.hist-pct   { font-size: 18px; font-weight: 700; color: #1D6B35; }

/* NC CARD */
.nc-card {
    background: #FFF0F0; border-radius: 12px;
    border: 0.5px solid #E24B4A; padding: 12px 16px;
    margin: 6px 16px;
    display: flex; align-items: center; justify-content: space-between;
}
.nc-name { font-size: 13px; font-weight: 500; color: #501313; }
.nc-meta  { font-size: 11px; color: #9C0006; margin-top: 2px; }

/* WA BUTTON */
.wa-btn-wrap { margin: 12px 16px; }
.wa-link {
    display: block; background: #25D366; color: #fff;
    border-radius: 12px; padding: 14px;
    text-align: center; font-size: 14px; font-weight: 600;
    text-decoration: none; letter-spacing: -0.2px;
}

/* DIVIDER */
.div { height: 0.5px; background: #D6EDD9; margin: 12px 16px; }

/* BOTTOM ACTIONS */
.bottom-actions { padding: 12px 16px 24px; display: flex; flex-direction: column; gap: 8px; }
</style>
""", unsafe_allow_html=True)

# ── Dados ─────────────────────────────────────────────────────
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

def get_itens(turno, local):
    if turno not in ITENS: return []
    g = ITENS[turno]
    if turno == "Turno Comercial":
        return list(g.get("Sala VIP", []))
    itens = list(g.get("Todos", []))
    if local in g:
        itens += g[local]
    return itens

# ── Session state ─────────────────────────────────────────────
for k, v in [("tela","inicio"),("respostas",{}),("conf",{}),("historico",[]),("fiscal","Fiscal")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── TOP BAR ───────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
    <div class="topbar-brand">Genba <span>Quality</span> Analytics</div>
    <div class="topbar-user">👤 {st.session_state.fiscal}</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TELA: INÍCIO
# ═══════════════════════════════════════════════════════════════
if st.session_state.tela == "inicio":

    # Tabs mobile
    tab1, tab2, tab3 = st.tabs(["📋 Conferência", "📊 Histórico", "⚡ NCs"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Nova Conferência</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-sub">Selecione a unidade e turno para iniciar</div>', unsafe_allow_html=True)

        local = st.selectbox("Unidade", LOCAIS, key="sel_local")
        turnos_disp = ["Turno Comercial"] if local == "Sala VIP" else ["Turno 1","Turno 2","Turno 3"]
        turno = st.selectbox("Turno", turnos_disp, key="sel_turno")
        fiscal = st.selectbox("Fiscal", FISCAIS, key="sel_fiscal")
        data_conf = st.date_input("Data", value=date.today(), key="sel_data")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div style="margin: 0 16px 24px;">', unsafe_allow_html=True)
        st.markdown('<div class="btn-green">', unsafe_allow_html=True)
        if st.button("▶  Iniciar conferência", key="btn_iniciar", use_container_width=True):
            itens = get_itens(turno, local)
            st.session_state.conf = {"local":local,"turno":turno,"fiscal":fiscal,"data":str(data_conf),"itens":itens}
            st.session_state.fiscal = fiscal
            st.session_state.respostas = {it: None for it in itens}
            st.session_state.tela = "conferencia"
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    with tab2:
        hist = st.session_state.historico
        if not hist:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📋</div>
                <div class="empty-title">Nenhuma conferência ainda</div>
                <div class="empty-sub">As conferências finalizadas aparecerão aqui</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-lbl">Conferências realizadas</div>', unsafe_allow_html=True)
            for h in reversed(hist):
                nc_list = [it for it, v in h['respostas'].items() if v == "NC"]
                st.markdown(f"""
                <div class="hist-card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <div>
                            <div class="hist-title">📍 {h['local']} · {h['turno']}</div>
                            <div class="hist-meta">{h['data']} · {h['fiscal']}</div>
                            <div style="margin-top:8px;font-size:12px;color:#6B8F72;">
                                ✅ {h['total_c']} C &nbsp;|&nbsp; ❌ {h['total_nc']} NC
                            </div>
                            {''.join([f'<div style="font-size:11px;color:#9C0006;margin-top:3px;">• {n}</div>' for n in nc_list]) if nc_list else ''}
                        </div>
                        <div class="hist-pct">{h['pct']}%</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    with tab3:
        hist = st.session_state.historico
        ncs = [(h, it) for h in hist for it, v in h['respostas'].items() if v == "NC"]
        if not ncs:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">✅</div>
                <div class="empty-title">Nenhuma NC registrada</div>
                <div class="empty-sub">Todas as conferências estão conformes</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="section-lbl">{len(ncs)} não conformidade(s)</div>', unsafe_allow_html=True)
            for h, it in ncs:
                st.markdown(f"""
                <div class="nc-card">
                    <div>
                        <div class="nc-name">{it}</div>
                        <div class="nc-meta">{h['local']} · {h['turno']} · {h['data']}</div>
                    </div>
                    <span class="badge badge-nc">NC</span>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TELA: CONFERÊNCIA
# ═══════════════════════════════════════════════════════════════
elif st.session_state.tela == "conferencia":
    conf = st.session_state.conf
    resp = st.session_state.respostas
    itens = conf["itens"]

    total_c  = sum(1 for v in resp.values() if v == "C")
    total_nc = sum(1 for v in resp.values() if v == "NC")
    avaliados = total_c + total_nc
    total = len(itens)
    pct = int((avaliados / total) * 100) if total else 0

    # Header
    st.markdown(f"""
    <div class="conf-header">
        <div class="conf-title">{conf['local']} · {conf['turno']}</div>
        <div class="conf-meta">{conf['data']} · {conf['fiscal']}</div>
    </div>""", unsafe_allow_html=True)

    # Progress
    st.markdown(f"""
    <div class="prog-wrap">
        <div class="prog-bg"><div class="prog-fill" style="width:{pct}%"></div></div>
        <div class="prog-label"><span>{avaliados} de {total} avaliados</span><span>{pct}%</span></div>
    </div>""", unsafe_allow_html=True)

    # Chips
    st.markdown(f"""
    <div class="chips">
        <div class="chip chip-c"><div class="chip-lbl">Conformes</div><div class="chip-val">{total_c}</div></div>
        <div class="chip chip-nc"><div class="chip-lbl">Não Conformes</div><div class="chip-val">{total_nc}</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-lbl">Itens para avaliar</div>', unsafe_allow_html=True)

    # Itens
    for item in itens:
        status = resp.get(item)
        cls = "item-row c" if status == "C" else "item-row nc" if status == "NC" else "item-row"
        bdg = '<span class="badge badge-c">C</span>' if status=="C" else '<span class="badge badge-nc">NC</span>' if status=="NC" else '<span class="badge badge-p">—</span>'
        st.markdown(f"""
        <div class="{cls}">
            <div class="item-top">
                <div class="item-name">{item}</div>
                {bdg}
            </div>
        </div>""", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,2,1])
        with c1:
            st.markdown('<div class="btn-c">', unsafe_allow_html=True)
            if st.button("✔ Conforme", key=f"c_{item}", use_container_width=True):
                st.session_state.respostas[item] = "C"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="btn-nc">', unsafe_allow_html=True)
            if st.button("✖ Não Conforme", key=f"nc_{item}", use_container_width=True):
                st.session_state.respostas[item] = "NC"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
            if st.button("↺", key=f"r_{item}", use_container_width=True):
                st.session_state.respostas[item] = None; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    # WhatsApp
    if total_nc > 0:
        ncs_txt = "\n".join([f"• {it}" for it, v in resp.items() if v == "NC"])
        msg = (f"🔍 *NCs — Genba Quality Analytics*\n"
               f"📍 {conf['local']} · {conf['turno']}\n"
               f"📅 {conf['data']}\n"
               f"👤 Fiscal: {conf['fiscal']}\n\n"
               f"❌ *Itens NC:*\n{ncs_txt}\n\n"
               f"✅ C: {total_c}  ❌ NC: {total_nc}  📊 {pct}% conformidade")
        wa_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
        st.markdown(f"""
        <div class="wa-btn-wrap">
            <a href="{wa_url}" target="_blank" class="wa-link">
                📲 Enviar {total_nc} NC(s) via WhatsApp
            </a>
        </div>""", unsafe_allow_html=True)

    # Finalizar
    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown('<div style="margin:0 0 0 16px"><div class="btn-green">', unsafe_allow_html=True)
        if st.button("✓ Finalizar", use_container_width=True):
            st.session_state.historico.append({
                **conf, "respostas": dict(resp),
                "total_c": total_c, "total_nc": total_nc, "pct": pct
            })
            st.session_state.tela = "inicio"
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="margin:0 16px 0 0"><div class="btn-back">', unsafe_allow_html=True)
        if st.button("← Voltar", use_container_width=True):
            st.session_state.tela = "inicio"; st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
