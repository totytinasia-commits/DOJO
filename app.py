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
    "📜 CERTIFICAZIONI ESERCIZI",
    "👤 SCHEDE GIOCATORE",
    "📊 STATISTICHE"
]

PLAYERS = [
    "JFF_ANDERWAL", "ITABOYZ_VIN", "JFF_CLIP",
    "ITABOYZ_GALLO", "ITABOYZ_IMPERATUBER", "JFF_POTA",
    "ITABOYZ_CASCO", "JFF_CIKKO", "JFF_SINNER"
]

STATS_OPTIONS = ["🏋️ TRAINING", "🏆 STATCOMP"]

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

        f13_val, h13_val = "", ""
        f14_val, h14_val = "", ""
        box_pix_rows = []
        box_nino_rows = []
        box2_rows = []

        try:
            creds = ottieni_credenziali()
            if creds:
                client = gspread.authorize(creds)
                sheet = client.open_by_key(SHEET_ID)
                target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(GID_ACADEMY).strip()), None)

                if target_ws:
                    f13_val = target_ws.acell("F13").value or ""
                    h13_val = target_ws.acell("H13").value or ""
                    f14_val = target_ws.acell("F14").value or ""
                    h14_val = target_ws.acell("H14").value or ""

                    # Dati fissi per ARES PIX
                    box_pix_rows = [
                        ["JFF_CLIP", "L/M/G/D", "DOJO MAP"],
                        ["itaboyz_Casco", "L/M/G/D", "DOJO MAP"],
                        ["itaBOYZ_VIN", "L/M/G/D", "DOJO MAP"],
                        ["itaboyz_imperat", "L/M/G/D", "DOJO MAP"],
                        ["itaboyz_gallo", "L/M/G/D", "DOJO MAP"]
                    ]

                    # Dati fissi per ARES NINO
                    box_nino_rows = [
                        ["JFF_SINNER", "L/M/G/D", "DOJO MAP"],
                        ["JFF_POTA", "L/M/G/D", "DOJO MAP"],
                        ["JFF_ANDERWAL", "L/M/G/D", "DOJO MAP"],
                        ["JFF_DANI", "L/M/G/D", "DOJO MAP"],
                        ["itaboyz_faire", "L/M/G/D", "DOJO MAP"]
                    ]

                    # Preleviamo l'intervallo C28:E50 per il Registro Attività
                    raw_box2 = target_ws.get("C28:E50")
                    for r in raw_box2:
                        box2_rows.append([
                            r[0] if len(r) > 0 else "",
                            r[1] if len(r) > 1 else "",
                            r[2] if len(r) > 2 else ""
                        ])
        except Exception as e:
            st.warning(f"Errore nel caricamento dati Academy: {e}")

        # Header principale superiore
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

        # ==========================================
        # 1. SEZIONE FISSA: ARES PIX
        # ==========================================
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

        # ==========================================
        # 2. SEZIONE FISSA: ARES NINO
        # ==========================================
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

        # ==========================================
        # 3. REGISTRO ATTIVITA' (EDITABILE) - C28:E50
        # ==========================================
        st.markdown("""
        <div style='background-color: #000000; border: 2px solid #ff0000; border-radius: 6px; overflow: hidden; margin-bottom: 20px;'>
            <div style='background-color: #FFFF00; color: #000000; text-align: center; font-weight: bold; font-size: 1.1rem; padding: 8px;'>
                REGISTRO ATTIVITA'
            </div>
            <div class='fixed-box-header'>
                <span style='flex: 2;'>allievi a carico</span>
                <span style='flex: 1; text-align: center;'>giorni</span>
                <span style='flex: 1; text-align: right;'>mappa</span>
            </div>
        """, unsafe_allow_html=True)

        if not box2_rows:
            box2_rows = [["", "", ""]] * 10

        df_registro = pd.DataFrame(box2_rows, columns=["allievi a carico", "giorni", "mappa"])

        edited_df = st.data_editor(
            df_registro,
            use_container_width=True,
            num_rows="dynamic",
            key="editor_registro_attivita",
            hide_index=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("💾 SALVA MODIFICHE REGISTRO"):
            try:
                data_to_write = edited_df.values.tolist()
                creds = ottieni_credenziali()
                if creds:
                    client = gspread.authorize(creds)
                    sheet = client.open_by_key(SHEET_ID)
                    target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(GID_ACADEMY).strip()), None)
                    if target_ws:
                        end_row = 28 + len(data_to_write) - 1
                        target_ws.update(f"C28:E{end_row}", data_to_write)
                        
                        # Mostra il popup di successo (toast e messaggio a schermo)
                        st.toast("✅ Modifiche effettuate con successo!", icon="🎉")
                        st.success("Modifiche salvate con successo su Google Sheet (C28:E50)!")
                        
                        time.sleep(1)
                        st.rerun()
            except Exception as ex:
                st.error(f"Errore durante il salvataggio: {ex}")

        st.markdown("<br>", unsafe_allow_html=True)

    elif current == "📋 ANAGRAFICA":
        st.subheader("📋 Anagrafica")

    elif current == "📈 PROGRESSI":
        st.subheader("📈 Progressi")

    elif current == "📜 CERTIFICAZIONI ESERCIZI":
        st.subheader("📜 Certificazioni")

    elif current == "👤 SCHEDE GIOCATORE":
        st.subheader("👤 Schede Giocatore")

        if "selected_player" not in st.session_state:
            st.session_state.selected_player = PLAYERS[0]

        for player_name in PLAYERS:
            btn_type = "primary" if st.session_state.selected_player == player_name else "secondary"
            if st.button(player_name, key=f"btn_p_{player_name}", type=btn_type):
                st.session_state.selected_player = player_name
                st.rerun()

        st.markdown("---")
        st.write(f"Giocatore selezionato: **{st.session_state.selected_player}**")

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

        if st.session_state.stat_tab == "🏋️ TRAINING":
            st.write("Vista selezionata: **TRAINING**")

        elif st.session_state.stat_tab == "🏆 STATCOMP":
            st.markdown("<div style='background-color: #0e1117; border: 2px solid #262730; border-radius: 12px; padding: 15px;'>", unsafe_allow_html=True)
            st.markdown("### 👤 Personal Stats Dashboard")

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
