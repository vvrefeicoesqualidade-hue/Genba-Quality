import streamlit as st
import pandas as pd
import urllib.parse
import base64
from datetime import date, datetime, timedelta

st.set_page_config(
    page_title="Genba Log",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { color-scheme: light !important; }
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
[data-testid="stSelectbox"] div[data-baseweb="select"] *,
[data-testid="stSelectbox"] div[data-baseweb="select"] input,
[data-testid="stDateInput"] input,
[data-testid="stTextInput"] input {
    color: #0F2D1A !important;
    -webkit-text-fill-color: #0F2D1A !important;
    opacity: 1 !important;
    font-weight: 500 !important;
}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    opacity: 1 !important;
}
[data-testid="stSelectbox"] svg {
    fill: #0F2D1A !important;
    opacity: 1 !important;
}
ul[data-baseweb="menu"], ul[role="listbox"] {
    background: #fff !important;
}
ul[data-baseweb="menu"] li, ul[role="listbox"] li {
    color: #0F2D1A !important;
    -webkit-text-fill-color: #0F2D1A !important;
    opacity: 1 !important;
}
.stButton > button {
    border-radius: 12px !important; font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important; font-size: 14px !important;
    padding: 12px 20px !important; width: 100% !important; border: none !important;
}
[class*="st-key-kgreen"] button { background: #0F2D1A !important; color: #EAFBF0 !important; }
[class*="st-key-kconf-"] button { background: #1D9E75 !important; color: #fff !important; font-size: 12px !important; padding: 8px 4px !important; }
[class*="st-key-knc-"] button { background: #E24B4A !important; color: #fff !important; font-size: 12px !important; padding: 8px 4px !important; }
[class*="st-key-kna-"] button { background: #F0F4F1 !important; color: #6B8F72 !important; font-size: 12px !important; padding: 8px 4px !important; border: 1px solid #D6EDD9 !important; }
[class*="st-key-kreset-"] button { background: #F0F4F1 !important; color: #6B8F72 !important; font-size: 12px !important; padding: 8px !important; }
[class*="st-key-kclear"] button { background: #F0F4F1 !important; color: #6B8F72 !important; font-size: 12px !important; padding: 8px !important; }
[class*="st-key-kback"] button { background: #F0F4F1 !important; color: #0F2D1A !important; }
[class*="st-key-kdanger"] button { background: #E24B4A !important; color: #fff !important; }
.prog-wrap { margin: 8px 16px 0; }
.prog-bg { height: 6px; background: #D6EDD9; border-radius: 99px; overflow: hidden; }
.prog-fill { height: 100%; background: #7DC65A; border-radius: 99px; }
.prog-label { display: flex; justify-content: space-between; font-size: 11px; color: #6B8F72; margin-top: 4px; }
.chips { display: flex; gap: 8px; margin: 10px 16px 0; }
.chip { flex: 1; border-radius: 12px; padding: 10px 6px; text-align: center; }
.chip-c { background: #EAF5ED; } .chip-nc { background: #FFF0F0; } .chip-na { background: #F0F4F1; }
.chip-lbl { font-size: 9px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em; color: #6B8F72; }
.chip-val { font-size: 20px; font-weight: 700; }
.chip-c .chip-val { color: #1D6B35; } .chip-nc .chip-val { color: #9C0006; } .chip-na .chip-val { color: #6B8F72; }
.item-row { background: #fff; border: 0.5px solid #D6EDD9; border-radius: 12px; padding: 12px 14px; margin-bottom: 6px; }
.item-row.c { border-color: #1D9E75; background: #EAF5ED; }
.item-row.nc { border-color: #E24B4A; background: #FFF0F0; }
.item-row.na { border-color: #B4B2A9; background: #F5F5F3; }
.item-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.item-name { font-size: 13px; font-weight: 500; color: #0F2D1A; flex: 1; padding-right: 8px; line-height: 1.4; }
.item-row.nc .item-name { color: #501313; }
.badge { font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 99px; flex-shrink: 0; }
.badge-c { background: #1D9E75; color: #fff; } .badge-nc { background: #E24B4A; color: #fff; } .badge-na { background: #B4B2A9; color: #fff; }
.badge-p { background: #E8F0E9; color: #6B8F72; border: 0.5px solid #D6EDD9; }
.conf-header { background: #0F2D1A; padding: 12px 16px 14px; }
.conf-title { font-size: 15px; font-weight: 600; color: #EAFBF0; }
.conf-meta { font-size: 11px; color: #5DAF78; margin-top: 2px; }
.section-lbl { font-size: 10px; font-weight: 700; color: #6B8F72; text-transform: uppercase; letter-spacing: 0.06em; padding: 14px 16px 6px; }
.cat-lbl { font-size: 12px; font-weight: 700; color: #0F2D1A; background: #EAF5ED; padding: 8px 16px; margin-top: 6px; }
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
.rank-row { display: flex; align-items: center; justify-content: space-between; padding: 9px 0; border-bottom: 0.5px solid #EEF4EF; }
.rank-row:last-child { border-bottom: none; }
.rank-left { display: flex; align-items: center; gap: 10px; }
.rank-pos { width: 22px; height: 22px; border-radius: 50%; background: #F0F4F1; color: #6B8F72; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.rank-pos.top { background: #FFF0F0; color: #9C0006; }
.rank-local { font-size: 13px; color: #0F2D1A; font-weight: 500; }
.rank-nc { font-size: 13px; font-weight: 700; color: #9C0006; }
.rank-nc.zero { color: #1D6B35; }
.bar-row { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.bar-label { font-size: 12px; color: #0F2D1A; font-weight: 500; width: 60px; flex-shrink: 0; }
.bar-bg { flex: 1; height: 20px; background: #F0F4F1; border-radius: 99px; overflow: hidden; }
.bar-fill-g { height: 100%; background: #1D9E75; border-radius: 99px; }
.bar-fill-r { height: 100%; background: #E24B4A; border-radius: 99px; }
.bar-pct { font-size: 12px; font-weight: 600; color: #0F2D1A; width: 38px; text-align: right; flex-shrink: 0; }
.chips-row { display: flex; gap: 8px; margin: 10px 16px; }
.sum-chip { flex: 1; background: #fff; border: 0.5px solid #D6EDD9; border-radius: 12px; padding: 12px 8px; text-align: center; }
.sum-chip-val { font-size: 18px; font-weight: 700; color: #0F2D1A; }
.sum-chip-lbl { font-size: 9px; color: #6B8F72; font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em; margin-top: 2px; }
.wa-link { display: block; background: #25D366; color: #fff; border-radius: 12px; padding: 14px; text-align: center; font-size: 14px; font-weight: 600; text-decoration: none; margin: 12px 16px; }
.div { height: 0.5px; background: #D6EDD9; margin: 12px 16px; }
.sync-ok { background: #EAF5ED; border: 0.5px solid #1D9E75; border-radius: 10px; padding: 8px 14px; font-size: 12px; color: #085041; margin: 8px 16px; }
.sync-err { background: #FFF0F0; border: 0.5px solid #E24B4A; border-radius: 10px; padding: 8px 14px; font-size: 12px; color: #501313; margin: 8px 16px; }
.fiscal-row { background: #fff; border: 0.5px solid #D6EDD9; border-radius: 10px; padding: 12px 14px; margin: 4px 16px; display: flex; align-items: center; justify-content: space-between; }
.fiscal-name { font-size: 14px; font-weight: 500; color: #0F2D1A; }
.admin-locked { background: #FAEEDA; border: 0.5px solid #EF9F27; border-radius: 12px; padding: 16px; margin: 12px 16px; }
.admin-title { font-size: 14px; font-weight: 600; color: #633806; margin-bottom: 4px; }
.admin-sub { font-size: 12px; color: #633806; margin-bottom: 12px; }
[data-testid="stTextArea"] textarea {
    border-radius: 10px !important; border-color: #D6EDD9 !important; background: #F5FAF6 !important;
    color: #0F2D1A !important; font-size: 12px !important;
}
[data-testid="stTextArea"] label {
    font-size: 10px !important; font-weight: 600 !important; color: #6B8F72 !important;
    text-transform: uppercase !important; letter-spacing: 0.05em !important;
}
.comment-wrap { margin: -4px 16px 10px; }
</style>
""", unsafe_allow_html=True)

# ── Google Sheets ─────────────────────────────────────────────
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SHEET_NAME = "Base_GenbaDiario"

@st.cache_resource
def get_client():
    creds = Credentials.from_service_account_info(dict(st.secrets["gcp_service_account"]), scopes=SCOPES)
    return gspread.authorize(creds)

@st.cache_data(ttl=60)
def carregar_nutricionistas():
    try:
        sh = get_client().open(SHEET_NAME)
        ws = sh.worksheet("Usuários")
        rows = ws.get_all_records()
        return [r["Nome"] for r in rows if r.get("Perfil") == "Nutricionista de Qualidade" and r.get("Ativo") == "Sim"], True
    except:
        return ["Adriele Ferreira", "Luanna Mattos", "Victoria Lucena"], False

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
            if not c.get("ID_Conferencia"):
                continue
            respostas = {r["Nome_Item"]: r["Status_C_NC_NA"] for r in resp_rows if r.get("ID_Conferencia") == c["ID_Conferencia"]}
            comentarios = {r["Nome_Item"]: r.get("Comentario", "") for r in resp_rows if r.get("ID_Conferencia") == c["ID_Conferencia"]}
            total_c = sum(1 for v in respostas.values() if v == "C")
            total_nc = sum(1 for v in respostas.values() if v == "NC")
            total_na = sum(1 for v in respostas.values() if v == "NA")
            total = total_c + total_nc
            historico.append({
                "local": c.get("Local", ""), "nutricionista": c.get("Nutricionista", ""),
                "data": str(c.get("Data", "")), "respostas": respostas, "comentarios": comentarios,
                "total_c": total_c, "total_nc": total_nc, "total_na": total_na,
                "pct": int((total_c / total) * 100) if total else 0,
                "id": c["ID_Conferencia"],
            })
        return historico, True
    except:
        return [], False

def salvar_conferencia(conf, respostas, comentarios=None):
    try:
        import uuid
        comentarios = comentarios or {}
        sh = get_client().open(SHEET_NAME)
        ws_conf = sh.worksheet("Conferências")
        ws_resp = sh.worksheet("Respostas")
        conf_id = str(uuid.uuid4())[:8]
        total_c = sum(1 for v in respostas.values() if v == "C")
        total_nc = sum(1 for v in respostas.values() if v == "NC")
        total_na = sum(1 for v in respostas.values() if v == "NA")
        total_itens = len(respostas)
        total_avaliado = total_c + total_nc
        pct = int((total_c / total_avaliado) * 100) if total_avaliado else 0
        ws_conf.append_row([conf_id, conf["data"], conf["local"], "", conf["nutricionista"],
                             "Finalizada", total_itens, total_c, total_nc, total_na, f"{pct}%", ""])
        ws_resp.append_rows([[f"RS{conf_id}{i:03d}", conf_id, "", v, comentarios.get(it, ""), it, conf["local"]]
                              for i, (it, v) in enumerate(respostas.items())])
        carregar_historico.clear()
        return True, conf_id
    except Exception as e:
        return False, str(e)

def adicionar_nutricionista(nome):
    try:
        sh = get_client().open(SHEET_NAME)
        ws = sh.worksheet("Usuários")
        rows = ws.get_all_records()
        novo_id = f"US{len(rows) + 1:03d}"
        ws.append_row([novo_id, nome, "Todos", "Nutricionista de Qualidade", "Sim", "", ""])
        carregar_nutricionistas.clear()
        return True
    except Exception:
        return False

def remover_nutricionista(nome):
    try:
        sh = get_client().open(SHEET_NAME)
        ws = sh.worksheet("Usuários")
        cell = ws.find(nome)
        if cell:
            ws.update_cell(cell.row, 5, "Não")
        carregar_nutricionistas.clear()
        return True
    except:
        return False

def apagar_conferencia(conf_id):
    try:
        sh = get_client().open(SHEET_NAME)
        ws_conf = sh.worksheet("Conferências")
        ws_resp = sh.worksheet("Respostas")
        cell = ws_conf.find(conf_id)
        if not cell:
            return False, f"ID_Conferencia '{conf_id}' não encontrado na aba Conferências."
        ws_conf.batch_clear([f"A{cell.row}:Z{cell.row}"])
        resp_cells = ws_resp.findall(conf_id)
        if resp_cells:
            ranges = [f"A{c.row}:Z{c.row}" for c in resp_cells]
            ws_resp.batch_clear(ranges)
        carregar_historico.clear()
        return True, ""
    except Exception as e:
        return False, str(e)

def apagar_todo_historico():
    try:
        sh = get_client().open(SHEET_NAME)
        ws_conf = sh.worksheet("Conferências")
        ws_resp = sh.worksheet("Respostas")
        if ws_conf.row_count > 1:
            ws_conf.batch_clear([f"A2:Z{ws_conf.row_count}"])
        if ws_resp.row_count > 1:
            ws_resp.batch_clear([f"A2:Z{ws_resp.row_count}"])
        carregar_historico.clear()
        return True, ""
    except Exception as e:
        return False, str(e)

# ── Checklist (itens) ────────────────────────────────────────
CATEGORIAS = [
    ("Manipuladores", [
        "Asseio corporal e do vestuário (incluindo ausência de barba)",
        "Higienização de mãos a cada troca de atividade, antes e após uso de luvas descartáveis",
        "Ausência de lesões e/ou sintomas de enfermidades que comprometam a segurança dos alimentos",
        "Uniforme padrão completo e EPI's em condições adequadas (sem camisas de eventos/datas comemorativas)",
        "Cabelos totalmente cobertos; quando usado gorro, touca descartável por baixo",
        "Roupas e objetos pessoais guardados em local específico",
        "Ausência de adornos, maquiagem e cílios postiços",
        "Unhas curtas, sem alongamento artificial e sem pintura",
        "Abstenção de fumo, manuseio de dinheiro e outros atos que comprometam a higiene (tocar máscara, provar alimento na mão, tocar protetor auricular, etc.)",
        "Visitantes/terceiros seguem requisitos mínimos de higiene ao entrar na cozinha (touca, sapato de segurança, capa, sem adornos)",
    ]),
    ("Recebimento de Mercadorias", [
        "Recepção em área protegida e limpa",
        "Inspeção sensorial e das condições físicas das embalagens",
        "Materiais reprovados/vencidos identificados e separados imediatamente",
        "Acondicionamento em paletes, estrados e/ou prateleiras higienizados",
        "Transferência de produtos de caixas de madeira/ráfia para monoblocos ou sacos plásticos próprios",
        "Avaliação das condições do entregador e do veículo",
    ]),
    ("Estoque Seco", [
        "Limpeza e organização (pisos, paredes, teto, prateleiras, caixas, estrados)",
        "Produtos químicos separados dos alimentos, em local fechado e identificado",
        "Recipientes de produtos químicos identificados (com data de diluição quando aplicável)",
        "Departamentalização por tipo, evitando cruzamento entre alimentos, descartáveis e químicos",
        "Produtos sobre prateleiras/paletes, sem contato direto com o piso",
        "Prateleiras identificadas com etiqueta padrão",
        "Etiquetas, validade e rastreabilidade dos produtos em dia",
        "Retirada de produtos segue critério PVPS",
        "Ausência de caixas de papelão (ou envelopadas quando presentes)",
        "Produtos de desinfecção de alimentos armazenados separados dos demais químicos",
    ]),
    ("Câmaras e Refrigeração", [
        "Limpeza e organização de câmaras, freezers, geladeiras e gelopar",
        "Verificação e controle de temperatura",
        "Bom estado de conservação dos equipamentos",
        "Produtos identificados, íntegros, dentro da validade e com boas características organolépticas",
        "Reembalagem e identificação corretas após abertura",
        "Armazenamento imediato após recebimento, por prioridade (refrigerados/congelados)",
        "Caixas plásticas limpas e íntegras",
        "Pré-seleção dos hortifrútis, sem resíduos e com boa aparência",
        "Ausência de papelão/ráfia/estopa em contato com os alimentos",
        "Alimentos separados por gênero, sem cruzamento entre crus e preparados",
        "Ovos armazenados refrigerados, longe de calor, embalados e identificados",
        "Controle de fluxo de entrada e saída de insumos",
    ]),
    ("Áreas de Produção", [
        "Limpeza e organização geral (pisos, paredes, teto, equipamentos, móveis)",
        "Limpeza e organização da área da salada",
        "Limpeza e organização da área da sobremesa",
        "Embalagem de gelatinas conforme padrão",
        "Etiquetas corretas nas preparações",
        "Ausência de contaminação cruzada (cru x cozido, sujo x limpo, entre gêneros, pragas)",
        "Descongelamento correto (por lotes, protegido, temperatura monitorada ≤ +5°C, etiqueta padrão)",
        "Descongelamento forçado seguro (embalado, água corrente, temperatura monitorada)",
        "Prova de alimentos com utensílios/copos descartáveis exclusivos",
        "Uso de luvas descartáveis nas etapas críticas (sanduíches, doces, hortifrútis pós-desinfecção, prontos, frutas ácidas)",
        "Pré-preparo de carnes in natura em lote, respeitando tempo/temperatura",
        "Potes de condimentos limpos, identificados e dentro da validade",
        "Sanitização do FVL conforme instruções do fabricante, com validação por fita teste",
        "Cocção atinge temperatura adequada",
        "Matérias-primas e preparações da UPR identificadas, protegidas e em temperatura adequada",
        "Catação de grãos antes do cozimento, em local iluminado",
        "Finalização das preparações com pegadores, pinças, luvas",
        "Placas de polietileno limpas, conservadas e usadas por cor",
        "Utensílios de apoio limpos, secos e protegidos",
        "Lavatório exclusivo para mãos, abastecido corretamente",
        "Reaproveitamento de alimentos conforme Manual de Boas Práticas",
        "Dessalgue de carnes iniciado com antecedência e em condições seguras",
        "Medidas de controle para corpos estranhos",
        "Qualidade dos insumos em processamento",
    ]),
    ("Boiler / Área Quente", [
        "Limpeza de paredes e portas",
        "Estado de conservação dos utensílios",
        "Processo de higienização adequado",
    ]),
    ("Área de Pães", [
        "Etiquetas e controle de validade",
    ]),
    ("Área de Lavagem (Triagem e Panelário) / Copa", [
        "Limpeza de pisos, paredes, teto, pias",
        "Utensílios sujos/não higienizados fora do contato direto com o piso",
        "Utensílios higienizados organizados e protegidos em bancadas e prateleiras",
        "Secagem segura (natural ou pano descartável)",
        "Móveis e equipamentos limpos e conservados",
        "Máquina de lavar louças limpa e abastecida com produtos químicos corretos",
        "Controle de produtos químicos utilizados",
    ]),
    ("Bebida Litro", [
        "Higienização das garrafas térmicas",
        "Organização das prateleiras",
    ]),
    ("DML", [
        "Organização dos produtos químicos",
        "Controle de abastecimento",
    ]),
    ("Distribuição / Salão", [
        "Limpeza do piso, balcões, grills e equipamentos de distribuição",
        "Limpeza das máquinas de bebidas",
        "Utensílios de apoio limpos, secos e em quantidade suficiente",
        "Recipientes de molhos/alimentos adicionais limpos e identificados",
        "Etiquetas corretas em produtos químicos",
        "Uso de luvas descartáveis no porcionamento e uso de peróxi food",
        "Sobras limpas dentro dos critérios aceitáveis de quantidade",
        "Retratamento controlado dos alimentos de reposição",
        "Reposições sem contato direto com o manipulador",
        "Manutenção da limpeza durante o serviço",
        "Ausência de preparações de risco/proibidas na linha",
        "Ausência de evidências de pragas",
        "Pias dos clientes abastecidas com sabão e papel toalha",
    ]),
    ("Instalações e Áreas Gerais", [
        "Limpeza das rampas (incluindo parte inferior e entre elas)",
        "Limpeza e organização dos passthrough",
        "Limpeza dos elevadores",
        "Limpeza e organização da doca",
        "Controle do lixo orgânico (borra de café, casca de ovos – pesagem)",
        "Aberturas externas e exaustão com telas milimetradas removíveis",
        "Ausência de objetos em desuso ou estranhos ao ambiente",
        "Luminárias apropriadas e protegidas",
        "Equipamentos e filtros de climatização limpos e conservados",
        "Balança íntegra, limpa, calibrada e higienizada após uso",
        "Pias com sifão adequado",
        "Coletores de resíduos limpos, identificados e abastecidos",
        "Utensílios de limpeza adequados, conservados e bem armazenados",
        "Produtos químicos regulamentados em quantidade suficiente",
        "Quadros informativos e adesivos atualizados e conservados",
        "Documentação e licenças expostas e atualizadas no quadro Gestão à Vista",
    ]),
    ("Lixeira Central", [
        "Limpeza de pisos, paredes, teto, luminárias, portas, paletes, lixeiras",
        "Sacos de resíduos acomodados corretamente (paletes/lixeiras)",
        "Sistema de refrigeração funcionando adequadamente",
    ]),
    ("Controles de Qualidade", [
        "Teste de AFVT",
        "Coleta e acondicionamento correto das amostras (higienização prévia, sem contato interno, etiqueta padrão, quantidade mínima)",
        "Controle de temperatura (pista quente/fria, câmaras, distribuição)",
    ]),
]
TODOS_ITENS = [item for _, itens in CATEGORIAS for item in itens]
LOCAIS = ["R1", "R2", "R3", "R5", "Sala VIP"]

# ── Session state ─────────────────────────────────────────────
for k, v in [("tela", "splash"), ("respostas", {}), ("comentarios", {}), ("conf", {}), ("nutricionista", "Nutricionista"),
             ("historico_loaded", False), ("admin_ok", False), ("confirm_wipe_all", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# SPLASH
if st.session_state.tela == "splash":
    st.markdown("""
<style>
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
.main, .block-container {
    background: #0F2D1A !important;
}
[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(circle at 12% 18%, rgba(125,198,90,0.10) 0%, rgba(125,198,90,0) 42%),
        radial-gradient(circle at 88% 86%, rgba(125,198,90,0.08) 0%, rgba(125,198,90,0) 40%) !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute; top: 6%; left: -18%;
    width: 260px; height: 260px; border-radius: 50%;
    border: 1.5px solid rgba(125,198,90,0.22);
    pointer-events: none;
}
[data-testid="stAppViewContainer"]::after {
    content: "";
    position: absolute; bottom: 4%; right: -20%;
    width: 220px; height: 220px; border-radius: 50%;
    border: 1.5px solid rgba(125,198,90,0.16);
    pointer-events: none;
}
.splash-line-1, .splash-line-2 {
    position: absolute; height: 1px; background: rgba(125,198,90,0.28);
    pointer-events: none;
}
.splash-line-1 { top: 11%; right: 8%; width: 90px; transform: rotate(-32deg); }
.splash-line-2 { bottom: 18%; left: 6%; width: 70px; transform: rotate(-28deg); }
.splash-wrap { text-align: center; padding: 90px 28px 0; position: relative; z-index: 2; }
.splash-brand-name { font-size: 26px; font-weight: 800; color: #F4FBF5; letter-spacing: -0.4px; margin-bottom: 6px; }
.splash-brand-sub { font-size: 13px; color: #5DAF78; margin-bottom: 26px; }
.splash-divider { width: 46px; height: 2px; background: #7DC65A; border-radius: 99px; margin: 0 auto 26px; }
.splash-title { font-size: 21px; font-weight: 700; color: #EAFBF0; margin-bottom: 6px; }
.splash-sub { font-size: 13px; color: #5DAF78; margin-bottom: 34px; }
.splash-brand { font-size: 11px; color: #6FAE7E; margin-top: 22px; }
.splash-credit { font-size: 10px; color: #3a7a4a; margin-top: 4px; }
div[data-testid="stVerticalBlock"] .stButton { padding: 0 28px; position: relative; z-index: 2; }
.stButton > button { background: #7DC65A !important; color: #0F2D1A !important; font-weight: 700 !important; border-radius: 14px !important; padding: 15px !important; font-size: 15px !important; box-shadow: 0 6px 18px rgba(125,198,90,0.25) !important; }
</style>
<div class="splash-line-1"></div>
<div class="splash-line-2"></div>
<div class="splash-wrap">
    <div class="splash-brand-name">VV Refeições</div>
    <div class="splash-brand-sub">A refeição caseira da sua empresa</div>
    <div class="splash-divider"></div>
    <div class="splash-title">Genba Log</div>
    <div class="splash-sub">Qualidade baseada em dados.</div>
</div>""", unsafe_allow_html=True)
    if st.button("▶  Entrar", key="btn_entrar", use_container_width=True):
        st.session_state.tela = "inicio"
        st.rerun()
    st.markdown("""
<div style="text-align:center;position:relative;z-index:2;">
    <div class="splash-brand">VV Refeições · v1.0</div>
    <div class="splash-credit">Elaborado por Victoria Lucena · GestHD</div>
</div>""", unsafe_allow_html=True)
    st.stop()

if not st.session_state.historico_loaded:
    with st.spinner("Carregando dados..."):
        hist, ok = carregar_historico()
        nutris, _ = carregar_nutricionistas()
        st.session_state.historico = hist
        st.session_state.nutricionistas = nutris
        st.session_state.sheets_ok = ok
        st.session_state.historico_loaded = True

# ── TOP BAR ───────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
    <div class="topbar-brand">Genba <span>Log</span></div>
    <div class="topbar-user">👤 {st.session_state.nutricionista}</div>
</div>""", unsafe_allow_html=True)

sheets_status = "ok" if st.session_state.get("sheets_ok") else "err"
if sheets_status == "ok":
    st.markdown('<div class="sync-ok">✓ Conectado ao Google Sheets — dados salvos automaticamente</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="sync-err">⚠ Sem conexão com Sheets — configure as credenciais</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
if st.session_state.tela == "inicio":
    NUTRIS = st.session_state.get("nutricionistas", [])
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📋 Conferência", "📊 Histórico", "⚡ NCs", "📈 Relatório", "📅 Anual", "⚙️ Config"])

    # ── TAB 1: NOVA CONFERÊNCIA ────────────────────────────────
    with tab1:
        st.markdown('<div class="card"><div class="card-title">Nova Conferência</div><div class="card-sub">Selecione a unidade para iniciar</div>', unsafe_allow_html=True)
        local = st.selectbox("Unidade", LOCAIS, key="sel_local")
        nutricionista = st.selectbox("Nutricionista de Qualidade", NUTRIS if NUTRIS else ["—"], key="sel_nutri")
        data_conf = st.date_input("Data", value=date.today(), key="sel_data")
        st.markdown("</div>", unsafe_allow_html=True)
        with st.container(key="kgreen_iniciar"):
            if st.button("▶  Iniciar conferência", key="btn_iniciar", use_container_width=True):
                st.session_state.conf = {"local": local, "nutricionista": nutricionista, "data": str(data_conf), "itens": TODOS_ITENS}
                st.session_state.nutricionista = nutricionista
                st.session_state.respostas = {it: None for it in TODOS_ITENS}
                st.session_state.comentarios = {it: "" for it in TODOS_ITENS}
                st.session_state.tela = "conferencia"
                st.rerun()

    # ── TAB 2: HISTÓRICO ──────────────────────────────────────
    with tab2:
        hist = st.session_state.historico
        if not hist:
            st.markdown('<div class="empty-state"><div class="empty-icon">📋</div><div class="empty-title">Nenhuma conferência ainda</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-lbl">Conferências realizadas</div>', unsafe_allow_html=True)
            for h in reversed(hist):
                nc_list = [it for it, v in h["respostas"].items() if v == "NC"]
                h_coment = h.get("comentarios", {})
                ncs_html = "".join([
                    f'<div style="font-size:11px;color:#9C0006;margin-top:2px;">• {n}'
                    + (f' — 💬 {h_coment.get(n)}' if h_coment.get(n) else '')
                    + '</div>'
                    for n in nc_list
                ])
                hist_html = (
                    '<div class="hist-card">'
                    '<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
                    '<div>'
                    f'<div style="font-size:14px;font-weight:600;color:#0F2D1A;">📍 {h["local"]}</div>'
                    f'<div style="font-size:11px;color:#6B8F72;margin-top:2px;">{h["data"]} · {h["nutricionista"]}</div>'
                    f'<div style="margin-top:8px;font-size:12px;color:#6B8F72;">✅ {h["total_c"]} C &nbsp;|&nbsp; ❌ {h["total_nc"]} NC &nbsp;|&nbsp; ➖ {h["total_na"]} NA</div>'
                    f'{ncs_html}'
                    '</div>'
                    f'<div style="font-size:18px;font-weight:700;color:#1D6B35;">{h["pct"]}%</div>'
                    '</div>'
                    '</div>'
                )
                st.markdown(hist_html, unsafe_allow_html=True)
                h_id = h.get("id", f"{h['local']}_{h['data']}")
                confirm_key = f"confirm_del_{h_id}"
                if st.session_state.get(confirm_key):
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        with st.container(key=f"kdanger_confdel_{h_id}"):
                            if st.button("✕ Confirmar exclusão", key=f"conf_del_{h_id}", use_container_width=True):
                                with st.spinner("Apagando..."):
                                    ok, msg = apagar_conferencia(h_id)
                                if ok:
                                    st.session_state.historico = [x for x in st.session_state.historico if x.get("id", f"{x['local']}_{x['data']}") != h_id]
                                    st.session_state[confirm_key] = False
                                    st.success("Conferência apagada.")
                                    st.rerun()
                                else:
                                    st.error(f"Erro ao apagar: {msg}")
                    with cc2:
                        with st.container(key=f"kclear_canceldel_{h_id}"):
                            if st.button("Cancelar", key=f"cancel_del_{h_id}", use_container_width=True):
                                st.session_state[confirm_key] = False
                                st.rerun()
                else:
                    with st.container(key=f"kclear_del_{h_id}"):
                        if st.button("🗑 Apagar esta conferência", key=f"del_hist_{h_id}", use_container_width=True):
                            st.session_state[confirm_key] = True
                            st.rerun()
                    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── TAB 3: NCS ────────────────────────────────────────────
    with tab3:
        hist = st.session_state.historico
        ncs = [(h, it) for h in hist for it, v in h["respostas"].items() if v == "NC"]
        if not ncs:
            st.markdown('<div class="empty-state"><div class="empty-icon">✅</div><div class="empty-title">Nenhuma NC registrada</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="section-lbl">{len(ncs)} não conformidade(s)</div>', unsafe_allow_html=True)
            for h, it in ncs:
                coment_it = h.get("comentarios", {}).get(it, "")
                coment_html = f'<div style="font-size:12px;color:#6B2020;margin-top:6px;background:#fff;border-radius:8px;padding:6px 8px;">💬 {coment_it}</div>' if coment_it else ""
                st.markdown(
                    f'<div class="nc-card" style="flex-direction:column;align-items:stretch;">'
                    f'<div style="display:flex;align-items:center;justify-content:space-between;">'
                    f'<div><div class="nc-name">{it}</div><div class="nc-meta">{h["local"]} · {h["data"]}</div></div>'
                    f'<span class="badge badge-nc">NC</span></div>'
                    f'{coment_html}'
                    f'</div>', unsafe_allow_html=True)

    # ── TAB 4: RELATÓRIO ──────────────────────────────────────
    with tab4:
        hist = st.session_state.historico
        if not hist:
            st.markdown('<div class="empty-state"><div class="empty-icon">📈</div><div class="empty-title">Sem dados ainda</div></div>', unsafe_allow_html=True)
        else:
            df = pd.DataFrame([{"local": h["local"], "data": pd.to_datetime(h["data"]), "total_c": h["total_c"], "total_nc": h["total_nc"], "total_na": h["total_na"], "pct": h["pct"]} for h in hist])
            st.markdown('<div class="section-lbl">Filtros</div>', unsafe_allow_html=True)
            filtro_local = st.selectbox("Unidade", ["Todos"] + sorted(df["local"].unique().tolist()), key="rel_local")
            periodo = st.selectbox("Período", ["Todos", "Última semana", "Último mês", "Últimos 3 meses"], key="rel_periodo")
            with st.container(key="kgreen_filtrar"):
                filtrar = st.button("🔍  Gerar relatório", key="btn_filtrar", use_container_width=True)
            if not filtrar and "rel_resultado" not in st.session_state:
                st.markdown('<div class="empty-state"><div class="empty-icon">📊</div><div class="empty-title">Selecione os filtros e toque em Gerar relatório</div></div>', unsafe_allow_html=True)
            else:
                if filtrar:
                    st.session_state.rel_resultado = {"local": filtro_local, "periodo": periodo}
                f = st.session_state.get("rel_resultado", {"local": filtro_local, "periodo": periodo})
                df_f = df.copy()
                if f["local"] != "Todos":
                    df_f = df_f[df_f["local"] == f["local"]]
                hoje = pd.Timestamp.today()
                if f["periodo"] == "Última semana":
                    df_f = df_f[df_f["data"] >= hoje - timedelta(days=7)]
                elif f["periodo"] == "Último mês":
                    df_f = df_f[df_f["data"] >= hoje - timedelta(days=30)]
                elif f["periodo"] == "Últimos 3 meses":
                    df_f = df_f[df_f["data"] >= hoje - timedelta(days=90)]
                if df_f.empty:
                    st.markdown('<div class="empty-state"><div class="empty-icon">🔍</div><div class="empty-title">Nenhum dado para esse filtro</div></div>', unsafe_allow_html=True)
                else:
                    tc = len(df_f)
                    tc_sum = int(df_f["total_c"].sum())
                    tnc = int(df_f["total_nc"].sum())
                    tna = int(df_f["total_na"].sum())
                    avaliados_sum = tc_sum + tnc
                    mp = int((tc_sum / avaliados_sum) * 100) if avaliados_sum else 0
                    st.markdown(f'<div class="chips-row"><div class="sum-chip"><div class="sum-chip-val">{tc}</div><div class="sum-chip-lbl">Conferências</div></div><div class="sum-chip"><div class="sum-chip-val" style="color:#1D6B35">{mp}%</div><div class="sum-chip-lbl">Conformidade</div></div><div class="sum-chip"><div class="sum-chip-val" style="color:#9C0006">{tnc}</div><div class="sum-chip-lbl">NCs</div></div><div class="sum-chip"><div class="sum-chip-val" style="color:#6B8F72">{tna}</div><div class="sum-chip-lbl">NAs</div></div></div>', unsafe_allow_html=True)
                    por_local_grp = df_f.groupby("local").agg(c=("total_c", "sum"), nc=("total_nc", "sum"))
                    por_local = ((por_local_grp["c"] / (por_local_grp["c"] + por_local_grp["nc"]).replace(0, pd.NA)) * 100).fillna(0).sort_values(ascending=False)
                    st.markdown('<div class="rel-card"><div class="rel-card-title">Conformidade por Unidade</div>', unsafe_allow_html=True)
                    bars = ""
                    for l, p in por_local.items():
                        pv = int(p)
                        cor = "bar-fill-g" if pv >= 80 else "bar-fill-r"
                        bars += f'<div class="bar-row"><div class="bar-label">{l}</div><div class="bar-bg"><div class="{cor}" style="width:{pv}%"></div></div><div class="bar-pct">{pv}%</div></div>'
                    st.markdown(bars + "</div>", unsafe_allow_html=True)
                    rank_local = por_local_grp["nc"].astype(int).sort_values(ascending=False)
                    st.markdown('<div class="rel-card"><div class="rel-card-title">Ranking de Unidades por NCs</div>', unsafe_allow_html=True)
                    rk = ""
                    for idx, (l, ncv) in enumerate(rank_local.items(), 1):
                        pos_cls = "rank-pos top" if idx == 1 and ncv > 0 else "rank-pos"
                        nc_cls = "rank-nc" if ncv > 0 else "rank-nc zero"
                        rk += f'<div class="rank-row"><div class="rank-left"><span class="{pos_cls}">{idx}</span><span class="rank-local">{l}</span></div><span class="{nc_cls}">{ncv} NC</span></div>'
                    st.markdown(rk + "</div>", unsafe_allow_html=True)
                    nc_items = {}
                    conf_f = set((str(r["data"].date()), r["local"]) for _, r in df_f.iterrows())
                    for h in hist:
                        if (h["data"], h["local"]) in conf_f:
                            for it, v in h["respostas"].items():
                                if v == "NC":
                                    nc_items[it] = nc_items.get(it, 0) + 1
                    if nc_items:
                        top_nc = sorted(nc_items.items(), key=lambda x: x[1], reverse=True)[:5]
                        max_v = max(v for _, v in top_nc)
                        st.markdown('<div class="rel-card"><div class="rel-card-title">Itens mais não conformes</div>', unsafe_allow_html=True)
                        nh = ""
                        for item, count in top_nc:
                            pb = int((count / max_v) * 100)
                            nh += f'<div class="bar-row"><div class="bar-label" style="width:100px;font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{item[:18]}...</div><div class="bar-bg"><div class="bar-fill-r" style="width:{pb}%"></div></div><div class="bar-pct">{count}x</div></div>'
                        st.markdown(nh + "</div>", unsafe_allow_html=True)

    # ── TAB 5: ANUAL ──────────────────────────────────────────
    with tab5:
        hist = st.session_state.historico
        if not hist:
            st.markdown('<div class="empty-state"><div class="empty-icon">📅</div><div class="empty-title">Sem dados para o relatório anual</div></div>', unsafe_allow_html=True)
        else:
            df_a = pd.DataFrame([{"local": h["local"], "data": pd.to_datetime(h["data"]), "total_c": h["total_c"], "total_nc": h["total_nc"], "total_na": h["total_na"], "pct": h["pct"]} for h in hist])
            anos = sorted(df_a["data"].dt.year.unique().tolist(), reverse=True)
            ano_sel = st.selectbox("Ano", anos, key="ano_sel")
            df_ano = df_a[df_a["data"].dt.year == ano_sel]
            tc = len(df_ano)
            tc_sum = int(df_ano["total_c"].sum())
            tnc = int(df_ano["total_nc"].sum())
            tna = int(df_ano["total_na"].sum())
            avaliados_sum = tc_sum + tnc
            mp = int((tc_sum / avaliados_sum) * 100) if avaliados_sum else 0
            st.markdown(f'<div class="chips-row"><div class="sum-chip"><div class="sum-chip-val">{tc}</div><div class="sum-chip-lbl">Conferências</div></div><div class="sum-chip"><div class="sum-chip-val" style="color:#1D6B35">{mp}%</div><div class="sum-chip-lbl">Conformidade</div></div><div class="sum-chip"><div class="sum-chip-val" style="color:#9C0006">{tnc}</div><div class="sum-chip-lbl">NCs</div></div><div class="sum-chip"><div class="sum-chip-val" style="color:#6B8F72">{tna}</div><div class="sum-chip-lbl">NAs</div></div></div>', unsafe_allow_html=True)
            meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
            por_mes_grp = df_ano.groupby(df_ano["data"].dt.month).agg(c=("total_c", "sum"), nc=("total_nc", "sum"))
            por_mes = ((por_mes_grp["c"] / (por_mes_grp["c"] + por_mes_grp["nc"]).replace(0, pd.NA)) * 100).fillna(0)
            st.markdown('<div class="rel-card"><div class="rel-card-title">Conformidade por mês</div>', unsafe_allow_html=True)
            bm = ""
            for m in range(1, 13):
                if m in por_mes.index:
                    pv = int(por_mes[m])
                    cor = "bar-fill-g" if pv >= 80 else "bar-fill-r"
                    bm += f'<div class="bar-row"><div class="bar-label" style="width:28px;font-size:10px;">{meses[m-1]}</div><div class="bar-bg"><div class="{cor}" style="width:{pv}%"></div></div><div class="bar-pct">{pv}%</div></div>'
            st.markdown(bm + "</div>", unsafe_allow_html=True)
            por_local_grp = df_ano.groupby("local").agg(c=("total_c", "sum"), nc=("total_nc", "sum"))
            por_local = ((por_local_grp["c"] / (por_local_grp["c"] + por_local_grp["nc"]).replace(0, pd.NA)) * 100).fillna(0).sort_values(ascending=False)
            st.markdown('<div class="rel-card"><div class="rel-card-title">Conformidade por unidade</div>', unsafe_allow_html=True)
            bl = ""
            for l, pv in por_local.items():
                pv = int(pv)
                cor = "bar-fill-g" if pv >= 80 else "bar-fill-r"
                bl += f'<div class="bar-row"><div class="bar-label">{l}</div><div class="bar-bg"><div class="{cor}" style="width:{pv}%"></div></div><div class="bar-pct">{pv}%</div></div>'
            st.markdown(bl + "</div>", unsafe_allow_html=True)
            rank_local_ano = por_local_grp["nc"].astype(int).sort_values(ascending=False)
            st.markdown('<div class="rel-card"><div class="rel-card-title">Ranking de Unidades por NCs</div>', unsafe_allow_html=True)
            rka = ""
            for idx, (l, ncv) in enumerate(rank_local_ano.items(), 1):
                pos_cls = "rank-pos top" if idx == 1 and ncv > 0 else "rank-pos"
                nc_cls = "rank-nc" if ncv > 0 else "rank-nc zero"
                rka += f'<div class="rank-row"><div class="rank-left"><span class="{pos_cls}">{idx}</span><span class="rank-local">{l}</span></div><span class="{nc_cls}">{ncv} NC</span></div>'
            st.markdown(rka + "</div>", unsafe_allow_html=True)
            nc_ano = {}
            for h in hist:
                if pd.to_datetime(h["data"]).year == ano_sel:
                    for it, v in h["respostas"].items():
                        if v == "NC":
                            nc_ano[it] = nc_ano.get(it, 0) + 1
            if nc_ano:
                top_nc = sorted(nc_ano.items(), key=lambda x: x[1], reverse=True)[:5]
                max_v = max(v for _, v in top_nc)
                st.markdown('<div class="rel-card"><div class="rel-card-title">Top 5 itens não conformes</div>', unsafe_allow_html=True)
                nh = ""
                for item, count in top_nc:
                    pb = int((count / max_v) * 100)
                    nh += f'<div class="bar-row"><div class="bar-label" style="width:100px;font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{item[:18]}...</div><div class="bar-bg"><div class="bar-fill-r" style="width:{pb}%"></div></div><div class="bar-pct">{count}x</div></div>'
                st.markdown(nh + "</div>", unsafe_allow_html=True)
            nc_rows = "".join([f'<div style="background:#FFF0F0;border:1px solid #E24B4A;border-radius:8px;padding:8px 12px;margin-bottom:6px;display:flex;justify-content:space-between;"><span>{it}</span><strong>{c}x</strong></div>' for it, c in sorted(nc_ano.items(), key=lambda x: x[1], reverse=True)[:5]])
            local_rows = "".join([f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;"><div style="width:100px;font-size:13px;">{l}</div><div style="flex:1;height:16px;background:#F0F4F1;border-radius:99px;overflow:hidden;"><div style="height:100%;background:{"#1D9E75" if int(p)>=80 else "#E24B4A"};width:{int(p)}%;border-radius:99px;"></div></div><div style="width:40px;text-align:right;font-size:13px;font-weight:700;">{int(p)}%</div></div>' for l, p in por_local.items()])
            mes_rows = "".join([f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;"><div style="width:100px;font-size:13px;">{meses[m-1]}</div><div style="flex:1;height:16px;background:#F0F4F1;border-radius:99px;overflow:hidden;"><div style="height:100%;background:{"#1D9E75" if int(por_mes[m])>=80 else "#E24B4A"};width:{int(por_mes[m])}%;border-radius:99px;"></div></div><div style="width:40px;text-align:right;font-size:13px;font-weight:700;">{int(por_mes[m])}%</div></div>' for m in range(1, 13) if m in por_mes.index])
            rank_rows = "".join([f'<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 12px;border-bottom:1px solid #EEF4EF;"><span>{idx}. {l}</span><strong style="color:{"#9C0006" if ncv>0 else "#1D6B35"}">{ncv} NC</strong></div>' for idx, (l, ncv) in enumerate(rank_local_ano.items(), 1)])
            html_rel = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{{font-family:Arial,sans-serif;max-width:800px;margin:0 auto;padding:40px;color:#0F2D1A;}}h1{{color:#0F2D1A;border-bottom:3px solid #7DC65A;padding-bottom:10px;}}h2{{color:#1D6B35;margin-top:30px;}}.cr{{display:flex;gap:20px;margin:20px 0;}}.ch{{flex:1;background:#EAF5ED;border-radius:10px;padding:16px;text-align:center;}}.cv{{font-size:32px;font-weight:700;}}.cl{{font-size:12px;color:#6B8F72;text-transform:uppercase;}}.footer{{margin-top:40px;padding-top:20px;border-top:1px solid #D6EDD9;font-size:12px;color:#6B8F72;}}</style></head><body><h1>Genba Log — Relatório Anual {ano_sel}</h1><p>Gerado em {datetime.today().strftime('%d/%m/%Y')}</p><div class="cr"><div class="ch"><div class="cv">{tc}</div><div class="cl">Conferências</div></div><div class="ch"><div class="cv">{mp}%</div><div class="cl">Conformidade</div></div><div class="ch" style="background:#FFF0F0"><div class="cv" style="color:#9C0006">{tnc}</div><div class="cl">NCs</div></div></div><h2>Por Unidade</h2>{local_rows}<h2>Por Mês</h2>{mes_rows}<h2>Ranking de Unidades por NCs</h2>{rank_rows}<h2>Top NCs</h2>{nc_rows}<div class="footer">Genba Log | Checklist de higiene e segurança dos alimentos.</div></body></html>"""
            b64 = base64.b64encode(html_rel.encode()).decode()
            st.markdown(f'<a href="data:text/html;base64,{b64}" download="Relatorio_Anual_{ano_sel}.html" style="display:block;background:#0F2D1A;color:#7DC65A;border-radius:12px;padding:13px;text-align:center;font-size:13px;font-weight:700;text-decoration:none;margin:12px 16px;">⬇ Baixar relatório {ano_sel}</a>', unsafe_allow_html=True)
            st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # ── TAB 6: CONFIGURAÇÕES ──────────────────────────────────
    with tab6:
        st.markdown('<div class="section-lbl">Acesso administrativo</div>', unsafe_allow_html=True)
        if not st.session_state.admin_ok:
            st.markdown('<div class="admin-locked"><div class="admin-title">🔒 Área restrita</div><div class="admin-sub">Digite a senha de administrador para acessar</div></div>', unsafe_allow_html=True)
            senha = st.text_input("Senha", type="password", key="senha_admin")
            with st.container(key="kgreen_admin"):
                if st.button("Entrar", key="btn_admin", use_container_width=True):
                    senha_correta = st.secrets.get("admin_password")
                    if senha_correta and senha == senha_correta:
                        st.session_state.admin_ok = True
                        st.rerun()
                    else:
                        st.error("Senha incorreta")
        else:
            st.markdown('<div class="section-lbl">Nutricionistas ativas</div>', unsafe_allow_html=True)
            nutris = st.session_state.get("nutricionistas", [])
            for nu in nutris:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f'<div class="fiscal-row"><div class="fiscal-name">👤 {nu}</div></div>', unsafe_allow_html=True)
                with col2:
                    with st.container(key=f"kdanger_delnutri_{nu}"):
                        if st.button("✕", key=f"del_{nu}", use_container_width=True):
                            if remover_nutricionista(nu):
                                st.session_state.nutricionistas = [x for x in nutris if x != nu]
                                st.success(f"{nu} removida!")
                                st.rerun()

            st.markdown('<div class="div"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-lbl">Adicionar nutricionista</div>', unsafe_allow_html=True)
            nova_nutri = st.text_input("Nome completo", key="nova_nutri", placeholder="Ex: Maria Silva")
            with st.container(key="kgreen_addnutri"):
                if st.button("+ Adicionar nutricionista", key="btn_add_nutri", use_container_width=True):
                    if nova_nutri.strip():
                        if adicionar_nutricionista(nova_nutri.strip()):
                            st.session_state.nutricionistas.append(nova_nutri.strip())
                            st.success(f"{nova_nutri} adicionada!")
                            st.rerun()
                        else:
                            st.error("Erro ao adicionar. Verifique a conexão com o Sheets.")
                    else:
                        st.warning("Digite o nome da nutricionista.")

            st.markdown('<div class="div"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-lbl">⚠️ Zona de risco</div>', unsafe_allow_html=True)
            st.markdown('<div class="admin-locked" style="background:#FFF0F0;border-color:#E24B4A;"><div class="admin-title" style="color:#501313;">🗑 Apagar todo o histórico</div><div class="admin-sub" style="color:#501313;">Remove permanentemente todas as conferências salvas no Google Sheets (Conferências e Respostas). Use isso para zerar o app antes de começar a usar de verdade.</div></div>', unsafe_allow_html=True)
            if st.session_state.get("confirm_wipe_all"):
                st.warning("Tem certeza? Essa ação não pode ser desfeita e vai apagar TODO o histórico salvo.")
                wc1, wc2 = st.columns(2)
                with wc1:
                    with st.container(key="kdanger_wipeconfirm"):
                        if st.button("✕ Sim, apagar tudo", key="btn_wipe_confirm", use_container_width=True):
                            with st.spinner("Apagando todo o histórico..."):
                                ok, msg = apagar_todo_historico()
                            if ok:
                                st.session_state.historico = []
                                st.session_state.confirm_wipe_all = False
                                st.success("Histórico apagado com sucesso.")
                                st.rerun()
                            else:
                                st.error(f"Erro ao apagar: {msg}")
                with wc2:
                    with st.container(key="kclear_wipecancel"):
                        if st.button("Cancelar", key="btn_wipe_cancel", use_container_width=True):
                            st.session_state.confirm_wipe_all = False
                            st.rerun()
            else:
                with st.container(key="kdanger_wipeall"):
                    if st.button("🗑 Apagar todo o histórico", key="btn_wipe_all", use_container_width=True):
                        st.session_state.confirm_wipe_all = True
                        st.rerun()

            st.markdown('<div class="div"></div>', unsafe_allow_html=True)
            with st.container(key="kback_sairadmin"):
                if st.button("🔒 Sair da área admin", key="btn_sair_admin", use_container_width=True):
                    st.session_state.admin_ok = False
                    st.rerun()

# ═══════════════════════════════════════════════════════════════
elif st.session_state.tela == "conferencia":
    conf = st.session_state.conf
    resp = st.session_state.respostas
    itens = conf["itens"]
    total_c = sum(1 for v in resp.values() if v == "C")
    total_nc = sum(1 for v in resp.values() if v == "NC")
    total_na = sum(1 for v in resp.values() if v == "NA")
    avaliados = total_c + total_nc + total_na
    total = len(itens)
    pct_base = total_c + total_nc
    pct = int((total_c / pct_base) * 100) if pct_base else 0
    st.markdown(f'<div class="conf-header"><div class="conf-title">{conf["local"]}</div><div class="conf-meta">{conf["data"]} · {conf["nutricionista"]}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="prog-wrap"><div class="prog-bg"><div class="prog-fill" style="width:{int((avaliados/total)*100) if total else 0}%"></div></div><div class="prog-label"><span>{avaliados} de {total} avaliados</span><span>{pct}% conformidade</span></div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chips"><div class="chip chip-c"><div class="chip-lbl">Conformes</div><div class="chip-val">{total_c}</div></div><div class="chip chip-nc"><div class="chip-lbl">Não Conf.</div><div class="chip-val">{total_nc}</div></div><div class="chip chip-na"><div class="chip-lbl">N.A.</div><div class="chip-val">{total_na}</div></div></div>', unsafe_allow_html=True)

    for categoria, itens_cat in CATEGORIAS:
        st.markdown(f'<div class="cat-lbl">{categoria}</div>', unsafe_allow_html=True)
        for idx, item in enumerate(itens_cat):
            status = resp.get(item)
            cls = "item-row c" if status == "C" else "item-row nc" if status == "NC" else "item-row na" if status == "NA" else "item-row"
            bdg = ('<span class="badge badge-c">C</span>' if status == "C"
                   else '<span class="badge badge-nc">NC</span>' if status == "NC"
                   else '<span class="badge badge-na">NA</span>' if status == "NA"
                   else '<span class="badge badge-p">—</span>')
            st.markdown(f'<div class="{cls}"><div class="item-top"><div class="item-name">{item}</div>{bdg}</div></div>', unsafe_allow_html=True)
            safe_key = f"{categoria}_{idx}"
            c1, c2, c3 = st.columns([1, 1, 1])
            with c1:
                with st.container(key=f"kconf-{safe_key}"):
                    if st.button("✔ Conforme", key=f"c_{safe_key}", use_container_width=True):
                        st.session_state.respostas[item] = "C"
                        st.rerun()
            with c2:
                with st.container(key=f"knc-{safe_key}"):
                    if st.button("✖ Não Conf.", key=f"nc_{safe_key}", use_container_width=True):
                        st.session_state.respostas[item] = "NC"
                        st.rerun()
            with c3:
                with st.container(key=f"kna-{safe_key}"):
                    if st.button("N.A.", key=f"na_{safe_key}", use_container_width=True):
                        st.session_state.respostas[item] = "NA"
                        st.rerun()

            st.markdown('<div class="comment-wrap">', unsafe_allow_html=True)
            comentario_val = st.text_area(
                "Comentário (opcional)",
                value=st.session_state.comentarios.get(item, ""),
                key=f"com_{safe_key}",
                placeholder="Adicione uma observação, se necessário...",
                height=68,
            )
            st.session_state.comentarios[item] = comentario_val
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    if total_nc > 0 or total_c > 0:
        coment = st.session_state.comentarios
        c_txt = "\n".join([f"• {it}" for it, v in resp.items() if v == "C"])
        nc_txt = "\n".join([
            f"• {it}" + (f"\n   💬 {coment[it]}" if coment.get(it, "").strip() else "")
            for it, v in resp.items() if v == "NC"
        ])
        msg = (f"🔍 *Relatório — Genba Log*\n📍 {conf['local']}\n📅 {conf['data']}\n"
               f"👩‍⚕️ Nutricionista: {conf['nutricionista']}\n\n"
               f"✅ *Conformes:*\n{c_txt if c_txt else '—'}\n\n"
               f"❌ *Não Conformes:*\n{nc_txt if nc_txt else '—'}\n\n"
               f"📊 *Resumo:* {total_c} C · {total_nc} NC · {total_na} NA · {pct}% conformidade")
        wa_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
        st.markdown(f'<a href="{wa_url}" target="_blank" class="wa-link">📲 Enviar relatório via WhatsApp</a>', unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        with st.container(key="kgreen_finalizar"):
            if st.button("✓ Finalizar", use_container_width=True):
                with st.spinner("Salvando no Google Sheets..."):
                    ok, result = salvar_conferencia(conf, resp, st.session_state.comentarios)
                if ok:
                    st.session_state.historico.append({**conf, "respostas": dict(resp), "comentarios": dict(st.session_state.comentarios), "total_c": total_c, "total_nc": total_nc, "total_na": total_na, "pct": pct, "id": result})
                    st.session_state.tela = "inicio"
                    st.rerun()
                else:
                    st.error(f"Erro ao salvar: {result}")
    with c2:
        with st.container(key="kback_voltar"):
            if st.button("← Voltar", use_container_width=True):
                st.session_state.tela = "inicio"
                st.rerun()
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
