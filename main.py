from docx import Document
from md2pdf.core import md2pdf
from selenium import webdriver
from selenium.webdriver.common.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from getpass import getpass
import time
import selenium
import json
import shutil
import os

def skopiuj_i_zmien_nazwe(plik_wejsciowy, nowa_nazwa):
    try:
        # Skopiuj plik
        nowa_nazwa = nowa_nazwa + ".md"
        shutil.copy2(plik_wejsciowy, nowa_nazwa)
        print(f"Plik {plik_wejsciowy} został skopiowany jako {nowa_nazwa}")
    except FileNotFoundError:
        print(f"Błąd: Plik {plik_wejsciowy} nie istnieje.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

    return nowa_nazwa

def open_json():
    # Otwórz plik JSON
    with open('.pass.json', 'r') as file:
        dane_json = json.load(file)

    # Odczytaj login z danych JSON
    login = dane_json.get('login', None)

    # Wydrukuj login
    if login:
        print(f"Odczytany login: {login}")
    else:
        print("Brak informacji o loginie w pliku JSON.")
    
    return login

def zamien_na_styl(text):
    # Zamień na małe litery
    text = text.lower()

    # Zamień spacje na znaki podkreślenia
    text = text.replace(' ', '_')

    # Zamień polskie znaki na odpowiedniki bez kropek
    polskie_znaki = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ż': 'z', 'ź': 'z'}
    for polski, zamiennik in polskie_znaki.items():
        text = text.replace(polski, zamiennik)

    return text

def zmien_login_w_md(sciezka_do_pliku_md, nowy_login):
    with open(sciezka_do_pliku_md, 'r') as file:
        lines = file.readlines()

    with open(sciezka_do_pliku_md, 'w') as file:
        for line in lines:
            if "Login:" in line:
                # Zamień całą linijkę po napotkaniu "Login:"
                line = f"Login: {nowy_login}\n"
            file.write(line)

def zmien_haslo_w_md(sciezka_do_pliku_md, haslo):
    with open(sciezka_do_pliku_md, 'r') as file:
        lines = file.readlines()

    with open(sciezka_do_pliku_md, 'w') as file:
        for line in lines:
            if "Hasło:" in line:
                # Zamień całą linijkę po napotkaniu "Login:"
                line = f"\nHasło: {haslo}\n"
            file.write(line)

def zmien_imie_nazwisko(sciezka_do_pliku_md, imie_nazwisko):
    with open(sciezka_do_pliku_md, 'r') as file:
        lines = file.readlines()

    if len(lines) > 1:
        lines[1] = f"{imie_nazwisko}\n"

    with open(sciezka_do_pliku_md, 'w') as file:
        file.writelines(lines)

def stworz_skrzynke_home(login):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Uruchomienie w trybie headless

    service = selenium.webdriver.chrome.service.Service()
    driver = webdriver.Chrome(service=service,options=chrome_options)

    wait = WebDriverWait(driver, 10)
    driver.get("https://panel.home.pl/")

    input_element = driver.find_element(By.CLASS_NAME, "m-input-field__input")
    input_element.send_keys(open_json())
    haslo = getpass("Podaj haslo do twojego konta: ")

    input_element = driver.find_element(By.NAME, "password")
    input_element.send_keys(haslo + Keys.ENTER)

    print("zalogowano, trwa tworzenie konta")
    time.sleep(5)

    driver.get("https://cp.home.pl/ccp/v/home.pl/mailboxes/mailbox-new-advanced")

    time.sleep(3)

    iframe = driver.find_element(By.ID,"http://home.pl/mailboxes")
    driver.switch_to.frame(iframe)

    # domena
    radio_button_xpath = '//*[@id="mailbox-new-advanced_chooseFieldSetDomain"]/div/div[1]/div/div/div[1]/label/span'
    radio_button = driver.find_element(By.XPATH,radio_button_xpath)
    radio_button.click()

    drop_down_menu = driver.find_element(By.ID, "mailbox-new-advanced_availableDomains")
    select = Select(drop_down_menu)
    select.select_by_value("likims.com")

    print("generowanie hasła")
    password_button = wait.until(EC.element_to_be_clickable((By.ID, "mailbox-new-advanced_mailboxPassword_generateBtn")))
    password_button.click()

    password_input = driver.find_element(By.ID, "mailbox-new-advanced_mailboxPassword_textbox")
    haslo = password_input.get_attribute("value")

    # mail
    input_element_id = "mailbox-new-advanced_mailboxName"
    input_element = driver.find_element(By.ID,input_element_id)

    # Poczekaj, aż element stanie się klikalny
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, input_element_id)))

    input_element.send_keys(login + Keys.ENTER)
    print("kończenie")
    time.sleep(5)

    driver.quit()

    return haslo

nazwa = input(" Wprowadź imię i nazwisko: ")
login = zamien_na_styl(nazwa)


sciezka_do_pliku_md = skopiuj_i_zmien_nazwe("test.md",login)

zmien_imie_nazwisko(sciezka_do_pliku_md,nazwa)
zmien_login_w_md(sciezka_do_pliku_md, login + "@likims.com")

haslo = stworz_skrzynke_home(login)

zmien_haslo_w_md(sciezka_do_pliku_md, haslo)

nazwa_pdf = nazwa + ".pdf"

md2pdf(nazwa_pdf,
       md_content=None,
       md_file_path=sciezka_do_pliku_md,
       css_file_path=None,
       base_url=None)
