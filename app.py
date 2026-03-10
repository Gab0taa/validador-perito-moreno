import streamlit as st
import pandas as pd
import re
import time

# --- DISEÑO DE LA PÁGINA ---
st.set_page_config(page_title="Validador Municipal", page_icon="🔎", layout="centered")

# --- TÍTULO ---
st.markdown("<h2 style='text-align: center;'>🔎 Validador de Beneficios</h2>", unsafe_allow_html=True)
st.markdown("---")

# --- CONEXIÓN A GOOGLE SHEETS ---
URL_BASE = "https://docs.google.com/spreadsheets/d/1QZ7CDpZFhPZX8z5aarc4s7ns6SETDUJ07z_CYVLQo-s/export?format=csv&gid=1316691732"

# --- INTERFAZ ---
dni_buscado = st.text_input("Ingrese el DNI del beneficiario (sin puntos):", placeholder="Ej: 38811108")

if dni_buscado:
    try:
        # 1. Traemos los datos frescos
        URL_FRESCA = f"{URL_BASE}&t={int(time.time())}"
        df = pd.read_csv(URL_FRESCA)
        
        # 2. Limpieza de columnas (Borra espacios invisibles en los títulos)
        df.columns = df.columns.str.strip()
        
        # 3. Limpieza de datos (DNI de la base y DNI del usuario)
        df['DNI'] = df['DNI'].astype(str).str.split('.').str[0].str.replace(r'\D', '', regex=True)
        dni_limpio = re.sub(r'\D', '', str(dni_buscado))

        # 4. Búsqueda
        resultado = df[df['DNI'] == dni_limpio]

        # 5. Resultados
        if not resultado.empty:
            nombre = resultado.iloc[0]['Nombre']
            apellido = resultado.iloc[0]['Apellido']
            sector = resultado.iloc[0]['Sector'] if 'Sector' in df.columns else "No especificado"
            
            st.success("✅ **DESCUENTO AUTORIZADO**")
            st.subheader(f"Titular: {nombre} {apellido}")
            st.write(f"📍 Sector: {sector}")
            st.balloons()
        else:
            st.error("❌ EL DNI NO FIGURA EN EL PADRÓN")
            st.info("Debe registrarse en el bloque municipal para acceder al beneficio.")
            
    except Exception as e:
        st.error("Hubo un error al procesar los datos.")
        st.error(f"EL ERROR REAL ES: {e}")
        
# --- FOOTER PERSONALIZADO ---
st.markdown("---")
st.markdown('<p style="color: grey; text-align: center;">Proyecto llevado a cabo por Valeria Garcia Concejal</p>', unsafe_allow_html=True)