import streamlit as st
import google.generativeai as genai
import time

# --- OSNOVNA KONFIGURACIJA ---
st.set_page_config(page_title="Neni AI", layout="centered")

# Ubaci svoj API ključ ovde
API_KEY = AIzaSyBXcOfYFRNj_NcqogVUD_nibhhlzL8CVWk
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- STIL I LICE ---
st.markdown("""
<style>
.neni-face {
background-color: #1a1a1a;
border-radius: 50px;
padding: 40px;
text-align: center;
border: 5px solid #00d4ff;
width: 300px;
margin: 0 auto;
}
.eyes { color: #00d4ff; font-size: 50px; font-weight: bold; letter-spacing: 40px; }
.brows { color: #00d4ff; font-size: 30px; letter-spacing: 45px; margin-bottom: -10px; }
.mouth { color: #00d4ff; font-size: 40px; margin-top: 10px; }
</style>
<div class="neni-face">
<div class="brows">~ ~</div>
<div class="eyes">• •</div>
<div class="mouth">━━━</div>
</div>
""", unsafe_allow_html=True)

# --- LOGIKA MEMORIJE ---
if "step" not in st.session_state:
    st.session_state.step = "welcome"
    st.session_state.violations = []
    st.session_state.mode = None
    st.session_state.last_active = time.time()
# Spisak dozvoljenih imena
DOZVOLJENA_IMENA = ["Sava", "Hana", "Leo", "Andrea", "Acko", "Mila", "Lara", "Nemanja 1", "Marijo", "Lenka", "Jakša", "Maša", "Nemanja 2"]

# --- FUNKCIJA ZA GLAS I SLUŠANJE (Hands-free simulator) ---
def neni_speak(text):
js = f"""
<script>
var msg = new SpeechSynthesisUtterance('{text}');
msg.lang = 'sr-RS';
window.speechSynthesis.speak(msg);
</script>
"""
st.components.v1.html(js, height=0)

# --- AUTOMATSKO GAŠENJE (3 MINUTA) ---
if time.time() - st.session_state.last_active > 180:
st.warning("Neni se ugasio zbog neaktivnosti.")
st.stop()

# --- GLAVNI TOK RAZGOVORA ---

if st.session_state.step == "welcome":
intro = "Zdravo prijatelju. Ja sam Neni, AI sistem koji će ti pomoći. Zdravo! Kako se zoveš?"
st.subheader(intro)
neni_speak(intro)
ime = st.text_input("Reci ime:")
if ime:
st.session_state.last_active = time.time()
if ime in DOZVOLJENA_IMENA:
odgovor = f"Zdravo {ime}! Drago mi je što ti mogu pomoći. Šta mogu uraditi sada?"
neni_speak(odgovor)
st.session_state.step = "choose_mode"
st.rerun()
else:
neni_speak("Izvinite ali ne mogu vam pomoći. Idete kod drugog jer se u ovoj crkvi nećete moliti.")
st.stop()

elif st.session_state.step == "choose_mode":
st.write("### Izaberi mod: Dadilja, Zabavan, Ja")
mod = st.radio("Modovi:", ["Dadilja mod", "Zabavan mod", "Ja mod"])
if st.button("Potvrdi mod"):
st.session_state.mode = mod
st.session_state.step = "active"
neni_speak(f"Aktiviran je {mod}.")
st.rerun()

elif st.session_state.step == "active":
st.info(f"Trenutni mod: {st.session_state.mode}")

user_input = st.chat_input("Reci nešto (Neni sluša)...")

if user_input:
st.session_state.last_active = time.time()

# Logika za Dadilja mod
if st.session_state.mode == "Dadilja mod":
if "tužim" in user_input.lower():
# Ovde bi išla logika za beleženje (npr. "Tužim Marka za pravilo 2")
st.session_state.violations.append(user_input)
neni_speak("Zapisano.")
elif "da li je neko prekršijo pravila" in user_input.lower():
if not st.session_state.violations:
neni_speak("Niko nije prekršio pravila.")
else:
prekrsaji = ", ".join(st.session_state.violations)
neni_speak(f"Prekršena pravila su: {prekrsaji}")

# Logika za Zabavan mod
elif st.session_state.mode == "Zabavan mod":
# Ovde AI koristi Gemini za igre
response = model.generate_content(f"Igramo igru u zabavnom modu. Korisnik kaže: {user_input}. Odgovori kratko na srpskom.")
st.write(response.text)
neni_speak(response.text)

# Standardni "Ja" mod sa pristupom internetu
else:
response = model.generate_content(user_input)
st.write(response.text)
neni_speak(response.text)
