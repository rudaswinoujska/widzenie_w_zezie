import streamlit as st
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.transforms as transforms
import matplotlib.pyplot as plt
import io
import numpy as np
import matplotlib.image as mpimg
from matplotlib.patches import Circle, Arc
import matplotlib.patheffects as path_effects


# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Widzenie w zezie", layout="centered")

# --- TYTUŁ I OPIS ---
st.title("Jak widzi pacjent z zezem")
st.write("Wprowadź dane po lewej, aby wygenerować rysunek.")

# --- PANEL BOCZNY (INTERFEJS) ---
st.sidebar.header("Wprowadź dane")
opcja_map = {"Oko prawe": "OD", "Oko lewe": "OS"}
wybor = st.sidebar.radio("Wybierz oko", list(opcja_map.keys()))
oko = opcja_map[wybor]

# Suwak (Slider) - 
kat_obiektywny = st.sidebar.slider("kąt obiektywny", min_value=-50, max_value=50, value=20, step=5)

kat_subiektywny = st.sidebar.slider("kąt subiektywny", min_value=-50, max_value=50, value=-10, step=5)

fiksacja = st.sidebar.slider("fikacja", min_value=-50, max_value=50, value=10, step=5)
st.sidebar.caption("skroniowa (-), nosowa (+)")

# --- PRZELICZANIE PARAMETRÓW ---
kat_anomalii = kat_obiektywny - kat_subiektywny
kat_ct = kat_obiektywny - fiksacja

# punkty w oku zezującym
p_zerowy = (kat_obiektywny, 0) # punkt padania światła gdy oko prowadzące fiksuje na wprost
p_ekscentryczny = (kat_ct, 0) # punkt ekscentrycznego fiksacji 
p_anomalny = (kat_subiektywny, 0) # punkt korespondujący z dołeczkiem oka prowadzącego
p_dołeczek = (0, 0) # anatomiczny dołeczek


col1, col2 = st.columns(2)
with col1:
       
# --- obraz siatkówki ---

    st.markdown("### obraz siatkówki") 
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100, facecolor='none')
    img = mpimg.imread("retina OP.png")
    # Odbicie lustrzane dla lewego oka
    if oko == "OS":
        img = np.fliplr(img)

    ax.imshow(img, extent=[0, 400, 0, 400], aspect='auto', alpha=0.7)
    ax.axis('off')  # usuń osie

    # Funkcja do odbicia X względem środka 210
    def flip_x(x):
        return 400 - x if oko == "OS" else x

    # dołeczek
    ax.scatter(flip_x(210), 210, color='#F4B20B', s=30, zorder=10)
    ax.text(flip_x(210), 210, "f", color='#F4B20B', fontsize=20, ha='left', va='bottom', zorder=11)
    # punkt ekscentryczny
    ax.scatter(flip_x(210+fiksacja*3), 210, color="#5D21BD", s=30, zorder=10)
    ax.text(flip_x(210+fiksacja*3), 210, "e", color='#5D21BD', fontsize=20, ha='right', va='bottom', zorder=11)
    # punkt anomalny
    ax.scatter(flip_x(210+kat_anomalii*3), 210, color="#1B9FA8", s=30, zorder=10)
    ax.text(flip_x(210+kat_anomalii*3), 210, "a", color='#1B9FA8', fontsize=20, ha='right', va='top', zorder=11)
    # punkt zerowy
    ax.scatter(flip_x(210+kat_obiektywny*3), 210, color='#291D27', s=30, zorder=10)
    ax.text(flip_x(210+kat_obiektywny*3), 210, "0", color='#291D27', fontsize=20, ha='left', va='top', zorder=11)
    st.pyplot(fig)

# --- schemat 2D --- dodać punkty na rysunku!

