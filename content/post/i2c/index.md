---
title: "I2C - Wyświetlacz OLED"
date: 2023-02-13T16:41:27+01:00
draft: true
weight: 4
ShowToc: true
---

# Magistrala I2C
Magistrala I2C, pozwala na komunikację wielu równolegle połączonych urządzeń. Korzysta przy tym z dwóch linii:
- SCL/SCK (Clock) - pin D1
- SDA (Data) - pin D2
  
Komunikacja jest możliwa dzięki wykorzystaniu adresów. Każde urządzenie posiada swój adres 7 bitowy (127 adresów). Moduły zazwyczaj posiadają dodatkowe piny pozwalające na zmianę adresu poprzez ich zwarcie. Pozwala to na jednoczesne połączenie wielu takich samych układów (na przykład czujników temperatury).

## Komunikacja przy użyciu I2C
Połącz mikrokontroler oraz wyświetlacz OLED w następujący sposób:

| Mikrokontroler | OLED |
| :------------: | :--: |
| 3V3            | VCC  |
| GND            | GND  |
| SCL (D1)       | SCK  |
| SDA (D2)       | SDA  |

### Skaner I2C
Zazwyczaj, adres urządzenia możemy sprawdzić w dokumentacji. W przypadku gdy nie mamy do niej dostępu,
dokumentacja nie specyfikuje adresu, albo po prostu "coś nie działa", warto napisać prosty skaner.
  
W środowisku arduino, do obsługi I2C używamy biblioteki `Wire.h`. Nasz skaner inicjalizuje obiekt `Wire`, 
a następnie próbuje rozpocząć transmisję z każdym adresem po kolei. Jeśli próba zakończy się powodzeniem
(nie będzie błędu transmisji, a więc `error == false`), adres zostanie wypisany na port szeregowy.
  
