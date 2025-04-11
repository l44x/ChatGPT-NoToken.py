from discord import app_commands, Intents, Client, Interaction, Activity, ActivityType
import asyncio
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from init_webdriver_ec import init_webdriver_ec
import time as cm

class Bot(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync(guild=None)

bot = Bot(intents=Intents.default())

@bot.event
async def on_ready():
    await bot.change_presence(activity=Activity(type=ActivityType.playing, name="/help | Hexanot Bot"))
    print(f"Logged in as {bot.user.name} - {bot.user.id}")
    print("Bot is ready!")

@bot.tree.command(name="chatgpt", description="Habla con ChatGPT desde el bot.")
@app_commands.describe(mensaje="Mensaje que se enviará a ChatGPT")
async def chatgpt(interaction: Interaction, mensaje: str):
    await interaction.response.defer(thinking=True)

    def tarea_selenium(mensaje):
        try:
            driver = init_webdriver_ec(headless=False, pos="derecha")
            wait = WebDriverWait(driver, 20)

            driver.get("https://chatgpt.com/")
            cm.sleep(2)

            prompt = wait.until(ec.visibility_of_element_located((By.ID, "prompt-textarea")))
            prompt.send_keys(mensaje)
            cm.sleep(2)
            driver.execute_script('document.querySelector("#composer-submit-button").click()')
            cm.sleep(10)
            elementos_respuesta = wait.until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.markdown.prose.dark')))

            message_content=[]
            for message in elementos_respuesta:
                if message:
                    texto = message.text.strip()
                    message_content.append(texto)
                else:
                    print("No, tiene contenido. :/")

            driver.quit()
            return "\n".join(message_content) if message_content else "⚠️ No se encontró contenido en la respuesta."

        except TimeoutException:
            driver.quit()
            return "⏳ La página tardó demasiado en responder."
        except Exception as e:
            driver.quit()
            return f"❌ Ocurrió un error: {e}"


    respuesta = await asyncio.to_thread(tarea_selenium, mensaje)
    
    MAX_LENGTH = 1900
    partes = [respuesta[i:i+MAX_LENGTH] for i in range(0, len(respuesta), MAX_LENGTH)]

    try:    
        for i, parte in enumerate(partes):
            await interaction.followup.send(f"💬 **Respuesta de ChatGPT (Parte {i+1}):**\n```\n{parte}\n```")
    except:
            await interaction.followup.send(f"💬 Ha Ocurrido un Error. Vuelve a intentarlo. - Hexanot AI \n```")

bot.run("<YOUR-TOKEN-DISCORD>")
