# VoBee AI Asistent 🐝

Progresivní webová aplikace (PWA) poskytující českého chatbota pro finanční vzdělávání v oblastech kryptoměn, akcií, ETF, finanční gramotnosti, insolvence a šetření.

## Funkce

- **PWA podpora**: Service worker pro offline funkcionalitu, manifest pro instalaci na domovskou obrazovku
- **Česká databáze znalostí**: Komplexní Q&A databáze finančních témat s kontextovými odpověďmi
- **Interaktivní UI**: Navigace podle témat, rychlé odpovědi, historie konverzace v localStorage
- **Spuštění jedním příkazem**: `npx http-server -p 8080` nebo `npm start`

## Struktura projektu

```
├── index.html              # Hlavní shell aplikace
├── sw.js                   # Service worker (cache-first strategie)
├── manifest.json           # PWA manifest
├── css/style.css           # Tmavý motiv, responzivní design
├── js/
│   ├── app.js              # PWA handlery, UI logika
│   ├── chatbot.js          # Zpracování zpráv, pattern matching
│   └── knowledge-base.js   # Česká finanční databáze znalostí
└── icons/                  # PNG ikony 72x72 až 512x512
```

## Témata

- **Kryptoměny**: Bitcoin, Ethereum, peněženky, investování do krypta
- **Akcie**: Základy, dividendy, P/E ratio, jak začít
- **ETF**: Co je ETF, jak vybrat, nákladovost (TER)
- **Finanční gramotnost**: Rozpočet, inflace, nouzový fond
- **Insolvence**: Oddlužení, exekuce, řešení dluhů
- **Šetření**: Tipy na spoření, stavební spoření, penzijní připojištění

## Použití

### Spuštění lokálně

```bash
# Pomocí http-server
npx http-server -p 8080 -c-1

# Otevřete http://localhost:8080
```

### Instalace jako PWA

1. Otevřete aplikaci v podporovaném prohlížeči (Chrome, Edge, Firefox)
2. Klikněte na "Nainstalovat" v promptu nebo přes menu prohlížeče
3. Aplikace se přidá na domovskou obrazovku

## Technologie

- Vanilla JavaScript (bez frameworků)
- CSS3 s custom properties
- Service Worker API
- Web App Manifest
- LocalStorage pro persistenci

## Licence

MIT