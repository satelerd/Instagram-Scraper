from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import time
import xlsxwriter

# AQUI DEBES LLENAR LOS DATOS
# -------------------------------------------------------
profile = "santiagoadicto"    # AQUI VA EL NOMBRE DEL PERFIL QUE QUIERES HACER SCRAPE (sin @)
username = "sateler"   # AQUI VA TU NOMBRE DE USUARIO DE INSTAGRAM
password = ""   # AQUI VA TU CLAVE DE INSTAGRAM
n_post = 50  # AQUI VA LA CANTIDAD DE PUBLICACIONES A LAS QUE SE QUIERE HACER SCRAPE (ej. si pongo 50, va a hacer scrape en las ultimas 50 publicaciones)


PATH = "C:\Program Files (x86)\chromedriver.exe"    # Direccion de donde tienes instalado el driver en tu computador
wb_PATH = ""    # Direccion de donde quieres que se guarde el archivo excel. Dejar vacio para guardarlo en el mismo directorio que este archivo.
# -------------------------------------------------------

# WEB SCRAPING
time1 = time.time()

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


# Correcion a los numeros cuando tienen simbolos o letras
def num_correction(metric):
    correction = ""
    comma = False
    for num in metric:
        if num == "." or num == ",":
            comma = True
            continue
        elif num == "k":
            correction += "000"
        elif num == "m":
            if comma == True:
                correction += "00000"
            else:
                correction += "000000"
            break
        else:
            correction += num
    return int(correction)


# Obtiene el numero de seguidores de la cuenta
def topbar():
    selenium_code_lenpost = driver.find_elements_by_class_name("g47SY ")

    elements = []
    for element in selenium_code_lenpost:
        elements.append(element.text)

    lenpost = num_correction(elements[0])   # Cantidad de publicaciones
    n_followers = num_correction(elements[1])   # Cantidad de seguidores
    n_follows = num_correction(elements[2])   # Cantidad de seguidos

    return lenpost, n_followers, n_follows


# Consigue los links, likes y fecha de cada publicacion
def post_to_post():
    # Variables
    links = []
    likes = []
    comments = []
    cont_post = 1

    for i in range(n_post):
        selenium_code_links = driver.find_elements_by_tag_name(
            "a")  # Te entrega los links pero en formato selenium
        selenium_code_links = driver.find_elements_by_tag_name("a")

        # Links y Likes
        for publicacion in selenium_code_links:
            # Lo pasa a formato html y lo appendea a links_total
            link = publicacion.get_attribute("href")

            if link in links:
                continue

            if "/p/" in link:  # Filtra los links que no son publicaciones
                cont_post += 1

                # Links
                links.append(link)  # Apendea los links necesarios

                # Likes
                hover = ActionChains(driver).move_to_element(publicacion)
                hover.perform()

                code = driver.find_elements_by_class_name("-V_eO")

                likes.append(num_correction(code[0].text))
                comments.append(num_correction(code[1].text))

                if cont_post == n_post + 1:
                    break

        if cont_post == n_post + 1:
            break

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
        driver.switch_to.window(driver.window_handles[1])   # Cambia a la nueva pestaña
        driver.get(link)  # Abre el link

        # Fechas
        # Te entrega los datos pero en formato selenium
        selenium_code = driver.find_element_by_tag_name("time")
        # Lo pasa a formato html y lo appendea a fechas
        dates.append(selenium_code.get_attribute("title"))

        # Aria label
        try:
            selenium_code_video = driver.find_element_by_tag_name("video")
            aria_label.append("Video")
        except:
            aria_label.append("Foto")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return dates, aria_label


# Crea el excel
def excel():
    # Crea el archivo
    wb = xlsxwriter.Workbook(f"{wb_PATH}Ws_{profile}.xlsx")
    sheet = wb.add_worksheet()

    # Formatos
    bg_color = wb.add_format({"bg_color": "#0099FF", "border": 2})
    border1 = wb.add_format({"border": 1})
    border2 = wb.add_format({"border": 2})

    # Creamos las pestañas de tipo de datos
    sheet.write(0, 0, "Tipo de post", border2)
    sheet.write(0, 1, "Likes", border2)
    sheet.write(0, 2, "comments", border2)
    sheet.write(0, 3, "Fecha", border2)
    sheet.write(0, 4, "Link", border2)

    # Numero de post, seguidores y seguidos
    sheet.write(0, 8, "Publicaciones", border2)
    sheet.write(0, 9, "Seguidores", border2)
    sheet.write(0, 10, "seguidos", border2)

    sheet.write(1, 7, f"{profile}", bg_color)

    # Rows
    row = 1

    sheet.write(1, 8, lenpost_prf, border1)
    sheet.write(1, 9, seguidores_prf, border1)
    sheet.write(1, 10, seguidos_prf, border1)

    for i in range(len(links_prf)):
        sheet.write(i + row, 0, aria_label_prf[i], border1)  # Tipo de post
        sheet.write(i + row, 1, likes_prf[i], border1)  # Likes
        sheet.write(i + row, 2, comments_prf[i], border1)  # comments
        sheet.write(i + row, 3, dates_prf[i], border1)  # Fecha
        sheet.write(i + row, 4, links_prf[i], border1)  # Links
    row += len(links_prf)

    wb.close()

    time2 = time.time()
    return (f"Fueron: {int(time2 - time1)} segundos")


# FIN DE FUNCIONES


# DATA
finder(profile)
lenpost_prf, seguidores_prf, seguidos_prf = topbar()
links_prf, likes_prf, comments_prf = post_to_post()
dates_prf, aria_label_prf = tab(links_prf)

# Prints
print(f"{lenpost_prf} publicaciones")
print(f"{seguidores_prf} seguidores")
print(f"{seguidos_prf} seguidos")
print(f"Los links de los post son: {links_prf}")
print(f"los likes de los post son: {likes_prf}")
print(f"El numero de comments por cada post son: {comments_prf}")
print(f"la fecha de los post son: {dates_prf}")
print(f"El area label de por cada post son: {aria_label_prf}")

driver.quit()

# EXCEL
xls = excel()
print(xls)
