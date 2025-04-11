import undetected_chromedriver as uc
import pickle


def init_webdriver_ec(headless=False, pos="maximizada"):

    options = uc.ChromeOptions()
    # desactivar el guardado de credenciales - el mensaje que aparece.
    #options.add_argument("--password-store=basic")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")


    # Desactivar las características de automatización
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")


    # Agregar un user-agent simulado para evitar que el bot sea detectado.
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    options.add_experimental_option(
        "prefs",
        {   
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
    )
    driver = uc.Chrome(
        options=options,
        headless=headless,
        log_level=3
    )

    if not headless:
        driver.maximize_window()
        if pos != "maximizada":
            ancho, alto = driver.get_window_size().values()
            if pos == "izquierda":
                driver.set_window_rect(x=0,y=0,width=ancho//2,height=alto)
            elif pos == "derecha":
                driver.set_window_rect(x=ancho//2,y=0,width=ancho//2,height=alto)

    return driver

