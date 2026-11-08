import os
import streamlit as st
import pandas as pd

# ==============================================================================
# SEITENKONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Was wählen Kraniche? · Der Salzgitter Wahl-O-Mat",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# GEGEBENE DATEN (ORIGINAL & VOLLSTÄNDIG UNVERÄNDERT)
# ==============================================================================
PARTEIEN = ["Die Grünen", "Die Linke", "SPD", "FDP", "CDU", "AfD"]

NAMEN = {
    "Die Grünen": "Grünen-Kranich",
    "Die Linke": "Linken-Kranich",
    "SPD": "SPD-Kranich",
    "FDP": "FDP-Kranich",
    "CDU": "CDU-Kranich",
    "AfD": "AfD-Kranich"
}

THESEN = [
    {
        "text": "Die Busse und Bahnen der KVG Salzgitter sollten für alle Schülerinnen und Schüler komplett kostenlos sein.",
        "positionen": [1, 1, 1, -1, -1, 0]
    },
    {
        "text": "Salzgitter sollte mehr Geld in freies WLAN an Schulen und öffentlichen Plätzen investieren, statt zuerst Schulgebäude zu sanieren.",
        "positionen": [1, -1, -1, 1, -1, 1]
    },
    {
        "text": "An Schulen sollte es ein generelles Handyverbot auf dem gesamten Gelände geben, auch in den Pausen.",
        "positionen": [-1, -1, 0, -1, 1, 1]
    },
    {
        "text": "Die Stadt sollte mehr Treffpunkte für Jugendliche schaffen, auch wenn dafür weniger Geld für Straßen zur Verfügung steht.",
        "positionen": [1, 1, 1, 0, -1, -1]
    },
    {
        "text": "Das Jugendparlament sollte echtes Stimmrecht im Stadtrat erhalten.",
        "positionen": [1, 1, 1, 1, -1, -1]
    },
    {
        "text": "Grillen und laute Musik sollten am Salzgittersee und in Parks stärker eingeschränkt werden.",
        "positionen": [0, -1, -1, -1, 1, 1]
    },
    {
        "text": "Die Stadt sollte Jugendpartys, Festivals oder eine Disco für Jugendliche finanziell unterstützen.",
        "positionen": [1, 1, 1, 0, 0, -1]
    },
    {
        "text": "An Schulkiosken und in Mensen sollte ausschließlich gesundes oder vegetarisches Essen verkauft werden dürfen.",
        "positionen": [1, 1, 0, -1, -1, -1]
    },
    {
        "text": "An Kriminalitätsschwerpunkten sollte es mehr Kameras und Videoüberwachung geben.",
        "positionen": [-1, -1, 1, 1, 1, 1]
    },
    {
        "text": "Salzgitter sollte mehr Fahrradstraßen bauen, auf denen Autos eingeschränkt sind.",
        "positionen": [1, 1, 1, -1, -1, -1]
    },
    {
        "text": "Die Stadt sollte Sportvereine so unterstützen, dass Kinder und Jugendliche kostenlos Mitglied werden können.",
        "positionen": [1, 1, 1, 0, 0, -1]
    },
    {
        "text": "Schulen sollten im Unterricht mehr über Klimaschutz und umweltfreundliches Leben behandeln.",
        "positionen": [1, 1, 1, -1, -1, -1]
    }
]

ANTWORTEN = {
    "Ich stimme zu": 1,
    "keine Angabe": 0,
    "Ich lehne ab": -1
}

# Thematische Kategorien (rein optische Kennzeichnung zur schnellen Orientierung)
KATEGORIEN = [
    "Nahverkehr & Mobilität",
    "Digitalisierung & Schule",
    "Schulordnung & Medien",
    "Treffpunkte & Jugend",
    "Jugendbeteiligung & Stadtrat",
    "Freizeit & Salzgittersee",
    "Jugendkultur & Events",
    "Ernährung & Schulkiosk",
    "Sicherheit & Ordnung",
    "Radverkehr & Verkehrswende",
    "Sport & Vereinsleben",
    "Umwelt & Klimaschutz"
]

