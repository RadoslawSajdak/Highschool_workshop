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
  Serial.begin(9600);
  
  display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS);

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.print("Hello World!");
  display.display();
}
  
void loop()
{
 
}
```

Jeśli zainstalowałeś/aś bibliotekę poprawnie, na ekranie ukaże się napis.