with col2:

    st.markdown("### schemat 2D")
    # Oko prawe (OP)
    fig_op, ax_op = plt.subplots(figsize=(2, 2), dpi=100, facecolor='none')
    ax_op.set_facecolor('none')
    if oko == "OD":        
        t_op = transforms.Affine2D().rotate_deg_around(130, 130, kat_obiektywny) + ax_op.transData
    else:
        t_op = ax_op.transData
    circle_op = Circle((130, 130), 40, edgecolor="#DBDBDB", facecolor='none', lw=2, transform=t_op)
    ax_op.add_patch(circle_op)
    cornea_op = Arc((130, 182), 70, 60, angle=0, theta1=220, theta2=320, edgecolor="#DBDBDB", lw=2, transform=t_op)
    ax_op.add_patch(cornea_op)
    ax_op.scatter(130, 90, color='#F4B20B', s=30, zorder=10, transform=t_op)
    ax_op.set_xlim(80, 180)
    ax_op.set_ylim(80, 180)
    ax_op.set_aspect('equal')
    ax_op.axis('off')
   

    # Oko lewe (OL) - odbicie lustrzane
    fig_ol, ax_ol = plt.subplots(figsize=(2, 2), dpi=100, facecolor='none')
    ax_ol.set_facecolor('none')
    if oko == "OS":        
        t_ol = transforms.Affine2D().rotate_deg_around(130, 130, kat_obiektywny) + ax_ol.transData
    else:
        t_ol = ax_ol.transData
    circle_ol = Circle((130, 130), 40, edgecolor="#DBDBDB", facecolor='none', lw=2, transform=t_ol)
    ax_ol.add_patch(circle_ol)
    cornea_ol = Arc((130, 182), 70, 60, angle=0, theta1=220, theta2=320, edgecolor="#DBDBDB", lw=2, transform=t_ol)
    ax_ol.add_patch(cornea_ol)
    ax_ol.scatter(130, 90, color='#F4B20B', s=30, zorder=10, transform=t_ol)
    ax_ol.set_xlim(80, 180)
    ax_ol.set_ylim(80, 180)
    ax_ol.set_aspect('equal')
    ax_ol.axis('off')
    ax_ol.invert_xaxis()
     

    c1, c2 = st.columns(2)
    with c1:
        st.pyplot(fig_ol)
    with c2:
        st.pyplot(fig_op)
    
    if kat_ct > 0:
        kierunek = "z nosa"
    elif kat_ct < 0:
        kierunek = "ze skroni"
    else:
        kierunek = "brak ruchu"
    st.write(f"    Ruch nastawczny przy CT: {kierunek}, {kat_ct}°")
    st.write(f"    Kąt anomalii: {kat_anomalii}°")

    # Typ korespondencji wg reguł użytkownika
    def typ_korespondencji(kat_anomalii, kat_subiektywny, kat_obiektywny):
        if kat_anomalii == 0:
            return "Korespondencja Prawidłowa (NRC)"
        elif kat_subiektywny == 0 and kat_anomalii == kat_obiektywny:
            return "Korespondencja Nieprawidłowa Harmonijna (Harc)"
        elif abs(kat_subiektywny) > 0 and abs(kat_subiektywny) < abs(kat_obiektywny) and (kat_subiektywny * kat_obiektywny > 0):
            return "Korespondencja Nieprawidłowa Nieharmonijna (Uharc)"
        elif (kat_subiektywny > 0 and kat_obiektywny < 0) or (kat_subiektywny < 0 and kat_obiektywny > 0):
            return "Korespondencja Paradoksalna Typu I"
        elif abs(kat_subiektywny) > abs(kat_obiektywny):
            return "Korespondencja Paradoksalna Typu II"
        else:
            return "Inny/Nietypowy stan kliniczny"

    typ_korespondencji_wynik = typ_korespondencji(kat_anomalii, kat_subiektywny, kat_obiektywny)
    st.write(f"{typ_korespondencji_wynik}")

    

col3, col4, col5 = st.columns(3)
with col3:
       
