import os
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Was wählen Kraniche? - Salzgitter Wahl-O-Mat", layout="centered")

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
    {"text": "Die Busse und Bahnen der KVG Salzgitter sollten für alle Schülerinnen und Schüler komplett kostenlos sein.", "positionen": [1, 1, 1, -1, -1, 0]},
    {"text": "Salzgitter sollte mehr Geld in freies WLAN an Schulen und öffentlichen Plätzen investieren, statt zuerst Schulgebäude zu sanieren.", "positionen": [-1, -1, 1, 1, -1, 1]},
    {"text": "An Schulen sollte es ein generelles Handyverbot auf dem gesamten Gelände geben, auch in den Pausen.", "positionen": [-1, -1, 0, -1, 1, 1]},
    {"text": "Die Stadt sollte mehr Treffpunkte für Jugendliche schaffen, auch wenn dafür weniger Geld für Straßen zur Verfügung steht.", "positionen": [1, 1, 1, 0, -1, -1]},
    {"text": "Das Jugendparlament sollte echtes Stimmrecht im Stadtrat erhalten.", "positionen": [1, 1, 1, 1, -1, -1]},
    {"text": "Grillen und laute Musik sollten am Salzgittersee und in Parks stärker eingeschränkt werden.", "positionen": [0, -1, -1, -1, 1, 1]},
    {"text": "Die Stadt sollte Jugendpartys, Festivals oder eine Disco für Jugendliche finanziell unterstützen.", "positionen": [1, 1, 1, 0, 0, -1]},
    {"text": "An Schulkiosken und in Mensen sollte ausschließlich gesundes oder vegetarisches Essen verkauft werden dürfen.", "positionen": [1, 1, 0, -1, -1, -1]},
    {"text": "An Kriminalitätsschwerpunkten sollte es mehr Kameras und Videoüberwachung geben.", "positionen": [-1, -1, 1, 1, 1, 1]},
    {"text": "Salzgitter sollte mehr Fahrradstraßen bauen, auf denen Autos eingeschränkt sind.", "positionen": [1, 1, 1, -1, -1, -1]},
    {"text": "Die Stadt sollte Sportvereine so unterstützen, dass Kinder und Jugendliche kostenlos Mitglied werden können.", "positionen": [1, 1, 1, 0, 0, -1]},
    {"text": "Schulen sollten im Unterricht mehr über Klimaschutz und umweltfreundliches Leben behandeln.", "positionen": [1, 1, 1, -1, -1, -1]}
]

FARBEN = {
    "Die Grünen": "#15803d", "Die Linke": "#a21caf", "SPD": "#dc2626",
    "FDP": "#ca8a04", "CDU": "#1e293b", "AfD": "#0284c7"
}

