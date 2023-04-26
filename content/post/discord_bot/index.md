---
title: "Aplikacja - Discord BOT"
date: 2023-02-13T16:42:09+01:00
draft: false
weight: 7
---

# Discord BOT - aplikacja zaawansowana
W tym rozdziale zaprezentowano przykład aplikacji z wykorzystaniem Discord API. Jest to prosta aplikacja mrugająca diodą LED w odpowiedzi na wiadomość na kanale Discord.
Niemniej, jej stworzenie wymaga instalacji i zrozumienia wielu różnych zagadnień.

## Instalacja środowiska
Do stworzenia aplikacji, potrzebujemy zainstalować:
- Discord App - (desktop/mobile)
- Python3
- Dodatkowe biblioteki python:
   - discord.py
   - python-dotenv

### Discord App
Pobierz i zainstaluj aplikację Discord. Załóż również konto w aplikacji. Wystarczająca będzie aplikacja na telefon.
- https://discord.com/download

### Python3
Sugerowanym poradnikiem dla wszystkich platform jest poradnik ze strony [djangogirls](https://tutorial.djangogirls.org/pl/python_installation/)

### Biblioteki python3
**Windows:**
- Wciśnij przycisj `Win` (flaga)
- Wpisz `cmd`
- W wyświetlonym terminalu wpisz `pip3 install -U discord.py`
- Następnie wpisz komendę `pip3 install -U python-dotenv`

**Ubuntu:**
- Otwórz nowe okno terminala
- Wpisz `pip3 install -U discord.py python-dotenv`

## Discord Developer Portal
Discord, udostępnia deweloperom API, czyli zestaw funkcji pozwalających na komunikację z ich aplikacją.
W pierwszej kolejności, należy stworzyć bota z odpowiednimi uprawnieniami. W tym celu, skorzystaj z 
portalu https://www.geeksforgeeks.org/building-a-discord-bot-in-python/ . Jest to portal na którym można znaleźć
wiele wskazówek odnośnie tworzenia kodu.  
Jeśli nie czujesz się płynnie w języku angielskim, w prawym górnym rogu strony możesz automatycznie przetłumaczyć stronę.

**UWAGA** Zatrzymaj się na podrozdziale `Writing Code for Bot` (Pisanie kodu bota). Stworzymy własny kod, dopasowany do 
naszej aplikacji. Kod ze strony posiada również błędy wynikające z ostatnich zmian w API Discorda.

## Hello bot
Jeśli udało Ci się przejść przez wszystkie poprzednie kroki, czas uruchomić `hello_world`. Stwórz dwa pliki:
- bot.py
- .env
A następnie wklej do nich poniższy kod

```python
# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "Hello bot!":
        response = "Hello " + str(message.author)
        await message.channel.send(response)

client.run(TOKEN)

```

```python
# .env
DISCORD_TOKEN=TWÓJ TOKEN
DISCORD_GUILD="NAZWA TWOJEGO SERWERA"
```

W pliku `.env` koniecznie podmień TOKEN (krok 5. w `Creating a bot`)  
  
Czas na uruchomienie aplikacji. Wywołaj komendę  
`python3 bot.py`

W Twoim terminalu powinno pokazać się kilka wiadomości i co najważniejsze - lista członków serwera.
![terminal](images/auth_bot.png#center)

Teraz, na dowolnym kanale tekstowym Discord napisz wiadomość `Hello bot!`!
![hello_bot](images/hello_bot.png#center)

## Implementacja
### Implementacja - Klient UDP
Kolejnym krokiem, jest stworzenie klienta UDP działającego na naszym ESP. Będzie on odbierać dane na odpowiednim porcie, a następnie wykonywał zaprogramowaną akcję. W tym przypadku, włączał i wyłączał LED.

Więcej na temat UDP, przeczytasz tutaj: https://pasja-informatyki.pl/sieci-komputerowe/protokol-udp/

### Implementacja - ESP
Kluczową biblioteką, jest `WiFiUdp.h`. Dodaj ją do swojego projektu.
- Zdefiniuj `WIFI_SSID` jako `"workshop_h3x"`
- Zdefiniuj `WIFI_PASSWORD` jako `"workshop_h3x"`
- Zdefiniuj `MAX_PACKET_LEN` jako `1500`
- Stwórz globalne tablice:
    - char packet_buffer[MAX_PACKET_LEN + 1]
    - char reply_buffer[] = "Got data \r\n"
- Stwórz globalny obiekt `WiFiUDP` o nazwie `udp`
- Zainicjalizuj:
    - Port szeregowy (baudrate `115200`)
    - WiFi (.mode(WIFI_STA), następnie .begin())
    - obiekt `udp`, wywołując `udp.begin(8888)`
- Wyprintuj po połączeniu lokalny IP który dostało Twoje ESP

Następnie, w funkcji `loop()`:
- Zadeklaruj `packet_size` typu int i przypisz do niego `udp.parsePacket()`
- Jeżeli `packet_size` jest niezerowy to wywołaj kolejno:
    - Do zmiennej `n` typu int przypisz `udp.read(packet_buffer, MAX_PACKET_LEN)`
    - Ustaw wartość `n` elementu tablicy `packet_buffer` na 0
    - Wyprintuj zawartość `packet_buffer`
    - Doklej poniższe 3 linie kodu. Wyślą one odpowiedź na wiadomość
```C
    udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    udp.write(ReplyBuffer);
    udp.endPacket();
```

Rozwiązanie powyższego kodu znajdziesz poniżej:
{{< spoiler_code label="udp_server_esp">}}

<pre><code class="language-c">

#include "Arduino.h"
#include "ESP8266WiFi.h"
#include "WiFiUdp.h"

#define SSID "workshop_h3x"
#define PASSWORD "workshop_h3x"
#define MAX_PACKET_LEN 1500

// buffers for receiving and sending data
char packet_buffer[MAX_PACKET_LEN];      // buffer to hold incoming packet,
char reply_buffer[] = "Data ok";     // a string to send back

WiFiUDP udp;

void setup()
{
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);
    WiFi.begin(SSID, PASSWORD);
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print('.');
        delay(500);
    }
    Serial.println("Connected! IP address: ");
    Serial.println(WiFi.localIP());

    udp.begin(8888);
}

void loop()
{
    // if there's data available, read a packet
    int packet_size = udp.parsePacket();
    if (packet_size)
    {
        // read the packet into packetBufffer
        int n = udp.read(packet_buffer, MAX_PACKET_LEN);
        packet_buffer[n] = 0;
        Serial.print("Contents:  ");
        Serial.println(packet_buffer);

        // send a reply, to the IP address and port that sent us the packet we received
        udp.beginPacket(udp.remoteIP(), udp.remotePort());
        udp.write(reply_buffer);
        udp.endPacket();
    }
}

</pre></code>
{{< /spoiler_code >}}

Stworzony kod, powinien wyświetlić otrzymane dane. Aby przetestować jego działanie:
- Uruchom poniższy kod, podmieniając `IP_ADDRESS` na adres Twojego ESP. Zapisz plik jako `send_udp.py`

```python
# Python
import socket

def send_udp(message):
    IP_ADDRESS = "127.0.0.1"
    UDP_PORT = 8888

    print("UDP target IP: ", IP_ADDRESS)
    print("UDP target port: ", UDP_PORT)
    print("message: ", message)

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(message, "utf-8"), (IP_ADDRESS, UDP_PORT))

    data, addr = sock.recvfrom(1500) # buffer size is 1500 bytes
    print("Got: ", data)
    sock.close()

if __name__ == "__main__":
    send_udp("Hello world!")
```

W Twoim terminalu powinieneś zobaczyć
![data_ok](images/data_ok.png#center)
### Implementacja - Bot discord

Czas połączyć wszystkie kropki!
- Na początku pliku `bot.py` dodaj linię `from send_udp import send_udp`
- Do zmiennej `response` w pliku `bot.py` przypisz dowolną wiadomość
- W kolejnej linii (przecd await) wywołaj `send_udp(response)`

Uruchom bota na Discord i wyślij do niego wybraną (`message.content`) wiadomość. Czy otrzymałeś `response` na discordzie oraz ESP?

![bot_success](images/bot_success.png#center)

### Blinky discord - Zadanie zaawansowane
Masz już pełny zestaw narzędzi, pozwalających wykonać ostatnie zadanie tego kursu. Stosując wiedzę z **WSZYSTKICH** poprzednich zadań, dodaj do kodu ESP
włączanie i wyłączanie LED przy użyciu bota Discord. Niech wiadomość
   - LED on - włącza led
   - LED off - wyłącza led
W przypadku każdej innej wiadomości, LED powinna zamrugać i wrócić do stanu sprzed mrugnięcia.

Odpowiedzi znajdziesz poniżej:
#### bot.py

{{< spoiler_code label="bot ready">}}

<pre><code class="language-python">

# bot.py
import os

import discord
from dotenv import load_dotenv
from send_udp import send_udp

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "LED on":
        response = "I turned the LED on"
        send_udp("LED on")
        await message.channel.send(response)

    elif message.content == "LED off":
        response = "I turned the LED off"
        send_udp("LED off")
        await message.channel.send(response)
    
    else:
        response = "I dont know this command"
        send_udp("Wrong input!")
        await message.channel.send(response)
    

client.run(TOKEN)

</pre></code>
{{< /spoiler_code >}}

#### kod ESP
{{< spoiler_code label="esp ready">}}

<pre><code class="language-c">

#include "Arduino.h"
#include "ESP8266WiFi.h"
#include "WiFiUdp.h"

#define SSID "workshop_h3x"
#define PASSWORD "workshop_h3x"
#define MAX_PACKET_LEN 1500

// buffers for receiving and sending data
char packet_buffer[MAX_PACKET_LEN];      // buffer to hold incoming packet,
char reply_buffer[] = "Data ok";     // a string to send back

WiFiUDP udp;

void setup()
{
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);

    WiFi.mode(WIFI_STA);
    WiFi.begin(SSID, PASSWORD);
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print('.');
        delay(500);
    }
    Serial.println("Connected! IP address: ");
    Serial.println(WiFi.localIP());

    udp.begin(8888);
}

void blink(int n_times)
{
    bool prev_state = digitalRead(LED_BUILTIN);
    for (int i = 0; i < n_times; i++)
    {
        digitalWrite(LED_BUILTIN, LOW);
        delay(200);
        digitalWrite(LED_BUILTIN, HIGH);
        delay(200);
    }
    digitalWrite(LED_BUILTIN, prev_state);
}

void loop()
{
    // if there's data available, read a packet
    int packet_size = udp.parsePacket();
    if (packet_size)
    {
        // read the packet into packetBufffer
        int n = udp.read(packet_buffer, MAX_PACKET_LEN);
        packet_buffer[n] = 0;
        Serial.print("Contents:  ");
        Serial.println(packet_buffer);
        if (0 == strcmp("LED on", packet_buffer))
        {
            digitalWrite(LED_BUILTIN, LOW);
        }
        else if (0 == strcmp("LED off", packet_buffer))
        {
            digitalWrite(LED_BUILTIN, HIGH);
        }
        else
            blink(3);

        // send a reply, to the IP address and port that sent us the packet we received
        udp.beginPacket(udp.remoteIP(), udp.remotePort());
        udp.write(reply_buffer);
        udp.endPacket();
    }
}

</pre></code>
{{< /spoiler_code >}}

Na podstawie tego rozdziału, możesz zrobić wiele własnych projektów. Wiele urządzeń IoT (kamery, zdalne gniazdka itp.)
wystawiają swoje API w pythonie lub JavaScript. Korzystając z dostępnych w internecie poradników w sposób, który
został tutaj przedstawiony, możesz stworzyć duże i ciekawe rozwiązania! :)