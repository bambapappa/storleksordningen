# Spiken — vad som händer om man matar in registret rakt av

En mätning, inte en produkt. Frågan var enkel: **hur långt kommer man med
ImmersaDocs som den ser ut i dag, utan att ändra en enda rad i den?**

Svaret är: förvånansvärt långt på de kanaler som finns, och inte alls på de
fyra av tio löften som kostar noll.

Körd 2026-08-01 mot utlovat.se:s öppna gränssnitt.

## Så gick det till

ImmersaDocs väljer profil genom att titta efter attributet `requestedAmount`
på objektet den får. Ett vanligt Python-objekt med rätt attributnamn går
därför rakt genom `grant`-profilen utan att någon kod behöver röras. Löftena
kläddes alltså som bidragsansökningar:

| utlovat | ImmersaDocs | |
| --- | --- | --- |
| kostnad för mandatperioden | `requestedAmount` | → höjd, logaritmisk |
| parti | `fundingBody` | → mark |
| kategori | `fordClassification` | → trädart |
| Handlingsvågens dom | `trl` | → mognadsfas |
| antal kopplingar | `workPackages` | → grenar |
| delat löfte (`group_id`) | `consortiumPartners` | → stammar |

Mappningstabellerna ligger i [`profil-utlovat.json`](profil-utlovat.json) och
läses av ImmersaDocs egen `load_profiles()`. Partinamn blev mark, kategorier
blev arter. Ingen kod ändrad, i något repo.

```
python spik/spik.py          # kräver pydantic; se IMMERSADOCS_ROT i spik.py
```

## Vad mätningen visade

```
263 av 428 löften gick genom motorn
165 kraschade
deterministisk: ja
höjd: 0,30 … 5,49   (5,19 tiopotenser)
```

### 1. Fyra av tio löften kan inte komma in i världen

**Alla 165 kraschar på samma rad**, med samma fel:

```
ValueError: Budget must be positive, got 0
```

`budget_to_height()` tar logaritmen av beloppet och vägrar ta emot noll. Och
noll är inget fel i datat — det är ett resultat. Enligt utlovat.se:s
kostnadsregler prissätts en lag, ett förbud, en avreglering eller ett
utredningslöfte till noll, därför att det är lagändringen som bär löftet, inte
plånboken.

Det drabbar **alla åtta partierna**, i den här ordningen: M 32, C 26, S 24,
MP 24, V 20, L 14, KD 14, SD 11. Det är alltså inte en egenhet hos ett parti
utan en egenskap hos registret.

En värld som ritar 263 av 428 löften och tiger om resten är inte en
förenkling, den är en felaktig bild. Nollöftena behöver en egen form — något
man går förbi och kan läsa, som säger att lagen bär det här löftet — och
motorn behöver kunna beskriva ett objekt som inte har någon höjd alls.

### 2. Höjdskalan beter sig bra

5,19 tiopotenser mellan minsta och största löftet, och fördelningen är nära
log-normal: de flesta objekt hamnar i mitten, ett fåtal blir jättar. Det är
goda nyheter för navigerbarheten — en logaritmisk skog blir inte platt.

Det ändrar inte att logaritmen döljer just den skillnad granskningen handlar
om. Måttstocken måste synas, och siffran stå bredvid.

### 3. Grupperingen finns som namn, men inte som plats

Alla åtta partier fick var sin mark, och alla nio kategorier fick var sin art.
Kanalerna fungerar.

Men `biome` är bara en sträng på varje objekt, och `SceneDescriptor` bär
ingen position. Objekt med samma mark hamnar därför inte bredvid varandra —
frontenden ställer ut allt i en cirkel och ger varje objekt sin egen lilla
markskiva. Det finns alltså ingen partiets skog, bara 263 lösryckta träd som
råkar veta vilket parti de tillhör.

Detsamma gäller de delade löftena: 109 löften bär ett `group_id`, men
släktskapet överlever bara som en siffra i `consortium_size`. Ingen relation,
ingen flätning, ingen kant.

### 4. Handlingsvågens signal syns nästan inte

Av 263 objekt fick 247 fasen `seed`. Bara 16 fick något annat.

Två skäl: Handlingsvågens rutnät täcker 149 löften, inte 428, och en stor del
av de dömda löftena är just sådana som kostar noll och därför redan kraschat.
Mognadskanalen — den vackraste mappningen på papperet — är i praktiken tom
tills de två andra problemen är lösta.

### 5. Fältnamnen ljuger

Utdatan innehåller `requested_amount_eur: 12000` för ett löfte på 12 miljarder
kronor. Attributnamnen är grant-domänens och bär ett valutapåstående som är
falskt här. Så länge det bara är en spik gör det ingenting, men det visar att
`attributes` är en fri påse utan kontrakt: profilen bestämmer innehållet, och
ingenting hindrar att det säger fel saker.

### 6. Determinismen håller

Samma indata två gånger gav byte-identisk utdata över alla 263 objekt. Det är
den egenskap hela idén vilar på — att en granskningssajts visualisering ska gå
att kontrollera, inte bara betraktas — och den bekräftades.

## Slutsats

Motorn bär. Det som saknas är inte mappningar utan **scennivån**:
position, gruppering, färg och relationer mellan objekt, plus förmågan att
beskriva ett objekt utan höjd. Fyra saker, alla i kärnan, och alla saknas lika
mycket för ImmersaDocs två befintliga profiler.

## Vad som ligger här

| Fil | |
| --- | --- |
| `spik.py` | mätningen |
| `profil-utlovat.json` | mappningstabellerna, läses av ImmersaDocs `load_profiles()` |
| `resultat/rapport.json` | siffrorna ovan, maskinläsbara |
| `resultat/scener.json` | alla 263 objekt som motorn producerade |
| `resultat/kraschade.json` | alla 165 som inte kom in, med skäl |

Resultaten är incheckade med flit. De är bevis för påståendena ovan, och en
körning som ingen kan reproducera är inte en mätning.
