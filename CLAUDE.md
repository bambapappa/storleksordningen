# Projektminne för Storleksordningen

Regler som gäller allt arbete i det här repot — chatt, commit-texter,
PR-texter, sajtcopy, dokumentation.

## Vad det är

utlovat.se i tre dimensioner: en värld man går omkring i, byggd av
partiernas löften, ståndpunkter och riksdagshandlingar inför valet 2026.
Motorn kommer från [ImmersaDocs](https://github.com/bambapappa/ImmersaDocs);
datat kommer från utlovat.se:s öppna gränssnitt. Ingenting räknas om här och
ingen språkmodell är inblandad — det som ritas är det som står i registret.

Repot är publikt. **En gren i ett publikt repo är publik**: allt som pushas
är läsbart för vem som helst, mergat eller inte.

## De fyra reglerna

Går före allt annat. De följer av vad utlovat.se är.

1. **Måttstocken ska alltid synas.** Höjd är logaritmisk — annars går världen
   inte att gå i, beloppen spänner över fem tiopotenser. Men logaritmen gör
   hundra gånger till dubbelt så högt, och den skillnaden är hela poängen med
   granskningen. Ett belopp får därför aldrig visas som enbart en höjd:
   siffran i klartext och en synlig skala hör alltid ihop med objektet.
2. **De åtta partierna behandlas likadant.** Samma ljus, samma kamera, samma
   avstånd, samma formspråk, samma startläge. Grammatiken är deterministisk,
   så likabehandlingen går att kontrollera och inte bara påstå.
3. **Citatet läses aldrig i VR.** Ordagranna citat, källa, arkivlänk och
   uträkning hör hemma i en vanlig tvådimensionell panel. Läshastigheten
   faller kraftigt i headset, och citatet är det enda som inte får bli
   ungefär.
4. **Tomrum ritas som tomrum.** Saknas ett rent citat, eller kostar ett löfte
   noll för att en lag bär det, ska det synas — inte utelämnas och inte ritas
   som något litet. Fyra av tio löften i registret kostar noll med flit, och
   drygt sju av tio celler i frågerutnätet är tomma. Ritas de bort försvinner
   större delen av sanningen.

## Formen

**Inte fantasyskog — pappersdiorama.** utlovat.se är byggd i papper och
svärta, utan rundade hörn. Samma palett gäller här. Ingen dimma, inga
partiklar, ingen musik, ingenting episkt. Ju vackrare världen är, desto mer
känns beloppen påhittade — och att de inte är påhittade är hela värdet.

Rättelser ritas som synliga lagningar i pappret. Tyst rättelse är förbjuden
på utlovat.se, och det gäller även här.

## Språkregler

Ärvda från utlovat.se, och de kostar ingenting att följa.

- **Ordet "verbatim" är förbjudet.** Skriv "ordagrant", "exakt citat" eller
  "ord för ord". Gäller överallt: chatt, commits, PR-texter, sajttexter,
  dokumentation.
- **Skriv "mänskligt beslut", aldrig "ägarbeslut".**
- Skriv språk som alla förstår. Ingen teknisk jargong i texter som möter
  läsare, partier eller journalister. Interna koder hör aldrig hemma i något
  som publiceras.

## Data

Hämtas från utlovat.se, aldrig kopierat hit:

- `https://utlovat.se/api/v1/` — löften, partier, sakfrågor, ståndpunkter
- `https://utlovat.se/handlingsvagen/api/hv/` — handlingar och domar

Data är **CC BY 4.0** och kräver att "utlovat.se" anges som källa, även på
den här sajten. Två fält som behövs saknas i dag i det publika
gränssnittet — den öppna uträkningen och jämförelsekonstanterna. De ska
läggas till i `valflask`, inte kringgås genom att läsa råfiler.

Sajten bakom gränssnittet ligger bakom Cloudflare, som nekar
`Python-urllib` rakt av. Sätt en egen, ärlig användaragent — utge dig inte
för att vara en webbläsare.

## ImmersaDocs

Motorn ligger i sitt eget repo och ska förbli allmän. **Domänspecifikt
beteende hör hemma i profiler, alltså konfiguration — aldrig som särfall
inne i motorn.** Behöver något som saknas i kärnan byggas, byggs det som
allmän förmåga där, inte som stöd för utlovat här.

Läs `spik/README.md` innan du planerar mot en funktion i ImmersaDocs. Dess
README beskriver flera saker i presens som inte finns i koden.

## Överlämningen ligger inte här

Läget, besluten och lärdomarna ligger i det privata repot
`bambapappa/handoff` under `projekt/storleksordningen/`. Börja där, med
`AGENTS.md`. Skriv inte en ny överlämning här.
