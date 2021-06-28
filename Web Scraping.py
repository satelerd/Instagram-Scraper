from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import time
import xlsxwriter

# AQUI DEBES LLENAR LOS DATOS
# -------------------------------------------------------
perfil = "nombre_perfil" # AQUI VA EL NOMBRE DEL PERFIL QUE QUIERES HACER SCRAPE (sin @)
username = "tu_usuario" # AQUI VA TU NOMBRE DE USUARIO DE INSTAGRAM
clave = "tu_clave" # AQUI VA TU CLAVE DE INSTAGRAM
# -------------------------------------------------------

# WEB SCRAPING
tiempo1 = time.time()
PATH = "C:\Program Files (x86)\chromedriver.exe"  # Direccion de donde tengo instalado el driver en mi computador
driver = webdriver.Chrome(PATH)  # Usar el driver en Chrome

url = f"https://www.instagram.com"
driver.get(url)  # Abre Chrome con la pagina del url
sleep(2)

# Inicia sesíon
usuario = driver.find_element_by_name("username")
usuario.send_keys(username)  
contrasena = driver.find_element_by_name("password")
contrasena.send_keys(clave)  
contrasena.send_keys(Keys.RETURN)  # Apreta enter
sleep(5)


# Busca el perfil
def buscador(perfilx):
    driver.get(f"https://www.instagram.com/{perfilx}/")


# Obtiene el numero de seguidores de la cuenta
def topbar():
    selenium_code_lenpost = driver.find_elements_by_class_name("g47SY ")

    elementos = []
    for elemento in selenium_code_lenpost:
        elementos.append(elemento.text)

    # Cantidad de publicaciones
    lenpost = ""
    for num in elementos[0]:  # Para poder borrar la coma
        if num != ",":
            lenpost += num
        else:
            continue
    lenpost = int(lenpost)

    # Cantidad de seguidores
    n_seguidores = ""
    for num in elementos[1]:  # Para poder borrar la coma
        if num != ",":
            n_seguidores += num
        else:
            continue
    n_seguidores = int(n_seguidores)

    # Cantidad de seguidos
    n_seguidos = ""
    for num in elementos[2]:  # Para poder borrar la coma
        if num != ",":
            n_seguidos += num
        else:
            continue
    n_seguidos = int(n_seguidos)

    return lenpost, n_seguidores, n_seguidos


# Consigue los links, likes y fecha de cada publicacion
def post_a_post(lenpost):
    # selenium_code_fechas = driver.find_elements_by_tag_name("img")  # Te entrega los links pero en formato selenium

    # Variables
    links = []
    likes = []
    aria_label = []
    comentarios = []
    repeticiones = int((lenpost * 2) / 36) - 1

    for i in range(repeticiones):
        selenium_code_links = driver.find_elements_by_tag_name("a")  # Te entrega los links pero en formato selenium
        selenium_code_arealabel = driver.find_elements_by_tag_name("span")
        selenium_code_links = driver.find_elements_by_tag_name("a")
        aria_label_repeticiones = []
        cont = 0

        """# Aria label primera parte
        for i in selenium_code_arealabel:
            aria_label_act = i.get_attribute("aria-label")
            if aria_label_act is None or aria_label_act == 'Siguiendo' or aria_label_act == 'Relaciones':
                continue
            else:
                aria_label_repeticiones.append(aria_label_act)
        print("arialabelrepeticiones: ", aria_label_repeticiones)"""

        # Links y Likes
        for publicacion in selenium_code_links:
            link = publicacion.get_attribute("href")  # Lo pasa a formato html y lo appendea a links_total

            if link in links:
                continue

            if "/p/" in link:  # Filtra los links que no son publicaciones

                # Links
                links.append(link)  # Apendea los links necesarios

                # Likes
                hover = ActionChains(driver).move_to_element(publicacion)
                hover.perform()
                code = driver.find_elements_by_class_name("-V_eO")
                likes.append(code[0].text)
                comentarios.append(code[1].text)

                """# Aria label segunda parte
                todopost = publicacion.find_elements_by_class_name("eLAPa")  # Todos los post tienen esta class

                try:
                    especiales = publicacion.find_element_by_class_name("u7YqG")  # Solo los post que son distintos a una foto tienen esta class
                    print("try: ", especiales)
                except:
                    especiales = None

                if especiales is None:
                    aria_label.append("Foto")
                else:
                    aria_label.append("especiales")  # aca me gustaria hacer append del tipo de post que es..."""

        # Scroll
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        sleep(2)

    return links, likes, comentarios


