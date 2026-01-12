import streamlit as st
import matplotlib.pyplot as plt

# Nagłówek aplikacji
st.title("Mój Generator Rysunków")

# Panel boczny z ustawieniami
st.sidebar.header("Ustawienia")
kolor_linii = st.sidebar.color_picker("Wybierz kolor linii", "#00f900")
grubosc = st.sidebar.slider("Grubość punktów", 1, 20, 5)
typ_rysunku = st.sidebar.selectbox("Co rysujemy?", ["Linie promieniście", "Punkty losowe"])

# Tworzenie rysunku za pomocą Matplotlib
fig, ax = plt.subplots()

if typ_rysunku == "Linie promieniście":
    for i in range(1, 11):
        ax.plot([0, i], [0, 10], color=kolor_linii)
else:
    ax.scatter([1, 2, 3, 4, 5], [5, 2, 8, 1, 6], s=grubosc*10, color=kolor_linii)

# Wyświetlenie rysunku na stronie
st.pyplot(fig)

# Przycisk do pobierania (opcjonalnie)
st.download_button("Pobierz jako obrazek", "rysunek.png")