PARTEI_FARBEN = {
    "Die Grünen": "#15803d",
    "Die Linke": "#a21caf",
    "SPD": "#dc2626",
    "FDP": "#ca8a04",
    "CDU": "#1e293b",
    "AfD": "#0284c7"
}

# ==============================================================================
# BENUTZERDEFINIERTES DESIGN & CSS
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Hauptcontainer */
    .block-container {
        max-width: 800px !important;
        padding-top: 2.8rem !important;
        padding-bottom: 4rem !important;
    }
    
    /* Kopfzeilen-Badge */
    .app-header {
        text-align: center;
        margin-top: 0.5rem;
        margin-bottom: 1.8rem;
    }
    .header-badge {
        display: inline-block;
        padding: 0.35rem 0.95rem;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        color: #1d4ed8;
        font-weight: 700;
        font-size: 0.82rem;
        border-radius: 9999px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border: 1px solid #bfdbfe;
        margin-bottom: 0.6rem;
    }
    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        letter-spacing: -0.025em;
        line-height: 1.2;
    }
    .app-subtitle {
        font-size: 1.05rem;
        color: #64748b;
        margin-top: 0.35rem;
    }

    /* Bilder im Intro */
    .stImage img {
        border-radius: 16px !important;
        box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.08) !important;
    }

    /* Intro-Stepper */
    .intro-stepper {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #f8fafc;
        padding: 0.65rem 1.1rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.2rem;
        font-size: 0.88rem;
        font-weight: 600;
        color: #475569;
    }

    /* Thesen-Karte */
    .these-wrapper {
        background: white;
        border-radius: 20px;
        padding: 2rem 1.8rem;
        box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.08);
        border: 1px solid #e2e8f0;
        margin: 1.2rem 0 1.5rem 0;
        position: relative;
    }
    .these-category {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: #f1f5f9;
        color: #334155;
        font-size: 0.82rem;
        font-weight: 700;
        border-radius: 8px;
        margin-bottom: 0.9rem;
        letter-spacing: 0.02em;
    }
    .these-text {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.45;
        margin: 0;
    }
    .gewicht-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
        padding: 0.28rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-top: 1rem;
    }

    /* Navigations-Pills für Thesen 1-12 */
    div[class*="st-key-nav_jump_"] button {
        padding: 0.3rem 0.1rem !important;
        min-height: 38px !important;
        height: 38px !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        white-space: nowrap !important;
        letter-spacing: -0.04em !important;
        border-radius: 10px !important;
    }

    /* Farbige Antworten-Buttons */
    /* 1. Zustimmen */
    div[class*="st-key-btn_agree_unsel"] button {
        border: 2px solid #22c55e !important;
        color: #15803d !important;
        background-color: #f0fdf4 !important;
        font-weight: 700 !important;
    }
    div[class*="st-key-btn_agree_unsel"] button:hover {
        background-color: #dcfce7 !important;
        border-color: #16a34a !important;
    }
    div[class*="st-key-btn_agree_sel"] button {
        background-color: #16a34a !important;
        color: white !important;
        border: 2px solid #15803d !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.3) !important;
    }

    /* 2. Neutral / keine Angabe */
    div[class*="st-key-btn_neutral_unsel"] button {
        border: 2px solid #94a3b8 !important;
        color: #475569 !important;
        background-color: #f8fafc !important;
        font-weight: 700 !important;
    }
    div[class*="st-key-btn_neutral_unsel"] button:hover {
        background-color: #f1f5f9 !important;
        border-color: #64748b !important;
    }
    div[class*="st-key-btn_neutral_sel"] button {
        background-color: #64748b !important;
        color: white !important;
        border: 2px solid #475569 !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 12px rgba(100, 116, 139, 0.3) !important;
    }

    /* 3. Ablehnen */
    div[class*="st-key-btn_disagree_unsel"] button {
        border: 2px solid #ef4444 !important;
        color: #b91c1c !important;
        background-color: #fef2f2 !important;
        font-weight: 700 !important;
    }
    div[class*="st-key-btn_disagree_unsel"] button:hover {
        background-color: #fee2e2 !important;
        border-color: #dc2626 !important;
    }
    div[class*="st-key-btn_disagree_sel"] button {
        background-color: #dc2626 !important;
        color: white !important;
        border: 2px solid #b91c1c !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3) !important;
    }

    /* Ergebnis-Hero */
    .hero-result-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 60%, #3b82f6 100%);
        color: white;
        border-radius: 20px;
        padding: 2.2rem 1.8rem;
        text-align: center;
        box-shadow: 0 15px 35px -5px rgba(37, 99, 235, 0.35);
        margin-bottom: 2rem;
    }
    .hero-badge {
        display: inline-block;
        padding: 0.35rem 0.95rem;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    .hero-name {
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0.2rem 0;
        line-height: 1.15;
    }
    .hero-percent {
        font-size: 3.8rem;
        font-weight: 900;
        line-height: 1;
        margin: 0.5rem 0;
        color: #fde047;
    }
    .party-result-row {
        background: white;
        border-radius: 16px;
        padding: 1.15rem 1.4rem;
        margin-bottom: 0.9rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        transition: transform 0.15s ease;
    }
    .party-result-row:hover {
        transform: translateX(4px);
        border-color: #cbd5e1;
    }

    /* Detailkarten */
    .detail-card {
        background: white;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.9rem;
        border-left: 5px solid #cbd5e1;
        border-top: 1px solid #f1f5f9;
        border-right: 1px solid #f1f5f9;
        border-bottom: 1px solid #f1f5f9;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    .status-badge {
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-agree { background: #dcfce7; color: #15803d; }
    .badge-neutral { background: #f1f5f9; color: #475569; }
    .badge-disagree { background: #fee2e2; color: #dc2626; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SESSION STATE INITIALISIERUNG
# ==============================================================================
if "intro_schritt" not in st.session_state:
    st.session_state.intro_schritt = 0
if "frage" not in st.session_state:
    st.session_state.frage = 0
if "antworten" not in st.session_state:
    st.session_state.antworten = {}
if "gewichtung" not in st.session_state:
    st.session_state.gewichtung = {}
if "fertig" not in st.session_state:
    st.session_state.fertig = False
if "balloons_gezeigt" not in st.session_state:
    st.session_state.balloons_gezeigt = False

# ==============================================================================
# HILFSFUNKTIONEN
# ==============================================================================
def lade_bild_sicher(dateiname_ohne_endung):
    """Lädt das lokale Bild mit verschiedenen Dateiendungen ohne Fehler."""
    endungen = [".jpeg", ".JPEG", ".jpg", ".JPG", ".png", ".PNG"]
    for endung in endungen:
        pfad = f"{dateiname_ohne_endung}{endung}"
        if os.path.exists(pfad):
            try:
                st.image(pfad, width="stretch")
            except Exception:
                st.image(pfad, use_container_width=True)
            return True
    st.warning(f"Bild '{dateiname_ohne_endung}' wurde im Projektverzeichnis nicht gefunden.")
    return False

def quiz_neustarten():
    """Setzt alle Auswahlen und Schritte vollständig zurück."""
    st.session_state.intro_schritt = 0
    st.session_state.frage = 0
    st.session_state.antworten = {}
    st.session_state.gewichtung = {}
    st.session_state.fertig = False
    st.session_state.balloons_gezeigt = False
    st.rerun()

def berechne_ergebnisse():
    """
    Berechnet die Übereinstimmung mit den Parteien.
    Wahl-O-Mat Algorithmus mit optionaler Thesen-Gewichtung (2x).
    """
    ergebnisse = []
    
    # Berechne maximale erreichbare Punkte unter Berücksichtigung der Gewichtung
    max_punkte = 0
    for frage_index in range(len(THESEN)):
        ist_doppelt = st.session_state.gewichtung.get(frage_index, False)
        gewicht = 2 if ist_doppelt else 1
        max_punkte += (2 * gewicht)

    for partei_index, partei in enumerate(PARTEIEN):
        punkte = 0
        for frage_index, these in enumerate(THESEN):
            deine_antwort = st.session_state.antworten.get(frage_index, 0)
            partei_antwort = these["positionen"][partei_index]
            ist_doppelt = st.session_state.gewichtung.get(frage_index, False)
            gewicht = 2 if ist_doppelt else 1
            
            diff = abs(deine_antwort - partei_antwort)
            if diff == 0:
                punkte += (2 * gewicht)
            elif diff == 1:
                punkte += (1 * gewicht)
            # diff == 2 ergibt 0 Punkte

        prozent = (punkte / max_punkte * 100) if max_punkte > 0 else 0
        ergebnisse.append({
            "partei": partei,
            "name": NAMEN[partei],
            "prozent": prozent,
            "punkte": punkte,
            "max_punkte": max_punkte,
            "farbe": PARTEI_FARBEN[partei]
        })

    ergebnisse.sort(key=lambda x: x["prozent"], reverse=True)
    return ergebnisse

# ==============================================================================
# KOPFZEILE / LOGO
# ==============================================================================
st.markdown("""
<div class="app-header">
    <span class="header-badge"> Salzgitter · Jugend & Schule</span>
    <h1 class="app-title">Was wählen Kraniche?</h1>
    <p class="app-subtitle">Finde heraus, welcher Kranich deine Meinungen vertritt!</p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# ANSICHT: INTERAKTIVES INTRO (SCHRITTE 0 BIS 5)
# ==============================================================================
if st.session_state.intro_schritt < 6 and not st.session_state.fertig:
    schritt = st.session_state.intro_schritt
    gesamt_schritte = 6
    
    # Stepper & Fortschritt
    step_titles = [
        "1. Willkommen im Schwarm",
        "2. Briefkasten",
        "3. Eine neue Nachricht",
        "4. Versiegelter Brief",
        "5. Deine Einladung",
        "6. Startaufstellung"
    ]
    
    st.markdown(f"""
    <div class="intro-stepper">
        <span> Einführung: {step_titles[schritt]}</span>
        <span>Schritt {schritt + 1} von {gesamt_schritte}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress((schritt + 1) / gesamt_schritte)
    
    # Medienanzeige pro Schritt
    if schritt == 0:
        lade_bild_sicher("banner")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        lade_bild_sicher("crowd")
    elif schritt == 1:
        lade_bild_sicher("intro_text")
    elif schritt == 2:
        lade_bild_sicher("brief_hinweis")
    elif schritt == 3:
        lade_bild_sicher("brief_zu")
    elif schritt == 4:
        lade_bild_sicher("brief_offen")
    elif schritt == 5:
        lade_bild_sicher("start_seite")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Aktions-Buttons
    col_zurueck, col_weiter, col_skip = st.columns([1, 2, 1.2])
    
    with col_zurueck:
        if schritt > 0:
            if st.button("← Zurück", key=f"intro_prev_{schritt}", use_container_width=True):
                st.session_state.intro_schritt -= 1
                st.rerun()
                
    with col_weiter:
        labels = [
            "Weiter ➔",
            "Weiter ➔",
            "Postkasten öffnen",
            "Siegel brechen & öffnen",
            "Brief schließen & Weiter",
            "JETZT QUIZ STARTEN"
        ]
        if st.button(labels[schritt], key=f"intro_next_{schritt}", type="primary", use_container_width=True):
            st.session_state.intro_schritt += 1
            st.rerun()

    with col_skip:
        if st.button("Direkt zum Quiz", key=f"intro_skip_{schritt}", use_container_width=True):
            st.session_state.intro_schritt = 6
            st.rerun()

# ==============================================================================
# ANSICHT: DAS QUIZ (SCHRITT 6)
# ==============================================================================
elif st.session_state.intro_schritt == 6 and not st.session_state.fertig:
    aktuelle_frage = st.session_state.frage
    these = THESEN[aktuelle_frage]
    kategorie = KATEGORIEN[aktuelle_frage]
    ist_doppelt = st.session_state.gewichtung.get(aktuelle_frage, False)
    aktuelle_auswahl = st.session_state.antworten.get(aktuelle_frage, None)
    
    # Fortschrittsbalken oben
    beantwortete_anzahl = len(st.session_state.antworten)
    fortschritt_wert = (aktuelle_frage + 1) / len(THESEN)
    
    col_info, col_counter = st.columns([2, 1])
    with col_info:
        st.markdown(f"**These {aktuelle_frage + 1} von {len(THESEN)}**")
    with col_counter:
        st.markdown(f"<div style='text-align: right; color: #64748b; font-size: 0.9rem;'>Beantwortet: {beantwortete_anzahl}/{len(THESEN)}</div>", unsafe_allow_html=True)
        
    st.progress(fortschritt_wert)
    
    # Interaktive Thesen-Navigationsleiste (Schnellspringer 1 bis 12)
    nav_cols = st.columns(12)
    for idx in range(12):
        with nav_cols[idx]:
            hat_antwort = idx in st.session_state.antworten
            ist_aktiv = idx == aktuelle_frage
            hat_stern = st.session_state.gewichtung.get(idx, False)
            
            btn_label = f"{idx + 1}{'★' if hat_stern else ''}"
            btn_type = "primary" if ist_aktiv else "secondary"
            
            if st.button(btn_label, key=f"nav_jump_{idx}", type=btn_type, use_container_width=True):
                st.session_state.frage = idx
                st.rerun()

    # Thesen-Karte
    st.markdown(f"""
    <div class="these-wrapper">
        <span class="these-category">{kategorie}</span>
        <h2 class="these-text">{these["text"]}</h2>
        {f'<div class="gewicht-badge">★ Doppelt gewichtet (zählt 2x)</div>' if ist_doppelt else ''}
    </div>
    """, unsafe_allow_html=True)

    # Thesen-Gewichtung (Toggle rechtsbündig)
    col_gew1, col_gew2 = st.columns([2.2, 1.8])
    with col_gew2:
        neue_gewichtung = st.toggle("Diese These doppelt werten", value=ist_doppelt, key=f"toggle_weight_{aktuelle_frage}")
        if neue_gewichtung != ist_doppelt:
            st.session_state.gewichtung[aktuelle_frage] = neue_gewichtung
            st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 3 Hauptantwort-Buttons (Farblich hervorgehoben)
    b1, b2, b3 = st.columns(3)
    
    with b1:
        is_sel = (aktuelle_auswahl == 1)
        btn_key = f"btn_agree_{'sel' if is_sel else 'unsel'}_{aktuelle_frage}"
        label_agree = "Ich stimme zu" if is_sel else "Ich stimme zu"
        if st.button(label_agree, key=btn_key, use_container_width=True):
            st.session_state.antworten[aktuelle_frage] = 1
            if aktuelle_frage < len(THESEN) - 1:
                st.session_state.frage += 1
            else:
                st.session_state.fertig = True
            st.rerun()

    with b2:
        is_sel = (aktuelle_auswahl == 0)
        btn_key = f"btn_neutral_{'sel' if is_sel else 'unsel'}_{aktuelle_frage}"
        label_neutral = "keine Angabe" if is_sel else "keine Angabe"
        if st.button(label_neutral, key=btn_key, use_container_width=True):
            st.session_state.antworten[aktuelle_frage] = 0
            if aktuelle_frage < len(THESEN) - 1:
                st.session_state.frage += 1
            else:
                st.session_state.fertig = True
            st.rerun()

    with b3:
        is_sel = (aktuelle_auswahl == -1)
        btn_key = f"btn_disagree_{'sel' if is_sel else 'unsel'}_{aktuelle_frage}"
        label_disagree = "Ich lehne ab" if is_sel else "Ich lehne ab"
        if st.button(label_disagree, key=btn_key, use_container_width=True):
            st.session_state.antworten[aktuelle_frage] = -1
            if aktuelle_frage < len(THESEN) - 1:
                st.session_state.frage += 1
            else:
                st.session_state.fertig = True
            st.rerun()

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    st.divider()

    # Untere Navigationsleiste
    c_prev, c_skip, c_eval = st.columns([1, 1, 1.2])
    
    with c_prev:
        if aktuelle_frage > 0:
            if st.button("← Vorherige These", key=f"quiz_prev_{aktuelle_frage}", use_container_width=True):
                st.session_state.frage -= 1
                st.rerun()

    with c_skip:
        if aktuelle_frage < len(THESEN) - 1:
            if st.button("Überspringen ➔", key=f"quiz_skip_{aktuelle_frage}", use_container_width=True):
                st.session_state.frage += 1
                st.rerun()

    with c_eval:
        if len(st.session_state.antworten) > 0:
            btn_txt = "Ergebnis auswerten" if aktuelle_frage == len(THESEN) - 1 else "Vorzeitig auswerten"
            if st.button(btn_txt, key="quiz_finish_now", type="primary", use_container_width=True):
                st.session_state.fertig = True
                st.rerun()

# ==============================================================================
# ANSICHT: DAS ERGEBNIS
# ==============================================================================
else:
    ergebnisse = berechne_ergebnisse()
    top_partei = ergebnisse[0]
    
    # Feier-Balloons beim ersten Anzeigen
    if not st.session_state.balloons_gezeigt:
        st.balloons()
        st.session_state.balloons_gezeigt = True

    # Hero-Banner für den Spitzenreiter
    st.markdown(f"""
    <div class="hero-result-card">
        <span class="hero-badge">Dein politischer Schwarm-Spitzenreiter</span>
        <div class="hero-percent">{top_partei['prozent']:.1f} %</div>
        <h2 class="hero-name">{top_partei['name']}</h2>
        <div style="font-size: 1.15rem; opacity: 0.95; font-weight: 600;">{top_partei['partei']}</div>
        <p style="margin-top: 0.8rem; font-size: 0.95rem; opacity: 0.9; max-width: 500px; margin-left: auto; margin-right: auto;">
            Mit diesem Kranich stimmen deine Positionen in Salzgitter am stärksten überein!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Interaktive Tabs
    tab_ranking, tab_detail, tab_anpassen = st.tabs([
        "Rangliste aller Kraniche",
        "Detaillierter Thesenvergleich",
        "Antworten & Gewichtung anpassen"
    ])

    # --------------------------------------------------------------------------
    # TAB 1: RANGLISTE ALLER PARTEIEN
    # --------------------------------------------------------------------------
    with tab_ranking:
        st.subheader("Übersicht aller Ergebnisse")
        
        for index, item in enumerate(ergebnisse, start=1):
            medaille = "" if index == 1 else ("" if index == 2 else ("" if index == 3 else f"#{index}"))
            
            st.markdown(f"""
            <div class="party-result-row">
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.4rem;">
                    <div>
                        <span style="font-size: 1.15rem; font-weight: 800; margin-right: 0.5rem;">{medaille}</span>
                        <strong style="font-size: 1.15rem; color: #0f172a;">{item['name']}</strong>
                        <span style="color: #64748b; font-size: 0.95rem; margin-left: 0.35rem;">({item['partei']})</span>
                    </div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: {item['farbe']};">
                        {item['prozent']:.1f} %
                    </div>
                </div>
                <div style="background: #e2e8f0; height: 12px; border-radius: 9999px; overflow: hidden; margin: 0.5rem 0;">
                    <div style="background: {item['farbe']}; height: 100%; width: {item['prozent']}%; border-radius: 9999px; transition: width 0.6s ease;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; color: #64748b; margin-top: 0.3rem;">
                    <span>Erreichte Punktzahl: <strong>{item['punkte']}</strong> von {item['max_punkte']} möglichen Punkten</span>
                    <span>Übereinstimmungsgrad</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        # Diagramm zur visuellen Gegenüberstellung
        df_chart = pd.DataFrame({
            "Kranich-Mascot": [f"{e['name']} ({e['partei']})" for e in ergebnisse],
            "Übereinstimmung in %": [e['prozent'] for e in ergebnisse]
        }).set_index("Kranich-Mascot")
        
        st.bar_chart(df_chart)

    # --------------------------------------------------------------------------
    # TAB 2: DETAILVERGLEICH
    # --------------------------------------------------------------------------
    with tab_detail:
        st.subheader("Vergleich deiner Positionen mit den Parteien")
        st.write("Wähle einen Kranich aus, um jede These Punkt für Punkt zu vergleichen:")
        
        vergleich_partei = st.selectbox(
            "Partei zum Vergleich auswählen:",
            options=PARTEIEN,
            format_func=lambda p: f"{NAMEN[p]} ({p})",
            key="select_detail_party"
        )
        
        partei_idx = PARTEIEN.index(vergleich_partei)
        
        text_werte = {1: "Zustimmung", 0: "Keine Angabe", -1: "Ablehnung"}
        badge_class = {1: "badge-agree", 0: "badge-neutral", -1: "badge-disagree"}
        
        for f_idx, these in enumerate(THESEN):
            user_val = st.session_state.antworten.get(f_idx, 0)
            party_val = these["positionen"][partei_idx]
            ist_gew = st.session_state.gewichtung.get(f_idx, False)
            
            diff = abs(user_val - party_val)
            if diff == 0:
                match_txt = "Volle Übereinstimmung (+2 Pkt)"
                card_border = "#15803d"
            elif diff == 1:
                match_txt = "Teilweise Übereinstimmung (+1 Pkt)"
                card_border = "#eab308"
            else:
                match_txt = "Keine Übereinstimmung (0 Pkt)"
                card_border = "#dc2626"
                
            st.markdown(f"""
            <div class="detail-card" style="border-left-color: {card_border};">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b; margin-bottom: 0.3rem;">
                    <span>These {f_idx + 1} · {KATEGORIEN[f_idx]}</span>
                    <span>{match_txt} {('· <strong>2x gewichtet</strong>' if ist_gew else '')}</span>
                </div>
                <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.6rem; font-size: 0.98rem;">
                    {these['text']}
                </div>
                <div style="display: flex; gap: 1rem; font-size: 0.88rem;">
                    <div>Deine Meinung: <span class="status-badge {badge_class[user_val]}">{text_werte[user_val]}</span></div>
                    <div>{NAMEN[vergleich_partei]}: <span class="status-badge {badge_class[party_val]}">{text_werte[party_val]}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # TAB 3: ANTWORTEN ANPASSEN
    # --------------------------------------------------------------------------
    with tab_anpassen:
        st.subheader("Deine Antworten überprüfen & anpassen")
        st.write("Du kannst hier Antworten oder Gewichtungen direkt ändern und das Ergebnis neu berechnen lassen:")
        
        for f_idx, these in enumerate(THESEN):
            with st.expander(f"These {f_idx + 1}: {these['text'][:55]}..."):
                st.write(f"**Vollständige These:** {these['text']}")
                c_opt1, c_opt2 = st.columns([2, 1])
                
                with c_opt1:
                    aktuelle = st.session_state.antworten.get(f_idx, 0)
                    options = [1, 0, -1]
                    labels_map = {1: "Ich stimme zu", 0: "keine Angabe", -1: "Ich lehne ab"}
                    
                    neue_auswahl = st.radio(
                        "Deine Position:",
                        options=options,
                        format_func=lambda x: labels_map[x],
                        index=options.index(aktuelle),
                        key=f"edit_ans_{f_idx}"
                    )
                    st.session_state.antworten[f_idx] = neue_auswahl

                with c_opt2:
                    war_gew = st.session_state.gewichtung.get(f_idx, False)
                    neue_gew = st.checkbox("2x Gewichtung", value=war_gew, key=f"edit_weight_{f_idx}")
                    st.session_state.gewichtung[f_idx] = neue_gew

        if st.button("Ergebnisse sofort neu berechnen 🔄", key="recalc_results_btn", type="primary", use_container_width=True):
            st.rerun()

    # --------------------------------------------------------------------------
    # ABSCHLIESSENDE AKTIONEN
    # --------------------------------------------------------------------------
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.divider()
    
    col_restart, col_share = st.columns([1, 1])
    
    with col_restart:
        st.button("Quiz erneut starten", on_click=quiz_neustarten, use_container_width=True)
        
    with col_share:
        # Generiere Text-Zusammenfassung zum Teilen
        zusammenfassung = "Mein Ergebnis beim Kranich-Wahlomat Salzgitter:\n"
        for i, item in enumerate(ergebnisse, 1):
            zusammenfassung += f"{i}. {item['name']} ({item['partei']}): {item['prozent']:.1f}%\n"
            
        with st.popover("Ergebnis teilen / Text kopieren", use_container_width=True):
            st.write("Kopiere dein Ergebnis einfach für WhatsApp, Instagram oder Discord:")
            st.code(zusammenfassung, language="text")