# --- maddox ---
    st.markdown("### test maddoxa") 
    st.write("szkiełko maddoxa OP")
    fig_maddox, ax_maddox = plt.subplots(figsize=(4, 4), dpi=100, facecolor='none')
    # Rysowanie żółtego plusika z kropką na środku
    center = (2, 2)
    ramie = 1.5  # długość ramienia
    ax_maddox.plot([center[0] - ramie, center[0] + ramie], [center[1], center[1]], color="#E6E2CE", lw=12, zorder=10)
    ax_maddox.plot([center[0], center[0]], [center[1] - ramie, center[1] + ramie], color="#E6E2CE", lw=12, zorder=10)
    # Zamiast słoneczka, wstawiamy znak ☀︎
    txt = ax_maddox.text(center[0], center[1] - 0.1, '☀︎', fontsize=60, ha='center', va='center', color='#F5DC51', zorder=20)
    txt.set_path_effects([path_effects.Stroke(linewidth=2, foreground="#16181D"), path_effects.Normal()])
    ax_maddox.set_xlim(0, 4)
    ax_maddox.set_ylim(0, 4)
    ax_maddox.set_aspect('equal')
    ax_maddox.axis('off')

    # linia czerwona - przesunięcie w zależności od kąta subiektywnego
    if oko == "OS":
        x= -kat_subiektywny/20  # skalowanie kąta do rysunku
    else:
        x=kat_subiektywny/20  # skalowanie kąta do rysunku
    ax_maddox.plot([center[0] + x, center[0] + x], [center[1] - ramie, center[1] + ramie], color="#E21E2ECC", lw=4, zorder=30)

    st.pyplot(fig_maddox)


with col4:
    # --- worth ---
    #oko prawe czerwony filtr (widzi czerwone kształty), oko lewe zielony filtr
    
    st.markdown("### test wortha")
    st.write("OP-red, OL-green")

    fig_worth, ax_worth = plt.subplots(figsize=(2, 2), dpi=100, facecolor='none')

    #przesunięcia poziome
    if oko == "OD":
        x_offset_red = kat_subiektywny / 40  # skalowanie kąta do rysunku
        x_offset_green = 0
    else:
        x_offset_red = 0
        x_offset_green = kat_subiektywny / 40
    
    # Czerwone obiekty (widoczne dla jednego oka)
    ax_worth.scatter(1 + x_offset_red, 0.6, color='#FF414B', s=120, zorder=20, edgecolors='none')  # kółko
    ax_worth.scatter(1 + x_offset_red, 1.4, color="#FF414B", marker='D', s=100, zorder=10, edgecolors='none')  # romb
    # Zielone obiekty (widoczne dla drugiego oka)
    ax_worth.scatter(0.6 + x_offset_green, 1, color='#41FF6A', marker='P', s=120, zorder=10, edgecolors='none')  # krzyżyk
    ax_worth.scatter(1.4 + x_offset_green, 1, color='#41FF6A', marker='P', s=120, zorder=10, edgecolors='none')  # krzyżyk
    ax_worth.scatter(1 + x_offset_green, 0.6, color="#41FF6A", s=120, zorder=10, edgecolors='none')  # kółko
    ax_worth.set_xlim(0, 2)
    ax_worth.set_ylim(0, 2)
    ax_worth.set_aspect('equal')
    ax_worth.axis('off')
    
    st.pyplot(fig_worth)


with col5:
# --- rlt ---
    st.markdown("### rlt")
    #oko prowadzące czerwony filtr + pryzmat dysocjujący baza dół
    st.write("FE-red+10Δ BD")
    fig_rlt, ax_rlt = plt.subplots(figsize=(2, 2), dpi=100, facecolor='none')

    #przesunięcia poziome
    if oko == "OD":
        x_offset_red = kat_subiektywny / 40  # skalowanie kąta do rysunku
    else:
        x_offset_red = -kat_subiektywny / 40 

    x_offset_white = 0
    y_offset = -0.25  # przesunięcie pionowe dla bazy dół
    # Czerwone obiekty (widoczne dla jednego oka)
    ax_rlt.scatter(1 + x_offset_red, 1 - y_offset, color='#FF414B', s=120, zorder=20, edgecolors='none')  # kółko
       
    ax_rlt.scatter(1 + x_offset_white, 1, color="#F5DC51", s=120, zorder=10, edgecolors='none')  # kółko
    ax_rlt.set_xlim(0, 2)
    ax_rlt.set_ylim(0, 2)
    ax_rlt.set_aspect('equal')
    ax_rlt.axis('off')
    
    st.pyplot(fig_rlt)

