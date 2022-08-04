# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 19:41:31 2021

@author: Pedro Caicedo Fandiño
"""

#Python
import os
import requests
import time
import winsound
#Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#Chrome
from webdriver_manager.chrome import ChromeDriverManager
#Utils
from utils import constants as c


def test_url(url):
    print('entra test')
    result = True
    cita = requests.get(url)
    print(cita)
    try:
        status_code = cita.status_code
        print(status_code)
        if status_code == 200:
            print(f'La página sirve {url}')
        else:
            print('la página no sirve')
    except Exception as e:
        print('error')
        print(e)
        result = False
    return result

def get_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    #options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path = ChromeDriverManager().install(), options = options)
    try:
        driver.get(url)
    except Exception as e:
        print(f"error {e}")
    return driver

def select_province(driver, exec_again, province):
    print("select province")
    print(province)
    try:
        print('Selecciona provincia')
        province_list = driver.find_element(By.XPATH, '//*[@id="form"]')
        province_list.send_keys(province)
    except Exception as e:
        print(f"error {e}")
        driver.close()
        exec_again = True
        return exec_again
    time.sleep(1)
    try:
        boton_aceptar = driver.find_element(By.XPATH, '//*[@id="btnAceptar"]')
        driver.execute_script("arguments[0].click();", boton_aceptar)
        print('Da click en aceptar la provincia')
    except Exception as e:
        print(f"error {e}")
        driver.close()
        exec_again = True
    print(exec_again)
    return exec_again

def select_office(driver, exec_again, office):
    print("select office")
    print(office)
    try:
        office_list = driver.find_element(By.XPATH, '//*[@id="tramiteGrupo[1]"]')
        office_list.send_keys(office)
        province_accept_btn = driver.find_element(By.XPATH, '//*[@id="btnAceptar"]')
        driver.execute_script("arguments[0].click();", province_accept_btn)
        time.sleep(1)
    except Exception as e:
        print(f"error {e}")
        driver.close()
        exec_again = True
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)
    print(exec_again)
    return exec_again

def fill_passport_form(driver, exec_again, user):
    print("fill passport form")
    try:
        docs_accept_btn = driver.find_element(By.XPATH, '//*[@id="btnEntrar"]')
        driver.execute_script("arguments[0].click();", docs_accept_btn)
        passport_btn = driver.find_element(By.XPATH, '//*[@id="comp04_id_citado"]/div[1]/fieldset/ul/li[2]/label')
        driver.execute_script("arguments[0].click();", passport_btn)
        passport_box = driver.find_element(By.XPATH, '//*[@id="txtIdCitado"]')
        passport_box.send_keys(user['passport'])
        name_box = driver.find_element(By.XPATH, '//*[@id="txtDesCitado"]')
        name_box.send_keys(user['full_name'])
        year_box = driver.find_element(By.XPATH, '//*[@id="txtAnnoCitado"]')
        year_box.send_keys(user['year'])
        country_box = driver.find_element(By.XPATH, '//*[@id="txtPaisNac"]')
        country_box.send_keys(user['country'])
        data_btn = driver.find_element(By.XPATH, '//*[@id="btnEnviar"]')
        driver.execute_script("arguments[0].click();", data_btn)
        print('Llena datos de la persona')
    except Exception as e:
        print(f"error {e}")
        driver.close()
        exec_again = True
    print(exec_again)
    return exec_again

def request_appointment(driver, exec_again):
    print("request appointment")
    try:
        appnt_btn = driver.find_element(By.XPATH, '//*[@id="btnEnviar"]')
        driver.execute_script("arguments[0].click();", appnt_btn)
        result = driver.find_element(By.XPATH, '//*[@id="mainWindow"]/div/div/section/div[2]/form/div[1]/p').text
        print('solicita cita')
        error = "En este momento no hay citas disponibles"
        print(result)
        if error in result:
            exit_btn = driver.find_element(By.XPATH, '//*[@id="btnSalir"]')
            driver.execute_script("arguments[0].click();", exit_btn)
            appointed = False
        else:
            appointed = True
        time.sleep(10)
    except Exception as e:
        print(f"error {e}")
        driver.close()
        exec_again = True
    print(appointed, exec_again)
    return appointed, exec_again


def get_appointment(user):
    province = user['province']
    office = user['office']
    appointed = False
    exec_again = True
    wait_time = 300
    tries = 0
    while exec_again == True:
        print('Inicia el proceso')
        driver = get_driver(c.APPOINTMENT_URL)
        while appointed == False:
            tries = tries + 1
            print(tries)
            
            exec_again = select_province(driver, exec_again, province)
            time.sleep(1)
            exec_again = select_office(driver, exec_again, office)
            time.sleep(1)
            exec_again = fill_passport_form(driver, exec_again, user)
            time.sleep(1)
            appointed, exec_again = request_appointment(driver, exec_again)
        print(f"exec again {exec_again}" )
        print(f"waiting {wait_time} seconds")
        time.sleep(wait_time)     
    return appointed, exec_again

def main():
    for user in c.USERS:       
        appointed, exec_again = get_appointment(user)
        print(appointed, exec_again)
        
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Process was interrupted')

