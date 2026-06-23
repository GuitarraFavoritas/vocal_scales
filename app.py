import base64
import json
import os
import streamlit.components.v1 as components
import streamlit as st
from midiutil import MIDIFile

# --- HACK PARA EVITAR EL TECLADO EN MÓVILES ---
components.html(
    """
    <script>
    const doc = window.parent.document;
    function disableMobileKeyboard() {
        const inputs = doc.querySelectorAll('div[data-baseweb="select"] input');
        inputs.forEach(input => {
            input.setAttribute('inputmode', 'none');
            input.setAttribute('readonly', 'readonly');
        });
    }
    disableMobileKeyboard();
    const observer = new MutationObserver(disableMobileKeyboard);
    observer.observe(doc.body, { childList: true, subtree: true });
    </script>
    """,
    height=0, width=0
)

# ==========================================
# GESTOR DE BASE DE DATOS LOCAL (Archivo JSON)
# ==========================================
DB_FILE = "ejercicios_db.json"

default_patterns = {
    "1st Repeated x5": "1[x3], 1[x3], 1[x3], 1[x3], 1[x9]",
    "Octave Sustain, scale to 9th": "1, 3, 5, 8[x6], 7[x0.5], 8[x0.5], 9[x0.5], 8[x0.5], 7[x0.5], 6[x0.5], 5[x0.5], 4[x0.5], 3[x0.5], 2[x0.5], 1[x3]",
    "Octave Sustain, scale to 9th x2": "1, 3, 5, 8[x6], 7[x0.5], 8[x0.5], 9[x0.5], 8[x0.5], 7[x0.5], 6[x0.5], 5[x0.5], 4[x0.5], 3[x0.5], 2[x0.5], 1[x0.5], 2[x0.5], 3[x0.5], 4[x0.5], 5[x0.5], 6[x0.5], 7[x0.5], 8[x0.5], 9[x0.5], 8[x0.5], 7[x0.5], 6[x0.5], 5[x0.5], 4[x0.5], 3[x0.5], 2[x0.5], 1[x3]",
    "5 Tone x2, scale to 9th": "1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1[x3]",
}

def load_patterns():
    if not os.path.exists(DB_FILE):
        save_patterns(default_patterns)
        return default_patterns
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_patterns

