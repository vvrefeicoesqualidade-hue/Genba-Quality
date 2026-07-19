import streamlit as st
import pandas as pd
import urllib.parse
import base64
from datetime import date, datetime, timedelta

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
    background: #F5FAF6 !important; font-family: 'Inter', sans-serif !important;
    max-width: 480px !important; margin: 0 auto !important;
}
[data-testid="stHeader"],[data-testid="stToolbar"],footer,#MainMenu { display: none !important; }
.block-container { padding: 0 !important; max-width: 480px !important; }
.topbar { background: #0F2D1A; padding: 16px 20px 14px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 999; }
.topbar-brand { font-size: 16px; font-weight: 600; color: #EAFBF0; letter-spacing: -0.3px; }
.topbar-brand span { color: #7DC65A; }
.topbar-user { font-size: 11px; color: #5DAF78; }
.card { background: #fff; border-radius: 14px; border: 0.5px solid #D6EDD9; margin: 12px 16px; padding: 16px; }
.card-title { font-size: 16px; font-weight: 600; color: #0F2D1A; margin-bottom: 4px; }
.card-sub { font-size: 12px; color: #6B8F72; margin-bottom: 16px; }
[data-testid="stSelectbox"] label,[data-testid="stDateInput"] label,[data-testid="stTextInput"] label {
    font-size: 11px !important; font-weight: 600 !important; color: #6B8F72 !important;
    text-transform: uppercase !important; letter-spacing: 0.05em !important;
}
[data-testid="stSelectbox"] > div > div,[data-testid="stDateInput"] > div > div {
    border-radius: 10px !important; border-color: #D6EDD9 !important; background: #F5FAF6 !important;
}
.stButton > button {
    border-radius: 12px !important; font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important; font-size: 14px !important;
    padding: 12px 20px !important; width: 100% !important; border: none !important;
}
.btn-green > button { background: #0F2D1A !important; color: #EAFBF0 !important; }
.btn-c > button { background: #1D9E75 !important; color: #fff !important; font-size: 13px !important; padding: 8px !important; }
.btn-nc > button { background: #E24B4A !important; color: #fff !important; font-size: 13px !important; padding: 8px !important; }
.btn-clear > button { background: #F0F4F1 !important; color: #6B8F72 !important; font-size: 12px !important; padding: 8px !important; }
.btn-back > button { background: #F0F4F1 !important; color: #0F2D1A !important; }
.btn-danger > button { background: #E24B4A !important; color: #fff !important; }
.prog-wrap { margin: 8px 16px 0; }
.prog-bg { height: 6px; background: #D6EDD9; border-radius: 99px; overflow: hidden; }
.prog-fill { height: 100%; background: #7DC65A; border-radius: 99px; }
.prog-label { display: flex; justify-content: space-between; font-size: 11px; color: #6B8F72; margin-top: 4px; }
.chips { display: flex; gap: 10px; margin: 10px 16px 0; }
.chip { flex: 1; border-radius: 12px; padding: 10px; text-align: center; }
.chip-c { background: #EAF5ED; } .chip-nc { background: #FFF0F0; } .chip-t { background: #E6F1FB; }
.chip-lbl { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; color: #6B8F72; }
.chip-val { font-size: 22px; font-weight: 700; }
.chip-c .chip-val { color: #1D6B35; } .chip-nc .chip-val { color: #9C0006; } .chip-t .chip-val { color: #185FA5; }
.item-row { background: #fff; border: 0.5px solid #D6EDD9; border-radius: 12px; padding: 12px 14px; margin-bottom: 6px; }
.item-row.c { border-color: #1D9E75; background: #EAF5ED; }
.item-row.nc { border-color: #E24B4A; background: #FFF0F0; }
.item-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.item-name { font-size: 13px; font-weight: 500; color: #0F2D1A; flex: 1; padding-right: 8px; line-height: 1.4; }
.item-row.nc .item-name { color: #501313; }
.badge { font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 99px; flex-shrink: 0; }
.badge-c { background: #1D9E75; color: #fff; } .badge-nc { background: #E24B4A; color: #fff; }
.badge-p { background: #E8F0E9; color: #6B8F72; border: 0.5px solid #D6EDD9; }
.conf-header { background: #0F2D1A; padding: 12px 16px 14px; }
.conf-title { font-size: 15px; font-weight: 600; color: #EAFBF0; }
.conf-meta { font-size: 11px; color: #5DAF78; margin-top: 2px; }
.section-lbl { font-size: 10px; font-weight: 700; color: #6B8F72; text-transform: uppercase; letter-spacing: 0.06em; padding: 14px 16px 6px; }
.empty-state { text-align: center; padding: 48px 24px; color: #6B8F72; }
.empty-icon { font-size: 40px; margin-bottom: 12px; }
.empty-title { font-size: 15px; font-weight: 600; color: #0F2D1A; }
.empty-sub { font-size: 13px; margin-top: 4px; }
.hist-card { background: #fff; border-radius: 12px; border: 0.5px solid #D6EDD9; padding: 14px 16px; margin: 6px 16px; }
.nc-card { background: #FFF0F0; border-radius: 12px; border: 0.5px solid #E24B4A; padding: 12px 16px; margin: 6px 16px; display: flex; align-items: center; justify-content: space-between; }
.nc-name { font-size: 13px; font-weight: 500; color: #501313; }
.nc-meta { font-size: 11px; color: #9C0006; margin-top: 2px; }
.rel-card { background: #fff; border-radius: 14px; border: 0.5px solid #D6EDD9; margin: 0 16px 8px; padding: 16px; }
.rel-card-title { font-size: 13px; font-weight: 600; color: #0F2D1A; margin-bottom: 12px; }
.bar-row { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.bar-label { font-size: 12px; color: #0F2D1A; font-weight: 500; width: 60px; flex-shrink: 0; }
.bar-bg { flex: 1; height: 20px; background: #F0F4F1; border-radius: 99px; overflow: hidden; }
.bar-fill-g { height: 100%; background: #1D9E75; border-radius: 99px; }
.bar-fill-r { height: 100%; background: #E24B4A; border-radius: 99px; }
.bar-pct { font-size: 12px; font-weight: 600; color: #0F2D1A; width: 38px; text-align: right; flex-shrink: 0; }
.chips-row { display: flex; gap: 8px; margin: 10px 16px; }
.sum-chip { flex: 1; background: #fff; border: 0.5px solid #D6EDD9; border-radius: 12px; padding: 12px 10px; text-align: center; }
.sum-chip-val { font-size: 20px; font-weight: 700; color: #0F2D1A; }
.sum-chip-lbl { font-size: 10px; color: #6B8F72; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; margin-top: 2px; }
.wa-link { display: block; background: #25D366; color: #fff; border-radius: 12px; padding: 14px; text-align: center; font-size: 14px; font-weight: 600; text-decoration: none; margin: 12px 16px; }
.div { height: 0.5px; background: #D6EDD9; margin: 12px 16px; }
.sync-ok { background: #EAF5ED; border: 0.5px solid #1D9E75; border-radius: 10px; padding: 8px 14px; font-size: 12px; color: #085041; margin: 8px 16px; }
.sync-err { background: #FFF0F0; border: 0.5px solid #E24B4A; border-radius: 10px; padding: 8px 14px; font-size: 12px; color: #501313; margin: 8px 16px; }
.fiscal-row { background: #fff; border: 0.5px solid #D6EDD9; border-radius: 10px; padding: 12px 14px; margin: 4px 16px; display: flex; align-items: center; justify-content: space-between; }
.fiscal-name { font-size: 14px; font-weight: 500; color: #0F2D1A; }
.admin-locked { background: #FAEEDA; border: 0.5px solid #EF9F27; border-radius: 12px; padding: 16px; margin: 12px 16px; }
.admin-title { font-size: 14px; font-weight: 600; color: #633806; margin-bottom: 4px; }
.admin-sub { font-size: 12px; color: #633806; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# ── Google Sheets ─────────────────────────────────────────────
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
SHEET_NAME = "Base_Conferencias APP Genba de Planilhas"

@st.cache_resource
def get_client():
    creds = Credentials.from_service_account_info(dict(st.secrets["gcp_service_account"]), scopes=SCOPES)
    return gspread.authorize(creds)

@st.cache_data(ttl=60)
def carregar_fiscais():
    try:
        sh = get_client().open(SHEET_NAME)
        ws = sh.worksheet("Usuários")
        rows = ws.get_all_records()
        return [r["Nome"] for r in rows if r.get("Perfil") == "Fiscal" and r.get("Ativo") == "Sim"], True
    except:
        return ["Adriele Ferreira","Luanna Mattos","Victoria Lucena","Karoline Teles","Tailândia","Larissa Brito"], False

@st.cache_data(ttl=60)
def carregar_historico():
    try:
        sh = get_client().open(SHEET_NAME)
        ws_conf = sh.worksheet("Conferências")
        ws_resp = sh.worksheet("Respostas")
        conf_rows = ws_conf.get_all_records()
        resp_rows = ws_resp.get_all_records()
        historico = []
        for c in conf_rows:
            if not c.get("ID_Conferencia"): continue
            respostas = {r["Nome_Item"]: r["Status_C_NC"] for r in resp_rows if r.get("ID_Conferencia") == c["ID_Conferencia"]}
            total_c = sum(1 for v in respostas.values() if v == "C")
            total_nc = sum(1 for v in respostas.values() if v == "NC")
            total = total_c + total_nc
            historico.append({
                "local": c.get("Local",""), "turno": c.get("Turno",""),
                "fiscal": c.get("Fiscal",""), "data": str(c.get("Data","")),
                "respostas": respostas, "total_c": total_c,
                "total_nc": total_nc, "pct": int((total_c/total)*100) if total else 0,
                "id": c["ID_Conferencia"],
            })
        return historico, True
    except:
        return [], False

def salvar_conferencia(conf, respostas):
    try:
        import uuid
        sh = get_client().open(SHEET_NAME)
        ws_conf = sh.worksheet("Conferências")
        ws_resp = sh.worksheet("Respostas")
        conf_id = str(uuid.uuid4())[:8]
        total_c = sum(1 for v in respostas.values() if v == "C")
        total_nc = sum(1 for v in respostas.values() if v == "NC")
        total = total_c + total_nc
        pct = int((total_c/total)*100) if total else 0
        ws_conf.append_row([conf_id, conf["data"], conf["turno"], conf["local"],
                            conf["fiscal"], "", "Finalizada", total, total_c, total_nc, f"{pct}%", ""])
        ws_resp.append_rows([[f"RS{conf_id}{i:03d}", conf_id, "", v, "", it, conf["turno"], conf["local"]]
                             for i, (it, v) in enumerate(respostas.items())])
        carregar_historico.clear()
        return True, conf_id
    except Exception as e:
        return False, str(e)

def adicionar_fiscal(nome):
    try:
        sh = get_client().open(SHEET_NAME)
        ws = sh.worksheet("Usuários")
        rows = ws.get_all_records()
        novo_id = f"US{len(rows)+1:03d}"
        ws.append_row([novo_id, nome, "Todos", "Todos", "Fiscal", "Sim", "", ""])
        carregar_fiscais.clear()
        return True
    except Exception as e:
        return False

def remover_fiscal(nome):
    try:
        sh = get_client().open(SHEET_NAME)
        ws = sh.worksheet("Usuários")
        cell = ws.find(nome)
        if cell:
            ws.update_cell(cell.row, 6, "Não")
        carregar_fiscais.clear()
        return True
    except:
        return False

# ── Dados fixos ───────────────────────────────────────────────
ITENS = {
    "Turno 1": {
        "Todos": ["Controle de Higiene e Saúde dos Colaboradores","Checklist Diário de Higienização dos Ralos e Piso","Controle de Sanitização dos Hortifrutis","Controle de Cocção","Controle de Troca de Óleo de Fritura","Controle de Coleta de Amostras","Controle de Temperatura de Alimentos na Distribuição","Controle de Temperatura de Equipamentos de Apoio de Distribuição","Controle de Temperatura dos Equipamentos no Armazenamento","Checklist de Condições de Armazenamento","Controle de Vetores e Pragas","Ficha de Rastreabilidade","Checklist de Entrega de Garrafas","Controle de Limpeza","Controle ASOS"],
        "R1": ["Planilha de Monitoramento de Saída de Refeições"],
    },
    "Turno 2": {
        "Todos": ["Controle de Higiene e Saúde dos Colaboradores","Checklist Diário de Higienização dos Ralos e Piso","Controle de Sanitização dos Hortifrutis","Controle de Cocção","Controle de Coleta de Amostras","Controle de Temperatura de Alimentos na Distribuição","Controle de Temperatura de Equipamentos de Apoio de Distribuição","Controle de Temperatura dos Equipamentos no Armazenamento","Checklist de Condições de Armazenamento","Controle de Vetores e Pragas","Ficha de Rastreabilidade","Checklist de Entrega de Garrafas","Controle ASOS"],
        "R1": ["Planilha de Monitoramento de Saída de Refeições"],
    },
    "Turno 3": {
        "Todos": ["Controle de Higiene e Saúde dos Colaboradores","Checklist Diário de Higienização dos Ralos e Piso","Controle de Sanitização dos Hortifrutis","Controle de Cocção","Controle de Coleta de Amostras","Controle de Temperatura de Alimentos na Distribuição","Controle de Temperatura de Equipamentos de Apoio de Distribuição","Controle de Temperatura dos Equipamentos no Armazenamento","Checklist de Condições de Armazenamento","Controle de Vetores e Pragas","Checklist de Entrega de Garrafas","Enzilimp","Controle ASOS"],
        "R1": ["Planilha de Monitoramento de Saída de Refeições"],
    },
    "Turno Comercial": {
        "Sala VIP": ["Controle de Higiene e Saúde dos Colaboradores","Checklist Diário de Higienização dos Ralos e Piso","Controle de Sanitização dos Hortifrutis","Controle de Cocção","Controle de Troca de Óleo de Fritura","Controle de Coleta de Amostras","Controle de Temperatura de Alimentos na Distribuição","Controle de Temperatura de Equipamentos de Apoio de Distribuição","Controle de Temperatura dos Equipamentos no Armazenamento","Checklist de Condições de Armazenamento","Controle de Vetores e Pragas","Ficha de Rastreabilidade","Planilha de Monitoramento de Saída de Refeições","Controle ASOS"],
    },
}
LOCAIS = ["R1","R2","R3","R5","Sala VIP"]

def get_itens(turno, local):
    if turno not in ITENS: return []
    g = ITENS[turno]
    if turno == "Turno Comercial": return list(g.get("Sala VIP",[]))
    return list(g.get("Todos",[])) + (g.get(local,[]) if local in g else [])

# ── Session state ─────────────────────────────────────────────
for k, v in [("tela","inicio"),("respostas",{}),("conf",{}),("fiscal","Fiscal"),
             ("historico_loaded",False),("admin_ok",False)]:
    if k not in st.session_state: st.session_state[k] = v

if not st.session_state.historico_loaded:
    with st.spinner("Carregando dados..."):
        hist, ok = carregar_historico()
        fiscais, _ = carregar_fiscais()
        st.session_state.historico = hist
        st.session_state.fiscais = fiscais
        st.session_state.sheets_ok = ok
        st.session_state.historico_loaded = True

# ── TOP BAR ───────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
    <div class="topbar-brand">Genba <span>Quality</span> Analytics</div>
    <div class="topbar-user">👤 {st.session_state.fiscal}</div>
</div>""", unsafe_allow_html=True)

sheets_status = "ok" if st.session_state.get("sheets_ok") else "err"
if sheets_status == "ok":
    st.markdown('<div class="sync-ok">✓ Conectado ao Google Sheets — dados salvos automaticamente</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="sync-err">⚠ Sem conexão com Sheets — configure as credenciais</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
if st.session_state.tela == "inicio":
    FISCAIS = st.session_state.get("fiscais", [])
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📋 Conferência","📊 Histórico","⚡ NCs","📈 Relatório","📅 Anual","⚙️ Config"])

    # ── TAB 1: NOVA CONFERÊNCIA ────────────────────────────────
    with tab1:
        st.markdown('<div class="card"><div class="card-title">Nova Conferência</div><div class="card-sub">Selecione a unidade e turno para iniciar</div>', unsafe_allow_html=True)
        local = st.selectbox("Unidade", LOCAIS, key="sel_local")
        turnos_disp = ["Turno Comercial"] if local == "Sala VIP" else ["Turno 1","Turno 2","Turno 3"]
        turno = st.selectbox("Turno", turnos_disp, key="sel_turno")
        fiscal = st.selectbox("Fiscal", FISCAIS if FISCAIS else ["—"], key="sel_fiscal")
        data_conf = st.date_input("Data", value=date.today(), key="sel_data")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div style="margin:0 16px 24px"><div class="btn-green">', unsafe_allow_html=True)
        if st.button("▶  Iniciar conferência", key="btn_iniciar", use_container_width=True):
            itens = get_itens(turno, local)
            st.session_state.conf = {"local":local,"turno":turno,"fiscal":fiscal,"data":str(data_conf),"itens":itens}
            st.session_state.fiscal = fiscal
            st.session_state.respostas = {it: None for it in itens}
            st.session_state.tela = "conferencia"
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── TAB 2: HISTÓRICO ──────────────────────────────────────
    with tab2:
        hist = st.session_state.historico
        if not hist:
            st.markdown('<div class="empty-state"><div class="empty-icon">📋</div><div class="empty-title">Nenhuma conferência ainda</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-lbl">Conferências realizadas</div>', unsafe_allow_html=True)
            for h in reversed(hist):
                nc_list = [it for it, v in h['respostas'].items() if v == "NC"]
                st.markdown(f"""<div class="hist-card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <div>
                            <div style="font-size:14px;font-weight:600;color:#0F2D1A;">📍 {h['local']} · {h['turno']}</div>
                            <div style="font-size:11px;color:#6B8F72;margin-top:2px;">{h['data']} · {h['fiscal']}</div>
                            <div style="margin-top:8px;font-size:12px;color:#6B8F72;">✅ {h['total_c']} C &nbsp;|&nbsp; ❌ {h['total_nc']} NC</div>
                            {''.join([f'<div style="font-size:11px;color:#9C0006;margin-top:2px;">• {n}</div>' for n in nc_list])}
                        </div>
                        <div style="font-size:18px;font-weight:700;color:#1D6B35;">{h['pct']}%</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── TAB 3: NCS ────────────────────────────────────────────
    with tab3:
        hist = st.session_state.historico
        ncs = [(h, it) for h in hist for it, v in h['respostas'].items() if v == "NC"]
        if not ncs:
            st.markdown('<div class="empty-state"><div class="empty-icon">✅</div><div class="empty-title">Nenhuma NC registrada</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="section-lbl">{len(ncs)} não conformidade(s)</div>', unsafe_allow_html=True)
            for h, it in ncs:
                st.markdown(f'<div class="nc-card"><div><div class="nc-name">{it}</div><div class="nc-meta">{h["local"]} · {h["turno"]} · {h["data"]}</div></div><span class="badge badge-nc">NC</span></div>', unsafe_allow_html=True)

    # ── TAB 4: RELATÓRIO ──────────────────────────────────────
    with tab4:
        hist = st.session_state.historico
        if not hist:
            st.markdown('<div class="empty-state"><div class="empty-icon">📈</div><div class="empty-title">Sem dados ainda</div></div>', unsafe_allow_html=True)
        else:
            df = pd.DataFrame([{"local":h["local"],"turno":h["turno"],"data":pd.to_datetime(h["data"]),"total_c":h["total_c"],"total_nc":h["total_nc"],"pct":h["pct"]} for h in hist])
            st.markdown('<div class="section-lbl">Filtros</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1: filtro_local = st.selectbox("Unidade", ["Todos"]+sorted(df["local"].unique().tolist()), key="rel_local")
            with c2: filtro_turno = st.selectbox("Turno", ["Todos"]+sorted(df["turno"].unique().tolist()), key="rel_turno")
            periodo = st.selectbox("Período", ["Todos","Última semana","Último mês","Últimos 3 meses"], key="rel_periodo")
            st.markdown('<div style="margin:0 0 16px"><div class="btn-green">', unsafe_allow_html=True)
            filtrar = st.button("🔍  Gerar relatório", key="btn_filtrar", use_container_width=True)
            st.markdown("</div></div>", unsafe_allow_html=True)
            if not filtrar and "rel_resultado" not in st.session_state:
                st.markdown('<div class="empty-state"><div class="empty-icon">📊</div><div class="empty-title">Selecione os filtros e toque em Gerar relatório</div></div>', unsafe_allow_html=True)
            else:
                if filtrar: st.session_state.rel_resultado = {"local":filtro_local,"turno":filtro_turno,"periodo":periodo}
                f = st.session_state.get("rel_resultado",{"local":filtro_local,"turno":filtro_turno,"periodo":periodo})
                df_f = df.copy()
                if f["local"] != "Todos": df_f = df_f[df_f["local"]==f["local"]]
                if f["turno"] != "Todos": df_f = df_f[df_f["turno"]==f["turno"]]
                hoje = pd.Timestamp.today()
                if f["periodo"]=="Última semana": df_f=df_f[df_f["data"]>=hoje-timedelta(days=7)]
                elif f["periodo"]=="Último mês": df_f=df_f[df_f["data"]>=hoje-timedelta(days=30)]
                elif f["periodo"]=="Últimos 3 meses": df_f=df_f[df_f["data"]>=hoje-timedelta(days=90)]
                if df_f.empty:
                    st.markdown('<div class="empty-state"><div class="empty-icon">🔍</div><div class="empty-title">Nenhum dado para esse filtro</div></div>', unsafe_allow_html=True)
                else:
                    tc=len(df_f); mp=int(df_f["pct"].mean()); tnc=int(df_f["total_nc"].sum())
                    st.markdown(f'<div class="chips-row"><div class="sum-chip"><div class="sum-chip-val">{tc}</div><div class="sum-chip-lbl">Conferências</div></div><div class="sum-chip"><div class="sum-chip-val" style="color:#1D6B35">{mp}%</div><div class="sum-chip-lbl">Conformidade</div></div><div class="sum-chip"><div class="sum-chip-val" style="color:#9C0006">{tnc}</div><div class="sum-chip-lbl">NCs</div></div></div>', unsafe_allow_html=True)
                    por_local = df_f.groupby("local")["pct"].mean().sort_values(ascending=False)
                    st.markdown('<div class="rel-card"><div class="rel-card-title">Conformidade por Unidade</div>', unsafe_allow_html=True)
                    bars=""
                    for l,p in por_local.items():
                        pv=int(p); cor="bar-fill-g" if pv>=80 else "bar-fill-r"
                        bars+=f'<div class="bar-row"><div class="bar-label">{l}</div><div class="bar-bg"><div class="{cor}" style="width:{pv}%"></div></div><div class="bar-pct">{pv}%</div></div>'
                    st.markdown(bars+"</div>", unsafe_allow_html=True)
                    nc_items={}
                    conf_f=set((str(r["data"].date()),r["local"],r["turno"]) for _,r in df_f.iterrows())
                    for h in hist:
                        if (h["data"],h["local"],h["turno"]) in conf_f:
                            for it,v in h["respostas"].items():
                                if v=="NC": nc_items[it]=nc_items.get(it,0)+1
                    if nc_items:
                        top_nc=sorted(nc_items.items(),key=lambda x:x[1],reverse=True)[:5]
                        max_v=max(v for _,v in top_nc)
                        st.markdown('<div class="rel-card"><div class="rel-card-title">Itens mais não conformes</div>', unsafe_allow_html=True)
                        nh=""
                        for item,count in top_nc:
                            pb=int((count/max_v)*100)
                            nh+=f'<div class="bar-row"><div class="bar-label" style="width:100px;font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{item[:18]}...</div><div class="bar-bg"><div class="bar-fill-r" style="width:{pb}%"></div></div><div class="bar-pct">{count}x</div></div>'
                        st.markdown(nh+"</div>", unsafe_allow_html=True)

    # ── TAB 5: ANUAL ──────────────────────────────────────────
    with tab5:
        hist = st.session_state.historico
        if not hist:
            st.markdown('<div class="empty-state"><div class="empty-icon">📅</div><div class="empty-title">Sem dados para o relatório anual</div></div>', unsafe_allow_html=True)
        else:
            df_a = pd.DataFrame([{"local":h["local"],"data":pd.to_datetime(h["data"]),"total_c":h["total_c"],"total_nc":h["total_nc"],"pct":h["pct"]} for h in hist])
            anos = sorted(df_a["data"].dt.year.unique().tolist(), reverse=True)
            ano_sel = st.selectbox("Ano", anos, key="ano_sel")
            df_ano = df_a[df_a["data"].dt.year==ano_sel]
            tc=len(df_ano); mp=int(df_ano["pct"].mean()); tnc=int(df_ano["total_nc"].sum())
            st.markdown(f'<div class="chips-row"><div class="sum-chip"><div class="sum-chip-val">{tc}</div><div class="sum-chip-lbl">Conferências</div></div><div class="sum-chip"><div class="sum-chip-val" style="color:#1D6B35">{mp}%</div><div class="sum-chip-lbl">Conformidade</div></div><div class="sum-chip"><div class="sum-chip-val" style="color:#9C0006">{tnc}</div><div class="sum-chip-lbl">NCs</div></div></div>', unsafe_allow_html=True)
            meses=["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
            por_mes=df_ano.groupby(df_ano["data"].dt.month)["pct"].mean()
            st.markdown('<div class="rel-card"><div class="rel-card-title">Conformidade por mês</div>', unsafe_allow_html=True)
            bm=""
            for m in range(1,13):
                if m in por_mes.index:
                    pv=int(por_mes[m]); cor="bar-fill-g" if pv>=80 else "bar-fill-r"
                    bm+=f'<div class="bar-row"><div class="bar-label" style="width:28px;font-size:10px;">{meses[m-1]}</div><div class="bar-bg"><div class="{cor}" style="width:{pv}%"></div></div><div class="bar-pct">{pv}%</div></div>'
            st.markdown(bm+"</div>", unsafe_allow_html=True)
            por_local=df_ano.groupby("local")["pct"].mean().sort_values(ascending=False)
            st.markdown('<div class="rel-card"><div class="rel-card-title">Conformidade por unidade</div>', unsafe_allow_html=True)
            bl=""
            for l,pv in por_local.items():
                pv=int(pv); cor="bar-fill-g" if pv>=80 else "bar-fill-r"
                bl+=f'<div class="bar-row"><div class="bar-label">{l}</div><div class="bar-bg"><div class="{cor}" style="width:{pv}%"></div></div><div class="bar-pct">{pv}%</div></div>'
            st.markdown(bl+"</div>", unsafe_allow_html=True)
            nc_ano={}
            for h in hist:
                if pd.to_datetime(h["data"]).year==ano_sel:
                    for it,v in h["respostas"].items():
                        if v=="NC": nc_ano[it]=nc_ano.get(it,0)+1
            if nc_ano:
                top_nc=sorted(nc_ano.items(),key=lambda x:x[1],reverse=True)[:5]
                max_v=max(v for _,v in top_nc)
                st.markdown('<div class="rel-card"><div class="rel-card-title">Top 5 itens não conformes</div>', unsafe_allow_html=True)
                nh=""
                for item,count in top_nc:
                    pb=int((count/max_v)*100)
                    nh+=f'<div class="bar-row"><div class="bar-label" style="width:100px;font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{item[:18]}...</div><div class="bar-bg"><div class="bar-fill-r" style="width:{pb}%"></div></div><div class="bar-pct">{count}x</div></div>'
                st.markdown(nh+"</div>", unsafe_allow_html=True)
            nc_rows="".join([f'<div style="background:#FFF0F0;border:1px solid #E24B4A;border-radius:8px;padding:8px 12px;margin-bottom:6px;display:flex;justify-content:space-between;"><span>{it}</span><strong>{c}x</strong></div>' for it,c in sorted(nc_ano.items(),key=lambda x:x[1],reverse=True)[:5]])
            local_rows="".join([f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;"><div style="width:100px;font-size:13px;">{l}</div><div style="flex:1;height:16px;background:#F0F4F1;border-radius:99px;overflow:hidden;"><div style="height:100%;background:{"#1D9E75" if int(p)>=80 else "#E24B4A"};width:{int(p)}%;border-radius:99px;"></div></div><div style="width:40px;text-align:right;font-size:13px;font-weight:700;">{int(p)}%</div></div>' for l,p in por_local.items()])
            mes_rows="".join([f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;"><div style="width:100px;font-size:13px;">{meses[m-1]}</div><div style="flex:1;height:16px;background:#F0F4F1;border-radius:99px;overflow:hidden;"><div style="height:100%;background:{"#1D9E75" if int(por_mes[m])>=80 else "#E24B4A"};width:{int(por_mes[m])}%;border-radius:99px;"></div></div><div style="width:40px;text-align:right;font-size:13px;font-weight:700;">{int(por_mes[m])}%</div></div>' for m in range(1,13) if m in por_mes.index])
            html_rel=f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{{font-family:Arial,sans-serif;max-width:800px;margin:0 auto;padding:40px;color:#0F2D1A;}}h1{{color:#0F2D1A;border-bottom:3px solid #7DC65A;padding-bottom:10px;}}h2{{color:#1D6B35;margin-top:30px;}}.cr{{display:flex;gap:20px;margin:20px 0;}}.ch{{flex:1;background:#EAF5ED;border-radius:10px;padding:16px;text-align:center;}}.cv{{font-size:32px;font-weight:700;}}.cl{{font-size:12px;color:#6B8F72;text-transform:uppercase;}}.footer{{margin-top:40px;padding-top:20px;border-top:1px solid #D6EDD9;font-size:12px;color:#6B8F72;}}</style></head><body><h1>Genba Quality Analytics — Relatório Anual {ano_sel}</h1><p>Gerado em {datetime.today().strftime('%d/%m/%Y')}</p><div class="cr"><div class="ch"><div class="cv">{tc}</div><div class="cl">Conferências</div></div><div class="ch"><div class="cv">{mp}%</div><div class="cl">Conformidade</div></div><div class="ch" style="background:#FFF0F0"><div class="cv" style="color:#9C0006">{tnc}</div><div class="cl">NCs</div></div></div><h2>Por Unidade</h2>{local_rows}<h2>Por Mês</h2>{mes_rows}<h2>Top NCs</h2>{nc_rows}<div class="footer">Genba Quality Analytics | Qualidade baseada em dados.</div></body></html>"""
            b64=base64.b64encode(html_rel.encode()).decode()
            st.markdown(f'<a href="data:text/html;base64,{b64}" download="Relatorio_Anual_{ano_sel}.html" style="display:block;background:#0F2D1A;color:#7DC65A;border-radius:12px;padding:13px;text-align:center;font-size:13px;font-weight:700;text-decoration:none;margin:12px 16px;">⬇ Baixar relatório {ano_sel}</a>', unsafe_allow_html=True)
            st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # ── TAB 6: CONFIGURAÇÕES ──────────────────────────────────
    with tab6:
        st.markdown('<div class="section-lbl">Acesso administrativo</div>', unsafe_allow_html=True)
        if not st.session_state.admin_ok:
            st.markdown('<div class="admin-locked"><div class="admin-title">🔒 Área restrita</div><div class="admin-sub">Digite a senha de administrador para acessar</div></div>', unsafe_allow_html=True)
            senha = st.text_input("Senha", type="password", key="senha_admin")
            st.markdown('<div style="margin:0 16px 24px"><div class="btn-green">', unsafe_allow_html=True)
            if st.button("Entrar", key="btn_admin", use_container_width=True):
                senha_correta = st.secrets.get("admin_password", "genba2024")
                if senha == senha_correta:
                    st.session_state.admin_ok = True
                    st.rerun()
                else:
                    st.error("Senha incorreta")
            st.markdown("</div></div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-lbl">Fiscais ativos</div>', unsafe_allow_html=True)
            fiscais = st.session_state.get("fiscais", [])
            for f in fiscais:
                col1, col2 = st.columns([4,1])
                with col1:
                    st.markdown(f'<div class="fiscal-row"><div class="fiscal-name">👤 {f}</div></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
                    if st.button("✕", key=f"del_{f}", use_container_width=True):
                        if remover_fiscal(f):
                            st.session_state.fiscais = [x for x in fiscais if x != f]
                            st.success(f"{f} removido!")
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="div"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-lbl">Adicionar fiscal</div>', unsafe_allow_html=True)
            novo_fiscal = st.text_input("Nome completo", key="novo_fiscal", placeholder="Ex: Maria Silva")
            st.markdown('<div style="margin:8px 16px 8px"><div class="btn-green">', unsafe_allow_html=True)
            if st.button("+ Adicionar fiscal", key="btn_add_fiscal", use_container_width=True):
                if novo_fiscal.strip():
                    if adicionar_fiscal(novo_fiscal.strip()):
                        st.session_state.fiscais.append(novo_fiscal.strip())
                        st.success(f"{novo_fiscal} adicionado!")
                        st.rerun()
                    else:
                        st.error("Erro ao adicionar. Verifique a conexão com o Sheets.")
                else:
                    st.warning("Digite o nome do fiscal.")
            st.markdown("</div></div>", unsafe_allow_html=True)

            st.markdown('<div class="div"></div>', unsafe_allow_html=True)
            st.markdown('<div style="margin:0 16px 24px"><div class="btn-back">', unsafe_allow_html=True)
            if st.button("🔒 Sair da área admin", key="btn_sair_admin", use_container_width=True):
                st.session_state.admin_ok = False
                st.rerun()
            st.markdown("</div></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
elif st.session_state.tela == "conferencia":
    conf = st.session_state.conf
    resp = st.session_state.respostas
    itens = conf["itens"]
    total_c=sum(1 for v in resp.values() if v=="C")
    total_nc=sum(1 for v in resp.values() if v=="NC")
    avaliados=total_c+total_nc
    total=len(itens)
    pct=int((total_c/total)*100) if total else 0
    st.markdown(f'<div class="conf-header"><div class="conf-title">{conf["local"]} · {conf["turno"]}</div><div class="conf-meta">{conf["data"]} · {conf["fiscal"]}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="prog-wrap"><div class="prog-bg"><div class="prog-fill" style="width:{pct}%"></div></div><div class="prog-label"><span>{avaliados} de {total} avaliados</span><span>{pct}%</span></div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chips"><div class="chip chip-c"><div class="chip-lbl">Conformes</div><div class="chip-val">{total_c}</div></div><div class="chip chip-nc"><div class="chip-lbl">Não Conformes</div><div class="chip-val">{total_nc}</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-lbl">Itens para avaliar</div>', unsafe_allow_html=True)
    for item in itens:
        status=resp.get(item)
        cls="item-row c" if status=="C" else "item-row nc" if status=="NC" else "item-row"
        bdg='<span class="badge badge-c">C</span>' if status=="C" else '<span class="badge badge-nc">NC</span>' if status=="NC" else '<span class="badge badge-p">—</span>'
        st.markdown(f'<div class="{cls}"><div class="item-top"><div class="item-name">{item}</div>{bdg}</div></div>', unsafe_allow_html=True)
        c1,c2,c3=st.columns([2,2,1])
        with c1:
            st.markdown('<div class="btn-c">', unsafe_allow_html=True)
            if st.button("✔ Conforme",key=f"c_{item}",use_container_width=True):
                st.session_state.respostas[item]="C"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="btn-nc">', unsafe_allow_html=True)
            if st.button("✖ Não Conforme",key=f"nc_{item}",use_container_width=True):
                st.session_state.respostas[item]="NC"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
            if st.button("↺",key=f"r_{item}",use_container_width=True):
                st.session_state.respostas[item]=None; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    if total_nc>0:
        ncs_txt="\n".join([f"• {it}" for it,v in resp.items() if v=="NC"])
        msg=f"🔍 *NCs — Genba Quality Analytics*\n📍 {conf['local']} · {conf['turno']}\n📅 {conf['data']}\n👤 Fiscal: {conf['fiscal']}\n\n❌ *Itens NC:*\n{ncs_txt}\n\n✅ C: {total_c}  ❌ NC: {total_nc}  📊 {pct}% conformidade"
        wa_url=f"https://wa.me/?text={urllib.parse.quote(msg)}"
        st.markdown(f'<a href="{wa_url}" target="_blank" class="wa-link">📲 Enviar {total_nc} NC(s) via WhatsApp</a>', unsafe_allow_html=True)
    c1,c2=st.columns([3,2])
    with c1:
        st.markdown('<div style="margin:0 0 0 16px"><div class="btn-green">', unsafe_allow_html=True)
        if st.button("✓ Finalizar",use_container_width=True):
            with st.spinner("Salvando no Google Sheets..."):
                ok,result=salvar_conferencia(conf,resp)
            if ok:
                st.session_state.historico.append({**conf,"respostas":dict(resp),"total_c":total_c,"total_nc":total_nc,"pct":pct,"id":result})
                st.session_state.tela="inicio"
                st.rerun()
            else:
                st.error(f"Erro ao salvar: {result}")
        st.markdown("</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="margin:0 16px 0 0"><div class="btn-back">', unsafe_allow_html=True)
        if st.button("← Voltar",use_container_width=True):
            st.session_state.tela="inicio"; st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