st.markdown("""
<style>
    * { font-family: Arial, Helvetica, sans-serif !important; }
    html, body, [class*="css"], .stMarkdown, p, div, button, h1, h2, h3, span, input, label { 
        font-family: Arial, Helvetica, sans-serif !important; 
    }
    /* Streamlit-Anker-Icons vollständig ausblenden */
    [data-testid="stHeaderActionElements"], .header-anchor, a.anchor-link, [aria-label*="link to heading"], [aria-label*="Direct link"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    .block-container { max-width: 800px !important; padding-top: 3.8rem !important; }
    .header-box { text-align: center; margin-top: 0.5rem; margin-bottom: 1.5rem; }
    .header-badge { display: inline-block; padding: 0.25rem 0.8rem; background: #fef3c7; color: #92400e; font-weight: 700; font-size: 0.78rem; border-radius: 9999px; text-transform: uppercase; margin-bottom: 0.5rem; }
    .these-card { 
        background: white; 
        border-radius: 16px; 
        padding: 1.8rem 2.2rem; 
        border: 1px solid #e2e8f0; 
        box-shadow: 0 4px 16px rgba(0,0,0,0.05); 
        margin: 1.2rem 0 1rem 0; 
        height: 195px; 
        min-height: 195px; 
        max-height: 195px; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        text-align: center; 
        overflow: hidden; 
        box-sizing: border-box;
    }
    .these-title { 
        font-size: 1.32rem; 
        font-weight: 700; 
        color: #0f172a; 
        line-height: 1.45; 
        margin: 0; 
        text-align: center; 
    }
    .hero-card { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: white; border-radius: 18px; padding: 2rem; text-align: center; margin-bottom: 1.8rem; }
    .hero-pct { font-size: 3.5rem; font-weight: 900; color: #facc15; margin: 0.3rem 0; }
    .party-card { background: white; border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.75rem; border: 1px solid #e2e8f0; }
    .detail-row { background: white; border-radius: 10px; padding: 0.9rem 1.1rem; margin-bottom: 0.75rem; border-left: 4px solid #cbd5e1; border-top: 1px solid #f1f5f9; border-right: 1px solid #f1f5f9; border-bottom: 1px solid #f1f5f9; }
    div[class*="st-key-nav_"] button { padding: 0.2rem !important; height: 36px !important; font-size: 0.8rem !important; font-weight: 700 !important; }
    div[class*="st-key-btn_agree"] button { border: 2px solid #16a34a !important; color: #15803d !important; font-weight: 700 !important; }
    div[class*="st-key-btn_neutral"] button { border: 2px solid #94a3b8 !important; color: #475569 !important; font-weight: 700 !important; }
    div[class*="st-key-btn_disagree"] button { border: 2px solid #dc2626 !important; color: #b91c1c !important; font-weight: 700 !important; }
    div[class*="st-key-btn_agree_sel"] button { background: #16a34a !important; color: white !important; }
    div[class*="st-key-btn_neutral_sel"] button { background: #64748b !important; color: white !important; }
    div[class*="st-key-btn_disagree_sel"] button { background: #dc2626 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

if "intro" not in st.session_state: st.session_state.intro = 0
if "frage" not in st.session_state: st.session_state.frage = 0
if "antworten" not in st.session_state: st.session_state.antworten = {}
if "gewichtung" not in st.session_state: st.session_state.gewichtung = {}
if "fertig" not in st.session_state: st.session_state.fertig = False

def zeige_bild(nummer):
    pfade = [f"Template/{nummer}.png", f"Template/{nummer}.jpeg", f"Template/{nummer}.jpg"]
    for p in pfade:
        if os.path.exists(p):
            try: st.image(p, width="stretch")
            except Exception: st.image(p, use_container_width=True)
            return True
    return False

def quiz_reset():
    st.session_state.intro = 0
    st.session_state.frage = 0
    st.session_state.antworten = {}
    st.session_state.gewichtung = {}
    st.session_state.fertig = False
    st.rerun()

def berechne_score():
    max_pts = sum(2 * (2 if st.session_state.gewichtung.get(i, False) else 1) for i in range(len(THESEN)))
    res = []
    for p_idx, p in enumerate(PARTEIEN):
        pts = 0
        for f_idx, t in enumerate(THESEN):
            gew = 2 if st.session_state.gewichtung.get(f_idx, False) else 1
            diff = abs(st.session_state.antworten.get(f_idx, 0) - t["positionen"][p_idx])
            if diff == 0: pts += 2 * gew
            elif diff == 1: pts += 1 * gew
        res.append({
            "partei": p, "name": NAMEN[p], "punkte": pts, "max": max_pts,
            "prozent": (pts / max_pts * 100) if max_pts > 0 else 0, "farbe": FARBEN[p]
        })
    res.sort(key=lambda x: x["prozent"], reverse=True)
    return res

def zeige_footer():
    st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
    st.divider()
    with st.popover("Quellen und Hintergrundinformationen", use_container_width=True):
        st.markdown("""
        **Projekt:**  
        Kranich-Wahl-O-Mat (Projekt zur politischen Bildung am Kranich-Gymnasium Salzgitter).

     

Für die Einordnung der sechs Ratsfraktionen (Die Linke, Bündnis 90/Die Grünen, SPD, FDP, CDU und AfD) wurden vor allem die aktuellen **Kommunalwahlprogramme zur Wahl 2026 in Salzgitter** ausgewertet. Wo es auf kommunaler Ebene keine eigene Aussage gab, wurden Landes- und Bundesprogramme sowie bekannte Positionen aus dem Stadtrat herangezogen.

**Die wichtigsten Grundlagendokumente:**
* [Kommunalwahlprogramm 2026 – Die Linke Salzgitter (PDF)](https://die-linke-salzgitter.de/documents/Kommunalwahl_Programm-2026.pdf)
* [Kommunalwahlprogramm 2026 „Mach's Grün“ – Grüne Salzgitter (PDF)](https://gruene-salzgitter.de/wp-content/uploads/sites/102/2026/07/MACHS-GRUeN.pdf)
* [Kommunalwahlprogramm 2026 (Langfassung) – SPD Salzgitter (PDF)](https://www.spd-salzgitter.de/wp-content/uploads/sites/884/2026/07/SPD_Wahlprogramm_Langfassung.pdf) sowie [SPD-Programm 2021–2026 (PDF)](https://www.spd-salzgitter.de/wp-content/uploads/sites/884/2021/08/01_Kommunalwahlprogramm_SPD_Salzgitter_fertig.pdf)
* [Kommunalwahlprogramm 2026 „Stark für Salzgitter“ – CDU Salzgitter (PDF)](https://www.cdu-salzgitter.de/image/kopfgrafiken/CDU%20Wahlprogramm%202026.pdf)

---

**Belege zu den einzelnen Thesen:**

1. **Kostenlose Busse und Bahnen (KVG):**  
   Linke ([S. 14](https://die-linke-salzgitter.de/documents/Kommunalwahl_Programm-2026.pdf)), Grüne ([S. 7](https://gruene-salzgitter.de/wp-content/uploads/sites/102/2026/07/MACHS-GRUeN.pdf)) und SPD ([S. 8](https://www.spd-salzgitter.de/wp-content/uploads/sites/884/2026/07/SPD_Wahlprogramm_Langfassung.pdf)) setzen sich für kostenlosen ÖPNV bzw. freie Fahrt für Kinder und Jugendliche ein. Die CDU setzt stattdessen auf ein abgestimmtes Schulbuskonzept bei solider Haushaltslage ([S. 7, 9–10](https://www.cdu-salzgitter.de/image/kopfgrafiken/CDU%20Wahlprogramm%202026.pdf)).
2. **WLAN vs. Schulsanierung:**  
   Linke ([S. 11](https://die-linke-salzgitter.de/documents/Kommunalwahl_Programm-2026.pdf)), Grüne ([S. 13–14](https://gruene-salzgitter.de/wp-content/uploads/sites/102/2026/07/MACHS-GRUeN.pdf)) und CDU ([S. 7](https://www.cdu-salzgitter.de/image/kopfgrafiken/CDU%20Wahlprogramm%202026.pdf)) legen den Schwerpunkt klar auf die bauliche Sanierung der Schulgebäude. Die SPD ([S. 14](https://www.spd-salzgitter.de/wp-content/uploads/sites/884/2026/07/SPD_Wahlprogramm_Langfassung.pdf) / [Programm 2021, S. 9](https://www.spd-salzgitter.de/wp-content/uploads/sites/884/2021/08/01_Kommunalwahlprogramm_SPD_Salzgitter_fertig.pdf)) und die FDP (Landesprogramm Niedersachsen, Punkt 6) betonen stärker den Ausbau von kostenfreiem Schul-WLAN.
3. **Generelles Handyverbot an Schulen:**  
   Die AfD fordert auf Bundesebene ein generelles Mobiltelefonverbot an Schulen (Positionspapier der AfD-Bundestagsfraktion). Die Linke setzt dagegen auf Medienscouts und digitale Ausstattung ([S. 11–12](https://die-linke-salzgitter.de/documents/Kommunalwahl_Programm-2026.pdf)).
4. **Mehr Jugendtreffs statt Straßenbau:**  
   Linke ([S. 7](https://die-linke-salzgitter.de/documents/Kommunalwahl_Programm-2026.pdf)) und Grüne ([S. 15](https://gruene-salzgitter.de/wp-content/uploads/sites/102/2026/07/MACHS-GRUeN.pdf)) fordern eigene, selbstverwaltete Jugendräume und mehr Geld für Jugendzentren. Die SPD unterstützt ebenfalls die Weiterführung und den Ausbau der Jugendarbeit ([Programm 2021, S. 5](https://www.spd-salzgitter.de/wp-content/uploads/sites/884/2021/08/01_Kommunalwahlprogramm_SPD_Salzgitter_fertig.pdf)).
5. **Echtes Stimmrecht fürs Jugendparlament:**  
   Linke ([S. 7](https://die-linke-salzgitter.de/documents/Kommunalwahl_Programm-2026.pdf)), Grüne ([S. 15](https://gruene-salzgitter.de/wp-content/uploads/sites/102/2026/07/MACHS-GRUeN.pdf)) und SPD ([Programm 2021, S. 5](https://www.spd-salzgitter.de/wp-content/uploads/sites/884/2021/08/01_Kommunalwahlprogramm_SPD_Salzgitter_fertig.pdf)) wollen das Jugendparlament deutlich stärker an Entscheidungen im Stadtrat und in den Ausschüssen beteiligen.
6. **Grillen und Musik am Salzgittersee:**  
   Die SPD spricht sich im Programm gegen pauschale Verbote aus und will stattdessen zusätzliche legale Grillplätze am Salzgittersee schaffen ([S. 11](https://www.spd-salzgitter.de/wp-content/uploads/sites/884/2026/07/SPD_Wahlprogramm_Langfassung.pdf) / [Programm 2021, S. 8](https://www.spd-salzgitter.de/wp-content/uploads/sites/884/2021/08/01_Kommunalwahlprogramm_SPD_Salzgitter_fertig.pdf)).
7. **Zuschüsse für Jugendpartys und Festivals:**  
   Linke ([S. 7](https://die-linke-salzgitter.de/documents/Kommunalwahl_Programm-2026.pdf)) und Grüne ([S. 15](https://gruene-salzgitter.de/wp-content/uploads/sites/102/2026/07/MACHS-GRUeN.pdf)) machen sich für mehr Veranstaltungs- und Kulturräume für Jugendliche stark. Auch die SPD unterstützt Kultur- und Jugendveranstaltungen ([Programm 2021, S. 8 & 17](https://www.spd-salzgitter.de/wp-content/uploads/sites/884/2021/08/01_Kommunalwahlprogramm_SPD_Salzgitter_fertig.pdf)).
8. **Gesundes / vegetarisches Essen in Mensen:**  
   Die Grünen fordern im Ganztag ein gesundes Mittagessen für alle Schülerinnen und Schüler ([S. 14](https://gruene-salzgitter.de/wp-content/uploads/sites/102/2026/07/MACHS-GRUeN.pdf)), die Linke orientiert sich am Landesprogramm Niedersachsen (Punkt 2.2) für kostenfreie, gesunde Schulverpflegung.
9. **Mehr Videoüberwachung:**  
   CDU ([S. 10](https://www.cdu-salzgitter.de/image/kopfgrafiken/CDU%20Wahlprogramm%202026.pdf)), SPD ([S. 11](https://www.spd-salzgitter.de/wp-content/uploads/sites/884/2026/07/SPD_Wahlprogramm_Langfassung.pdf) / Initiative zur Videoüberwachung an Bahnhöfen) und FDP (Landtagswahlprogramm Niedersachsen) befürworten Kameras an Problemorten. Die Linke lehnt eine Ausweitung der Überwachung aus Gründen des Datenschutzes ab (Themenseite Digitalisierung).
10. **Mehr Fahrradstraßen:**  
    Linke ([S. 15](https://die-linke-salzgitter.de/documents/Kommunalwahl_Programm-2026.pdf)), Grüne ([S. 7–8](https://gruene-salzgitter.de/wp-content/uploads/sites/102/2026/07/MACHS-GRUeN.pdf)) und SPD ([S. 8](https://www.spd-salzgitter.de/wp-content/uploads/sites/884/2026/07/SPD_Wahlprogramm_Langfassung.pdf)) fordern den Ausbau des Radwegenetzes und geschützte Fahrradstraßen vor Schulen. Die CDU setzt stärker auf einen flüssigen Autoverkehr und die Pflege bestehender Wege ([S. 9](https://www.cdu-salzgitter.de/image/kopfgrafiken/CDU%20Wahlprogramm%202026.pdf)).
11. **Kostenlose Sportvereine für Kinder:**  
    Grüne ([S. 15 & 28](https://gruene-salzgitter.de/wp-content/uploads/sites/102/2026/07/MACHS-GRUeN.pdf)), SPD ([S. 15](https://www.spd-salzgitter.de/wp-content/uploads/sites/884/2026/07/SPD_Wahlprogramm_Langfassung.pdf)) und Linke (Landesprogramm Niedersachsen, Punkt 7.6) wollen Sportangebote und Vereinsmitgliedschaften für junge Menschen möglichst kostenfrei oder stark vergünstigt halten.
12. **Klimaschutz im Unterricht:**  
    Die Grünen verknüpfen Umweltprojekte und Bildung direkt im Schulalltag ([S. 13–14](https://gruene-salzgitter.de/wp-content/uploads/sites/102/2026/07/MACHS-GRUeN.pdf)), die Linke setzt ebenfalls auf ökologische Schulprojekte (Landesprogramm Niedersachsen).

**Hinweis zur Einordnung:**  
Wenn eine Partei zu einer Frage im Programm keine eindeutige Aussage getroffen hat, wurde dies mit `0` (neutral / keine Angabe) bewertet oder aus ihrer bisherigen Linie im Rat der Stadt Salzgitter abgeleitet. Das Ergebnis soll dir einen ersten Überblick geben, ersetzt aber nicht den eigenen Blick in die Programme.


st.markdown("""
<div class="header-box">
    <span class="header-badge">Salzgitter - Schüler-Umfrage</span>
    <div style="font-size:2.2rem; font-weight:800; color:#0f172a; line-height:1.2; margin:0;">Was wählen Kraniche?</div>
    <p style="color:#64748b; margin-top:0.35rem; font-size:1rem;">Finde heraus, welcher Kranich am besten zu deinen Ansichten passt.</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.intro < 6 and not st.session_state.fertig:
    s = st.session_state.intro
    titel = ["1. Willkommen", "2. Postkasten", "3. Hinweis", "4. Brief erhalten", "5. Brief geöffnet", "6. Startseite"]
    
    col_st1, col_st2 = st.columns([2, 1])
    col_st1.caption(f"Einführung: {titel[s]}")
    col_st2.markdown(f"<div style='text-align:right; color:#64748b; font-size:0.85rem;'>Schritt {s+1} von 6</div>", unsafe_allow_html=True)
    st.progress((s + 1) / 6)

    if s == 0:
        zeige_bild(1)
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        zeige_bild(2)
    elif s == 1: zeige_bild(3)
    elif s == 2: zeige_bild(4)
    elif s == 3: zeige_bild(5)
    elif s == 4: zeige_bild(6)
    elif s == 5: zeige_bild(7)

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    c_back, c_next, c_skip = st.columns([1, 2, 1.2])
    
    with c_back:
        if s > 0 and st.button("Zurück", key=f"in_b_{s}", use_container_width=True):
            st.session_state.intro -= 1
            st.rerun()
    with c_next:
        lbls = ["Weiter", "Weiter", "Postkasten öffnen", "Siegel brechen & öffnen", "Brief schließen & Weiter", "JETZT QUIZ STARTEN"]
        if st.button(lbls[s], key=f"in_n_{s}", type="primary", use_container_width=True):
            st.session_state.intro += 1
            st.rerun()
    with c_skip:
        if st.button("Intro überspringen", key=f"in_s_{s}", use_container_width=True):
            st.session_state.intro = 6
            st.rerun()

    zeige_footer()

elif st.session_state.intro == 6 and not st.session_state.fertig:
    q = st.session_state.frage
    these = THESEN[q]
    cur_ans = st.session_state.antworten.get(q, None)
    is_gew = st.session_state.gewichtung.get(q, False)

    c1, c2 = st.columns([2, 1])
    c1.markdown(f"**These {q + 1} von {len(THESEN)}**")
    c2.markdown(f"<div style='text-align:right; color:#64748b; font-size:0.85rem;'>Beantwortet: {len(st.session_state.antworten)}/{len(THESEN)}</div>", unsafe_allow_html=True)
    st.progress((q + 1) / len(THESEN))

    n_cols = st.columns(12)
    for i in range(12):
        with n_cols[i]:
            star = "*" if st.session_state.gewichtung.get(i, False) else ""
            if st.button(f"{i+1}{star}", key=f"nav_{i}", type="primary" if i == q else "secondary", use_container_width=True):
                st.session_state.frage = i
                st.rerun()

    st.markdown(f"""
    <div class="these-card">
        <div class="these-title">{these["text"]}</div>
    </div>
    """, unsafe_allow_html=True)

    _, c_gew, _ = st.columns([1, 1.4, 1])
    with c_gew:
        new_gew = st.toggle("Doppelt werten (2x)", value=is_gew, key=f"toggle_w_{q}")
        if new_gew != is_gew:
            st.session_state.gewichtung[q] = new_gew
            st.rerun()

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    
    def set_antwort(wert):
        st.session_state.antworten[q] = wert
  
        offen = [i for i in range(len(THESEN)) if i not in st.session_state.antworten]
        if offen:
            naechste = [i for i in offen if i > q]
            st.session_state.frage = naechste[0] if naechste else offen[0]
        else:
            st.session_state.fertig = True
        st.rerun()

    with b1:
        if st.button("Ich stimme zu", key=f"btn_agree_{'sel' if cur_ans == 1 else 'unsel'}_{q}", use_container_width=True):
            set_antwort(1)
    with b2:
        if st.button("keine Angabe", key=f"btn_neutral_{'sel' if cur_ans == 0 else 'unsel'}_{q}", use_container_width=True):
            set_antwort(0)
    with b3:
        if st.button("Ich lehne ab", key=f"btn_disagree_{'sel' if cur_ans == -1 else 'unsel'}_{q}", use_container_width=True):
            set_antwort(-1)

    zeige_footer()


else:
    results = berechne_score()
    top = results[0]

    st.markdown(f"""
    <div class="hero-card">
        <div style="font-size:0.85rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; opacity:0.85;">Dein Spitzenreiter</div>
        <div class="hero-pct">{top['prozent']:.1f} %</div>
        <div style="font-size:2.1rem; font-weight:800; margin:0.3rem 0;">{top['name']}</div>
        <div style="font-size:1.1rem; opacity:0.9;">Partei: {top['partei']}</div>
    </div>
    """, unsafe_allow_html=True)

    tab_rank, tab_comp = st.tabs(["Rangliste", "Thesenvergleich"])

    with tab_rank:
        st.subheader("Übersicht aller Ergebnisse")
        for idx, item in enumerate(results, start=1):
            st.markdown(f"""
            <div class="party-card">
                <div style="display:flex; justify-content:space-between; align-items:baseline;">
                    <div>
                        <strong style="font-size:1.1rem; color:#0f172a;">Platz {idx}: {item['name']}</strong>
                        <span style="color:#64748b; font-size:0.9rem; margin-left:0.3rem;">({item['partei']})</span>
                    </div>
                    <div style="font-size:1.25rem; font-weight:800; color:{item['farbe']};">{item['prozent']:.1f} %</div>
                </div>
                <div style="background:#e2e8f0; height:10px; border-radius:9999px; overflow:hidden; margin:0.5rem 0;">
                    <div style="background:{item['farbe']}; height:100%; width:{item['prozent']}%; border-radius:9999px;"></div>
                </div>
                <div style="font-size:0.8rem; color:#64748b;">
                    Erreichte Punkte: <strong>{item['punkte']}</strong> von {item['max']} Punkten
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        df_chart = pd.DataFrame({
            "Kranich": [f"{r['name']} ({r['partei']})" for r in results],
            "Übereinstimmung in %": [r['prozent'] for r in results]
        }).set_index("Kranich")
        st.bar_chart(df_chart)

    with tab_comp:
        st.subheader("Vergleich deiner Positionen")
        sel_party = st.selectbox("Partei auswählen:", options=PARTEIEN, format_func=lambda p: f"{NAMEN[p]} ({p})", key="comp_party")
        p_idx = PARTEIEN.index(sel_party)
        txt_map = {1: "Zustimmung", 0: "Keine Angabe", -1: "Ablehnung"}
        
        for f_idx, t in enumerate(THESEN):
            u_val = st.session_state.antworten.get(f_idx, 0)
            p_val = t["positionen"][p_idx]
            diff = abs(u_val - p_val)
            if diff == 0:
                match_txt = "Volle Übereinstimmung (+2 Punkte)"
                border_color = "#15803d"
            elif diff == 1:
                match_txt = "Teilweise Übereinstimmung (+1 Punkt)"
                border_color = "#ca8a04"
            else:
                match_txt = "Keine Übereinstimmung (0 Punkte)"
                border_color = "#dc2626"

            gew_str = " (2x gewichtet)" if st.session_state.gewichtung.get(f_idx, False) else ""
            st.markdown(f"""
            <div class="detail-row" style="border-left-color:{border_color};">
                <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#64748b; margin-bottom:0.3rem;">
                    <span>These {f_idx + 1}</span>
                    <span><strong>{match_txt}</strong>{gew_str}</span>
                </div>
                <div style="font-weight:700; color:#0f172a; margin-bottom:0.5rem;">{t['text']}</div>
                <div style="display:flex; gap:1.5rem; font-size:0.85rem;">
                    <div>Deine Auswahl: <strong>{txt_map[u_val]}</strong></div>
                    <div>{NAMEN[sel_party]}: <strong>{txt_map[p_val]}</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    st.divider()
    st.button("Quiz erneut starten", on_click=quiz_reset, use_container_width=True)

    zeige_footer()
