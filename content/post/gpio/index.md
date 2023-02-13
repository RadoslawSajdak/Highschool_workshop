---
title: "GPIO"
date: 2023-02-13T16:35:29+01:00
draft: false
weight: 2
ShowToc: true
---

# GPIO (General-Purpose Input Output)

## Obsługa wielu wyjść cyfrowych
Po ukończeniu wprowadzenia, wiesz już jak zamrugać diodą. Każda dioda, ma katodę (-) oraz anodę (+).
Anoda, posiada krótszą nóżkę i to do niej należy podłączyć zasilanie. Można skojarzyć to prez znaną
nazwę AK47 (prąd płynie A -> K, a 4 jest mniejsze niż 7 :)). Dodatkowo, aby ograniczyć prąd płynący przez
diodę, należy szeregowo włączyć do niej rezystor. Podobnie jak na poniższym obrazku, podłącz trzy diody
do pinów **D5, D6, D7**.

{{< img src="images/three_leds.png" label="three_leds">}}

Wiedząc, że
```c
digitalWrite(PIN_NUMBER, LOGIC_LEVEL);
```
oraz
```c
pinMode(PIN_NUMBER, LOGIC_LEVEL);
```
spróbuj zamrugać trzema diodami po kolei.

{{< spoiler_code label="code0">}}

<pre><code class="language-c">
#include <Arduino.h>
#define LED_PIN1 D6
#define LED_PIN2 D7
#define LED_PIN3 D8
#define LED_BLINK_PERIOD 1000

void setup()
{
    pinMode(LED_PIN1, OUTPUT);
    pinMode(LED_PIN2, OUTPUT);
    pinMode(LED_PIN3, OUTPUT);
}

void loop()
{
    digitalWrite(LED_PIN1, HIGH);
    delay(LED_BLINK_PERIOD);
    digitalWrite(LED_PIN1, LOW);
    delay(LED_BLINK_PERIOD);

    digitalWrite(LED_PIN2, HIGH);
    delay(LED_BLINK_PERIOD);
    digitalWrite(LED_PIN2, LOW);
    delay(LED_BLINK_PERIOD);

    digitalWrite(LED_PIN3, HIGH);
    delay(LED_BLINK_PERIOD);
    digitalWrite(LED_PIN3, LOW);
    delay(LED_BLINK_PERIOD);
}
</pre></code>
{{< /spoiler_code >}}

## Funkcja, mrugająca diodą
Aby uniknąć powielania kodu, co zrobiliśmy powyżej, tworzymy funkcje. W językach o typie statycznym (C, C++)
mają zazwyczaj format **[typ zwracany] nazwa_funkcji(typ argumentu1, typ argumentu2){ [Kod tutaj] }**. 
  
Typy, różnią się od siebie rozmiarem.
Wyjątkiem, jest typ **void** który informuje nas, że funkcja nie zwraca niczego.
  
Spróbuj napisać funkcję mrugającą diodą:
- o nazwie **blinkLED**
- zwracającą **void**
- przyjmującą jeden argument typu **uint8_t**.  
  
Na ten moment przyjmijmy, że funkcje znajdują się powyżej
```c
void setup()
{

}
```
{{< spoiler_code label="code1">}}
<pre><code class="language-c">
void blinkLED(uint8_t ledNo)
{
    digitalWrite(ledNo, HIGH);
    delay(LED_BLINK_PERIOD);
    digitalWrite(ledNo, LOW);
    delay(LED_BLINK_PERIOD);
}
</pre></code>
{{< /spoiler_code >}}
Używając napisanej przez Ciebie funkcji, popraw nasz wcześniejszy przykład.

{{< spoiler_code label="code2">}}
<pre><code class="language-c">
void loop()
{
    blinkLED(LED_PIN1);
    blinkLED(LED_PIN2);
    blinkLED(LED_PIN3);
}
</pre></code>
{{< /spoiler_code >}}

## Sterowanie jasnością LED - PWM (Pulse Width Modulation)
Każdy z naszych pinów, może pracować w różnych trybach. Jednym z nich jest PWM, czyli modulacja wypełnieniem sygnału.
Upraszczając, możemy sterować tym jaki procent czasu pin jest w stanie wysokim, a jaki w niskim. Służy do tego funkcja
```c
analogWrite(PIN_NUMBER, VALUE(0-255));
```
  