Zwróć uwagę, że użyliśmy funkcji `printf()`. Więcej na jej temat możesz przeczytać [tutaj](https://cpp0x.pl/dokumentacja/standard-C/printf/321)
  
Wgraj kod na płytkę i obserwuj port szeregowy. Pamiętaj, o odpowiedniej prędkości transmisji!

```C
#include "Arduino.h"
#include "Wire.h" 

void setup()
{
  Wire.begin();
  Serial.begin(115200);
}
  
void loop()
{
    Serial.println("Scanning...");
 
    for(uint8_t address = 1; address < 127; address++ )
    {
        Wire.beginTransmission(address);
        uint8_t error = Wire.endTransmission();
        if(!error)
        {
            Serial.printf("I2C device found at: 0x%02X\n", address);
        }
    }
    delay(3000);
}
```

### Instalacja bibliotek
Do obsługi różnych modułów, możemy skorzystać z gotowych bibliotek. W Arduino IDE instalacja bibliotek jest wyjątkowo prosta.
- Otwórz menedżer bibliotek
- Wyszukaj SSD1306
- Zainstaluj Adafruit SSD1306 by Adafruit **oraz wszystkie zależności (wyskakujące okno)**

{{< img src="images/library_install.png" label="library_install">}}

Aby sprawdzić, czy wszystko działa poprawnie, wgraj poniższy kod. 
  
**Podmień `PUT_ADDRESS_HERE` na adres, który znalazł skaner!**

```C
#include "Arduino.h"
#include "Wire.h" 
#include "Adafruit_GFX.h"
#include "Adafruit_SSD1306.h"

#define SCREEN_ADDRESS 0x3C
Adafruit_SSD1306 display(128, 32, &Wire, -1);

void setup()
{
  Wire.begin();
  Serial.begin(115200);
  
  display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS);

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);
  display.print("Hello World!");
  display.display();
}
  
void loop()
{
 
}
```

Jeśli zainstalowałeś/aś bibliotekę poprawnie, na ekranie ukaże się napis.

  
Powyższy program, wymaga kilku wyjaśnień:
- `clearDisplay()` - czyści wszystko, co aktualnie jest narysowane na wyświetlaczu. Funkcja ta jest niezbędna, ponieważ odpowiada za odświeżanie ekranu
- `setTextColor(SSD1306_WHITE)` - ustawia kolor wyświetlanych tekstów na biały. SSD1306_WHITE to predefiniowana wartość z biblioteki. Dzięki niej, gdyby w kodzie bibliotecznym zostały wprowadzone zmiany, programy na nim oparte nie przestaną działać
- `setCursor(x,y)` - Wyświetlacz z którego korzystamy, ma rozdzielczość 128x32 pixele. Rozpoczyna rysowanie **zawsze** od miejsca, w którym ustawimy jego kursor
- `print()` - Działa jak Serial.print(), jednak wysyła tekst do wyświetlacza
- `display()` - Najważniejsza z funkcji - wyświetla to, co wpisaliśmy do wyświetlacza
  
Wielokrotnie, będziemy mieć potrzebę wyświetlenia tekstu, zawierającego różne liczby. Pomaga nam w tym funkcja `sprintf()`.
Dokumentację do funkcji znajdziesz [tutaj](https://cplusplus.com/reference/cstdio/sprintf/)
  
#### Zadanie
Korzystając z dokumentacji funkcji `sprintf()` napisz progam który: będzie w kółko liczył od 0 do 10 i wyświetlał aktualną liczbę na ekranie. Ustaw rozmiar tekstu na 4.
  
Pamiętaj o:
- Czyszczeniu wyświetlacza
- Stworzeniu globalnego bufora o rozmiarze większym, niż najdłuższa wyświetlana wiadomość
- Użyciu pętli `for()`

{{< spoiler_code label="0to10with1sstep">}}

<pre><code class="language-c">
#include "Arduino.h"
#include "Wire.h" 
#include "Adafruit_GFX.h"
#include "Adafruit_SSD1306.h"

#define SCREEN_ADDRESS 0x3C
Adafruit_SSD1306 display(128, 32, &Wire, -1);

char buffer[5];

void setup()
{
    Wire.begin();
    Serial.begin(115200);
    
    display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS);

    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(4);
}
  
void loop()
{
    for (int i = 0; i <= 10; i++)
    {
        display.clearDisplay();
        display.setCursor(0,0);
        sprintf(buffer, "%d", i);
        display.print(buffer);
        display.display();
        delay(1000);
    }
}

</pre></code>
{{< /spoiler_code >}}


#### Zadanie (opcjonalne)
Spróbuj przerobić powyższą pętlę `loop` w taki sposób, aby liczyć co 100ms. Pamiętaj, aby użyć zmiennoprzecinkowego typu `float`.
Dokładność zmiennej zapisywanej do stringa (ciągu znaków) możesz ustawić jako `"%.1f"` co odpowiada jednemu miejscu po przecinku.

{{< spoiler_code label="0to10with01sstep">}}

<pre><code class="language-c">

void loop()
{
    for (float i = 0; i <= 10; i += 0.1)
    {
        display.clearDisplay();
        display.setCursor(0,0);
        sprintf(buffer, "%.1f", i);
        display.print(buffer);
        display.display();
        delay(100);
    }
}

</pre></code>
{{< /spoiler_code >}}

### One Wire - czujnik temperatury

Wiedząc już, jak wyświetlać liczby zmiennoprzecinkowe na wyświetlaczu, spróbujmy użyć czujnika temperatury `DHT11`.
  
Na początek, zainstaluj bibliotekę do obsługi DHT: `DHT sensor library by Adafruit`
![libka](images/dht_install.png#center)

Następnie, **nie wypinając wyświetlacza**, podepnij DHT w następujący sposób
![dht](images/dht_connect.png#center)

W celu sprawdzenia, czy czujnik działa poprawnie, napiszmy krótki kod. Wyświetli on dane na porcie szeregowym.
  
Najpierw, załączmy odpowiednie biblioteki do kodu
```C
#include "Adafruit_Sensor.h"
#include "DHT.h"
#include "DHT_U.h"
```
oraz zdefiniujmy obiekt typu `DHT_Unified`. Jako argumenty inicjalizacji, podamy pin do którego podłączyliśmy linię danych - `D3` i typ czujnika `DHT11`
```C
DHT_Unified(D3, DHT11);
```
W funkcji `setup()`, zainicjalizujmy port szeregowy. Następnie, dodajmy również inicjalizację czujnika
```C
dht.begin();
```
Na koniec, w pętli `loop()` odczytajmy wartości z czujnika i wyślijmy je na port szeregowy
```C
void loop()
{
    sensors_event_t event;
    dht.temperature().getEvent(&event);

    Serial.print("Temperature: ");
    Serial.print(event.temperature);
    Serial.println("°C");

    dht.humidity().getEvent(&event);

    Serial.print("Humidity: ");
    Serial.print(event.relative_humidity);
    Serial.println("%");

    delay(1000);
}
```
(Sklejony kod, znajdziesz pod spoilerem poniżej)
{{< spoiler_code label="dht_test">}}

<pre><code class="language-c">

#include "Adafruit_Sensor.h"
#include "DHT.h"
#include "DHT_U.h"

DHT_Unified dht(D3, DHT11);

void setup()
{
    dht.begin();
    Serial.begin(115200);
}
  
void loop()
{
    sensors_event_t event;
    dht.temperature().getEvent(&event);

    Serial.print("Temperature: ");
    Serial.print(event.temperature);
    Serial.println("°C");

    dht.humidity().getEvent(&event);

    Serial.print("Humidity: ");
    Serial.print(event.relative_humidity);
    Serial.println("%");

    delay(1000);
}
</pre></code>
{{< /spoiler_code >}}

W powyższym fragmencie, pojawia się zmienna typu `sensors_event_t`. Jest ona zdefiniowana (opisana) wewnątrz bibliotek które dołączyliśmy. Jej zawartość, możesz sprawdzić przytrzymując `lctrl (lewy control)` i klikając w typ. Naszym oczom ukaże się skomplikowana struktura. Dostęp do jej pól możemy uzyskać przy użyciu kropki przy zmienne. Np. `event.temperature` odnosi się do pola `temperature` struktury `event` którą stworzyliśmy. Takie podejście, pozwala na znaczną poprawę czytelności kodu.

#### Zadanie - Wyświetlenie temperatury na wyświetlaczu OLED
Spróbuj połączyć przykład w którym wyświetlaliśmy milisekundy, z wyświetlaniem temperatury i wilgotności na wyświetlaczu OLED.
  
Pamiętaj o:
- Odpowiednim rozmiarze bufora
- Zmniejeszeniu rozmiaru tekstu na 1
- Ustawieniu kursora na odpowiednią linię (y), aby wyświetlić wyniki osobno
Oczekiwany wynik:
![result](images/result_oled.jpg#center)

{{< spoiler_code label="dht_oled">}}

<pre><code class="language-c">
#include "Arduino.h"
#include "Wire.h" 
#include "Adafruit_GFX.h"
#include "Adafruit_SSD1306.h"
#include "DHT.h"
#include "DHT_U.h"

#define SCREEN_ADDRESS 0x3C
Adafruit_SSD1306 display(128, 32, &Wire, -1);
DHT_Unified dht(D3, DHT11);

char buffer[50];

void setup()
{
    Wire.begin();
    Serial.begin(115200);
    dht.begin();
    
    display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS);

    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(1);
}
  
void loop()
{
    sensors_event_t event;

    display.clearDisplay();

    display.setCursor(0,0);
    dht.temperature().getEvent(&event);
    sprintf(buffer, "temperature: %.1f", event.temperature);
    display.print(buffer);

    display.setCursor(0,16);
    dht.humidity().getEvent(&event);
    sprintf(buffer, "humidity: %.1f", event.relative_humidity);
    display.print(buffer);

    display.display();
    delay(500);
}
}
</pre></code>
{{< /spoiler_code >}}

Spróbuj powoli dmuchać na czujnik ciepłym powietrzem. Czy wartości zmieniają się?