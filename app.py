import streamlit as st
import pandas as pd
import time
import gspread
from google.oauth2.service_account import Credentials

# ==========================================
# 1. CONFIGURAZIONE PAGINA
# ==========================================
st.set_page_config(
    page_title="Dojo Academy",
    page_icon="🎮",
    layout="centered"
)

# Costanti per Google Sheets
SHEET_ID = "1ul4pI3QDqGYz7kjj6p-QLgLXMkMMR3anv4JdEP0lI48"
GID_PERSONAL_STATS = "1148983819"
GID_ACADEMY = "625069530"
GID_ANAGRAFICA = "1502613256"
GID_PROGRESSI = "797090179"
GID_CERTIFICAZIONI = "886238750"
GID_ESERCIZI = "1935989008"
GID_SETTINGS = "1035088826"

# ==========================================
# 2. FUNZIONI HELPER GOOGLE SHEETS
# ==========================================
def ottieni_credenziali():
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        return Credentials.from_service_account_info(creds_dict, scopes=scopes)
    except Exception as e:
        st.error(f"Impossibile caricare le credenziali: {e}")
        return None

def scrivi_cella_per_gid(gid, cella, valore):
    try:
        creds = ottieni_credenziali()
        if creds:
            client = gspread.authorize(creds)
            sheet = client.open_by_key(SHEET_ID)
            target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(gid).strip()), None)
            if target_ws:
                target_ws.update_acell(cella, valore)
    except Exception as e:
        st.error(f"Errore nella scrittura della cella {cella}: {e}")