Dodatkowe informacje znajdziesz w:
- Dokumentacji biblioteki arduino [link](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/)
- Krótkim tutorialu o PWM [link](https://www.arduino.cc/pl/Tutorial/Foundations/PWM)

Spróbuj uruchomić na swojej płytce poniższy kod. Czy LED zmienia jasność krokowo?

```c
void loop(){
    analogWrite(LED_PIN1, 50);
    delay(LED_BLINK_PERIOD);
    analogWrite(LED_PIN1, 150);
    delay(LED_BLINK_PERIOD);
    analogWrite(LED_PIN1, 250);
    delay(LED_BLINK_PERIOD);
}
```

### Narastająca jasność - pętle
Chcąc aby nasz LED rozjaśniał się płynnie, musielibyśmy 255 razy wywołać funkcję `analogWrite()`. Nie 
byłoby to jednak ani czytelne, ani wydajne. Służą do tego **pętle**. Pozwalają one na wywołanie jakiegoś
fragmentu kodu, ściśle określoną ilość razy. W C, używamy trzech pętli:
- `do{ [kod] }while(warunek)`
- `while(warunek){ [kod] }`
- `for(iterator; warunek; instrukcja){ [kod] }`
   
Każda z nich, działa w trochę różny sposób.  
- `do{ [kod] }while(warunek)`, sprawdza warunek **po** wyjściu z bloku kodu
- `while(warunek){ [kod] }`, sprawdza warunek **przed** wejściem do bloku kodu
- `for(iterator; warunek; instrukcja){ [kod] }` może stworzyć element (np. iterator), sprawdza warunek **przed** wejściem,
ale również wykonuje jakąś instrukcje (np. dodawanie) **po** wyjściu z bloku.
  
Używany przez nas
```c
void loop()
{

}
```
To nic innego jak
```c
while(1)
{

}
```
  
W naszych przykładach, będziemy używać głównie pętli `for`. Jest ona najwygodniejsza w użyciu, ponieważ pozwala wykonać
wszystkie niezbędne operacje związane z pętlami w przejrzysty sposób.  
Więcej o pętli `for`, możesz przeczytać [tutaj](https://www.programiz.com/c-programming/c-for-loop)
  
Spróbuj napisać funkcję `fadeIn()`, która będzie rozjaśniać diodę led w sposób płynny. Użyj do tego pętli
```c
for(uint8_t i = 0; i < 255; i++)
{

}
```
**UWAGA!** Ze względu na charakterystykę diody, wyższe wartości `i` mogą nie wpływać wyraźnie na jasność diody, jednak bez problemu zaobserwujesz rozjaśnianie.


{{< spoiler_code label="code3">}}
<pre><code class="language-c">
#include <Arduino.h>
#define LED_PIN1 D6
#define LED_PIN2 D7
#define LED_PIN3 D8
#define LED_BLINK_PERIOD 1000

void setup()
{
    pinMode(LED_PIN1, OUTPUT);
    pinMode(LED_PIN2, OUTPUT);
    pinMode(LED_PIN3, OUTPUT);
}

void fadeIn(uint8_t ledNo)
{
    for(uint8_t i = 0; i < 255; i++){
        analogWrite(ledNo, i);
        delay(10);
    }
}

void loop()
{
    fadeIn(LED_PIN1);
    fadeIn(LED_PIN2);
    fadeIn(LED_PIN3);
}
</pre></code>
{{< /spoiler_code>}}

Czy jesteś w stanie napisać również funkcję `fadeOut()`, zmniejszającą jasność od największej do zera?

{{< spoiler_code label="code4">}}
<pre><code class="language-c">
void fadeOut(uint8_t ledNo)
{
    for(uint8_t i = 0; i < 255; i++){
        analogWrite(ledNo, 255 - i);
        delay(10);
    }
}
</pre></code>
{{< /spoiler_code>}}

### Pseudo asynchroniczna kontrola LED
W poprzednich przykładach, Mogliśmy jednocześnie zmieniać jasność tylko jednej diody. Nie jest to rozwiązanie stosowane
w praktyce, ponieważ nie chcemy aby nasz "potężny" procesor marnował tyle czasu. Dla przykładu, chcąc obrócić dwa koła samochodu o 360 stopni, musimy zrobić to jednocześnie. W przeciwnym razie, znajdziemy się w zupełnie innym miejscu (zakładając, że w ogóle ruszymy).
  
W tym celu skorzystamy z funkcji `milis()`. Zwraca ona liczbę milisekund które upłynęły od startu naszego
procesora. Czas ten, według dokumentacji, wyzeruje się po około 50 dniach. Dlatego, do zapamiętania czasu,
potrzebujemy zmiennej o dużym rozmiarze: `long`.
  
Zmienną o nazwie `lastUpdate` będziemy przechowywać poza blokami `setup()` oraz `loop`. Oznacza to, że 
będzie ona zmienną **gobalną**, dostępną w każdym miejscu kodu. Podobnie zapiszemy zmienną `currentBrightness`.


```c
#include <Arduino.h>
#define LED_PIN1 D6
#define LED_PIN2 D7
#define LED_PIN3 D8

long lastUpdate = 0;
uint8_t currentBrightness = 0;

void setup()
{
    pinMode(LED_PIN1, OUTPUT);
    pinMode(LED_PIN2, OUTPUT);
    pinMode(LED_PIN3, OUTPUT);
}

void loop()
{
    if( (lastUpdate + 50) < millis() )
    {
        analogWrite(LED_PIN1, currentBrightness);
        analogWrite(LED_PIN2, currentBrightness);
        analogWrite(LED_PIN3, currentBrightness);
        currentBrightness++;
        lastUpdate = millis();
    }   
    
}

```

W powyższym kodzie, znajduje się instrukcja warunkowa `if`. Sprawdza ona, czy wartość logiczna w nawiasach jest prawdą
(w tym przypadku, czy ostatnia aktualizacja, była ponad 50ms temu). Jeśli tak, to aktualizuje wartość każdej LED oraz zwiększa ją o jeden. 
  
Kod ten, zawiea jednak drobną pułapkę. `currentBrightness` będąc typu `uint8_t`, przyjmuje maksymalnie wartość 2 do potęgi 8 - 1 (255). Gdy spróbujemy ją zwiększyć, znów przyjmie wartość 0 gasząc diodę. Więcej na ten temat, przeczytasz [tutaj](https://www.bbc.co.uk/bitesize/guides/z26rcdm/revision/5).