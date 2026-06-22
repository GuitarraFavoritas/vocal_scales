import base64
import streamlit.components.v1 as components

import streamlit as st
from midiutil import MIDIFile

# --- HACK PARA EVITAR EL TECLADO EN MÓVILES ---
components.html(
    """
    <script>
    const doc = window.parent.document;
    
    function disableMobileKeyboard() {
        // Busca todos los inputs dentro de los menús desplegables
        const inputs = doc.querySelectorAll('div[data-baseweb="select"] input');
        inputs.forEach(input => {
            // Desactiva el teclado virtual en Android/iOS
            input.setAttribute('inputmode', 'none');
            input.setAttribute('readonly', 'readonly');
        });
    }

    // Ejecutar inmediatamente
    disableMobileKeyboard();

    // Mantener el bloqueo activo aunque Streamlit actualice la página (MutationObserver)
    const observer = new MutationObserver(disableMobileKeyboard);
    observer.observe(doc.body, { childList: true, subtree: true });
    </script>
    """,
    height=0, width=0
)
# ==============================
# PATTERN DEFINITIONS
# ==============================
patterns = {
    #Calentamiento
    "1st Repeated x5": "1[x3], 1[x3], 1[x3], 1[x3], 1[x9]", #D4 200BPM
    #SMckey
    "Octave Sustain, scale to 9th": "1, 3, 5, 8[x6], 7[x0.5], 8[x0.5], 9[x0.5], 8[x0.5], 7[x0.5], 6[x0.5], 5[x0.5], 4[x0.5], 3[x0.5], 2[x0.5], 1[x3]",
    "Octave Sustain, scale to 9th x2": "1, 3, 5, 8[x6], 7[x0.5], 8[x0.5], 9[x0.5], 8[x0.5], 7[x0.5], 6[x0.5], 5[x0.5], 4[x0.5], 3[x0.5], 2[x0.5], 1[x0.5], 2[x0.5], 3[x0.5], 4[x0.5], 5[x0.5], 6[x0.5], 7[x0.5], 8[x0.5], 9[x0.5], 8[x0.5], 7[x0.5], 6[x0.5], 5[x0.5], 4[x0.5], 3[x0.5], 2[x0.5], 1[x3]",
    "5 Tone x2, scale to 9th": "1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1[x3]",
    #Mis Ejercicios
    "2nd JumpX3Sus_C4": "1, 2, 1, 2, 1, 2[x6], 2[x6], 2, 1, 2, 1, 2, 1[x3]", #
    "3rd JumpX3Sus_A#3": "1, 3, 1, 3, 1, 3[x6], 3[x6], 3, 1, 3, 1, 3, 1[x3]", #
    "4th JumpX3Sus_A3": "1, 4, 1, 4, 1, 4[x6], 4[x6], 4, 1, 4, 1, 4, 1[x3]", #
    "5th JumpX3Sus_G3": "1, 5, 1, 5, 1, 5[x6], 5[x6], 5, 1, 5, 1, 5, 1[x3]", #
    "6th JumpX3Sus_F3": "1, 6, 1, 6, 1, 6[x6], 6[x6], 6, 1, 6, 1, 6, 1[x3]", #
    "7th JumpX3Sus_D#3": "1, 7, 1, 7, 1, 7[x6], 7[x6], 7, 1, 7, 1, 7, 1[x3]", #
    "8th JumpX3Sus_D3": "1, 8, 1, 8, 1, 8[x6], 8[x6], 8, 1, 8, 1, 8, 1[x3]", #
    "9th JumpX3Sus_C3": "1, 9, 1, 9, 1, 9[x6], 9[x6], 9, 1, 9, 1, 9, 1[x3]", #
    "10th JumpX3Sus_A#2": "1, 10, 1, 10, 1, 10[x6], 10[x6], 10, 1, 10, 1, 10, 1[x3]", #
    "11th JumpX3Sus_A2": "1, 11, 1, 11, 1, 11[x6], 11[x6], 11, 1, 11, 1, 11, 1[x3]", #
    "12th JumpX3Sus_A2": "1, 12, 1, 12, 1, 12[x6], 12[x6], 12, 1, 12, 1, 12, 1[x3]", #
    "13th JumpX3Sus_A2": "1, 13, 1, 13, 1, 13[x6], 13[x6], 13, 1, 13, 1, 13, 1[x3]", #
    "14th JumpX3Sus_A2": "1, 14, 1, 14, 1, 14[x6], 14[x6], 14, 1, 14, 1, 14, 1[x3]", #
    "3 ToneSus_A#3": "1, 2, 3, 1, 2, 3[x6], 3[x6], 3, 2, 1, 3, 2, 1[x3]", # 200BPM
    "4 ToneSus_A3": "1, 2, 3, 4[x6], 4[x6], 4, 3, 2, 1[x3]", #
    "5 ToneSus_G3": "1, 2, 3, 4, 5[x6], 5[x6], 5, 4, 3, 2, 1[x3]", #
    "6 ToneSus_F3": "1, 2, 3, 4, 5, 6[x6], 6[x6], 6, 5, 4, 3, 2, 1[x3]", #
    "7 ToneSus_D#3": "1, 2, 3, 4, 5, 6, 7[x6], 7[x6], 7, 6, 5, 4, 3, 2, 1[x3]", #
    "8 ToneSus_D3": "1, 2, 3, 4, 5, 6, 7, 8[x6], 8[x6], 8, 7, 6, 5, 4, 3, 2, 1[x3]", #    
    "9 ToneSus_C3": "1, 2, 3, 4, 5, 6, 7, 8, 9[x6], 9[x6], 9, 8, 7, 6, 5, 4, 3, 2, 1[x3]", #
    "10 ToneSus_A#2": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10[x6], 10[x6], 10, 9, 8, 7, 6, 5, 4, 3, 2, 1[x3]", #
    "11 ToneSus_A2": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11[x6], 11[x6], 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1[x3]", #
    "12 ToneSus_A2": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12[x6], 12[x6], 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1[x3]", #
    "13 ToneSus_": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13[x6], 13[x6], 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1[x3]", #
    "14 ToneSus_A2": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14[x6], 14[x6], 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1[x3]", #
    "Tonic Intervals": "1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 1, 7, 1, 8, 7, 8, 6, 8, 5, 8, 4, 8, 3, 8, 2, 8, 1[x3]", #160

    #Canciones
    "P4 M'olvide D'vivir 1" : "8[x0.5], 8[x0.75], 8[x0.75], 8[x0.5], 8[x0.75], 8[x0.75], 8[x0.5], 8[x0.75], 7[x0.75], 6[x0.5], 2[x2], 3[x0.5], 2[x0.5], 4[x4]",
    "P4 M'olvide D'vivir 2" : "7[x0.5], 7[x0.75], 7[x0.75], 7[x0.5], 9[x0.75], 7[x0.75], 7[x0.5], 7[x0.75], 6[x0.75], 5[x0.5], 1[x2], 2[x0.5], 1[x0.5], 3[x4]",
    #swift
    "S01 Foundation - 5 Tone": "1, 2, 3, 4, 5, 4, 3, 2, 1[x3]",
    "S02 Consistency - Scale to 9th": "1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1[x4]",
    "S03 Flexibility - Arpegio": "1, 3, 5, 8, 5, 3, 1[x3]",
    "S04 Presence - Octave Repeat": "1, 3, 5, 8, 8, 8, 8, 5, 3, 1[x3]",
    "S05 Sustain - Octave Repeat Sustain": "1, 3, 5, 8, 8, 8, 8[x8], 5, 3, 1[x3]",
    "S06 Range - 1.5 Scale": "1, 3, 5, 8, 10, 12, 11, 9, 7, 5, 4, 2, 1[x3]",
    "S07 Connection - 5 Semi-Tone x2": "1, 2b, 2, 3b, 3, 3b, 2, 2b, 1, 2b, 2, 3b, 3, 3b, 2, 2b, 1[x3]",
    "S08 Accuracy - Octave Sustain, scale to 9th": "1, 3, 5, 8[x6], 7[x0.5], 8[x0.5], 9[x0.5], 8[x0.5], 7[x0.5], 6[x0.5], 5[x0.5], 4[x0.5], 3[x0.5], 2[x0.5], 1[x3]",
    "S09 Precision - 2nd Intervals to 9th": "1, 3, 2, 4, 3, 5, 4, 6, 5, 7, 6, 8[x6], 7, 9, 7, 9[x3], 9, 7, 8, 6, 7, 5, 6, 4, 5, 3, 4, 2, 3, 1[x3]",
    "S10 Agility - Octave Sustain, 2nd Intervals descending": "1, 3, 5, 8[x6], 8, 10, 7, 9, 6, 8, 5, 7, 4, 6, 3, 5, 2, 4, 1[x3]",
    "S11 Performance - Scale to The 11th Groppo": "1, 1[x0.5], 2[x0.5], 3, 3[x0.5], 4[x0.5], 5, 5[x0.5], 6[x0.5], 7[x0.5], 8[x0.5], 9[x0.5], 10[x0.5], 11, 11[x0.5], 10[x0.5], 9, 9[x0.5], 8[x0.5], 7, 7[x0.5], 6[x0.5], 5[x0.5], 4[x0.5], 3[x0.5], 2[x0.5], 1[x3]",
    "S12 Power - 5 Tone x2, scale to 9th": "1[x0.5], 2[x0.5], 3[x0.5], 4[x0.5], 5[x0.5], 4[x0.5], 3[x0.5], 2[x0.5], 1[x0.5], 2[x0.5], 3[x0.5], 4[x0.5], 5[x0.5], 4[x0.5], 3[x0.5], 2[x0.5], 1[x0.5], 2[x0.5], 3[x0.5], 4[x0.5], 5[x0.5], 6[x0.5], 7[x0.5], 8[x0.5], 9[x0.5], 8[x0.5], 7[x0.5], 8[x0.5], 9[x0.5], 8[x0.5], 7[x0.5], 8[x0.5], 9[x0.5], 8[x0.5], 7[x0.5], 6[x0.5], 5[x0.5], 4[x0.5], 3[x0.5], 2[x0.5], 1[x3]",
    "S13 Pitch - Root Intervals": "1[x0.5], 2[x0.5], 1[x0.5], 3[x0.5], 1[x0.5], 4[x0.5], 1[x0.5], 5[x0.5], 1[x0.5], 6[x0.5], 1[x0.5], 7[x0.5], 1[x0.5], 8[x0.5], 7[x0.5], 8[x0.5], 6[x0.5], 8[x0.5], 5[x0.5], 8[x0.5], 4[x0.5], 8[x0.5], 3[x0.5], 8[x0.5], 2[x0.5], 8[x0.5], 1[x3]",
    "S14 Endurance - 5 Tone x2, Scale 9th & 11th": "1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 9, 7, 5, 4, 2, 1[x4]",
    "S15 Tono - 5 Tone x5": "1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1[x4]",
    "S16 Warm Down C - 5 Tone descending": "5, 4, 3, 2, 1[x3]",
    #SLS
    "3 Tonos": "1, 2, 3, 2, 1[x3]",
    "Octave Jump": "1[x3], 8[x7], 5, 3, 1[x3]",
    "1.5 Scale": "1, 3, 5, 8, 10, 12, 11, 9, 7, 5, 4, 2, 1[x3]",
    "1.5 Gallop": "1[x1.1], 3[x0.9], 5[x1.1], 8[x0.9], 10[x1.1], 12[x0.9], 11[x1.1], 9[x0.9], 7[x1.1], 5[x0.9], 4[x1.1], 2[x0.9], 1[x3]",
    "Octave More Repeat": "1, 3, 5, 8, 8, 8, 8, 5, 3, 1[x3]",
    "Octave More Sustain": "1, 3, 5, 8[x6], 8[x6], 5, 3, 1[x3]", #220 bpm
    "Octave More Sustain x5": "1, 3, 5, 8[x6], 8[x6], 8[x6], 8[x6], 8[x6], 5, 3, 1[x3]", #320 bpm
    "Octave More Sustain x2": "1, 3, 5, 8[x3], 8[x3], 5, 3, 1[x3], 1, 3, 5, 8[x3], 8[x3], 5, 3, 1[x3]",
    "Arpegio Descending": "8, 5, 3, 1[x3]",
    "Broken Arpegio": "1, 5, 3, 8, 5, 3, 1[x3]",
    "Broken Arpegio x3": "1, 5, 3, 8, 5, 3, 1, 5, 3, 8, 5, 3, 1, 5, 3, 8, 5, 3, 1[x3]",
    "Octave Sustain": "1, 3, 5, 8[x4], 5, 3, 1[x3]",
    "Octave Repeat": "1, 3, 5, 8, 8, 8, 8, 5, 3, 1[x3]",
    "Octave Repeat Sustain": "1, 3, 5, 8[x3], 8[x3], 8[x6], 5, 3, 1[x3]",
    "Mixed Double Octave": "1, 5, 3, 8, 5, 10, 8, 12, 10, 15, 10, 12, 8, 10, 5, 8, 3, 5, 1[x3]",
    "3 Octave Scale": "1, 3, 5, 8, 10, 12, 15, 17, 19, 22, 19, 17, 15, 12, 10, 8, 5, 3, 1[x3]",
    # B E L  C A N T O
    "Third jump x2": "1, 3, 1, 3, 1[x2]", #Nota de paso 2
    "Triad Descending": "5, 3, 1[x2]", #Nota de paso 2
    "Fifth jump x2": "1, 5, 1, 5, 1[x2]", #Nota de paso 2 bpm120
    "5 Tone x3": "1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1[x3]",
    "Repeated Tone": "1[x3], 1[x3], 1[x3], 1[x5]",
    # Caroline Jones
    "CJ Ej3": "1, 6[x2], 2, 7b[x1.5], 2[x0.5], 3, 9[x2], 3, 4[x2]",
    "CJ Ej4": "1, 3, 5, 8, 10[x6], 8, 5, 3, 1[x3], 1, 3, 5, 8, 10[x6], 8, 5, 3, 1[x3], 1, 3, 5, 8, 10[x6], 8, 5, 3, 1[x3]",
    "CJ Ej5": "8, 5, 3, 1, 1[x2]", #Nota de paso 2
    "5 Tone x2, scale to 9th": "1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1[x4]",
    #Otros
    "8ve Sustain Descending": "8[x3], 7, 6, 5, 4, 3, 2, 1[x3]",
    "5 Tone descending x2": "5, 3, 4, 2, 1[x2], 5, 3, 4, 2, 1[x3]",
    "3 Tone Descending": "3, 2, 1[x2]",
    "5 Tone sustain x3": "1, 2, 3, 4, 5[x6], 4, 3, 2, 1, 2, 3, 4, 5[x6], 4, 3, 2, 1, 2, 3, 4, 5[x6], 4, 3, 2, 1[x6]", #400bpm
    "5 Tone sustain x4": "1, 2, 3, 4, 5[x6], 4, 3, 2, 1, 2, 3, 4, 5[x6], 4, 3, 2, 1, 2, 3, 4, 5[x6], 4, 3, 2, 1, 2, 3, 4, 5[x6], 4, 3, 2, 1[x6]", #400bpm
    "5 Tone sustain x6": "1, 2, 3, 4, 5[x6], 4, 3, 2, 1, 2, 3, 4, 5[x6], 4, 3, 2, 1, 2, 3, 4, 5[x6], 4, 3, 2, 1, 2, 3, 4, 5[x6], 4, 3, 2, 1, 2, 3, 4, 5[x6], 4, 3, 2, 1, 2, 3, 4, 5[x6], 4, 3, 2, 1[x6]", #400bpm
}

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
#st.title("🎵 Generador de Ejercicios MIDI")

