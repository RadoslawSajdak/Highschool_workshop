---
title: "Wi-fi"
date: 2023-02-13T16:41:57+01:00
draft: true
weight: 6
ShowToc: true
---

# Wi-Fi
Wi-Fi jest zestawem standardów sieci bezprzewodowych. Obecne jest właściwie wszędzie. W IoT również
stosuje się je coraz częściej, ze względu na rozwijające się mechanizmy oszczędzania energii.
  
Więcej na temat sieci Wi-Fi, można przeczytać np. [w wikipedii](https://pl.wikipedia.org/wiki/Wi-Fi).

W poniższym ćwiczeniu, poznamy podstawy łączenia się z istniejącą siecią Wi-Fi oraz komunikacji przy
użyciu MQTT.
## Blinky dla Wi-Fi
Jak zawsze, pisanie kodu należy zacząć od `blinky`. W tym celu:
- Do pustego projektu zaincluduj bibliotekę `<ESP8266WiFi.h>`
- Zdefiniuj `WIFI_SSID "workshop_h3x"`
- Zdefiniuj `WIFI_PASSWORD "workshop_h3x"`

- Dodaj funkcję:
```C
void setup_wifi() {

    delay(10);

    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(WIFI_SSID);

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}
```
- Zainicjalizuj port szeregowy z prędkością `115200`
- Wywołaj funkcję `setup_wifi()`

Uruchom kod i obserwuj port szeregowy. Twoje urządzenie powinno połączyć się z siecią i otrzymać adres ip `172.30.0.xx`.

{{< spoiler_code label="wifi_blinky">}}

<pre><code class="language-c">
#include "Arduino.h"
#include "ESP8266WiFi.h"


#define WIFI_SSID "workshop_h3x"
#define WIFI_PASSWORD "workshop_h3x"

void setup_wifi()
{
    delay(10);

    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(WIFI_SSID);

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void setup()
{
    Serial.begin(115200);
    setup_wifi();

}
  
void loop()
{

}

</pre></code>
{{< /spoiler_code >}}


## MQTT - odczyt wiadomości w chmurze
MQTT jest lekkim protokołem IoT działającym w formacie subskrybcji. Urządzenia wysyłają oraz odbierają wiadomości w konkretnym wątku (Topic).
### Instalacja
Zainstaluj bibliotekę `PubSubClient`
![pubsub](images/pubsub.png#center)

### Implementacja klienta
Rozbuduj kod blinky w następujący sposób:
- Dodaj bibliotekę `<PubSubClient.h>`
- Zdefiniuj `MQTT_SERVER "broker.emqx.io"`
- Zdefiniuj `SENSOR_NAME "workshop/test1"` - test1 zmień na dowolną, wymyśloną przez siebie nazwę
- Stwórz globalne zmienne `WiFiClient espClient` oraz `PubSubClient client(espClient)`
- Dodaj do kodu funkcję `callback()` - Będzie ona wywoływana gdy urządzenie odbierze wiadomość
```C
void callback(char* topic, byte* payload, unsigned int length)
{
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");
    for (int i = 0; i < length; i++)
    {
        Serial.print((char)payload[i]);
    }
    Serial.println();
}
```
- Dodaj do kodu funkcję `reconnect()` - będzie ona łączyć urządzenie z brokerem (serwerem)
```C
void reconnect()
{
    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection...");
        String clientId = "client-";
        clientId += String(random(0xffff), HEX);
        if (client.connect(clientId.c_str()))
        {
        Serial.println("connected");
        client.publish(SENSOR_NAME, "hello world");
        client.subscribe(SENSOR_NAME);
        }
        else
        {
        delay(5000);
        }
    }
}
```
- Po połączeniu z Wi-Fi wywołaj funkcje `client.setServer(MQTT_SERVER, 1883)` oraz `client.setCallback(callback);`
- W funkcji loop wywołaj funkcję reconnect **jeśli** `!client.connected()`
- W funkcji loop wywołaj `client.loop()` - Jest to niezbędne dla obsłużenia przychodzących wiadomości

Skompiluj i uruchom swój kod. Obserwuj port szeregowy. Twoje urządzenie powinno połączyć się z wifi oraz
brokerem: (`Attempting MQTT connection...connected`).

{{< spoiler_code label="wifi_mqtt">}}

<pre><code class="language-c">

#include "Arduino.h"
#include "ESP8266WiFi.h"
#include "PubSubClient.h"

#define MQTT_SERVER "broker.emqx.io"
#define TOPIC "workshop/test1"
#define WIFI_SSID "workshop_h3x"
#define WIFI_PASSWORD "workshop_h3x"

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length)
{
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");
    for (int i = 0; i < length; i++)
    {
        Serial.print((char)payload[i]);
    }
    Serial.println();
}

void reconnect()
{
    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection...");
        String clientId = "client-";
        clientId += String(random(0xffff), HEX);
        if (client.connect(clientId.c_str()))
        {
            Serial.println("connected");
            client.publish(TOPIC, "hello world");
            client.subscribe(TOPIC);
        }
        else
        {
            delay(5000);
        }
    }
}

void setup_wifi()
{
    delay(10);

    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(WIFI_SSID);

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}


void setup()
{
    Serial.begin(115200);
    setup_wifi();
    client.setServer(MQTT_SERVER, 1883);
    client.setCallback(callback);
}
  
void loop()
{
    if (!client.connected())
    {
        reconnect();
    }
    client.loop();
}


</pre></code>
{{< /spoiler_code >}}

### Konfiguracja brokera
Aby odbierać wiadomości musimy mieć brokera. Czyli serwer, przekazujący wiadomości.
Wykorzystamy do tego narzędzie online [http://tools.emqx.io/](http://tools.emqx.io/)
W pierwszym kroku, należy stworzyć nowe połączenie. Wykorzystamy domyślne ustawienia, zmieniając jedynie nazwę. W pole `Name` wpisz dowolną, wybraną przez siebie nazwę połączenia.
![broker_connection](images/broker_new_connection.png#center)
![broker_connection2](images/broker_new_connection2.png#center)
Po dodaniu połączenia, po lewej stronie zobaczymy nasze połączenie wraz z zieloną kropką, sygnalizującą stan połączenia.
Przyciskiem `New subscription` należy stworzyć nową subskrubcję. W polu `Topic` wpisujemy zdefiniowane w kodzie `TOPIC`. Możemy również zmienić kolor, który będzie wyświetlany przy danym temacie.
![broker_connection](images/topic_name.png#center)
Na koniec, zresetuj swoją płytkę (lub wgraj kod od nowa). W przeglądarce, zobaczysz wiadomość, którą wysyła Twoje ESP.
![broker_connection](images/got_msg.png#center)
Możesz również wysłać wiadomość **do** swojej płytki. W tym celu na dole panelu:
- Ustaw `Payload` na `plaintext`
- Wpisz temat który subskrybuje w kodzie Twoje urządzenie (funkcja `client.subscribe()`)
- Wpisz dowolną wiadomość

![broker_connection](images/send_msg.png#center)

### Subskrubcja kilku tematów - zadanie dodatkowe
Zwróć uwagę, że za to czy odbierzemy wiadomość w jakimś temacie odpowiada funkcja `client.subscribe()`. Może być ona wywołana wielokrotnie, z różnymi argumentami, Podobnie, jak funkcja `client.publish()`. Dzięki temu, Twoje urządzenie może:
- Wysyłać konkretne informacje (temperatura, stan przycisku, wartość z czujnika) pod różne tematy
- Odbierać wiadomości i reagować w różny sposób w zależności od tematu wiadomości

Spróbuj przerobić kod w taki sposób aby:
- Subskrybował dwa różne tematy:
   - Temat A Będzie włączać lub wyłączać `LED_BUILTIN` w zależności czy otrzyma wartość `1` czy `0`
   - Temat B Będzie wypisywać otrzymaną wiadomość na port szeregowy
- Wysyłał wiadomość pod dwa różne tematy:
   - Temat A wyśle wiadomość `button pressed` gdy naciśniemy przycisk
   - Temat B wyśle wiadomość wpisaną na port szeregowy

Wskazówki:
- Wykorzystaj funkcję `void serialEvent()` z rozdziału UART. UWAGA! Funkcja `client.publish()` przyjmuje argumenty typu `char *`, czyli tablicę znaków. Wspomniany przykład używa obiektu `String`. Podając go jako argument, wywołaj na nim funkcję `.c_str()`:  
`client.publish(TOPIC_B_PUBLISH, inputString.c_str());`  
Przekonwertuje ona typ String, na char *.  
- Zdefiniuj osobne stałe dla kolejnych tematów np. `#define TOPIC_A_SUBSCRIBE "workshop/suba"`. Pamiętaj, że broker (przeglądarka) powinna publikować pod tematem, który urządzenie subskrybuje.  
- Stwórz dwie zmienne globalne typu `bool`: button_pressed oraz button_previously_pressed. Przy ich użyciu stwórz w funkcji `loop()` warunek który sprawi, że będziesz wysyłać **tylko jedną wiadomość**, w momencie naciskania przycisku.
- Skorzystaj z funkcji `strcmp(char *, char *)` aby sprawdzić pod jakim tematem otrzymałeś wiadomość. Zwróci ona 0 gdy oba teksty(tablice znaków, char*) są identyczne.
- Pamiętaj o odwróconej logice `LED_BUILTIN`
- Pamiętaj o konfiguracji pinów, w funkcji `setup()`

{{< spoiler_code label="mqtt_super_task">}}

<pre><code class="language-c">
#include "Arduino.h"
#include "ESP8266WiFi.h"
#include "PubSubClient.h"

#define BUTTON D1

#define MQTT_SERVER "broker.emqx.io"
#define TOPIC_A_SUBSCRIBE "workshop/suba"
#define TOPIC_B_SUBSCRIBE "workshop/subb"
#define TOPIC_A_PUBLISH "workshop/puba"
#define TOPIC_B_PUBLISH "workshop/pubb"

#define WIFI_SSID "workshop_h3x"
#define WIFI_PASSWORD "workshop_h3x"

WiFiClient espClient;
PubSubClient client(espClient);

bool button_pressed = false;
bool button_previously_pressed = false;

String inputString;

void callback(char* topic, byte* payload, unsigned int length)
{
    if (0 == strcmp(topic, TOPIC_A_SUBSCRIBE))
    {
        if ((char)payload[0] == '0')
            digitalWrite(LED_BUILTIN, HIGH);
        else if ((char)payload[0] == '1')
            digitalWrite(LED_BUILTIN, LOW);
        else
            Serial.println("Got wrong input");
    }
    else if (0 == strcmp(topic, TOPIC_B_SUBSCRIBE))
    {
        Serial.print("Message arrived [");
        Serial.print(topic);
        Serial.print("] ");
        for (int i = 0; i < length; i++)
        {
            Serial.print((char)payload[i]);
        }
        Serial.println();
    }
}

void reconnect()
{
    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection...");
        String clientId = "client-";
        clientId += String(random(0xffff), HEX);
        if (client.connect(clientId.c_str()))
        {
            Serial.println("connected");
            client.subscribe(TOPIC_A_SUBSCRIBE);
            client.subscribe(TOPIC_B_SUBSCRIBE);        
        }
        else
        {
            delay(5000);
        }
    }
}

void setup_wifi()
{
    delay(10);

    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(WIFI_SSID);

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void serialEvent()
{
    if (Serial.available() > 0) 
    {
        char character = Serial.read();
        inputString += character;
        if(character == '\n')
        {
            client.publish(TOPIC_B_PUBLISH, inputString.c_str());
            inputString = "";
        }
    }
}

void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);

    pinMode(BUTTON, INPUT_PULLUP);
    
    Serial.begin(115200);
    setup_wifi();
    client.setServer(MQTT_SERVER, 1883);
    client.setCallback(callback);

}

void loop()
{
    button_pressed = !digitalRead(BUTTON);
    if ((button_pressed != button_previously_pressed) && button_pressed)
    {
        client.publish(TOPIC_A_PUBLISH, "button pressed");
        delay(500);
    }

    if (!client.connected())
    {
        reconnect();
    }
    client.loop();
    button_previously_pressed = button_pressed;
}

</pre></code>
{{< /spoiler_code >}}

{{< img src="images/difficult_mqtt.png" label="difficult_mqtt">}}
{{< img src="images/difficult_mqtt2.png" label="difficult_mqtt2">}}