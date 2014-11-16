sousvide_314 -- Sous Vide 4 π
=============================

sv314 är en Python-app för [Raspberry Pi][rpi]  som är avsedd att styra en
[sous vide][sv]-kokare; d.v.s. se till att hålla ett vattenbad så nära en av
användaren angiven måltemperatur som möjligt.

Appen beståre av två delar:
- Kontrollmodulen som övervakar och justerar temperaturen
- Webbappen som är byggd med [Flask][flask] och erbjuder både ett grafiskt
  användargränssnitt och ett RESTigt API via JSON.

Det finns även en låtsaskontrollmodul man kan använda för att köra webbappen på
en vanlig dator och få det att verka någorlunda som på riktigt.

## Köra appen

Prerekvisit är att du har [`virtualenv`][venv] och Python (~2.7) på din `$PATH`.
Med dessa verktyg kan du köra `./scripts/devenv-setup.sh` för att få ner alla
beroenden till din utvecklingsmiljö.

För att starta appen i dummy-läge, kör följande kommando i reporoten:

    SV314_USE_DUMMY=true ./scripts/run-server.sh

Diverse andra hjälpsamma script finns i katalogen `scripts/`.


## Kontrollmodulen

Temperaturkontroll sköts med två komponenter:
- En termometer för att läsa av nuvarande temperatur. Temperaturavläsningarna
  görs genom att läsa en fil som exponeras av drivrutinen.
- En värmekälla som kopplas till ett starkströmsrelä som slås av och på efter
  behov med en GPIO-pinne. (Vi använde en elektronisk grilltändare som
  värmekälla, men en vattenkokare eller portabel kokplatta torde också fungera.)

### Utvecklingsmöjligheter för kontrollmodulen
Temperaturen uppdateras bara var femtonde sekund. Om man inte hittar en bättre
komponent som ger tätare uppdateringar kan man istället arbeta ut en heuristik
för att beräkna när det borde bli dags att slå av/på värmen, istället för att
bara förlita sig på temperaturavläsningarna.

## Webappen

Webappen körs på http://localhost:5000 och har ett enkelt gränssnitt för att slå
av/på hela systemet, samt för att ställa in måltemperatur.

### Utvecklingsmöjligheter för webappen

För att bara nämna några:
- Rappare feedback efter justering av måltemperatur, avstängning och påslagning.
  Nu syns inte uppdateringar som gjorts förrän kontrollmodulen gjort ett varv i
  sin uppdateringsloop.
- Grafer över hur temperaturen fluktuerat.


  [rpi]: http://www.raspberrypi.org/
  [sv]: https://en.wikipedia.org/wiki/Sous-vide
  [flask]: http://flask.pocoo.org/
  [venv]: http://virtualenv.readthedocs.org/en/latest/
