import telebot
import pyscreenshot
import os
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

load_dotenv()

ADMINS = (
    1414138652,
)

bot = telebot.TeleBot(os.getenv('TOKEN_TELE_CRYPTO'))

@bot.message_handler(commands=["cid"])
def cmd_cid(m):
    bot.send_message(m.chat.id, str(m.chat.id))
    
@bot.message_handler(commands=["1"])
def cmd_captura_servidor(m):
    if es_admin(m.chat.id):
        print("Captura de pantalla")
        captura = pyscreenshot.grab()
        print("Gaurdando captura")
        captura.save("captura.png")
        print("Enviando captura al chat")
        bot.send_document(m.chat.id, open("captura.png", "rb"), caption="Captura del servidor")
        print("eliminar captura")
        os.remove("captura.png")

@bot.message_handler(commands=["2"])
def cmd_captura_navegador(m):
    if es_admin(m.chat.id):
        print("Capturamos navegador")
        driver.save_screenshot("captura_chrome.png")
        print("Gaurdando captura")
        #captura.save("captura_chrome.png")
        print("Enviando captura al chat")
        bot.send_document(m.chat.id, open("captura_chrome.png", "rb"), caption="Captura del servidor")
        print("eliminar captura")
        os.remove("captura_chrome.png")
        print("Seleccionado un elemento")
        e = driver.findelement(By.CSS_SELECTOR, "header.entry-header")
        e.screenshot("captura_elemento.png")
        print("Enviando captura al chat")
        bot.send_document(m.chat.id, open("captura_elemento.png", "rb"), caption="Captura del servidor")
        print("eliminar captura")
        os.remove("captura_element.png")
    


    
def es_admin(cid, info=True):
    if cid in ADMINS:
        return True
    else:
        if info:
            print(f'α {cid} no se encuentra autorizado')
            bot.send_message(cid, f'α {cid} no se encuentra autorizado', parse_mode="html")
            return False
        return False

def iniciar_webdriver():
    #options = Options()
    #if headless:
    #options.add_argument("--headless")
    #options.add_argument("--window-size=1920,1080")
    #ruta = ChromeDriverManager('./chromedriver').install()
    #ruta = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    #lista = [
    #    'enable-automotion',
    #    'enable-logging',
    #]
    #options.add_experimental_optiion('excludeSwitches', lista)
    #s = ChromiumService(ruta)
    #driver = webdriver.Chrome(service=s, options=options)
    #driver = webdriver.Chrome()
    urls = [

    'https://www.google.com/' 
        
        ]
    
    s = FirefoxService(r"./geckodriver")

    for url in urls:
        #driver = webdriver.Chrome(service=s)
        #driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        #driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver = webdriver.Firefox(service=s)
        driver.get(url)
        #web_element = driver.find_element(By.NAME, 'q')
        #web_element.send_keys("Selenium webdriver" + Keys.ENTER)
        #time.sleep(30)
        #driver.quit()

    #driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    return driver
    



if __name__ == '__main__':
    print("INIANDO WEBDRIVER")
    driver = iniciar_webdriver()
    print("Cargando pagina")
    driver.get("https://www.google.com/")
    print("BOT INICIADO")
    bot.infinity_polling()