col6, col7, col8 = st.columns(3)
with col6:
    st.markdown("### bagolini")
    st.write("okulary typ V")
    fig_bago, ax_bago = plt.subplots(figsize=(4, 4), dpi=100, facecolor='none')

    ax_bago.set_xlim(0, 2)
    ax_bago.set_ylim(0, 2)
    ax_bago.set_aspect('equal')
    ax_bago.axis('off')


     #przesunięcia poziome
    if oko == "OD":
        x_offset_bgop = kat_subiektywny / 40  # skalowanie kąta do rysunku
        x_offset_bgol = 0
    else:
        x_offset_bgop = 0
        x_offset_bgol = kat_subiektywny / 40

    # op
    ax_bago.plot([0.4+x_offset_bgop, 1.6+x_offset_bgop], [0.4, 1.6], color="#F5DC51", lw=2)
    ax_bago.scatter(1+x_offset_bgop, 1, color="#F5DC51", s=1000, marker=r'$\hermitmatrix$', zorder=10, edgecolors='none')
    # ol
    ax_bago.plot([1.6+x_offset_bgol, 0.4+x_offset_bgol], [0.4, 1.6], color="#F5DC51", lw=2)
    ax_bago.scatter(1+x_offset_bgol, 1, color="#F5DC51", s=1000, marker=r'$\hermitmatrix$', zorder=10, edgecolors='none')
    
    st.pyplot(fig_bago)

with col7:
    st.markdown("### powidoki h-b")
    st.write("FE ( ¦ ), AE (╌)")
    fig_afterimage, ax_afterimage = plt.subplots(figsize=(4, 4), dpi=100, facecolor='none')
    
      #przesunięcia poziome
    if oko == "OD":
        x_offset_afterimage = kat_anomalii / 120  # skalowanie kąta do rysunku
        
    else:
        x_offset_afterimage = - kat_anomalii / 120
        
        
    # pozioma - AE
    ax_afterimage.plot([0.1+x_offset_afterimage, 0.45 +x_offset_afterimage], [0.5, 0.5], color="#4ECFE6", lw=8, zorder=10)
    ax_afterimage.plot([0.55+x_offset_afterimage, 0.9+x_offset_afterimage], [0.5, 0.5], color="#4ECFE6", lw=8, zorder=10)
    
    # pionowa - FE
    ax_afterimage.plot([0.5, 0.5], [0.1, 0.45], color="#4ECFE6", lw=8, zorder=10)
    ax_afterimage.plot([0.5, 0.5], [0.55, 0.9], color="#4ECFE6", lw=8, zorder=10)
    ax_afterimage.set_xlim(0, 1)
    ax_afterimage.set_ylim(0, 1)
    ax_afterimage.set_aspect('equal')
    ax_afterimage.axis('off')

    st.pyplot(fig_afterimage)

  
with col8:
    st.markdown("### transfer powidoku")
    st.write("FE ( ¦ ), AE obserwuje mitt")
    fig_mitt, ax_mitt = plt.subplots(figsize=(4, 4), dpi=100, facecolor='none')
    # Granatowy kwadrat
    ax_mitt.add_patch(plt.Rectangle((0.2, 0.2), 0.6, 0.6, color="#1E51EBFF", zorder=5))
    # Czarna kropka na środku
    ax_mitt.scatter(0.5, 0.5, color='black', s=100, zorder=10)
    #naświetlamy oko dominujące, obserwuje oko niedowidzące
    if oko == "OD":
        x_offset_ai = (kat_anomalii-fiksacja) / 120  # skalowanie kąta do rysunku
        x_offset_heid = -fiksacja / 120  # skalowanie kąta do rysunku
       
    else:
        x_offset_ai = -(kat_anomalii-fiksacja) / 120  # skalowanie kąta do rysunku
        x_offset_heid = fiksacja / 120  # skalowanie kąta do rysunku


    # powidoki
    ax_mitt.plot([0.5+x_offset_ai, 0.5+x_offset_ai], [0.1, 0.45], color="#4ECFE6C7", lw=8, zorder=10)
    ax_mitt.plot([0.5+x_offset_ai, 0.5+x_offset_ai], [0.55, 0.9], color="#4ECFE6C7", lw=8, zorder=10)
    #figura Heidingera
    ax_mitt.text(0.503+ x_offset_heid, 0.495, '$\\infty$', fontsize=30, ha='center', va='center', color='#F5DC51', rotation=90, zorder=20)
    ax_mitt.set_xlim(0, 1)
    ax_mitt.set_ylim(0, 1)
    ax_mitt.set_aspect('equal')
    ax_mitt.axis('off')
    st.pyplot(fig_mitt)

    
