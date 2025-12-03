# 🐝 VoBee AI Asistent

**Váš osobní finanční poradce v češtině** - Progresivní Webová Aplikace (PWA)

![VoBee AI](icons/icon-192x192.png)

## 📋 Popis

VoBee AI Asistent je interaktivní chatbot, který vám pomůže s finančními dotazy v následujících oblastech:

- 💰 **Kryptoměny** - Bitcoin, Ethereum, peněženky, burzy
- 📈 **Akcie** - investování, brokery, dividendy
- 📊 **ETF** - exchange-traded fondy, typy, jak nakupovat
- 📚 **Finanční gramotnost** - rozpočet, složené úročení, inflace
- ⚖️ **Insolvence** - oddlužení, proces, prevence
- 💵 **Šetření** - jak efektivně spořit, stavební spoření, penzijko

## ✨ Funkce

- ✅ **Offline režim** - funguje i bez internetu
- ✅ **Instalace na plochu** - PWA s ikonou na domovské obrazovce
- ✅ **Lokální ukládání** - historie konverzací se ukládá v prohlížeči
- ✅ **Responzivní design** - funguje na mobilu i počítači
- ✅ **Česky** - kompletně v českém jazyce

## 🚀 Spuštění

### Pomocí jednoho příkazu

```bash
npx http-server -p 8080 -c-1
```

Poté otevřete v prohlížeči: [http://localhost:8080](http://localhost:8080)

### Alternativní spuštění

```bash
# S npm
npm start

# S otevřením prohlížeče
npm run dev

# S Python
python3 -m http.server 8080

# S PHP
php -S localhost:8080
```

## 📱 Instalace jako aplikace

1. Otevřete aplikaci v prohlížeči Chrome nebo Edge
2. Klikněte na tlačítko "Instalovat" v horní liště
3. Potvrďte instalaci
4. Aplikace se přidá na vaši plochu

## 🛠️ Technologie

- **HTML5** - struktura
- **CSS3** - responzivní design, animace
- **JavaScript** - chatbot logika, PWA funkce
- **Service Worker** - offline podpora
- **Web Storage API** - lokální ukládání dat

## 📁 Struktura projektu

```
VoBee-AI-Assistant/
├── index.html          # Hlavní HTML stránka
├── manifest.json       # PWA manifest
├── sw.js              # Service Worker
├── css/
│   └── style.css      # Styly aplikace
├── js/
│   ├── app.js         # Hlavní aplikační logika
│   ├── chatbot.js     # Logika chatbota
│   └── knowledge-base.js  # Databáze znalostí
├── icons/             # PWA ikony
└── README.md          # Dokumentace
```

## 🔒 Soukromí

- Všechna data jsou uložena **pouze lokálně** ve vašem prohlížeči
- Žádná data nejsou odesílána na server
- Historie lze kdykoliv vymazat příkazem "vymaž historii"

## ⚠️ Disclaimer

VoBee AI Asistent poskytuje pouze obecné informace a nenahrazuje profesionální finanční poradenství. Před jakýmkoliv investičním rozhodnutím konzultujte kvalifikovaného finančního poradce.

## 📄 Licence

MIT License

---

Vytvořeno s 🐝 v České republice