def save_patterns(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

patterns = load_patterns()
pattern_names = list(patterns.keys())

# ==============================
# NOTE HELPERS
# ==============================
note_names = {"C":0,"C#":1,"D":2,"D#":3,"E":4,"F":5,"F#":6,"G":7,"G#":8,"A":9,"A#":10,"B":11}

def note_to_midi(note):
    return 12 * (int(note[-1]) + 1) + note_names[note[:-1]]

def parse_pattern(pat):
    result = []
    for token in pat.replace(" ", "").split(","):
        if "[x" in token:
            degree, length = token.split("[x")
            length = float(length[:-1])
        else:
            degree, length = token, 1.0
        if degree.endswith("b"):
            result.append((int(degree[:-1]), length, -1))
        elif degree.endswith("#"):
            result.append((int(degree[:-1]), length, +1))
        else:
            result.append((int(degree), length, 0))
    return result

def build_major_scale(root_midi):
    return [root_midi + i for i in [0,2,4,5,7,9,11,12,14,16,17,19,21,23,24]]

def pattern_fits_in_range(pattern_degrees, root, high_midi):
    scale = build_major_scale(root)
    max_degree = max(deg for deg,_,_ in pattern_degrees)
    return scale[max_degree-1] <= high_midi

# ==============================
# STREAMLIT UI 
# ==============================

if "selected_ex" not in st.session_state or st.session_state.selected_ex not in pattern_names:
    st.session_state.selected_ex = pattern_names[0]

def sync_selection():
    st.session_state.selected_ex = st.session_state.widget_selector

current_idx = pattern_names.index(st.session_state.selected_ex)

exercise = st.selectbox(
    "Selecciona el ejercicio", 
    options=pattern_names,
    index=current_idx,
    key="widget_selector",
    on_change=sync_selection
)

# --- GESTOR CRUD COMPLETO ---
with st.popover("🛠️ Gestor de Ejercicios (Crear / Editar / Borrar)"):
    tab_edit, tab_new, tab_del = st.tabs(["✏️ Editar actual", "➕ Crear nuevo", "🗑️ Borrar"])

    # 1. MODIFICAR EXISTENTE (Claves dinámicas f"_{exercise}")
    with tab_edit:
        st.caption(f"Modificando: **{exercise}**")
        
        edit_name = st.text_input(
            "Nombre del ejercicio:", 
            value=exercise, 
            key=f"ed_nm_{exercise}"  # <--- CLAVE DINÁMICA
        )
        edit_pat = st.text_area(
            "Patrón musical (grados y duraciones):", 
            value=patterns[exercise], 
            height=100, 
            key=f"ed_pt_{exercise}"  # <--- CLAVE DINÁMICA
        )
        
        if st.button("Guardar cambios", key="btn_save_ed", type="primary", use_container_width=True):
            if not edit_name.strip() or not edit_pat.strip():
                st.error("Los campos no pueden estar vacíos.")
            elif edit_name != exercise and edit_name in patterns:
                st.error("Ya existe otro ejercicio con ese nombre.")
            else:
                new_dict = {}
                for k, v in patterns.items():
                    if k == exercise:
                        new_dict[edit_name.strip()] = edit_pat.strip()
                    else:
                        new_dict[k] = v
                save_patterns(new_dict)
                st.session_state.selected_ex = edit_name.strip()
                if "widget_selector" in st.session_state: del st.session_state["widget_selector"]
                st.rerun()

    # 2. CREAR NUEVO
    with tab_new:
        st.caption("Añadir un ejercicio a la lista")
        new_name = st.text_input("Nombre:", placeholder="Ej: Arpegio veloz", key="in_nw_name")
        new_pat = st.text_area("Patrón:", placeholder="Ej: 1, 3, 5, 8[x4], 5, 3, 1[x2]", height=100, key="in_nw_pat")
        
        if st.button("Crear ejercicio", key="btn_save_nw", type="primary", use_container_width=True):
            if not new_name.strip() or not new_pat.strip():
                st.error("Por favor completa ambos campos.")
            elif new_name.strip() in patterns:
                st.error("Ese nombre ya existe.")
            else:
                patterns[new_name.strip()] = new_pat.strip()
                save_patterns(patterns)
                st.session_state.selected_ex = new_name.strip()
                if "widget_selector" in st.session_state: del st.session_state["widget_selector"]
                st.rerun()

    # 3. ELIMINAR
    with tab_del:
        st.warning(f"¿Eliminar definitivamente **'{exercise}'**?")
        if st.button("Sí, eliminar ejercicio", key="btn_del", use_container_width=True):
            if len(patterns) <= 1:
                st.error("No puedes borrar el último ejercicio de la base de datos.")
            else:
                del patterns[exercise]
                save_patterns(patterns)
                st.session_state.selected_ex = list(patterns.keys())[0]
                if "widget_selector" in st.session_state: del st.session_state["widget_selector"]
                st.rerun()

with st.popover("Rango, Dirección y BPM"):
    col1, col2 = st.columns(2)
    with col1:
        range_low = st.selectbox("LOW", ["A2","A#2","B2","C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4"])
    with col2:
        range_high = st.selectbox("HIGH", ["A4","G#4","G4","F#4","F4","E4","D#4","D4","C#4","C4","B3","A#3","A3","G#3","G3","----------","D5","C5","B4"])
    direction = st.selectbox("Dirección", ["ascend_descend","descend_ascend","ascend_only","descend_only"])
    bpm = st.slider("BPM", min_value= 0, max_value=400, value=200, step=5)

file_name = f"{exercise}_{bpm}bpm_{range_low}-{range_high}_{direction}.mid"

with st.popover("Otras configuraciones"):
    bridge = st.slider("Duración del puente..", min_value= 0, max_value=32, value=4, step=1)
    metronome_vol = st.slider("Metrónomo Vol.", min_value= 0, max_value=127, value=80, step=10)
    notes_vol = st.slider("Notas Vol..", min_value= 0, max_value=127, value=127, step=10)
    final_chord_vol = st.slider("Chord Vol..", min_value= 0, max_value=127, value=85, step=10)

# ==============================
# BOTÓN PARA GENERAR MIDI
# ==============================
if st.button("Generar MIDI"):
    
    try:
        pattern_notes = parse_pattern(patterns[exercise])
    except Exception:
        st.error("❌ Hay un error de sintaxis en el patrón musical de este ejercicio. Entra al 'Gestor de Ejercicios' y corrígelo.")
        st.stop()

    mf = MIDIFile(2) 

    track_music = 0
    mf.addTempo(track_music, 0, bpm)

    track_metronome = 1
    mf.addTempo(track_metronome, 0, bpm)
    channel_drums = 9
    woodblock = 76

    low_midi, high_midi = note_to_midi(range_low), note_to_midi(range_high)

    roots_up, root = [], low_midi
    while root <= high_midi:
        if not pattern_fits_in_range(pattern_notes, root, high_midi): break
        roots_up.append(root); root += 1

    dir_lower = direction.lower().replace(" ", "_")
    if dir_lower in ("ascend_only","low_to_high"):
        roots = roots_up
    elif dir_lower in ("descend_only","high_to_low"):
        start_root = high_midi
        while start_root >= low_midi and not pattern_fits_in_range(pattern_notes, start_root, high_midi):
            start_root -= 1
        roots = list(range(start_root, low_midi-1, -1))
    elif dir_lower in ("ascend_descend","up_down"):
        roots = roots_up + roots_up[-2::-1]
    elif dir_lower in ("descend_ascend","down_up"):
        roots_down = list(range(high_midi, low_midi-1, -1))
        roots_down = [r for r in roots_down if pattern_fits_in_range(pattern_notes, r, high_midi)]
        roots = roots_down + roots_down[-2::-1]
    else:
        roots = roots_up

    time = 0
    for beat in range(4):
        mf.addNote(track_metronome, channel_drums, woodblock, time+beat, 0.5, metronome_vol)
    time += 4

    for i, root in enumerate(roots):
        scale = build_major_scale(root)
        for idx, (degree, length, accidental) in enumerate(pattern_notes, start=1):
            note_num = scale[degree-1] + accidental
            mf.addNote(track_music, 0, note_num, time, length, notes_vol)
            dur = length
            beats = int(dur)
            for b in range(beats):
                mf.addNote(track_metronome, channel_drums, woodblock, time+b, 0.5, metronome_vol)
            time += dur

        if i < len(roots)-1:
            next_root = roots[i+1]
            mf.addNote(track_music, 0, next_root, time, bridge, notes_vol)
            for b in range(bridge):
                mf.addNote(track_metronome, channel_drums, woodblock, time+b, 0.5, metronome_vol)
            time += bridge

    final_scale = build_major_scale(low_midi)
    for degree,_,_ in pattern_notes:
        mf.addNote(track_music, 0, final_scale[degree-1], time, 4, final_chord_vol)
    for b in range(4):
        mf.addNote(track_metronome, channel_drums, woodblock, time+b, 0.5, metronome_vol)

    with open(file_name, "wb") as f:
        mf.writeFile(f)

    st.success(f"✅ {file_name}")
    
    with open(file_name, "rb") as f:
        midi_data = f.read()
    b64_midi = base64.b64encode(midi_data).decode("utf-8")
    midi_uri = f"data:audio/midi;base64,{b64_midi}"

    html_player = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <script src="https://cdn.jsdelivr.net/combine/npm/tone@14.7.58,npm/@magenta/music@1.23.1/es6/core.js,npm/focus-visible@5,npm/html-midi-player@1.5.0"></script>
        <style>
            * {{ box-sizing: border-box; }}
            body {{ margin: 0; padding: 0; width: 100vw; background-color: #121212; overflow-x: hidden; }}
            midi-player, midi-visualizer {{ width: 100%; display: block; }}
        </style>
    </head>
    <body>
        <div style="display: flex; flex-direction: column; width: 100%; gap: 10px; padding: 2px;">
            <midi-player src="{midi_uri}" sound-font visualizer="#mobileWaterfall"></midi-player>
            <midi-visualizer type="piano roll" id="mobileWaterfall" src="{midi_uri}" config='{{"noteRGB": "0, 190, 255", "activeNoteRGB": "255, 215, 0", "pixelsPerTimeStep": 45}}' style="height: 320px; background: #121212; border-radius: 12px; border: 1px solid #333; box-shadow: inset 0 0 10px rgba(0,0,0,0.8);"></midi-visualizer>
        </div>
    </body>
    </html>
    """
    components.html(html_player, height=395)

    st.download_button("Descargar Archivo MIDI", data=midi_data, file_name=file_name, mime="audio/midi")