# ==========================================
# 3. CSS PERSONALIZZATO
# ==========================================
st.markdown("""
    <style>
        .stApp {
            background-color: #0d0d0d !important;
            color: #FFFFFF !important;
        }
        .main .block-container {
            max-width: 500px !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1rem !important;
            margin: 0 auto !important;
        }
        [data-testid="stSidebar"] {
            display: none !important;
        }
        div[data-testid="stElementContainer"],
        div[data-testid="stColumn"],
        div.stButton {
            width: 100% !important;
            display: block !important;
        }
        div.stButton > button {
            width: 100% !important;
            display: block !important;
            background-color: #FFD700 !important;
            color: #000000 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 14px 10px !important;
            font-size: 15px !important;
            font-weight: 800 !important;
            margin-bottom: 8px !important;
            text-transform: uppercase !important;
            text-align: center !important;
            box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.6) !important;
        }
        div.stButton > button:hover {
            background-color: #FFC107 !important;
            color: #000000 !important;
        }
        div.stButton > button[kind="primary"] {
            background-color: #FF9900 !important;
            color: #000000 !important;
            border: 2px solid #FFFFFF !important;
        }
        .stat-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 10px 5px;
            text-align: center;
            margin-bottom: 8px;
        }
        .stat-label {
            color: #8b949e;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        .stat-value {
            color: #58a6ff;
            font-size: 1.1rem;
            font-weight: bold;
            margin-top: 4px;
        }
        .fixed-box-row {
            display: flex;
            justify-content: space-between;
            background-color: #161b22;
            border-bottom: 1px solid #30363d;
            padding: 8px 12px;
            font-size: 0.9rem;
        }
        .fixed-box-header {
            display: flex;
            justify-content: space-between;
            background-color: #21262d;
            border-bottom: 2px solid #30363d;
            padding: 8px 12px;
            font-weight: bold;
            font-size: 0.85rem;
            color: #8b949e;
            text-transform: uppercase;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. DATI DEL MENU
# ==========================================
SECTIONS = [
    "🏫 ACADEMY",
    "📋 ANAGRAFICA",
    "📈 PROGRESSI",
    "📜 CERTIFICAZIONI",
    "🏋️ ESERCIZI",
    "👤 SCHEDE GIOCATORE",
    "📊 STATISTICHE"
]

PLAYERS = [
    "JFF_ANDERWAL", "ITABOYZ_VIN", "JFF_CLIP",
    "ITABOYZ_GALLO", "ITABOYZ_IMPERATUBER", "JFF_POTA",
    "ITABOYZ_CASCO", "JFF_CIKKO", "JFF_SINNER"
]

STATS_OPTIONS = ["⚙️ SETTINGS", "🏋️ TRAINING", "🏆 STATCOMP"]

# ==========================================
# 5. STRUTTURA A 3 COLONNE (LAYOUT CENTRATO)
# ==========================================
left_space, center_col, right_space = st.columns([1, 2, 1])

with center_col:
    try:
        st.image("assets/logo.png", use_container_width=True)
    except Exception:
        st.image("https://via.placeholder.com/300x300.png?text=DOJO+ACADEMY", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if "current_section" not in st.session_state:
        st.session_state.current_section = "🏫 ACADEMY"

    for sec in SECTIONS:
        btn_type = "primary" if st.session_state.current_section == sec else "secondary"
        if st.button(sec, key=f"nav_{sec}", type=btn_type):
            st.session_state.current_section = sec
            st.rerun()

    st.markdown("---")

    current = st.session_state.current_section

    if current == "🏫 ACADEMY":
        st.subheader("🏫 Academy")

        # CSS personalizzato per etichette bianche e pulsante giallo
        st.markdown("""
        <style>
            .stTextInput label p, div[data-baseweb="input"] label, .stTextInput label {
                color: #FFFFFF !important;
            }
            [data-testid="stFormSubmitButton"] button {
                background-color: #FFFF00 !important;
                color: #000000 !important;
                width: 100% !important;
                font-weight: bold !important;
            }
            [data-testid="stFormSubmitButton"] button:hover {
                background-color: #cccc00 !important;
                color: #000000 !important;
            }
        </style>
        """, unsafe_allow_html=True)

        f13_val, h13_val = "", ""
        f14_val, h14_val = "", ""
        box_pix_rows = []
        box_nino_rows = []
        target_ws_obj = None

        try:
            creds = ottieni_credenziali()
            if creds:
                client = gspread.authorize(creds)
                sheet = client.open_by_key(SHEET_ID)
                target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(GID_ACADEMY).strip()), None)
                target_ws_obj = target_ws

                if target_ws:
                    f13_val = target_ws.acell("F13").value or ""
                    h13_val = target_ws.acell("H13").value or ""
                    f14_val = target_ws.acell("F14").value or ""
                    h14_val = target_ws.acell("H14").value or ""

                    box_pix_rows = [
                        ["JFF_CLIP", "L/M/G/D", "DOJO MAP"],
                        ["itaboyz_Casco", "L/M/G/D", "DOJO MAP"],
                        ["itaBOYZ_VIN", "L/M/G/D", "DOJO MAP"],
                        ["itaboyz_imperat", "L/M/G/D", "DOJO MAP"],
                        ["itaboyz_gallo", "L/M/G/D", "DOJO MAP"]
                    ]    

                    box_nino_rows = [
                        ["JFF_SINNER", "L/M/G/D", "DOJO MAP"],
                        ["JFF_POTA", "L/M/G/D", "DOJO MAP"],
                        ["JFF_ANDERWAL", "L/M/G/D", "DOJO MAP"],
                        ["JFF_DANI", "L/M/G/D", "DOJO MAP"],
                        ["itaboyz_faire", "L/M/G/D", "DOJO MAP"]
                    ]
        except Exception as e:
            st.warning(f"Errore nel caricamento dati Academy: {e}")

        st.markdown(f"""
        <div style='background-color: #000000; border: 2px solid #ff0000; border-radius: 6px; overflow: hidden; margin-bottom: 20px;'>
            <div style='background-color: #FFFF00; color: #000000; text-align: center; font-weight: bold; font-size: 1.2rem; padding: 10px;'>
                {f13_val} {h13_val}
            </div>
            <div style='color: #FFFFFF; text-align: center; font-size: 0.95rem; padding: 8px;'>
                {f14_val} &nbsp;&nbsp; {h14_val}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background-color: #000000; border: 2px solid #ff0000; border-radius: 6px; overflow: hidden; margin-bottom: 20px;'>
            <div style='background-color: #FFFF00; color: #000000; text-align: center; font-weight: bold; font-size: 1.1rem; padding: 8px;'>
                ARES PIX
            </div>
            <div class='fixed-box-header'>
                <span style='flex: 2;'>Allievi a carico</span>
                <span style='flex: 1; text-align: center;'>giorni</span>
                <span style='flex: 1; text-align: right;'>Mappa</span>
            </div>
        """, unsafe_allow_html=True)

        for row in box_pix_rows:
            st.markdown(f"""
            <div class='fixed-box-row'>
                <span style='flex: 2; color: #FFFFFF;'>{row[0]}</span>
                <span style='flex: 1; text-align: center; color: #8b949e;'>{row[1]}</span>
                <span style='flex: 1; text-align: right; color: #58a6ff;'>{row[2]}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='background-color: #000000; border: 2px solid #ff0000; border-radius: 6px; overflow: hidden; margin-bottom: 20px;'>
            <div style='background-color: #FFFF00; color: #000000; text-align: center; font-weight: bold; font-size: 1.1rem; padding: 8px;'>
                ARES NINO
            </div>
            <div class='fixed-box-header'>
                <span style='flex: 2;'>Allievi a carico</span>
                <span style='flex: 1; text-align: center;'>giorni</span>
                <span style='flex: 1; text-align: right;'>Mappa</span>
            </div>
        """, unsafe_allow_html=True)

        for row in box_nino_rows:
            st.markdown(f"""
            <div class='fixed-box-row'>
                <span style='flex: 2; color: #FFFFFF;'>{row[0]}</span>
                <span style='flex: 1; text-align: center; color: #8b949e;'>{row[1]}</span>
                <span style='flex: 1; text-align: right; color: #58a6ff;'>{row[2]}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # --- SEZIONE MODULO DI INSERIMENTO REGISTRO ATTIVITA' ---
        st.markdown("""
        <div style='background-color: #000000; border: 2px solid #ff0000; border-radius: 6px; overflow: hidden; margin-bottom: 20px;'>
            <div style='background-color: #FFFF00; color: #000000; text-align: center; font-weight: bold; font-size: 1.1rem; padding: 10px;'>
                REGISTRO ATTIVITA' - NUOVA VOCE
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("form_nuovo_registro", clear_on_submit=True):
            nuovo_allievo = st.text_input("Allievo a carico")
            nuovo_giorni = st.text_input("Giorni")
            nuova_mappa = st.text_input("Mappa")

            submit_button = st.form_submit_button("➕")

            if submit_button:
                if not nuovo_allievo.strip() and not nuovo_giorni.strip() and not nuova_mappa.strip():
                    st.warning("Compila almeno un campo prima di inviare.")
                else:
                    try:
                        if target_ws_obj:
                            range_data = target_ws_obj.get("C28:E50", value_render_option='UNFORMATTED_VALUE')
                        
                            next_row_index = 28
                            found_empty = False
                        
                            for i, row in enumerate(range_data):
                                if not row or all(str(cell).strip() == "" for cell in row):
                                    next_row_index = 28 + i
                                    found_empty = True
                                    break
                        
                            if not found_empty:
                                next_row_index = 28 + len(range_data)
                                if next_row_index > 50:
                                    st.error("Il registro (C28:E50) è pieno!")
                                    st.stop()

                            target_ws_obj.update(f"C{next_row_index}:E{next_row_index}", [[nuovo_allievo, nuovo_giorni, nuova_mappa]])
                        
                            st.toast("✅ Nuova voce aggiunta con successo!", icon="🎉")
                            st.success(f"Dati inseriti correttamente alla riga {next_row_index}!")
                        
                            time.sleep(1)
                            st.rerun()
                    except Exception as ex:
                        st.error(f"Errore durante l'inserimento: {ex}")

        st.markdown("<br>", unsafe_allow_html=True)

    elif current == "📋 ANAGRAFICA":
        st.subheader("📋 Anagrafica")

        st.markdown("""
        <div style='background-color: #000000; border: 2px solid #ff0000; border-radius: 6px; overflow: hidden; margin-bottom: 20px;'>
            <div style='background-color: #FFFF00; color: #000000; text-align: center; font-weight: bold; font-size: 1.1rem; padding: 10px;'>
                ANAGRAFICA ALLIEVI
            </div>
        </div>
        """, unsafe_allow_html=True)

        anagrafica_rows = []
        try:
            creds = ottieni_credenziali()
            if creds:
                client = gspread.authorize(creds)
                sheet = client.open_by_key(SHEET_ID)
                target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(GID_ANAGRAFICA).strip()), None)

                if target_ws:
                    raw_anagrafica = target_ws.get("C13:L35")
                    for r in raw_anagrafica:
                        anagrafica_rows.append([
                            r[0] if len(r) > 0 else "",
                            r[1] if len(r) > 1 else "",
                            r[2] if len(r) > 2 else "",
                            r[3] if len(r) > 3 else "",
                            r[4] if len(r) > 4 else "",
                            r[5] if len(r) > 5 else "",
                            r[6] if len(r) > 6 else "",
                            r[7] if len(r) > 7 else "",
                            r[8] if len(r) > 8 else "",
                            r[9] if len(r) > 9 else ""
                        ])
        except Exception as e:
            st.warning(f"Errore nel caricamento dati Anagrafica: {e}")

        if not anagrafica_rows:
            cols_names = ["Nickname", "Nome Reale", "Paese", "Data Ingresso", "Livello Attuale", "Coach", "Ore Totali", "Obiettivo", "Certificazione"]
            df_anagrafica = pd.DataFrame(columns=cols_names)
        else:
            header_anagrafica = anagrafica_rows[0] if len(anagrafica_rows) > 0 else ["ID", "Nickname", "Nome Reale", "Paese", "Data Ingresso", "Livello Attuale", "Coach", "Ore Totali", "Obiettivo", "Certificazione"]
            data_anagrafica = anagrafica_rows[1:] if len(anagrafica_rows) > 1 else [[""] * 10]
            
            cleaned_data = []
            for row in data_anagrafica:
                new_row = list(row)
                while len(new_row) < 10:
                    new_row.append("")
                val_livello = str(new_row[5])
                count_stars = val_livello.count('*')
                if count_stars > 0:
                    new_row[5] = "⭐" * count_stars
                cleaned_data.append(new_row)

            df_anagrafica = pd.DataFrame(cleaned_data, columns=header_anagrafica)

            if "ID" in df_anagrafica.columns:
                df_anagrafica = df_anagrafica.drop(columns=["ID"])

        # --- GESTIONE VISUALIZZAZIONE A TENDINA CON BOX PROFESSIONALI ---
        if df_anagrafica.empty:
            st.info("Nessun dato disponibile nell'anagrafica.")
        else:
            col_nickname = df_anagrafica.columns[0]
            df_valid = df_anagrafica[df_anagrafica[col_nickname].astype(str).str.strip() != ""]

            if df_valid.empty:
                st.info("Nessun allievo trovato.")
            else:
                lista_giocatori = df_valid[col_nickname].tolist()
                
                selected_player = st.selectbox("🔍 Seleziona un giocatore dal database:", lista_giocatori)

                if selected_player:
                    giocatore_data = df_valid[df_valid[col_nickname] == selected_player].iloc[0]
                    columns_list = df_valid.columns.tolist()

                    st.markdown(f"""
                    <div style='margin-top: 20px; margin-bottom: 15px; padding: 12px 20px; background: linear-gradient(90deg, #161b22 0%, #21262d 100%); border-left: 5px solid #58a6ff; border-radius: 4px;'>
                        <h3 style='margin: 0; color: #f0f6fc; font-size: 1.3rem;'>👤 Scheda Profilo: <span style='color: #58a6ff;'>{selected_player}</span></h3>
                    </div>
                    """, unsafe_allow_html=True)

                    def render_box(col_name, val):
                        valore_str = str(val).strip()
                        if not valore_str:
                            valore_str = "<span style='color: #6e7681; font-style: italic;'>Non specificato</span>"
                        
                        return f"""
                        <div style='background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                            <div style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: #8b949e; margin-bottom: 6px; font-weight: 600;'>{col_name}</div>
                            <div style='font-size: 1.05rem; color: #c9d1d9; font-weight: 500;'>{valore_str}</div>
                        </div>
                        """

                    # Separiamo gli ultimi campi: prendiamo tutti tranne l'ultimo per le due colonne, 
                    # e l'ultimo lo riserviamo per la riga a tutta larghezza.
                    campi_standard = columns_list[:-1]
                    ultimo_campo = columns_list[-1]

                    col1, col2 = st.columns(2)
                    half = (len(campi_standard) + 1) // 2

                    with col1:
                        for col in campi_standard[:half]:
                            st.markdown(render_box(col, giocatore_data[col]), unsafe_allow_html=True)

                    with col2:
                        for col in campi_standard[half:]:
                            st.markdown(render_box(col, giocatore_data[col]), unsafe_allow_html=True)

                    # L'ultimo campo viene renderizzato a tutta larghezza (full-width)
                    st.markdown(render_box(ultimo_campo, giocatore_data[ultimo_campo]), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
    elif current == "📈 PROGRESSI":
        st.subheader("📈 Progressi")

        st.markdown("""
        <div style='background-color: #000000; border: 2px solid #ff0000; border-radius: 6px; overflow: hidden; margin-bottom: 20px;'>
            <div style='background-color: #FFFF00; color: #000000; text-align: center; font-weight: bold; font-size: 1.1rem; padding: 10px;'>
                TABELLA PROGRESSI
            </div>
        </div>
        """, unsafe_allow_html=True)

        progressi_rows = []
        try:
            creds = ottieni_credenziali()
            if creds:
                client = gspread.authorize(creds)
                sheet = client.open_by_key(SHEET_ID)
                target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(GID_PROGRESSI).strip()), None)

                if target_ws:
                    raw_progressi = target_ws.get("B12:I35")
                    for r in raw_progressi:
                        progressi_rows.append([
                            r[0] if len(r) > 0 else "",
                            r[1] if len(r) > 1 else "",
                            r[2] if len(r) > 2 else "",
                            r[3] if len(r) > 3 else "",
                            r[4] if len(r) > 4 else "",
                            r[5] if len(r) > 5 else "",
                            r[6] if len(r) > 6 else "",
                            r[7] if len(r) > 7 else ""
                        ])
        except Exception as e:
            st.warning(f"Errore nel caricamento dati Progressi: {e}")

        expected_columns = ["Allievo", "AIM", "Building", "Movimento", "Teamwork", "Game Sense", "Leadership", "Media"]

        if not progressi_rows:
            df_progressi = pd.DataFrame(columns=expected_columns)
        else:
            data_progressi = progressi_rows[1:] if len(progressi_rows) > 1 else progressi_rows
            
            cleaned_data = []
            for row in data_progressi:
                new_row = list(row)
                while len(new_row) < 8:
                    new_row.append("")
                cleaned_data.append(new_row[:8])

            df_progressi = pd.DataFrame(cleaned_data, columns=expected_columns)

        df_progressi = df_progressi.replace(r'^\s*$', pd.NA, regex=True)
        df_progressi = df_progressi.dropna(how='all').fillna("")

        # --- GESTIONE VISUALIZZAZIONE A TENDINA CON BOX E BARRE DI PROGRESSO ---
        if df_progressi.empty:
            st.info("Nessun dato disponibile nei progressi.")
        else:
            col_allievo = df_progressi.columns[0]
            df_valid = df_progressi[df_progressi[col_allievo].astype(str).str.strip() != ""]

            if df_valid.empty:
                st.info("Nessun allievo trovato.")
            else:
                lista_allievi = df_valid[col_allievo].tolist()
                
                selected_allievo = st.selectbox("🔍 Seleziona un allievo per i progressi:", lista_allievi, key="select_progressi")

                if selected_allievo:
                    allievo_data = df_valid[df_valid[col_allievo] == selected_allievo].iloc[0]
                    columns_list = df_valid.columns.tolist()

                    st.markdown(f"""
                    <div style='margin-top: 20px; margin-bottom: 15px; padding: 12px 20px; background: linear-gradient(90deg, #161b22 0%, #21262d 100%); border-left: 5px solid #58a6ff; border-radius: 4px;'>
                        <h3 style='margin: 0; color: #f0f6fc; font-size: 1.3rem;'>📈 Statistiche Progressi: <span style='color: #58a6ff;'>{selected_allievo}</span></h3>
                    </div>
                    """, unsafe_allow_html=True)

                    def parse_val_to_float(val):
                        try:
                            clean = str(val).replace("%", "").replace(",", ".").strip()
                            return float(clean)
                        except:
                            return 0.0

                    def render_progress_box(col_name, val):
                        valore_str = str(val).strip()
                        if not valore_str:
                            return f"""
                            <div style='background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                                <div style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: #8b949e; margin-bottom: 6px; font-weight: 600;'>{col_name}</div>
                                <div style='font-size: 1.05rem; color: #6e7681; font-style: italic;'>Non specificato</div>
                            </div>
                            """

                        # Se è la prima colonna (Nome Allievo)
                        if col_name == columns_list[0]:
                            return f"""
                            <div style='background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                                <div style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: #8b949e; margin-bottom: 6px; font-weight: 600;'>{col_name}</div>
                                <div style='font-size: 1.05rem; color: #c9d1d9; font-weight: 500;'>{valore_str}</div>
                            </div>
                            """

                        # Per le metriche numeriche con percentuale
                        num_val = parse_val_to_float(valore_str)
                        
                        if num_val <= 40:
                            bar_color = "#ff0000"  # Rosso
                        elif num_val <= 80:
                            bar_color = "#ffaa00"  # Arancione
                        else:
                            bar_color = "#90ee90"  # Verde

                        return f"""
                        <div style='background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                                <span style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: #8b949e; font-weight: 600;'>{col_name}</span>
                                <span style='font-size: 0.95rem; color: #f0f6fc; font-weight: bold;'>{num_val}%</span>
                            </div>
                            <div style='background-color: #30363d; border-radius: 4px; overflow: hidden; height: 10px; width: 100%;'>
                                <div style='background-color: {bar_color}; width: {min(max(num_val, 0), 100)}%; height: 100%; border-radius: 4px;'></div>
                            </div>
                        </div>
                        """

                    # Abbiamo 8 colonne in totale: [Allievo, AIM, Building, Movimento, Teamwork, Game Sense, Leadership, Media]
                    # Dividiamo gli elementi in modo che "Movimento" e "Media" finiscano affiancati.
                    # Ad esempio: 
                    # Colonna 1: Allievo, AIM, Building, Movimento
                    # Colonna 2: Teamwork, Game Sense, Leadership, Media
                    
                    metà = len(columns_list) // 2  # 8 // 2 = 4 elementi per colonna
                    col1_items = columns_list[:metà]   # ["Allievo", "AIM", "Building", "Movimento"]
                    col2_items = columns_list[metà:]   # ["Teamwork", "Game Sense", "Leadership", "Media"]

                    col1, col2 = st.columns(2)

                    with col1:
                        for col in col1_items:
                            st.markdown(render_progress_box(col, allievo_data[col]), unsafe_allow_html=True)

                    with col2:
                        for col in col2_items:
                            st.markdown(render_progress_box(col, allievo_data[col]), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    elif current == "📜 CERTIFICAZIONI":
        st.subheader("📜 Certificazioni")

        st.markdown("""
        <div style='background-color: #000000; border: 2px solid #ff0000; border-radius: 6px; overflow: hidden; margin-bottom: 20px;'>
            <div style='background-color: #FFFF00; color: #000000; text-align: center; font-weight: bold; font-size: 1.1rem; padding: 10px;'>
                TABELLA CERTIFICAZIONI
            </div>
        </div>
        """, unsafe_allow_html=True)

        cert_rows = []
        try:
            creds = ottieni_credenziali()
            if creds:
                client = gspread.authorize(creds)
                sheet = client.open_by_key(SHEET_ID)
                target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(GID_CERTIFICAZIONI).strip()), None)

                if target_ws:
                    raw_cert = target_ws.get("B18:O40")
                    for r in raw_cert:
                        row_padded = []
                        for idx in range(14):
                            row_padded.append(r[idx] if idx < len(r) and r[idx] is not None else "")
                        cert_rows.append(row_padded)
        except Exception as e:
            st.warning(f"Errore nel caricamento dati Certificazioni: {e}")

        expected_cert_columns = [
            "Allievo", "Bronze Aim", "Silver Aim", "Gold Aim", 
            "SWITCH VELOCE ARMI", "BUILD DI PROTEZIONE", "BUILD PER PUSH", 
            "USO DI BUILD COMPLESSIVO", "MIRA", "LOOT", "SNIPER", 
            "TEORIA ARMI", "USO DELLE ARMI COMPLESSIVO", "TEAM WORK"
        ]

        if not cert_rows:
            df_certificazioni = pd.DataFrame(columns=expected_cert_columns)
        else:
            data_cert = cert_rows[1:] if len(cert_rows) > 1 else cert_rows
    
            cleaned_cert_data = []
            for row in data_cert:
                new_row = list(row)
                while len(new_row) < 14:
                    new_row.append("")
                cleaned_cert_data.append(new_row[:14])

            df_certificazioni = pd.DataFrame(cleaned_cert_data, columns=expected_cert_columns)

        df_certificazioni = df_certificazioni.replace(r'^\s*$', pd.NA, regex=True)
        df_certificazioni = df_certificazioni.dropna(how='all').fillna("")

        # --- GESTIONE VISUALIZZAZIONE A TENDINA CON BOX ---
        if df_certificazioni.empty:
            st.info("Nessun dato disponibile nelle certificazioni.")
        else:
            col_allievo = df_certificazioni.columns[0]
            df_valid = df_certificazioni[df_certificazioni[col_allievo].astype(str).str.strip() != ""]

            if df_valid.empty:
                st.info("Nessun allievo trovato.")
            else:
                lista_allievi = df_valid[col_allievo].tolist()
            
                selected_allievo = st.selectbox("🔍 Seleziona un allievo per le certificazioni:", lista_allievi, key="select_certificazioni")

                if selected_allievo:
                    allievo_data = df_valid[df_valid[col_allievo] == selected_allievo].iloc[0]
                    columns_list = df_valid.columns.tolist()

                    st.markdown(f"""
                    <div style='margin-top: 20px; margin-bottom: 15px; padding: 12px 20px; background: linear-gradient(90deg, #161b22 0%, #21262d 100%); border-left: 5px solid #58a6ff; border-radius: 4px;'>
                        <h3 style='margin: 0; color: #f0f6fc; font-size: 1.3rem;'>📜 Certificazioni: <span style='color: #58a6ff;'>{selected_allievo}</span></h3>
                    </div>
                    """, unsafe_allow_html=True)

                    def render_cert_box(col_name, val):
                        valore_str = str(val).strip()
                        if not valore_str:
                            valore_display = "<span style='color: #6e7681; font-style: italic;'>Non specificato</span>"
                        else:
                            valore_display = f"<span style='color: #f0f6fc; font-weight: bold;'>{valore_str}</span>"

                        return f"""
                        <div style='background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                            <div style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: #8b949e; margin-bottom: 6px; font-weight: 600;'>{col_name}</div>
                            <div style='font-size: 1.05rem;'>{valore_display}</div>
                        </div>
                        """

                    # Escludiamo la prima colonna (Nome Allievo) dai box delle metriche
                    campi_metriche = columns_list[1:]
                
                    # Dividiamo le 13 metriche in due colonne simmetriche
                    metà = (len(campi_metriche) + 1) // 2
                    col1_items = campi_metriche[:metà]
                    col2_items = campi_metriche[metà:]

                    col1, col2 = st.columns(2)

                    with col1:
                        for col in col1_items:
                            st.markdown(render_cert_box(col, allievo_data[col]), unsafe_allow_html=True)

                    with col2:
                        for col in col2_items:
                            st.markdown(render_cert_box(col, allievo_data[col]), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    elif current == "🏋️ ESERCIZI":
        st.subheader("🏋️ Esercizi")

        st.markdown("""
        <div style='background-color: #000000; border: 2px solid #ff0000; border-radius: 6px; overflow: hidden; margin-bottom: 20px;'>
            <div style='background-color: #FFFF00; color: #000000; text-align: center; font-weight: bold; font-size: 1.1rem; padding: 10px;'>
                GESTIONE ESERCIZI ALLIEVI
            </div>
        </div>
        """, unsafe_allow_html=True)

        esercizi_rows = []
        target_ws_obj = None
        try:
            creds = ottieni_credenziali()
            if creds:
                client = gspread.authorize(creds)
                sheet = client.open_by_key(SHEET_ID)
                target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(GID_ESERCIZI).strip()), None)
                target_ws_obj = target_ws

                if target_ws:
                    raw_es = target_ws.get("C17:M40")
                    for r in raw_es:
                        row_padded = []
                        for idx in range(11):
                            row_padded.append(r[idx] if idx < len(r) and r[idx] is not None else "")
                        esercizi_rows.append(row_padded)
        except Exception as e:
            st.warning(f"Errore nel caricamento dati Esercizi: {e}")

        expected_es_columns = [
            "Allievo", 
            "ESERCIZIO 1", "CHECK 1", 
            "ESERCIZIO 2", "CHECK 2", 
            "ESERCIZIO 3", "CHECK 3", 
            "ESERCIZIO 4", "CHECK 4", 
            "ESERCIZIO 5", "CHECK 5"
        ]

        if not esercizi_rows:
            df_esercizi = pd.DataFrame(columns=expected_es_columns)
        else:
            cleaned_es_data = []
            for row in esercizi_rows:
                new_row = list(row)
                while len(new_row) < 11:
                    new_row.append("")
            
                for check_idx in [2, 4, 6, 8, 10]:
                    val = new_row[check_idx]
                    if isinstance(val, bool):
                        new_row[check_idx] = val
                    else:
                        val_str = str(val).strip().upper()
                        if val_str in ["TRUE", "VERO", "1", "V", "YES", "X", "ON"]:
                            new_row[check_idx] = True
                        else:
                            new_row[check_idx] = False
                cleaned_es_data.append(new_row[:11])

            df_esercizi = pd.DataFrame(cleaned_es_data, columns=expected_es_columns)

        df_esercizi = df_esercizi.replace(r'^\s*$', pd.NA, regex=True)
        df_esercizi = df_esercizi.dropna(subset=["Allievo"], how='all').fillna({
            "Allievo": "",
            "ESERCIZIO 1": "", "CHECK 1": False,
            "ESERCIZIO 2": "", "CHECK 2": False,
            "ESERCIZIO 3": "", "CHECK 3": False,
            "ESERCIZIO 4": "", "CHECK 4": False,
            "ESERCIZIO 5": "", "CHECK 5": False
        })

        # --- SELEZIONE TRAMITE MENU A TENDINA E BOX ---
        df_valid_es = df_esercizi[df_esercizi["Allievo"].astype(str).str.strip() != ""]

        if df_valid_es.empty:
            st.info("Nessun allievo trovato nella tabella esercizi.")
        else:
            lista_allievi_es = df_valid_es["Allievo"].tolist()
            selected_allievo_es = st.selectbox("🔍 Seleziona un allievo per gli esercizi:", lista_allievi_es, key="select_esercizi_menu")

            if selected_allievo_es:
                # Troviamo la riga corrispondente nel dataframe
                row_idx_df = df_valid_es[df_valid_es["Allievo"] == selected_allievo_es].index[0]
                allievo_data = df_esercizi.loc[row_idx_df]

                st.markdown(f"""
                <div style='margin-top: 20px; margin-bottom: 15px; padding: 12px 20px; background: linear-gradient(90deg, #161b22 0%, #21262d 100%); border-left: 5px solid #FF0000; border-radius: 4px;'>
                    <h3 style='margin: 0; color: #f0f6fc; font-size: 1.3rem;'>🏋️ Esercizi di: <span style='color: #FFFF00;'>{selected_allievo_es}</span></h3>
                </div>
                """, unsafe_allow_html=True)

                with st.form(f"form_esercizi_{row_idx_df}"):
                    nuovi_valori_esercizi = {}
                
                    # Creiamo 5 box con esercizio (testo) e checkbox associata
                    for i in range(1, 6]:
                        es_col = f"ESERCIZIO {i}"
                        chk_col = f"CHECK {i}"
                    
                        val_es_attuale = str(allievo_data[es_col])
                        val_chk_attuale = bool(allievo_data[chk_col])

                        st.markdown(f"""
                        <div style='background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 15px; margin-bottom: 10px;'>
                            <div style='font-size: 0.8rem; text-transform: uppercase; color: #8b949e; font-weight: bold; margin-bottom: 5px;'>Esercizio {i}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        c_in1, c_in2 = st.columns([3, 1])
                        with c_in1:
                            nuovi_valori_esercizi[es_col] = st.text_input(f"Nome Esercizio {i}", value=val_es_attuale, key=f"input_es_{i}_{row_idx_df}", label_visibility="collapsed")
                        with c_in2:
                        nuovi_valori_esercizi[chk_col] = st.checkbox("Completato", value=val_chk_attuale, key=f"chk_es_{i}_{row_idx_df}")
    
                    # Pulsante Giallo in basso senza scritte descrittive o con stile personalizzato
                    st.markdown("""
                    <style>
                        [data-testid="stFormSubmitButton"] button {
                            background-color: #FFFF00 !important;
                            color: #000000 !important;
                            width: 100% !important;
                            font-weight: bold !important;
                        }
                        [data-testid="stFormSubmitButton"] button:hover {
                            background-color: #cccc00 !important;
                            color: #000000 !important;
                        }
                    </style>
                    """, unsafe_allow_html=True)

                    submit_es = st.form_submit_button("➕")

                    if submit_es:
                        try:
                            # Aggiorniamo il dataframe generale con i nuovi valori inseriti nel form
                            for col_k, val_k in nuovi_valori_esercizi.items():
                                df_esercizi.loc[row_idx_df, col_k] = val_k

                            # Prepariamo la lista da salvare su Google Sheets
                            data_to_write = df_esercizi.values.tolist()
                            if target_ws_obj:
                                end_row = 17 + len(data_to_write) - 1
                                target_ws_obj.update(f"C17:M{end_row}", data_to_write, value_input_option='USER_ENTERED')
                            
                                st.toast("✅ Modifiche Esercizi salvate con successo!", icon="🎉")
                                st.success("Dati aggiornati correttamente su Google Sheet!")
                            
                                time.sleep(1)
                                st.rerun()
                        except Exception as ex:
                            st.error(f"Errore durante il salvataggio: {ex}")

        st.markdown("<br>", unsafe_allow_html=True)

    elif current == "👤 SCHEDE GIOCATORE":
        st.subheader("👤 Schede Giocatore")

        if "selected_player" not in st.session_state:
            st.session_state.selected_player = PLAYERS[0]

        player_gids = {
            "JFF_ANDERWAL": "341001551",
            "ITABOYZ_VIN": "1483818122",
            "JFF_CLIP": "1771413751",
            "ITABOYZ_GALLO": "1353776186",
            "ITABOYZ_IMPERATUBER": "132907169",
            "JFF_POTA": "596698328",
            "ITABOYZ_CASCO": "89864457",
            "JFF_CIKKO": "1697770491",
            "JFF_SINNER": "1148507572"
        }

        for player_name in PLAYERS:
            btn_type = "primary" if st.session_state.selected_player == player_name else "secondary"
            if st.button(player_name, key=f"btn_p_{player_name}", type=btn_type):
                st.session_state.selected_player = player_name
                st.rerun()

        st.markdown("---")
        
        current_gid = player_gids.get(st.session_state.selected_player, "")

        ruolo_consigliato = ""
        punti_di_forza_text = ""
        aree_miglioramento_text = ""

        try:
            creds = ottieni_credenziali()
            if creds and current_gid:
                client = gspread.authorize(creds)
                sheet = client.open_by_key(SHEET_ID)
                
                target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(current_gid).strip()), None)
                
                if target_ws:
                    ruolo_consigliato = target_ws.acell("F19").value if target_ws.acell("F19") else ""
                    punti_di_forza_text = target_ws.acell("F21").value if target_ws.acell("F21") else ""
                    aree_miglioramento_text = target_ws.acell("F29").value if target_ws.acell("F29") else ""
        except Exception as e:
            st.warning(f"Errore nel caricamento dati per {st.session_state.selected_player}: {e}")

        def format_custom_box_text(raw_text):
            if not raw_text:
                return "<span style='color: #888;'>Nessun dato inserito per questo giocatore.</span>"
            
            import re
            clean_text = raw_text.strip()
            
            processed_text = re.sub(r'(^|\.\s+)([A-ZÀ-Úa-zà-ú\s\(\)]+?:)', r'\1<br><br><span style="color: #FFFF00; font-weight: bold;">\2</span>', clean_text)
            processed_text = re.sub(r'^<br><br>', '', processed_text)
            
            lines = processed_text.split('<br><br>')
            formatted_lines = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if "<span style=" in line:
                    formatted_lines.append(f"<div style='margin-bottom: 12px;'>{line}</div>")
                elif ":" in line:
                    parts = line.split(":", 1)
                    title_part = parts[0].strip()
                    desc_part = parts[1].strip()
                    formatted_lines.append(f"<div style='margin-bottom: 12px;'><span style='color: #FFFF00; font-weight: bold;'>{title_part}:</span> {desc_part}</div>")
                else:
                    formatted_lines.append(f"<div style='margin-bottom: 12px;'>{line}</div>")
            
            return "".join(formatted_lines)

        st.markdown("""
        <div style='border: 2px solid #ff0000; border-radius: 4px; background-color: #000000; margin-bottom: 20px; overflow: hidden;'>
            <div style='background-color: #000000; color: #ff0000; font-weight: bold; font-size: 1.1rem; padding: 12px 15px; border-bottom: 2px solid #0055ff;'>
                RUOLO CONSIGLIATO
            </div>
            <div style='background-color: #001133; color: #ffffff; padding: 15px; font-size: 1rem;'>
                {}
            </div>
        </div>
        """.format(ruolo_consigliato if ruolo_consigliato else "Nessun ruolo specificato"), unsafe_allow_html=True)

        formatted_forza = format_custom_box_text(punti_di_forza_text)
        st.markdown("""
        <div style='border: 2px solid #ff0000; border-radius: 4px; background-color: #000000; margin-bottom: 20px; overflow: hidden;'>
            <div style='background-color: #000000; color: #ff0000; font-weight: bold; font-size: 1.1rem; padding: 12px 15px; border-bottom: 2px solid #0055ff;'>
                PUNTI DI FORZA
            </div>
            <div style='background-color: #001133; color: #ffffff; padding: 15px; font-size: 1rem;'>
                {}
            </div>
        </div>
        """.format(formatted_forza), unsafe_allow_html=True)

        formatted_miglioramento = format_custom_box_text(aree_miglioramento_text)
        st.markdown("""
        <div style='border: 2px solid #ff0000; border-radius: 4px; background-color: #000000; margin-bottom: 20px; overflow: hidden;'>
            <div style='background-color: #000000; color: #ff0000; font-weight: bold; font-size: 1.1rem; padding: 12px 15px; border-bottom: 2px solid #0055ff;'>
                AREE DI MIGLIORAMENTO
            </div>
            <div style='background-color: #001133; color: #ffffff; padding: 15px; font-size: 1rem;'>
                {}
            </div>
        </div>
        """.format(formatted_miglioramento), unsafe_allow_html=True)

    elif current == "📊 STATISTICHE":
        st.subheader("📊 Statistiche")

        if "stat_tab" not in st.session_state:
            st.session_state.stat_tab = STATS_OPTIONS[0]

        for stat_opt in STATS_OPTIONS:
            btn_type = "primary" if st.session_state.stat_tab == stat_opt else "secondary"
            if st.button(stat_opt, key=f"btn_s_{stat_opt}", type=btn_type):
                st.session_state.stat_tab = stat_opt
                st.rerun()

        st.markdown("---")

        if st.session_state.stat_tab == "⚙️ SETTINGS":
            st.markdown("<div style='background-color: #0e1117; border: 2px solid #262730; border-radius: 12px; padding: 15px;'>", unsafe_allow_html=True)
            st.markdown("### ⚙️ Settings")

            settings_options = []
            option_to_date = {}
            try:
                creds = ottieni_credenziali()
                if creds:
                    client = gspread.authorize(creds)
                    sheet = client.open_by_key(SHEET_ID)
                    target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(GID_SETTINGS).strip()), None)
                    if target_ws:
                        # Legge contemporaneamente le colonne B e C dalla riga 6 alla 30
                        raw_b6_c30 = target_ws.get("B6:C30")
                        for row in raw_b6_c30:
                            if row and len(row) >= 1:
                                opt_val = str(row[1]).strip() if len(row) > 1 else ""
                                date_val = str(row[0]).strip() if len(row) > 0 else ""
                            
                                if opt_val and opt_val.lower() not in ["nan", "none", ""]:
                                    settings_options.append(opt_val)
                                    option_to_date[opt_val] = date_val if date_val.lower() not in ["nan", "none", ""] else "N/A"
            except Exception as e:
                st.warning(f"Errore nel caricamento delle opzioni da Settings: {e}")

            if not settings_options:
                settings_options = ["Nessun valore disponibile"]

            selected_setting = st.selectbox("Seleziona valore da C6:C30", settings_options, key="sb_settings_c6_c30")

            # Mostra la data dell'evento corrispondente alla riga della colonna B
            event_date = option_to_date.get(selected_setting, "N/A")
            st.markdown(f"""
                <div style='background-color: #161b22; padding: 10px 14px; border-radius: 6px; margin: 10px 0 15px 0; border: 1px solid #30363d;'>
                    <span style='color: #8b949e;'>📅 Data dell'evento:</span> <strong style='color: #58a6ff;'>{event_date}</strong>
                </div>
            """, unsafe_allow_html=True)

            if st.button("SCEGLI", key="btn_scegli_settings"):
                try:
                    scrivi_cella_per_gid(GID_SETTINGS, "E6", selected_setting)
                    st.toast("✅ Valore impostato con successo in E6!", icon="🎉")
                    st.success(f"Valore '{selected_setting}' impostato con successo nella cella E6!")
                    time.sleep(1)
                    st.rerun()
                except Exception as ex:
                    st.error(f"Errore durante l'impostazione del valore: {ex}")

            st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state.stat_tab == "🏋️ TRAINING":
            st.markdown("""
                <div style='text-align: center; margin-bottom: 25px;'>
                    <h2 style='color: #FFD700; text-transform: uppercase;'>🏋️ Training Data</h2>
                    <p style='color: #8b949e;'>Statistiche dettagliate di addestramento e armi</p>
                </div>
            """, unsafe_allow_html=True)

            def render_excel_table(df_source, start_row, end_row, start_col, end_col, border_color):
                try:
                    subset = df_source.iloc[start_row:end_row+1, start_col:end_col+1].copy()
                    if subset.empty:
                        return

                    title = str(subset.iloc[0, 0]).strip()
                    if title == "nan" or not title:
                        title = f"Tabella ({start_row+1}:{end_row+1})"
            
                    # Gestione dei nomi di colonna duplicati per evitare errori in pandas
                    raw_cols = subset.iloc[1].fillna("").astype(str).tolist()
                    seen = {}
                    unique_cols = []
                    for c in raw_cols:
                        col_name = c.strip() if c.strip() else "Unnamed"
                        if col_name in seen:
                            seen[col_name] += 1
                            unique_cols.append(f"{col_name}_{seen[col_name]}")
                        else:
                            seen[col_name] = 0
                            unique_cols.append(col_name)
                
                    subset.columns = unique_cols
                    table_data = subset.iloc[2:].reset_index(drop=True)

                    st.markdown(f"""
                        <div style='border-left: 5px solid {border_color}; background-color: #161b22; padding: 8px 12px; margin-top: 25px; border-radius: 4px;'>
                            <h4 style='color: {border_color}; margin: 0; text-transform: uppercase; font-size: 1.1rem;'>{title}</h4>
                        </div>
                    """, unsafe_allow_html=True)
            
                    st.dataframe(table_data, use_container_width=True, hide_index=True)
                except Exception as e:
                    st.error(f"Errore nel rendering della tabella [{start_row}:{end_row}]: {e}")

            training_sections = [
                (20, 47, 1, 12, "#2ea043"),  # B21:M48 (Armi 1)
                (51, 78, 1, 12, "#2ea043"),  # B52:M79 (Armi 2)
                (82, 109, 1, 13, "#FFD700"), # B83:N110 (Gialla)
                (111, 138, 1, 13, "#FFD700"),# B112:N139 (Gialla)
                (141, 168, 1, 13, "#FFD700"),# B142:N169 (Gialla)
                (171, 198, 1, 13, "#FFD700"),# B172:N199 (Gialla)
                (201, 228, 1, 13, "#FFD700"),# B202:N229 (Gialla)
                (230, 257, 1, 13, "#FFD700"),# B231:N258 (Gialla)
                (260, 287, 1, 13, "#1f6feb"),# B261:N288 (Blu)
                (290, 317, 1, 13, "#1f6feb"),# B291:N318 (Blu)
                (320, 347, 1, 13, "#1f6feb"),# B321:N348 (Blu)
                (350, 377, 1, 13, "#1f6feb"),# B351:N378 (Blu)
                (380, 407, 1, 13, "#238636"),# B381:N408 (Verde)
                (410, 437, 1, 13, "#ffa657"),# B411:N438 (Arancione)
                (440, 467, 1, 13, "#ffa657"),# B441:N468 (Arancione)
                (470, 497, 1, 13, "#ffa657"),# B471:N498 (Arancione)
                (500, 527, 1, 13, "#ffa657"),# B501:N528 (Arancione)
                (530, 557, 1, 13, "#ffa657"),# B531:N558 (Arancione)
                (560, 587, 1, 13, "#8957e5"),# B561:N588 (Viola)
                (590, 617, 1, 13, "#8957e5"),# B591:N618 (Viola)
                (620, 647, 1, 13, "#8957e5"),# B621:N648 (Viola)
                (650, 677, 1, 13, "#da3633"),# B651:N678 (Rosso)
                (680, 707, 1, 13, "#da3633") # B681:N708 (Rosso)
            ]

            GID_TRAINING = "1956525109"
            current_df = None

            try:
                with st.spinner("Caricamento dati di training in corso..."):
                    creds = ottieni_credenziali()
                    if creds:
                        client = gspread.authorize(creds)
                        sheet = client.open_by_key(SHEET_ID)
                        target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(GID_TRAINING).strip()), None)
                        if target_ws:
                            raw_data = target_ws.get_all_values()
                            current_df = pd.DataFrame(raw_data)
            except Exception as e:
                st.error(f"Errore nel caricamento del foglio Training da Google Sheets: {e}")

            if current_df is not None and not current_df.empty:
                for r_start, r_end, c_start, c_end, color in training_sections:
                    render_excel_table(current_df, r_start, r_end, c_start, c_end, color)
            else:
                st.error("⚠️ Impossibile caricare i dati dal foglio Training.")

        elif st.session_state.stat_tab == "🏆 STATCOMP":
            st.markdown("<div style='background-color: #0e1117; border: 2px solid #262730; border-radius: 12px; padding: 15px;'>", unsafe_allow_html=True)
            st.markdown("### 👤 Personal Stats")

            target_ws = None
            current_d13_val = ""
            extracted_players = []

            try:
                creds = ottieni_credenziali()
                if creds:
                    client = gspread.authorize(creds)
                    sheet = client.open_by_key(SHEET_ID)
                    target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(GID_PERSONAL_STATS).strip()), None)
                    
                    if target_ws:
                        d13_raw = target_ws.acell("D13").value
                        if d13_raw is not None and str(d13_raw).strip() != "":
                            current_d13_val = str(d13_raw).strip()
                    
                        col_c_values = target_ws.get("C12:C60")
                        for row in col_c_values:
                            if row and len(row) > 0:
                                p = str(row[0]).strip()
                                if p and p.lower() not in ["nan", "none", ""]:
                                    extracted_players.append(p)
                        extracted_players = list(dict.fromkeys(extracted_players))
            except Exception as e:
                st.warning(f"Error reading initial Personal Stats sheet: {e}")

            if not extracted_players:
                extracted_players = ["No players available"]

            player_index = 0
            if current_d13_val in extracted_players:
                player_index = extracted_players.index(current_d13_val)

            selected_d13_val = st.selectbox("Select Player", extracted_players, index=player_index, key="sb_player_d13")
            
            if str(selected_d13_val).strip().lower() != str(current_d13_val).strip().lower():
                scrivi_cella_per_gid(GID_PERSONAL_STATS, "D13", selected_d13_val)
                st.rerun()

            with st.spinner("Updating data..."):
                time.sleep(0.2)

            st.markdown("---")

            def format_val(val, is_percentage=False, decimals=2):
                try:
                    if val is None or str(val).strip() == "" or str(val).strip().lower() in ["nan", "none", "#n/a", "#valore!"]:
                        return "0.00%" if is_percentage else "0"
                    clean_val = str(val).replace("%", "").strip().replace(",", ".")
                    num = float(clean_val)
                    factor = 10 ** decimals
                    truncated = int(num * factor) / factor
                    if is_percentage:
                        return f"{truncated:.{decimals}f}%"
                    elif truncated.is_integer():
                        return str(int(truncated))
                    else:
                        return f"{truncated:.{decimals}f}"
                except Exception:
                    return str(val) if val is not None and str(val).strip() != "" else ("0.00%" if is_percentage else "0")

            summary_fired, summary_hit, summary_acc, summary_kill, summary_dmg, summary_mvp, summary_death = "0", "0", "0.00%", "0", "0", "0", "0"
            summary_revive, summary_oh_shots, summary_oh_hit, summary_oh_acc = "0", "0", "0", "0.00%"
            summary_th_shots, summary_th_hit, summary_th_acc = "0", "0", "0.00%"
            
            faster_banana_val = "-"
            total_assist_val = "0"
            
            deadliest_weapons = []
            weapon_rows_data = []

            try:
                if target_ws:
                    f16_s16 = target_ws.get("F16:S16")
                    if f16_s16 and len(f16_s16) > 0:
                        rv = f16_s16[0]
                        summary_fired    = format_val(rv[0] if len(rv) > 0 else 0)
                        summary_hit      = format_val(rv[1] if len(rv) > 1 else 0)
                        summary_acc      = format_val(rv[2] if len(rv) > 2 else 0, is_percentage=True)
                        summary_kill     = format_val(rv[3] if len(rv) > 3 else 0)
                        summary_dmg      = format_val(rv[4] if len(rv) > 4 else 0)
                        summary_mvp      = format_val(rv[5] if len(rv) > 5 else 0)
                        summary_death    = format_val(rv[6] if len(rv) > 6 else 0)
                        summary_revive   = format_val(rv[7] if len(rv) > 7 else 0)
                        summary_oh_shots = format_val(rv[8] if len(rv) > 8 else 0)
                        summary_oh_hit   = format_val(rv[9] if len(rv) > 9 else 0)
                        summary_oh_acc   = format_val(rv[10] if len(rv) > 10 else 0, is_percentage=True)
                        summary_th_shots = format_val(rv[11] if len(rv) > 11 else 0)
                        summary_th_hit   = format_val(rv[12] if len(rv) > 12 else 0)
                        summary_th_acc   = format_val(rv[13] if len(rv) > 13 else 0, is_percentage=True)

                    j18_l18 = target_ws.get("J18:L18")
                    if j18_l18 and len(j18_l18) > 0 and len(j18_l18[0]) > 0:
                        faster_banana_val = format_val(j18_l18[0][0])

                    q18_s18 = target_ws.get("Q18:S18")
                    if q18_s18 and len(q18_s18) > 0:
                        row_qa = q18_s18[0]
                        for cell_val in row_qa:
                            v_str = str(cell_val).strip()
                            if v_str and v_str.lower() not in ["nan", "none", ""]:
                                total_assist_val = format_val(v_str)
                                break

                    dw_configs = [
                        {"name_range": "H20:I20", "data_range": "H21:S21"},
                        {"name_range": "H23:I23", "data_range": "H24:S24"},
                        {"name_range": "H26:I26", "data_range": "H27:S27"}
                    ]

                    for cfg in dw_configs:
                        n_data = target_ws.get(cfg["name_range"])
                        w_name = "-"
                        if n_data and len(n_data) > 0:
                            row_n = n_data[0]
                            for cell in row_n:
                                val_str = str(cell).strip()
                                if val_str and val_str.lower() not in ["nan", "none", ""]:
                                    w_name = val_str
                                    break

                        r_data = target_ws.get(cfg["data_range"])
                        if r_data and len(r_data) > 0:
                            r_w = r_data[0]
                            deadliest_weapons.append({
                                "name": w_name,
                                "dmg": format_val(r_w[3] if len(r_w) > 3 else 0),  
                                "acc": format_val(r_w[4] if len(r_w) > 4 else 0, is_percentage=True), 
                                "onehand": format_val(r_w[6] if len(r_w) > 6 else 0),   
                                "shit_onehand": format_val(r_w[7] if len(r_w) > 7 else 0),
                                "acc_onehand": format_val(r_w[8] if len(r_w) > 8 else 0, is_percentage=True), 
                                "twohand": format_val(r_w[9] if len(r_w) > 9 else 0),   
                                "shit_twohand": format_val(r_w[10] if len(r_w) > 10 else 0),
                                "acc_twohand": format_val(r_w[11] if len(r_w) > 11 else 0, is_percentage=True)  
                            })
                        else:
                            deadliest_weapons.append({
                                "name": w_name, "dmg": "0", "acc": "0.00%", 
                                "onehand": "0", "shit_onehand": "0", "acc_onehand": "0.00%", 
                                "twohand": "0", "shit_twohand": "0", "acc_twohand": "0.00%"
                            })

                    weapons_raw = target_ws.get("F33:S74")
                    if weapons_raw:
                        for r_data in weapons_raw:
                            if r_data and len(r_data) > 0:
                                w_name = str(r_data[0]).strip()
                                if w_name and w_name.upper() not in ["NAN", "NONE", ""]:
                                    weapon_rows_data.append({
                                        "WEAPON": w_name,
                                        "TOT SHOTS": format_val(r_data[1] if len(r_data) > 1 else 0),
                                        "SHOT HIT": format_val(r_data[2] if len(r_data) > 2 else 0),
                                        "ACC%": format_val(r_data[3] if len(r_data) > 3 else 0, is_percentage=True),
                                        "DMG": format_val(r_data[4] if len(r_data) > 4 else 0),
                                        "HEADSHOT": format_val(r_data[5] if len(r_data) > 5 else 0),
                                        "MAX DISTANCE": format_val(r_data[6] if len(r_data) > 6 else 0), 
                                        "SHOT ONE": format_val(r_data[8] if len(r_data) > 8 else 0),
                                        "SHOT HIT ONE": format_val(r_data[9] if len(r_data) > 9 else 0),
                                        "ACC% ONE": format_val(r_data[10] if len(r_data) > 10 else 0, is_percentage=True),
                                        "SHOT TWO": format_val(r_data[11] if len(r_data) > 11 else 0),
                                        "SHOT HIT TWO": format_val(r_data[12] if len(r_data) > 12 else 0),
                                        "ACC% TWO": format_val(r_data[13] if len(r_data) > 13 else 0, is_percentage=True)
                                    })
            except Exception as e:
                st.warning(f"Error reading dashboard data: {e}")

            st.markdown("<h4 style='color: #93c5fd; font-size: 1rem;'>MATCH SUMMARY</h4>", unsafe_allow_html=True)
            
            def render_metric_row(m1, m2, m3):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"<div class='stat-card'><div class='stat-label'>{m1[0]}</div><div class='stat-value'>{m1[1]}</div></div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div class='stat-card'><div class='stat-label'>{m2[0]}</div><div class='stat-value'>{m2[1]}</div></div>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<div class='stat-card'><div class='stat-label'>{m3[0]}</div><div class='stat-value'>{m3[1]}</div></div>", unsafe_allow_html=True)

            render_metric_row(("DMG", summary_dmg), ("KILL", summary_kill), ("MVP", summary_mvp))
            render_metric_row(("SHOTS FIRED", summary_fired), ("SHOTS HIT", summary_hit), ("ACCURACY", summary_acc))
            render_metric_row(("DEATH", summary_death), ("REVIVE", summary_revive), ("FASTER BANANA", faster_banana_val))
            render_metric_row(("ONEHAND SHOTS", summary_oh_shots), ("ONEHAND HIT", summary_oh_hit), ("ONEHAND ACC%", summary_oh_acc))
            render_metric_row(("TWOHAND SHOTS", summary_th_shots), ("TWOHAND HIT", summary_th_hit), ("TWOHAND ACC%", summary_th_acc))

            st.markdown(f"""
            <div class='stat-card' style='width: 100%; height: 85px; margin-top: 10px;'>
                <div class='stat-label'>TOTAL ASSIST</div>
                <div class='stat-value'>{total_assist_val}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: #93c5fd; font-size: 1rem;'>DEADLIEST WEAPONS</h4>", unsafe_allow_html=True)
            
            for i, dw in enumerate(deadliest_weapons):
                st.markdown(f"""
                <div style='background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 15px;'>
                    <p style='color: #93c5fd; font-weight: bold; font-size: 1.1rem; margin-top: 0; margin-bottom: 12px; text-align: center;'>
                        Deadliest Weapon {i+1}: {dw['name']}
                    </p>
                """, unsafe_allow_html=True)
                
                dw_r1_c1, dw_r1_c2 = st.columns(2)
                with dw_r1_c1:
                    st.markdown(f"<div class='stat-card'><div class='stat-label'>DMG</div><div class='stat-value'>{dw['dmg']}</div></div>", unsafe_allow_html=True)
                with dw_r1_c2:
                    st.markdown(f"<div class='stat-card'><div class='stat-label'>ACC%</div><div class='stat-value'>{dw['acc']}</div></div>", unsafe_allow_html=True)

                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

                dw_r2_c1, dw_r2_c2, dw_r2_c3 = st.columns(3)
                with dw_r2_c1:
                    st.markdown(f"<div class='stat-card'><div class='stat-label'>ONEHAND</div><div class='stat-value'>{dw['onehand']}</div></div>", unsafe_allow_html=True)
                with dw_r2_c2:
                    st.markdown(f"<div class='stat-card'><div class='stat-label'>SHIT ONEHAND</div><div class='stat-value'>{dw['shit_onehand']}</div></div>", unsafe_allow_html=True)
                with dw_r2_c3:
                    st.markdown(f"<div class='stat-card'><div class='stat-label'>ACC% ONE</div><div class='stat-value'>{dw['acc_onehand']}</div></div>", unsafe_allow_html=True)

                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

                dw_r3_c1, dw_r3_c2, dw_r3_c3 = st.columns(3)
                with dw_r3_c1:
                    st.markdown(f"<div class='stat-card'><div class='stat-label'>TWOHAND</div><div class='stat-value'>{dw['twohand']}</div></div>", unsafe_allow_html=True)
                with dw_r3_c2:
                    st.markdown(f"<div class='stat-card'><div class='stat-label'>SHIT TWOHAND</div><div class='stat-value'>{dw['shit_twohand']}</div></div>", unsafe_allow_html=True)
                with dw_r3_c3:
                    st.markdown(f"<div class='stat-card'><div class='stat-label'>ACC% TWO</div><div class='stat-value'>{dw['acc_twohand']}</div></div>", unsafe_allow_html=True)
                    
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: #93c5fd; text-align: center;'>WEAPON PERFORMANCE</h4>", unsafe_allow_html=True)
            
            if weapon_rows_data:
                df_weapons_final = pd.DataFrame(weapon_rows_data)
            else:
                df_weapons_final = pd.DataFrame(columns=[
                    "WEAPON", "TOT SHOTS", "SHOT HIT", "ACC%", "DMG", "HEADSHOT", "MAX DISTANCE", 
                    "SHOT ONE", "SHOT HIT ONE", "ACC% ONE", "SHOT TWO", "SHOT HIT TWO", "ACC% TWO"
                ])

            st.dataframe(df_weapons_final, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)