# Abre una pestaña para cada publicacion
def pestana(links):
    fechas = []
    aria_label = []

    for link in links:
        driver.execute_script("window.open('');")  # Abre una nueva pestaña
        driver.switch_to.window(driver.window_handles[1])  # Cambia a la nueva pestaña
        driver.get(link)  # Abre el link

        # Fechas
        selenium_code = driver.find_element_by_tag_name("time")  # Te entrega los datos pero en formato selenium
        fechas.append(selenium_code.get_attribute("title"))  # Lo pasa a formato html y lo appendea a fechas

        # Aria label
        try:
            selenium_code_video = driver.find_element_by_tag_name("video")
            aria_label.append("Video")
        except:
            aria_label.append("Foto")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return fechas, aria_label


# def tzeirei():


# Data
buscador(perfil)
lenpost_tz, seguidores_tz, seguidos_tz = topbar()
links_tz, likes_tz, comentarios_tz = post_a_post(lenpost_tz)
fechas_tz, aria_label_tz = pestana(links_tz)

# Prints
print(f"{perfil} tiene {lenpost_tz} publicaciones")
print(f"{perfil} tiene {seguidores_tz} seguidores")
print(f"{perfil} tiene {seguidos_tz} seguidos")
print(f"Los links de los post de {perfil} son: {links_tz}")
print(len(links_tz))
print(f"los likes de los post de {perfil} son: {likes_tz}")
print(len(aria_label_tz))
print(f"El numero de comentarios por cada post de {perfil} son: {comentarios_tz}")
print(f"la fecha de los post son: {fechas_tz}")
print(f"El area label de por cada post de {perfil} son: {aria_label_tz}")
print(len(aria_label_tz))

print()
print()

driver.quit()

# EXCEL

# Crea el file
wb = xlsxwriter.Workbook("Web Scraping Instagram.xlsx")
sheet = wb.add_worksheet()

# Formatos
color_tz = wb.add_format({"bg_color": "#94e5ff", "border": 2})
border1 = wb.add_format({"border": 1})
border2 = wb.add_format({"border": 2})

# Creamos las pestañas de tipo de datos
sheet.write(0, 0, "Cuenta", border2)
sheet.write(0, 1, "Tipo de post", border2)
sheet.write(0, 2, "Likes", border2)
sheet.write(0, 3, "Comentarios", border2)
sheet.write(0, 4, "Fecha", border2)
sheet.write(0, 5, "Link", border2)

# Numero de post, seguidores y seguidos
sheet.write(0, 8, "Publicaciones", border2)
sheet.write(0, 9, "Seguidores", border2)
sheet.write(0, 10, "seguidos", border2)

sheet.write(1, 7, f"Tzeirei Ami", color_tz)

# Rows

row = 1

# Rows Tzeirei
sheet.write(1, 8, lenpost_tz, border1)
sheet.write(1, 9, seguidores_tz, border1)
sheet.write(1, 10, seguidos_tz, border1)

for i in range(len(links_tz)):
    sheet.write(i + row, 0, "tzeireiami", color_tz)  # Cuenta
    sheet.write(i + row, 1, aria_label_tz[i], border1)  # Tipo de post
    sheet.write(i + row, 2, int(likes_tz[i]), border1)  # Likes
    sheet.write(i + row, 3, int(comentarios_tz[i]), border1)  # Comentarios
    sheet.write(i + row, 4, fechas_tz[i], border1)  # Fecha
    sheet.write(i + row, 5, links_tz[i], border1)  # Links
row += len(links_tz)

wb.close()

tiempo2 = time.time()

print(f"Fueron: {tiempo2 - tiempo1}")
