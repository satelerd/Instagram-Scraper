from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import time
import xlsxwriter

# AQUI DEBES LLENAR LOS DATOS
# -------------------------------------------------------
profile = "" # AQUI VA EL NOMBRE DEL PERFIL QUE QUIERES HACER SCRAPE (sin @)
username = "" # AQUI VA TU NOMBRE DE USUARIO DE INSTAGRAM
password = "" # AQUI VA TU CLAVE DE INSTAGRAM
PATH = "C:\Program Files (x86)\chromedriver.exe"  # Direccion de donde tienes instalado el driver en tu computador
# -------------------------------------------------------

# WEB SCRAPING
tiempo1 = time.time()

driver = webdriver.Chrome(PATH)  # Usar el driver en Chrome

url = f"https://www.instagram.com"
driver.get(url)  # Abre Chrome con la pagina del url
sleep(2)

# Inicia sesíon
user = driver.find_element_by_name("username")
user.send_keys(username)  
pwd = driver.find_element_by_name("password")
pwd.send_keys(password)  
pwd.send_keys(Keys.RETURN)  # Apreta enter
sleep(5)

# FUNCIONES
# Busca el perfil
def finder(profilex):
    driver.get(f"https://www.instagram.com/{profilex}/")


# Obtiene el numero de seguidores de la cuenta
def topbar():
    selenium_code_lenpost = driver.find_elements_by_class_name("g47SY ")

    elements = []
    for element in selenium_code_lenpost:
        elements.append(element.text)

    # Cantidad de publicaciones
    lenpost = ""
    for num in elements[0]:  # Para poder borrar la coma
        if num != ",":
            lenpost += num
        else:
            continue
    lenpost = int(lenpost)

    # Cantidad de seguidores
    n_followers = ""
    for num in elements[1]:  # Para poder borrar la coma
        if num != ",":
            n_followers += num
        else:
            continue

    # Cantidad de seguidos
    n_follows = ""
    for num in elements[2]:  # Para poder borrar la coma
        if num != ",":
            n_follows += num
        else:
            continue
    n_follows = int(n_follows)

    return lenpost, n_followers, n_follows


# Consigue los links, likes y fecha de cada publicacion
def post_to_post(lenpost):
    # selenium_code_fechas = driver.find_elements_by_tag_name("img")  # Te entrega los links pero en formato selenium

    # Variables
    links = []
    likes = []
    comments = []
    repetitions = int((lenpost * 2) / 36) - 1
    print(repetitions)

    for i in range(repetitions):
        selenium_code_links = driver.find_elements_by_tag_name("a")  # Te entrega los links pero en formato selenium
        selenium_code_links = driver.find_elements_by_tag_name("a")

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
                comments.append(code[1].text)
     
        # Scroll
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        sleep(2)

    return links, likes, comments


# Abre una pestaña para cada publicacion
def tab(links):
    dates = []
    aria_label = []

    for link in links:
        driver.execute_script("window.open('');")  # Abre una nueva pestaña
        driver.switch_to.window(driver.window_handles[1])  # Cambia a la nueva pestaña
        driver.get(link)  # Abre el link

        # Fechas
        selenium_code = driver.find_element_by_tag_name("time")  # Te entrega los datos pero en formato selenium
        dates.append(selenium_code.get_attribute("title"))  # Lo pasa a formato html y lo appendea a fechas

        # Aria label
        try:
            selenium_code_video = driver.find_element_by_tag_name("video")
            aria_label.append("Video")
        except:
            aria_label.append("Foto")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return dates, aria_label

# FIN DE FUNCIONES


# DATA
finder(profile)
lenpost_tz, seguidores_tz, seguidos_tz = topbar()
links_tz, likes_tz, comments_tz = post_to_post(lenpost_tz)
dates, aria_label_tz = tab(links_tz)

# Prints
print(f"{lenpost_tz} publicaciones")
print(f"{seguidores_tz} seguidores")
print(f"{seguidos_tz} seguidos")
print(f"Los links de los post son: {links_tz}")
print(f"los likes de los post son: {likes_tz}")
print(f"El numero de comments por cada post son: {comments_tz}")
print(f"la fecha de los post son: {dates}")
print(f"El area label de por cada post son: {aria_label_tz}")

driver.quit()
# FIN DEL SCRAPE


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
sheet.write(0, 3, "comments", border2)
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
    sheet.write(i + row, 3, int(comments_tz[i]), border1)  # comments
    sheet.write(i + row, 4, dates[i], border1)  # Fecha
    sheet.write(i + row, 5, links_tz[i], border1)  # Links
row += len(links_tz)

wb.close()

tiempo2 = time.time()

print(f"Fueron: {int(tiempo2 - tiempo1)} segundos")
