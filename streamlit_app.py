mport streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Widzenie w Zezie", layout="centered")

st.title("Widzenie w Zezie — demo Streamlit")
st.write("Prosty interfejs demonstracyjny. Dodaj swój opis tutaj.")

with st.sidebar:
    st.header("Ustawienia")
    demo_mode = st.selectbox("Tryb demo", ["Interakcyjny", "Wykres"], index=0)
    show_examples = st.checkbox("Pokaż przykładowe dane", value=True)

st.header("Wejście")
uploaded_file = st.file_uploader("Wgraj obraz (opcjonalnie)", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Wgrany obraz", use_column_width=True)

name = st.text_input("Twoje imię", "Gość")
if st.button("Przywitaj"):
    st.success(f"Cześć, {name}! 👋")

if show_examples:
    st.subheader("Przykładowe dane i wykres")
    df = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"]).cumsum()
    st.dataframe(df)

    if demo_mode == "Wykres":
        st.line_chart(df)
    else:
        st.area_chart(df)
