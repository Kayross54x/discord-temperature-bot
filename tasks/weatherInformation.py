import datetime
import requests
from decouple import config
from discord.ext import commands, tasks

API_TOKEN = config("API_TOKEN")

class GetOpenWeatherInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.GetWeather.start()
    
    @tasks.loop(hours=8)
    async def GetWeather(self):
        dataArray = []

        channel = self.bot.get_channel(1028732635079508109)

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
                await self.channel.send("Ops... Acho que o servidor morreu!")
                print(error)
                
        now = datetime.datetime.now()
        timeNow = now.strftime("%d/%m/%Y ás %H:%M:%S")

        timeString = ""

        for item in dataArray:
            if (item['statusCode'] == 200):
                timeString =  timeString + f"\n Temperatura atual em {item['cityName'] }: {round(item['temp'], 2)} Graus"
            else:
                timeString = timeString + item['errorText'] + "\n\n"


        await channel.send(f"```\n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n Bot do tempo 🌥️🤖 - {timeNow} \n {timeString} \n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n (próximos dados em 8 horas) ```")

    @tasks.loop(hours=24)
    async def GetWeather(self):
        
        now = datetime.datetime.now()
        if(now.weekday() == 0):
            timeNow = now.strftime("%d/%m/%Y ás %H:%M:%S")

            dataArray = []

            channel = self.bot.get_channel(1028732635079508109)

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
                    await self.channel.send("Ops... Acho que o servidor morreu!")
                    print(error)

            timeString = ""

            for item in dataArray:
                if (item['statusCode'] == 200):
                    timeString =  timeString + f"\n Temperatura atual em {item['cityName'] }: {round(item['temp'], 2)} Graus"
                else:
                    timeString = timeString + item['errorText'] + "\n\n"


            await channel.send(f"```\n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n Bot do tempo, feliz segunda :( 🌥️🤖 - {timeNow} \n {timeString} \n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n ```")

def setup(bot):
    bot.add_cog(GetOpenWeatherInfo(bot))