exercise = st.selectbox("Selecciona el ejercicio", list(patterns.keys()))

with st.popover("Rango, Dirección y BPM"):
    col1, col2 = st.columns(2)
    with col1:
        range_low = st.selectbox("LOW", ["A2","A#2","B2","C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4"])
    with col2:
        range_high = st.selectbox("HIGH", ["A4","G#4","G4","F#4","F4","E4","D#4","D4","C#4","C4","B3","A#3","A3","G#3","G3","----------","D5","C5","B4"])
    direction = st.selectbox("Dirección", ["ascend_descend","descend_ascend","ascend_only","descend_only"])
    bpm = st.number_input( "BPM", value=200, placeholder="Type a number...")
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
    mf = MIDIFile(2)  # 2 tracks: música + metrónomo

    # Track música
    track_music = 0
    mf.addTempo(track_music, 0, bpm)

    # Track metrónomo
    track_metronome = 1
    mf.addTempo(track_metronome, 0, bpm)
    channel_drums = 9
    woodblock = 76

    # Roots y patrones
    pattern_notes = parse_pattern(patterns[exercise])
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

    # Compás inicial vacío con metrónomo
    time = 0
    for beat in range(4):
        mf.addNote(track_metronome, channel_drums, woodblock, time+beat, 0.5, metronome_vol)
    time += 4

    # Añadir notas + metrónomo constante
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

        # Puente
        if i < len(roots)-1:
            next_root = roots[i+1]
            mf.addNote(track_music, 0, next_root, time, bridge, notes_vol)
            for b in range(bridge):
                mf.addNote(track_metronome, channel_drums, woodblock, time+b, 0.5, metronome_vol)
            time += bridge

    # Final chord
    final_scale = build_major_scale(low_midi)
    for degree,_,_ in pattern_notes:
        mf.addNote(track_music, 0, final_scale[degree-1], time, 4, final_chord_vol)
    for b in range(4):
        mf.addNote(track_metronome, channel_drums, woodblock, time+b, 0.5, metronome_vol)

    # Guardar el archivo temporalmente
    with open(file_name, "wb") as f:
        mf.writeFile(f)

    st.success(f"✅ {file_name}")
    
    # ---------------------------------------------------------
    # REPRODUCTOR MIDI INTEGRADO (Inyección de JavaScript)
    # ---------------------------------------------------------
    # 1. Leer el archivo generado y convertirlo a base64
    with open(file_name, "rb") as f:
        midi_data = f.read()
    b64_midi = base64.b64encode(midi_data).decode("utf-8")
    midi_uri = f"data:audio/midi;base64,{b64_midi}"

   # 2. Inyectar el reproductor HTML/JS (Estructura HTML5 con Viewport móvil)
    html_player = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <!-- ESTA LÍNEA ES LA SOLUCIÓN: Obliga al iframe a medir exactamente los píxeles del celular -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        
        <script src="https://cdn.jsdelivr.net/combine/npm/tone@14.7.58,npm/@magenta/music@1.23.1/es6/core.js,npm/focus-visible@5,npm/html-midi-player@1.5.0"></script>
        
        <style>
            /* Reset CSS para evitar desbordes horizontales */
            * {{ box-sizing: border-box; }}
            body {{ margin: 0; padding: 0; width: 100vw; background-color: #121212; overflow-x: hidden; }}
            midi-player, midi-visualizer {{ width: 100%; display: block; }}
        </style>
    </head>
    <body>
        <div style="display: flex; flex-direction: column; width: 100%; gap: 10px; padding: 2px;">
            
            <midi-player
                src="{midi_uri}"
                sound-font 
                visualizer="#mobileWaterfall">
            </midi-player>

            <midi-visualizer 
                type="piano roll" 
                id="mobileWaterfall"
                src="{midi_uri}" 
                config='{{"noteRGB": "0, 190, 255", "activeNoteRGB": "255, 215, 0", "pixelsPerTimeStep": 45}}'
                style="height: 320px; background: #121212; border-radius: 12px; border: 1px solid #333; box-shadow: inset 0 0 10px rgba(0,0,0,0.8);">
            </midi-visualizer>
            
        </div>
    </body>
    </html>
    """
    
    components.html(html_player, height=395)

    # ---------------------------------------------------------
    # Botón de descarga normal
    # ---------------------------------------------------------
    #st.download_button("Descargar Archivo MIDI", data=midi_data, file_name=file_name, mime="audio/midi")
