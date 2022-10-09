import os
from decouple import config
from discord.ext import commands, tasks
import discord
import datetime
import requests


API_TOKEN = config("API_TOKEN")
TOKEN = config("TOKEN_SECRET")
#intents = discord.Intents.default()
#intents = discord.Intents.all()
#intents.members = True

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

# bot = commands.Bot("!") -> Todos os comandos do bot terão o prefixo !

# def load_cogs(bot):
#     bot.load_extension("manager")
#     bot.load_extension("tasks.weatherInformation")
#     for file in os.listdir("commands"):
#         if file.endswith(".py"):
#             cog = file[:-3]
#             bot.load_extension(f"commands.{cog}")

# load_cogs(bot)

@bot.event
async def on_ready():
    GetWeather.start()

@bot.command(name="tempo")
async def WeatherNow(ctx):
    await ctx.send(f"Olá, {ctx.author.name}, vou pegar as informações atuais da temperatura aqui pra você...")
    await GetWeather("now")

@tasks.loop(hours=4)
async def GetWeather(param="periodic"):
    dataArray = []

    channel = bot.get_channel(1028732635079508109)

    for city in ["belo horizonte", "ribeirão das neves", "esmeraldas"]:
        try:
            LINK = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_TOKEN}&lang=pt_br"
            
            response = requests.get(LINK)

            if (response.status_code == 200):
                data = response.json()

                dataDescription = data['weather'][0]['description']
                dataCityName = data['name']
                dataTemp = data['main']['temp'] - 273.15

                formatedObject = {
                    'description': dataDescription,
                    'cityName': dataCityName,
                    'temp': dataTemp,
                    'statusCode': response.status_code
                }  

                dataArray.append(formatedObject)
            elif (response.status_code == 404):
                print("Ocorreu algum erro ao obter os dados!")

                formatedObject = {
                    'errorText': "Ocorreu algum erro ao obter os dados da cidade {city} 😭!",
                    'statusCode': 404
                }  

                dataArray.append(formatedObject)

            elif (response.status_code == 500):
                print("Ocorreu algum de comunicação com o servidor")

                formatedObject = {
                    'errorText': "O servidor morreu ao tentar obter os dados da cidade {city} 😭!",
                    'statusCode': 500
                } 

                dataArray.append(formatedObject)
        except Exception as error: 
            await channel.send("Ops... Acho que o servidor morreu!")
            print(error)
            
    now = datetime.datetime.now()
    timeNow = now.strftime("%d/%m/%Y ás %H:%M:%S")

    timeString = ""

    for item in dataArray:
        if (item['statusCode'] == 200):
            timeString =  timeString + f"\n Temperatura atual em {item['cityName'] }: {round(item['temp'], 2)} Graus"
        else:
            timeString = timeString + item['errorText'] + "\n\n"

    if(param != "now"):
        await channel.send(f"```\n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n Bot do tempo 🌥️🤖 - {timeNow} \n {timeString} \n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n (próximos dados em 4 horas) ```")
    else:
        await channel.send(f"```\n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n Bot do tempo 🌥️🤖 - {timeNow} \n {timeString} \n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ```")

bot.run(TOKEN)