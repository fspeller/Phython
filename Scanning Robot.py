import time
import datetime

import pyautogui
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


import pywhatkit
from flask import Flask, request

#im1 = pyautogui.screenshot()
#im1 = im1.save("ScreenShot.jpg")
#exit()


# Open Website
browser = webdriver.Chrome(executable_path=r"C:\Users\user\Downloads\chromedriver.exe")
browser.get('https://www.exteriores.gob.es/Consulados/lahabana/es/ServiciosConsulares/Paginas/index.aspx?scco=Cuba'
            '&amp;amp;scd=166&amp;amp;scca=Visados&amp;amp;scs=Visados+de+familiar+de+ciudadano+de+la+Uni%c3%b3n')

pyautogui.hotkey('win', 'up')
actions = ActionChains(browser)

category = Select(browser.find_element(By.XPATH,
                     '//select[@id="ctl00_ctl45_g_edd31fb6_ac81_4417_a981_52a85dac1b3b_ctl00_ddlCategories"]'))
category.select_by_visible_text("Visados")


service = Select(browser.find_element(By.XPATH,
                     '//select[@id="ctl00_ctl45_g_edd31fb6_ac81_4417_a981_52a85dac1b3b_ctl00_ddlService"]'))
service.select_by_visible_text("Visados de familiar de ciudadano de la Unión")

browser.find_element(By.XPATH, '//input[@value="Buscar"]').click()

try:
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Reservar cita para visado')))
except:
    browser.find_element(By.XPATH, '//input[@value="Buscar"]').click()
    time.sleep(5)
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Reservar cita para visado')))

browser.find_element(By.LINK_TEXT, 'Reservar cita para visado').click()

# Scan

    # Press Continue Button
scan = "No Appointment"
while scan == "No Appointment":

    try:
        time.sleep(10)
        xcontinue, ycontinue= pyautogui.locateCenterOnScreen(
                r'C:\Users\user\PycharmProjects\Scanning_Robot\Buttons\Continue Button.jpg'
                , confidence=0.7)
        pyautogui.moveTo(xcontinue, ycontinue)
        pyautogui.click(xcontinue, ycontinue)
        time.sleep(15)
    except:
        xback, yback = pyautogui.locateCenterOnScreen(
            r'C:\Users\user\PycharmProjects\Scanning_Robot\Buttons\Back.jpg'
            , confidence=0.7)
        pyautogui.doubleClick(xback, yback)
        time.sleep(5)
        xcontinue, ycontinue = pyautogui.locateCenterOnScreen(
            r'C:\Users\user\PycharmProjects\Scanning_Robot\Buttons\Continue Button.jpg'
            , confidence=0.7)
        pyautogui.moveTo(xcontinue, ycontinue)
        pyautogui.click(xcontinue, ycontinue)
        time.sleep(15)

    # Scan for Appointments
    try:
        xsearch, ysearch = pyautogui.locateCenterOnScreen(
            r'C:\Users\user\PycharmProjects\Scanning_Robot\Buttons\No Appointments.jpg'
            , confidence=0.7)
        pyautogui.click(xsearch, ysearch)
        xback, yback = pyautogui.locateCenterOnScreen(
            r'C:\Users\user\PycharmProjects\Scanning_Robot\Buttons\Back.jpg'
            , confidence=0.7)
        pyautogui.click(xback, yback)
        scan = "No Appointment"
    except:
        now = datetime.datetime.now()
        scan = "Appointment Found"
        pywhatkit.sendwhatmsg('+162955555555', scan, now.hour, now.minute + 1)



