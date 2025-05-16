# Gyro Cookie Clicker

Gyro Cookie Clicker er et klikkespill med en twist der spilleren tjener poeng ved å klikke og defeate en "gyro-cookie". Spillet inkluderer en poengtavle, chat-funksjon og muligheten til å lagre poeng i et leaderboard.

## Innhold
1. [Introduksjon](#introduksjon)
2. [Struktur](#struktur)
3. [Installasjon](#installasjon)
4. [Funksjoner](#funksjoner)
5. [Brukerveiledning](#brukerveiledning)
6. [FAQ](#faq)
7. [Brukertesting](#brukertesting)
8. [Lovverk og Universell Utforming](#lovverk-og-universell-utforming)
9. [Risikoanalyse](#risikoanalyse)
10. [Feilsøking](#feilsøking)

---

## Introduksjon
Gyro Cookie Clicker er et læringsprosjekt som kombinerer enkel spillutvikling med backend og frontend-teknologier. Målet er å forstå hvordan man lager en sikker og brukervennlig applikasjon som oppfyller kravene til moderne utvikling.

---

## Struktur
Prosjektet består av følgende komponenter:
```
GYRO_CLICKER/
│
├── static/                # Mappen for statiske filer som CSS, bilder og JavaScript
│   ├── css/               # CSS-filer for styling
│   │   └── styles.css     # Hovedstilark for prosjektet
│   │
│   ├── images/            # Bilder og ikoner brukt i spillet
│   │   ├── criticalhpgyro.svg  # SVG-bilde for kritisk HP
│   │   ├── gyro.svg           # SVG-bilde for gyro-cookie
│   │   ├── gyrofirstbite.svg  # SVG-bilde for første bite av gyro
│   │   ├── gyroyum.png        # PNG-bilde for en "yum"-effekt
│   │   ├── halfgyro.svg       # SVG-bilde for halv gyro
│   │   └── lowhpgyro.svg      # SVG-bilde for lav HP
│   │
│   ├── js/                # JavaScript-filer for spilllogikk
│   │   ├── game.js        # Hoved-JavaScript-fil for spillfunksjonalitet
│   │   └── minecraft_eat.mp3  # Lydfil for en spiseeffekt
│
├── templates/             # Mappen for HTML-maler brukt av Flask
│   ├── chat.html          # HTML-mal for chat-siden
│   ├── index.html         # HTML-mal for hovedsiden
│   ├── leaderboard.html   # HTML-mal for poengtavle
│   ├── login.html         # HTML-mal for innlogging
│   ├── logout.html        # HTML-mal for utlogging
│   └── register.html      # HTML-mal for registrering
│
├── app.py                 # Hovedfil for Flask-applikasjonen
├── gyro_clicker.db        # SQLite-database for brukere, poeng og meldinger
├── requirements.txt       # Liste over nødvendige Python-avhengigheter
└── .gitattributes         # Git-konfigurasjon for spesifikke filtyper
```

---

## Installasjon

### Forhåndskrav
- Python 3.8+
- Pip (Python Package Installer)

### Steg for steg
1. **Last ned prosjektet**:
   ```bash
   git clone https://github.com/Odyi/gyro-cookie-clicker.git
   cd gyro-cookie-clicker
   ```

2. **Installer nødvendige pakker**:
   Installer alle avhengigheter fra `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start applikasjonen**:
   Start Flask-serveren:
   ```bash
   python app.py
   ```

4. **Åpne i nettleseren**:
   Gå til `http://127.0.0.1:5000`.

---

## Funksjoner

1. **Registrering og Innlogging**:
   - Registrer deg med et brukernavn og passord.
   - Logg inn for å få tilgang til spillet og chattefunksjonen.

2. **Klikkespill**:
   - Klikk på cookien og defeat den for å tjene poeng.

3. **Poengtavle**:
   - Se hvordan du rangerer sammenlignet med andre spillere.

4. **Chat**:
   - Delta i samtaler med andre spillere i sanntid.

---

## Brukerveiledning

### Komme i gang
1. **Start serveren**:
   ```bash
   python app.py
   ```
2. **Registrer deg**:
   - Fyll inn brukernavn og passord på registreringssiden.
3. **Logg inn**:
   - Bruk innloggingsinformasjonen din for å få tilgang til spillet.

### Spill spillet
- Klikk på cookien for å samle poeng.
- Send inn poengene dine til poengtavlen.

### Chatte med andre
- Gå til "Chat"-siden for å delta i samtaler med andre spillere.

---

## FAQ

### Hvordan registrerer jeg meg?
Gå til registreringssiden, fyll ut brukernavn og passord, og klikk "Registrer".

### Hvordan logger jeg inn?
Gå til innloggingssiden, skriv inn brukernavn og passord, og klikk "Logg inn".

### Hvor lagres poengene mine?
Poengene lagres i SQLite-databasen som er koblet til brukernavnet ditt.

### Hva gjør jeg hvis jeg har glemt passordet?
For øyeblikket må du kontakte spillutvikleren for å tilbakestille passordet.

---

## Brukertesting

### Gjennomføring
Tre testpersoner spilte spillet og ga tilbakemelding.

### Tilbakemeldinger og forbedringer
1. **Innlogging**:
   - Problem: Uklar feilmelding ved feil passord.
   - Løsning: Mer spesifikke feilmeldinger ble lagt til.

2. **Poengtavle**:
   - Problem: Manglet forklaring på hvordan poengene fungerer.
   - Løsning: Forklarende tekst ble lagt til.

3. **Design**:
   - Problem: Noen brukere fant layouten uoversiktlig.
   - Løsning: Redesign av forsiden.

---

## Lovverk og Universell Utforming

### Personvern
- Passord lagres kryptert ved hjelp av hashing.
- Ingen sensitive data deles med tredjeparter.

### Universell Utforming
- Designet for enkel navigasjon og skjermleserkompatibilitet.
- Retningslinjer fra WCAG følges.

### Relevante lover
- **GDPR**: Data håndteres i tråd med personvernforordningen.
- **Likestillings- og diskrimineringsloven**: Fokus på universell utforming.

---

## Risikoanalyse

### Tekniske Risikoer
1. **Datatap**:
   - Risiko: Databasen kan bli korrupt.
   - Tiltak: Regelmessige sikkerhetskopier.

2. **Sikkerhetsproblemer**:
   - Risiko: Passord kan bli kompromittert.
   - Tiltak: Bruk av hashing og sikre sesjoner.

### Brukeropplevelse
1. **Navigasjon**:
   - Risiko: Brukere kan finne grensesnittet forvirrende.
   - Tiltak: Forenklet design og hyppig brukertesting.

---

## Feilsøking

### Problem: Passord fungerer ikke ved innlogging
- **Årsak**: Passordene var ikke hashet i databasen.
- **Løsning**: Implementerte `werkzeug.security` for hashing.

### Problem: Poengtavlen viste duplikater
- **Årsak**: Samme bruker kunne sende inn flere poengsummer.
- **Løsning**: SQL-spørringen ble oppdatert for å erstatte gamle poeng.

---

## Nødvendige pakker
Alle nødvendige Python-pakker er spesifisert i `requirements.txt`:
```
Flask==2.0.3
Werkzeug==2.0.3
```

Installer dem med:
```bash
pip install -r requirements.txt
```

---

Med denne dokumentasjonen har du alt du trenger for å forstå, bruke og videreutvikle prosjektet Gyro Cookie Clicker. Gleder meg å se prosjektene deres!
