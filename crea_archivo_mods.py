import sys
import os
import discord


#Variables
TOKEN = 'token'
GUILD = 'Nombre Servidor'
#Introduce la id del canal
CANAL = 12

#Aqui crea el fichero que contiene todos los mods
ruta = sys.argv[1]
f = open("/opt/scripts/mods.txt", "w")
mods = ""
for file in os.listdir(ruta):
        mods+=file +" "
mods = mods.strip()
f.write(mods)
f.close()

#Aqui empieza la parte de discord
client = discord.Client(intents=discord.Intents.all())

#Este embed es el que contiene el listado de todos los mods.
mods_embes: discord.Embed = discord.Embed(title="Mods del servidor", color=0x0000FF)
mods_embes.set_thumbnail(url="https://i.blogs.es/8d2420/650_1000_java/1366_2000.png")
mods_embes.set_image(url="https://logolook.net/wp-content/uploads/2021/06/Symbol-Minecraft.png")
mods_embes.add_field(name="Carpeta de mods", value="[Carpeta de mods](https://drive.google.com/drive/folders/1oL4SzWVCRPBcAHNuZTiIxfkbYBmMIXt_?usp=sharing)", inline=False)

#Enviar mensaje con los mods existentes a discord
@client.event
async def on_ready():
    channel = client.get_channel(CANAL)
    for mod in mods:
        mods.add(mod)
        descripcion += "\n" + mod +"\n"
    
    mods_embes.description = descripcion
    await channel.send(embeds=[mods_embes])
