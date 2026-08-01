# Storleksordningen

**utlovat.se i tre dimensioner.** En värld man går omkring i, byggd av vad
partierna lovat inför riksdagsvalet 2026 — vad löftena kostar, var partierna
står, och vad de faktiskt gjort i riksdagen.

Namnet är avsiktligt bokstavligt. "I storleksordningen tio miljarder" betyder
i vanligt tal *ungefär* tio miljarder. Här betyder det vad det säger: man går
genom tiopotenserna.

> **Ingenting här är byggt än.** Repot innehåller i skrivande stund en
> mätning — se [`spik/`](spik/) — och den här beskrivningen. Läs den som en
> avsikt, inte som en beskrivning av något som finns.

## Vad det är

[utlovat.se](https://utlovat.se) granskar partiernas löften öppet och
spårbart: varje löfte har ett ordagrant citat med källa och arkivkopia, ett
kostnadsestimat med spann, och en uträkning som redovisas i klartext. Det är
en sajt av tabeller och text, med flit.

Storleksordningen är samma data sedd på ett annat sätt. Beloppen spänner över
fem tiopotenser — från två miljoner till sjuttioåtta miljarder om året — och
den skillnaden går inte att känna i en tabellcell. Den går att känna om man
går förbi den.

Motorn kommer från [ImmersaDocs](https://github.com/bambapappa/ImmersaDocs),
som gör textsamlingar till landskap. Här används den på ett register i
stället för på dokument.

## Varför det här datat passar ovanligt bra

ImmersaDocs läser normalt dokument och plockar ut betydelse ur dem, delvis
med språkmodell. utlovat.se har redan gjort det arbetet — och en människa har
godkänt varje belopp. Hela den delen av kedjan som skulle kunna hitta på en
siffra hoppas alltså över. Det som ritas är det som står i registret,
ingenting annat.

Det finns också en funktion som väntar på just den här formen.
Jämförelsetalen — vad ett löfte motsvarar i Förbifart Stockholm, i JAS 39E,
i sjuksköterskeår, i enkronor staplade mot månen — ligger som data på
utlovat.se men togs bort ur sajten sommaren 2026, för att de inte bär i text.
En rad man läser förbi säger ingenting. En sak man går runt gör det.

## Regler som gäller allt arbete här

Fyra saker som inte är smaksak. De följer av vad utlovat.se är, och de går
före allt annat i det här repot.

1. **Måttstocken ska alltid synas.** Höjd är logaritmisk, annars går världen
   inte att gå i. Men logaritmen gör hundra gånger till dubbelt så högt, och
   det är precis den skillnaden som är hela poängen med granskningen. Därför
   ska ett belopp aldrig visas som enbart en höjd: siffran i klartext och en
   synlig skala hör alltid ihop med objektet.
2. **De åtta partierna behandlas likadant.** Samma ljus, samma kamera, samma
   avstånd, samma formspråk. Grammatiken är deterministisk, så det går att
   kontrollera och inte bara påstå.
3. **Citatet läses aldrig i VR.** Det ordagranna citatet, källan, arkivlänken
   och uträkningen hör hemma i en vanlig tvådimensionell panel. Läshastigheten
   faller kraftigt i headset, och citatet är det enda som inte får bli ungefär.
4. **Tomrum ritas som tomrum.** Saknas ett rent citat, eller kostar ett löfte
   noll för att en lag bär det, ska det synas — inte utelämnas och inte ritas
   som något litet. Frånvaro är ett svar, och den ska vara lika synlig som de
   andra.

## Data

All data hämtas från utlovat.se:s öppna gränssnitt. Ingenting kopieras in i
det här repot, och ingen databas behövs.

| Vad | Var |
| --- | --- |
| Löften, partier, sakfrågor, ståndpunkter | `https://utlovat.se/api/v1/` |
| Riksdagshandlingar och domar | `https://utlovat.se/handlingsvagen/api/hv/` |
| Metoden bakom siffrorna | [utlovat.se/metod](https://utlovat.se/metod) |

Data är **CC BY 4.0** och kräver att "utlovat.se" anges som källa. Det gäller
även den här sajten.

## Licens

Koden: Apache-2.0, se [`LICENSE`](LICENSE).
Datat: CC BY 4.0, upphovsman utlovat.se.

## Var arbetet står

Läget, besluten och lärdomarna ligger i det privata `handoff`-repot under
`projekt/storleksordningen/`. Börja där om du ska ta vid.
