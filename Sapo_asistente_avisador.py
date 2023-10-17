import os
import discord
import sys
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

#Variables
TOKEN = 'token'
GUILD = 'Nombre Servidor'

#Introduce la id del canal
CANAL = 12

#Introduce la id del mensaje en el que se mostrara el listado de los mods.
#Es recomendable antes de ejecutar este script crearlo a mano o borrar el codigo referente
#al mensaje
MSG_MODS = 11

client = discord.Client(intents=discord.Intents.all())

#Aqui se crean los embeds, para hacer los mensajes de avisos mas vistoso
anyadido_embed: discord.Embed = discord.Embed(title="Se ha añadido un nuevo mod", color=0x32CD32)
anyadido_embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/57/57156.png")
anyadido_embed.set_image(url="https://logolook.net/wp-content/uploads/2021/06/Symbol-Minecraft.png")
eliminado_embed: discord.Embed = discord.Embed(title="Se ha eliminado un mod", color=0xff0000,)
eliminado_embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/41/41779.png")
eliminado_embed.set_image(url="https://logolook.net/wp-content/uploads/2021/06/Symbol-Minecraft.png")
actualizado_embed: discord.Embed = discord.Embed(title="Se ha actualizado un mod", color=0xffff00)
actualizado_embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/3489/3489659.png")
actualizado_embed.set_image(url="https://logolook.net/wp-content/uploads/2021/06/Symbol-Minecraft.png")

#Este embed es el que contiene el listado de todos los mods.
mods_embes: discord.Embed = discord.Embed(title="Mods del servidor", color=0x0000FF)
mods_embes.set_thumbnail(url="https://i.blogs.es/8d2420/650_1000_java/1366_2000.png")
mods_embes.set_image(url="https://logolook.net/wp-content/uploads/2021/06/Symbol-Minecraft.png")
mods_embes.add_field(name="Carpeta de mods", value="[Carpeta de mods](https://drive.google.com/drive/folders/1oL4SzWVCRPBcAHNuZTiIxfkbYBmMIXt_?usp=sharing)", inline=False)

#El primer argumento es la ruta en la que se encuentra la carpeta de mods

ruta = sys.argv[1]

#Es recomendable para usar pydrive en un servidor linux, usar una cuenta de servicio.
dir_creden = 'archivo donde estan las credenciales'

id_carpeta_drive = 'id carpeta de drive'



@client.event
async def on_ready():
    channel = client.get_channel(CANAL)
    mesg = await channel.fetch_message(MSG_MODS)
    mods = set()
    descripcion = ""
    descripcion = "**Estos son los mods del servidor:**\n\n"
    f = open("mods.txt", "r")
    l_mods = f.read().split()
    f.close()
    for mod in l_mods:
        mods.add(mod)
        descripcion += "\n" + mod +"\n"
    
    mods_embes.description = descripcion


    print(f'{client.user.name} sapo avisador está avisando')
    print("Mods", mods)
    
    descripcion = ""
    nuevo_mods: set = set()
    for file in os.listdir(ruta):
        nuevo_mods.add(file)

#Comprueba si se actualiza un mod

    if(len(mods)==len(nuevo_mods)):
        for m in nuevo_mods:
            if m not in mods:
                await cambiar_contenido(nuevo_mods, mesg)
                descripcion = "**Se ha actualizado el mod " + m + ", revisen en sus carpetas que las versiones de sus mods concuerden con las del hilo 'Mods del servidor'.**"
                actualizado_embed.description = descripcion
                await channel.send(embeds=[actualizado_embed])
                await channel.send('@everyone')
                ruta_mod = ruta +'/' + m
                actualizar_archivo(m, ruta_mod)

#Comprueba si se elimina un mod

    elif(len(mods)>len(nuevo_mods)):
        for m in mods:
            if m not in nuevo_mods:
                await cambiar_contenido(nuevo_mods, mesg)
                descripcion = "**Se ha eliminado el mod " + m + ", revisen en sus carpetas que hayan eliminado el mod, si no es el caso elimínenlo.**"
                eliminado_embed.description=descripcion
                await channel.send(embeds=[eliminado_embed])
                await channel.send('@everyone')
                eliminar_archivo(m)

#Comprueba si se anyade un mod

    else:
        for m in nuevo_mods:
            if m not in mods:
                await cambiar_contenido(nuevo_mods, mesg)
                descripcion = "**Se ha añadido el mod " + m + ", revisen sus carpetas para revisar lo tengan añadido, si no es el caso añádanlo.**"
                anyadido_embed.description = descripcion
                await channel.send(embeds=[anyadido_embed])
                await channel.send('@everyone')
                ruta_mod = ruta + '/' + m
                subir_archivo(ruta_mod, id_carpeta_drive)
                
    print("Nuevos mods", nuevo_mods)
    mods = nuevo_mods
    escribe_mods(mods)
    cerrar()

    
''''
@client.event
async def on_message(message: discord.Message):
    if(message.author == client.user):
        cerrar()
'''
#Escribe la descripcion que mostrara en discord los mods que hay  

async def cambiar_contenido(mods, mesg: discord.Message):
    descripcion = "**Estos son los mods del servidor:**\n\n"
    for m in mods:
        descripcion += "\n" + m + "\n"
    mods_embes.description = descripcion
    await mesg.edit(embed = mods_embes)

def cerrar():
    quit(0)

#Escribe los mods en el fichero donde se guarda que mods hay hasta ahora

def escribe_mods(mods):
    f = open("mods.txt", "w")
    s_mods = ""
    for mod in mods:
            s_mods+=mod +" "
    s_mods = s_mods.strip()
    f.write(s_mods)
    f.close()

#Inicio sesion

def login():
    #En service config se debe poner la ruta al archivo que contiene el secrets de la cuenta de servicio
    settings = {
        "client_config_backend": "service",
        "service_config": {
            "client_json_file_path": "/opt/scripts/service_secrets.json",
        }
    }
    gauth = GoogleAuth(settings=settings)
    gauth.ServiceAuth()
    return GoogleDrive(gauth)

#Subir archivo

def subir_archivo(ruta_archivo, carpeta):
    credenciales = login()
    archivo = credenciales.CreateFile({'parents': [{'kind': 'drive#fileLink', 'id': carpeta}]})
    archivo['title'] = ruta_archivo.split('/')[-1]
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload()

#Buscar archivo

def busca_archivo(nombre):
    credenciales = login()
    query = {'q': f"title = '{nombre}'"}
    archivo = credenciales.ListFile(query).GetList()
    print(archivo)
    if len(archivo)>0:
        return archivo[0]
    return -1

#Eliminar un archivo

def eliminar_archivo(nombre):
    credenciales = login()
    archivo = busca_archivo(nombre)
    if archivo != -1:
        archivo.Delete()

#Actualiza un archivo

def actualizar_archivo(nombre, ruta_archivo):
    credenciales = login()
    archivo = busca_archivo(nombre)
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload()

client.run(TOKEN)