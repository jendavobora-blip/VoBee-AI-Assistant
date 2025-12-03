// VoBee AI Assistant - Knowledge Base
// Databáze znalostí v češtině

const KnowledgeBase = {
    // Obecné odpovědi
    general: {
        greeting: [
            "Ahoj! Jsem VoBee, váš finanční asistent. 🐝 Jak vám mohu pomoci?",
            "Dobrý den! Jsem tu, abych vám pomohl s vašimi finančními dotazy.",
            "Zdravím! Co byste chtěli vědět o financích?"
        ],
        farewell: [
            "Na shledanou! Nezapomeňte, že moudrá včela šetří! 🐝",
            "Rád jsem vám pomohl! Přeji úspěšné investování!",
            "Děkuji za váš čas. Buďte finančně moudří!"
        ],
        thanks: [
            "Rádo se stalo! Máte další otázku?",
            "Nemáte zač! Jsem tu pro vás kdykoliv.",
            "To je můj úkol! Mohu vám ještě s něčím pomoci?"
        ],
        unknown: [
            "Omlouvám se, na tuto otázku nemám přesnou odpověď. Zkuste se zeptat jinak nebo vyberte konkrétní téma nahoře.",
            "Tato otázka je mimo mou specializaci. Mohu vám pomoci s kryptoměnami, akciemi, ETF, finanční gramotností, insolvencí nebo šetřením.",
            "Nejsem si jistý odpovědí. Vyberte prosím téma z nabídky nebo formulujte otázku jinak."
        ]
    },

    // Kryptoměny
    crypto: {
        basics: {
            question: ["co je kryptoměna", "kryptoměny", "cryptocurrency", "co jsou krypto"],
            answer: "Kryptoměny jsou digitální nebo virtuální měny zabezpečené kryptografií. Fungují na technologii blockchain, což je decentralizovaná databáze transakcí. Nejznámější kryptoměnou je Bitcoin (BTC), který byl vytvořen v roce 2009. Kryptoměny umožňují rychlé a levné mezinárodní převody bez prostředníků."
        },
        bitcoin: {
            question: ["bitcoin", "btc", "co je bitcoin"],
            answer: "Bitcoin (BTC) je první a nejznámější kryptoměna. Byl vytvořen anonymní osobou nebo skupinou pod pseudonymem Satoshi Nakamoto v roce 2009. Maximální množství Bitcoinů je omezeno na 21 milionů. Bitcoin slouží jako digitální zlato a uchovatel hodnoty. ⚠️ Upozornění: Investice do kryptoměn jsou vysoce rizikové!"
        },
        ethereum: {
            question: ["ethereum", "eth", "co je ethereum", "ether"],
            answer: "Ethereum (ETH) je druhá největší kryptoměna podle tržní kapitalizace. Na rozdíl od Bitcoinu umožňuje Ethereum vytvářet smart kontrakty a decentralizované aplikace (dApps). Ethereum 2.0 přešlo na Proof of Stake, což snižuje energetickou náročnost."
        },
        risks: {
            question: ["riziko", "rizika", "nebezpečí krypto", "je to bezpečné"],
            answer: "⚠️ Rizika investování do kryptoměn:\n\n• Vysoká volatilita - ceny mohou prudce kolísat\n• Regulační nejistota - zákony se mohou měnit\n• Kybernetické hrozby - hacky burz a peněženek\n• Ztráta přístupu - zapomenuté klíče = ztracené prostředky\n• Podvody - mnoho scamů a fake projektů\n\nNikdy neinvestujte více, než si můžete dovolit ztratit!"
        },
        wallet: {
            question: ["peněženka", "wallet", "jak uložit", "kde uchovávat"],
            answer: "Typy krypto peněženek:\n\n🔐 Hot wallets (online):\n• Mobilní aplikace (Trust Wallet, MetaMask)\n• Webové peněženky na burzách\n• Pohodlné, ale méně bezpečné\n\n🔒 Cold wallets (offline):\n• Hardware peněženky (Ledger, Trezor)\n• Paper wallets\n• Bezpečnější pro dlouhodobé držení\n\nDoporučení: Pro větší částky používejte hardware peněženku!"
        },
        buy: {
            question: ["kde koupit", "jak koupit", "burza", "nákup krypto"],
            answer: "Kde koupit kryptoměny v ČR:\n\n🏦 Licencované burzy:\n• Coinbase - největší světová burza\n• Binance - nejvíce obchodních párů\n• Kraken - dobrá bezpečnost\n• Anycoin - česká burza\n\n✅ Tipy pro nákup:\n1. Ověřte si burzu a její regulaci\n2. Používejte 2FA autentizaci\n3. Začněte s malými částkami\n4. Nikdy nesdílejte své klíče"
        }
    },

    // Akcie
    stocks: {
        basics: {
            question: ["co jsou akcie", "akcie", "co je akcie", "stock"],
            answer: "Akcie jsou cenné papíry představující podíl na vlastnictví společnosti. Když koupíte akcii, stáváte se spoluvlastníkem firmy. Akcie nabízejí:\n\n• Kapitálové zisky - růst ceny\n• Dividendy - podíl na zisku\n• Hlasovací práva - u některých akcií\n\nAkcie se obchodují na burzách jako NYSE, NASDAQ nebo v ČR na pražské burze (PSE)."
        },
        how_to_invest: {
            question: ["jak investovat", "jak začít", "investování do akcií", "začátečník"],
            answer: "Jak začít investovat do akcií:\n\n1️⃣ Vzdělávejte se - pochopte základy\n2️⃣ Stanovte si cíle a horizont\n3️⃣ Určete kolik můžete investovat\n4️⃣ Vyberte brokera (Fio, Degiro, XTB)\n5️⃣ Otevřete účet a ověřte identitu\n6️⃣ Začněte s diverzifikovaným portfoliem\n7️⃣ Pravidelně investujte (DCA strategie)\n\n💡 Tip: Pro začátečníky jsou vhodné ETF fondy!"
        },
        broker: {
            question: ["broker", "makléř", "kde obchodovat", "jaký broker"],
            answer: "Populární brokeři pro české investory:\n\n🇨🇿 Čeští brokeři:\n• Fio e-Broker - nízké poplatky na PSE\n• Patria - pro zkušenější\n\n🌍 Zahraniční brokeři:\n• Degiro - nízké poplatky\n• XTB - bez poplatků na akcie\n• Interactive Brokers - pro aktivní obchodníky\n• Trading 212 - jednoduchý pro začátečníky\n\n⚠️ Vždy ověřte regulaci brokera (ČNB, FCA, SEC)!"
        },
        dividend: {
            question: ["dividenda", "dividendy", "výplata dividend", "dividend"],
            answer: "Dividendy jsou část zisku společnosti vyplácená akcionářům.\n\n📊 Klíčové pojmy:\n• Dividendový výnos = roční dividenda / cena akcie\n• Ex-dividend datum = rozhodné datum pro nárok\n• Výplatní poměr = % zisku vyplaceného jako dividenda\n\n💰 Dividendové akcie v ČR:\n• ČEZ - energetická společnost\n• Komerční banka\n• O2 Czech Republic\n\n⚠️ Dividendy jsou v ČR zdaněny 15%"
        },
        risks: {
            question: ["riziko akcií", "rizika", "jsou akcie bezpečné"],
            answer: "Rizika investování do akcií:\n\n⚠️ Hlavní rizika:\n• Tržní riziko - ceny mohou klesat\n• Firemní riziko - bankrot společnosti\n• Měnové riziko - u zahraničních akcií\n• Likvidita - některé akcie těžko prodáte\n• Inflace - snižuje reálnou hodnotu\n\n🛡️ Jak snížit riziko:\n• Diverzifikace portfolia\n• Dlouhodobý horizont (5+ let)\n• Pravidelné investování\n• Nekupovat na margin"
        }
    },

    // ETF
    etf: {
        basics: {
            question: ["co je etf", "etf", "exchange traded fund", "fondy"],
            answer: "ETF (Exchange Traded Fund) je burzovně obchodovaný fond, který sleduje určitý index, sektor nebo komoditu.\n\n✅ Výhody ETF:\n• Nízké poplatky (často pod 0.5%)\n• Okamžitá diverzifikace\n• Transparentnost\n• Likvidita - obchoduje se jako akcie\n\n📈 Populární ETF:\n• S&P 500 ETF (VOO, SPY)\n• MSCI World ETF\n• Emerging Markets ETF"
        },
        types: {
            question: ["typy etf", "druhy etf", "jaké etf", "které etf"],
            answer: "Typy ETF fondů:\n\n📊 Indexové ETF:\n• Sledují akciové indexy (S&P 500, DAX)\n• Nejpopulárnější a nejlevnější\n\n💰 Dividendové ETF:\n• Zaměřené na dividendové akcie\n• Pravidelný příjem\n\n📈 Sektorové ETF:\n• Technologie, zdravotnictví, energie\n\n🌍 Regionální ETF:\n• USA, Evropa, Emerging Markets\n\n📦 Komoditní ETF:\n• Zlato, stříbro, ropa\n\n🏠 REIT ETF:\n• Nemovitostní fondy"
        },
        how_to_buy: {
            question: ["jak koupit etf", "kde koupit etf", "nákup etf"],
            answer: "Jak koupit ETF:\n\n1️⃣ Vyberte brokera (XTB, Degiro, Fio)\n2️⃣ Otevřete účet a ověřte identitu\n3️⃣ Vložte prostředky\n4️⃣ Vyberte ETF (ticker symbol)\n5️⃣ Zadejte nákupní příkaz\n\n💡 Tipy pro výběr ETF:\n• TER (Total Expense Ratio) pod 0.5%\n• Dostatečná velikost fondu (100M+ EUR)\n• UCITS verze pro EU investory\n• Akumulační vs distribuční"
        },
        accumulating_vs_distributing: {
            question: ["akumulační", "distribuční", "rozdíl etf", "reinvestice"],
            answer: "Akumulační vs Distribuční ETF:\n\n🔄 Akumulační (ACC):\n• Dividendy automaticky reinvestovány\n• Výhodnější pro dlouhodobý růst\n• Jednodušší daňově v ČR\n• Ideální pro budování majetku\n\n💵 Distribuční (DIST):\n• Dividendy vypláceny na účet\n• Pravidelný pasivní příjem\n• Nutné zdanit dividendy (15%)\n• Vhodné pro důchodce\n\n💡 Pro většinu investorů v ČR jsou akumulační ETF výhodnější!"
        },
        recommended: {
            question: ["doporučení etf", "nejlepší etf", "které etf koupit", "populární etf"],
            answer: "Populární ETF pro české investory:\n\n🌍 Celosvětové:\n• iShares MSCI World (IWDA) - TER 0.20%\n• Vanguard FTSE All-World (VWCE) - TER 0.22%\n\n🇺🇸 USA:\n• iShares S&P 500 (SXR8) - TER 0.07%\n• Invesco QQQ (NASDAQ) - TER 0.20%\n\n🇪🇺 Evropa:\n• iShares STOXX Europe 600 - TER 0.20%\n\n⚠️ Toto není investiční doporučení! Vždy proveďte vlastní analýzu."
        }
    },

    // Finanční gramotnost
    literacy: {
        basics: {
            question: ["finanční gramotnost", "základy", "jak začít", "co je finanční gramotnost"],
            answer: "Finanční gramotnost je schopnost rozumět penězům a efektivně s nimi nakládat.\n\n📚 Základní pilíře:\n1. Rozpočet - sledujte příjmy a výdaje\n2. Šetření - vytvořte si finanční rezervu\n3. Dluhy - vyhněte se zbytečným dluhům\n4. Investice - nechte peníze pracovat\n5. Pojištění - ochrana před riziky\n\n🎯 Pravidlo 50/30/20:\n• 50% na potřeby (nájem, jídlo)\n• 30% na přání (zábava, koníčky)\n• 20% úspory a investice"
        },
        budget: {
            question: ["rozpočet", "jak sestavit rozpočet", "osobní finance", "výdaje"],
            answer: "Jak sestavit osobní rozpočet:\n\n📝 Kroky:\n1. Spočítejte čisté měsíční příjmy\n2. Sepište všechny pravidelné výdaje\n3. Sledujte proměnlivé výdaje (2-3 měsíce)\n4. Najděte oblasti k úspoře\n5. Stanovte si finanční cíle\n\n💡 Užitečné nástroje:\n• Excel/Google Sheets\n• Aplikace: Wallet, YNAB, Spendee\n• Bankovní aplikace s kategorizací\n\n⚡ Tip: Automatizujte spoření - hned po výplatě!"
        },
        emergency_fund: {
            question: ["nouzový fond", "rezerva", "finanční polštář", "kolik mít v rezervě"],
            answer: "Finanční rezerva (nouzový fond):\n\n💰 Kolik mít v rezervě:\n• Minimum: 3 měsíční výdaje\n• Ideál: 6 měsíčních výdajů\n• S rodinou: 9-12 měsíčních výdajů\n\n🏦 Kde ji držet:\n• Spořicí účet (okamžitá dostupnost)\n• Termínovaný vklad (vyšší úrok)\n• Stavební spoření (bonus od státu)\n\n⚠️ Pravidla:\n• Použít jen na skutečné nouze\n• Pravidelně doplňovat\n• Oddělený účet od běžného"
        },
        compound_interest: {
            question: ["složené úročení", "compound interest", "úroky z úroků", "osmý div světa"],
            answer: "Složené úročení - 'osmý div světa' (Einstein)\n\n📈 Jak funguje:\nVáš výnos generuje další výnosy. Čím déle investujete, tím větší efekt.\n\n💡 Příklad:\n10 000 Kč měsíčně, 7% ročně:\n• Po 10 letech: 1,7 mil. Kč\n• Po 20 letech: 5,2 mil. Kč\n• Po 30 letech: 12,2 mil. Kč\n\n🎯 Klíčové faktory:\n1. Čas - začněte co nejdříve\n2. Pravidelnost - investujte každý měsíc\n3. Reinvestice - nechte výnosy pracovat"
        },
        inflation: {
            question: ["inflace", "co je inflace", "znehodnocení peněz"],
            answer: "Inflace = růst cenové hladiny, snížení kupní síly peněz.\n\n📊 Dopad inflace:\nPři 5% inflaci za 10 let:\n100 000 Kč dnes = 61 391 Kč kupní síly\n\n🛡️ Ochrana před inflací:\n• Investice do akcií/ETF\n• Nemovitosti\n• Dluhopisy vázané na inflaci\n• Komodity (zlato)\n\n⚠️ Proč je důležité investovat:\nPeníze na běžném účtu ztrácí hodnotu! Minimálně je dejte na spořicí účet nebo do konzervativních investic."
        },
        taxes: {
            question: ["daně", "zdanění investic", "jak zdanit", "daň z příjmu"],
            answer: "Zdanění investic v ČR:\n\n📊 Sazby daně:\n• Příjmy z kapitálového majetku: 15%\n• Dividendy: 15% (srážková daň)\n• Kryptoměny: 15% (jako ostatní příjem)\n\n✅ Osvobození od daně:\n• Akcie držené 3+ roky\n• Příjem do 100 000 Kč ročně (z prodeje CP)\n• Příjem do 30 000 Kč ročně (osvobozené příjmy)\n\n💡 Tip: Využijte časový test - držte akcie min. 3 roky!"
        }
    },

    // Insolvence
    insolvency: {
        basics: {
            question: ["co je insolvence", "insolvence", "oddlužení", "bankrot"],
            answer: "Insolvence je situace, kdy dlužník není schopen splácet své dluhy.\n\n📋 Možnosti řešení:\n1. Oddlužení (osobní bankrot)\n2. Konkurz\n3. Reorganizace (firmy)\n\n✅ Podmínky oddlužení:\n• Poctivý záměr\n• Schopnost splatit min. 30% dluhů (nebo méně od 2019)\n• Maximálně 5 let splácení\n• Žádné podvody\n\n⚠️ Důsledky:\n• Zápis v registru dlužníků\n• Omezení nakládání s majetkem"
        },
        process: {
            question: ["jak probíhá", "proces oddlužení", "průběh insolvence", "kroky"],
            answer: "Průběh oddlužení:\n\n1️⃣ Podání návrhu\n• Sepsání návrhu (advokát/notář)\n• Seznam dluhů a majetku\n• Poplatek 2 000 Kč\n\n2️⃣ Rozhodnutí soudu\n• Soud posoudí návrh\n• Ustanovení insolvenčního správce\n\n3️⃣ Schválení oddlužení\n• Splnění podmínek\n• Stanovení splátkového kalendáře\n\n4️⃣ Splácení (max 5 let)\n• Pravidelné splátky\n• Dohled správce\n\n5️⃣ Osvobození od zbytku dluhů"
        },
        consequences: {
            question: ["důsledky", "následky", "co mi hrozí", "omezení"],
            answer: "Důsledky insolvence:\n\n⚠️ Omezení:\n• Nelze uzavírat nové úvěry\n• Omezená dispozice s majetkem\n• Povinnost oznámit změny příjmu\n• Zápis v insolvenčním rejstříku\n\n📋 Po oddlužení:\n• Zůstatek dluhů odpuštěn\n• Výmaz z rejstříku (po 5 letech)\n• Lze opět žádat o úvěry\n\n💡 Výhody:\n• Zastavení exekucí\n• Jasný plán splácení\n• Konec stresujících situací"
        },
        prevention: {
            question: ["jak předejít", "prevence", "vyhnout se dluhům", "nezadlužit se"],
            answer: "Jak předejít předlužení:\n\n✅ Prevence:\n1. Vytvořte si rozpočet a dodržujte ho\n2. Mějte finanční rezervu (3-6 měsíců)\n3. Vyhněte se spotřebitelským úvěrům\n4. Nekupujte na splátky zbytečnosti\n5. Čtěte smlouvy před podpisem\n\n🚨 Varovné signály:\n• Splácíte půjčkou půjčku\n• Nevíte kolik dlužíte\n• Nemůžete platit nájem/energie\n• Ignorujete upomínky\n\n📞 Pomoc: Občanské poradny, finanční arbitr"
        },
        where_to_help: {
            question: ["kde najít pomoc", "pomoc s dluhy", "poradenství", "kam se obrátit"],
            answer: "Kde hledat pomoc s dluhy:\n\n📞 Bezplatná pomoc:\n• Občanské poradny - www.obcanskeporadny.cz\n• Finanční arbitr - www.finarbitr.cz\n• Člověk v tísni - dluhové poradenství\n• Poradna při finanční tísni - www.financnitisen.cz\n\n⚖️ Právní pomoc:\n• Advokáti (insolvenční specialisté)\n• Notáři\n• Exekutorská komora ČR\n\n⚠️ Pozor na:\n• Oddlužovací firmy (často podvodné)\n• Vysoké poplatky za sepsání návrhu\n• Sliby o smazání dluhů"
        }
    },

    // Šetření
    savings: {
        basics: {
            question: ["jak šetřit", "šetření", "úspory", "jak ušetřit"],
            answer: "Základy efektivního šetření:\n\n🎯 Strategie:\n1. Stanovte si cíl (konkrétní částka)\n2. Automatizujte spoření (příkaz po výplatě)\n3. Začněte malými kroky\n4. Sledujte výdaje\n\n💰 Pravidlo: Zaplať nejdřív sobě!\nHned po výplatě odložte 10-20% na spoření.\n\n📊 Kde šetřit:\n• Spořicí účet (pro rezervu)\n• Stavební spoření (bonus od státu)\n• Investiční účet (dlouhodobě)\n• Penzijní připojištění (daňová úleva)"
        },
        tips: {
            question: ["tipy na šetření", "jak ušetřit peníze", "úsporné tipy", "kde ušetřit"],
            answer: "Praktické tipy jak ušetřit:\n\n🛒 Nákupy:\n• Dělejte si seznam a držte se ho\n• Srovnávejte ceny (Heureka, Zboží.cz)\n• Využívejte slevové kupóny\n• Nakupujte ve slevách\n\n🏠 Domácnost:\n• Šetřete energií (LED, úsporné spotřebiče)\n• Porovnejte dodavatele energií\n• Vařte doma místo jídla venku\n\n📱 Služby:\n• Zkontrolujte mobilní tarif\n• Zrušte nevyužívané předplatné\n• Využívejte cashback programy\n\n💳 Finance:\n• Účet bez poplatků\n• Refinancování úvěrů"
        },
        building_savings: {
            question: ["stavební spoření", "stavebko", "jak funguje stavební spoření"],
            answer: "Stavební spoření v ČR:\n\n✅ Výhody:\n• Státní podpora až 2 000 Kč/rok\n• Garantovaný úrok\n• Možnost výhodného úvěru\n• Pojištění vkladů\n\n📋 Podmínky státní podpory:\n• Min. vklad 20 000 Kč/rok pro max. podporu\n• Vázací doba 6 let\n• Státní podpora 10% (max. 2 000 Kč)\n\n💡 Tip: Ideální pro střednědobé spoření s nízkým rizikem.\n\n⚠️ Od 2024 se plánují změny - sledujte aktuální podmínky!"
        },
        pension: {
            question: ["penzijní připojištění", "penze", "důchod", "spoření na důchod"],
            answer: "Penzijní připojištění a spoření:\n\n📊 Typy:\n• Doplňkové penzijní spoření (DPS)\n• Transformované penzijní fondy (staré smlouvy)\n\n✅ Výhody DPS:\n• Státní příspěvek až 2 760 Kč/rok\n• Daňová úleva až 24 000 Kč/rok\n• Příspěvek zaměstnavatele (osvobozeno od daně)\n\n💰 Optimální strategie:\n• Min. 1 000 Kč/měsíc = max. státní příspěvek\n• + dalších 2 000 Kč = max. daňová úleva\n\n⚠️ Nevýhody:\n• Peníze vázány do 60 let\n• Poplatky fondů"
        },
        for_children: {
            question: ["spoření pro děti", "jak šetřit pro děti", "investice pro děti"],
            answer: "Spoření pro děti:\n\n👶 Možnosti:\n1. Dětský spořicí účet\n   • Nízký úrok, bezpečné\n\n2. Stavební spoření\n   • Státní podpora 2 000 Kč/rok\n\n3. Investiční účet\n   • ETF fondy na jméno rodiče\n   • Dlouhodobě nejvyšší výnos\n\n4. Pojištění s investiční složkou\n   • Spíše nedoporučujeme (vysoké poplatky)\n\n💡 Tip: Pro horizont 18+ let jsou ETF nejefektivnější!\n\n📊 Příklad: 1 000 Kč měsíčně 18 let s 7% výnosem = ~400 000 Kč"
        },
        50_30_20: {
            question: ["pravidlo 50 30 20", "rozdělení příjmu", "kolik šetřit"],
            answer: "Pravidlo 50/30/20 pro rozdělení příjmu:\n\n💰 50% - Potřeby (nutné výdaje)\n• Nájem/hypotéka\n• Energie a služby\n• Jídlo a základní potřeby\n• Doprava do práce\n• Pojištění\n\n🎉 30% - Přání (volitelné výdaje)\n• Zábava a volný čas\n• Restaurace a kavárny\n• Oblečení (nad rámec nutnosti)\n• Dovolená\n• Předplatná (Netflix, Spotify)\n\n📈 20% - Úspory a investice\n• Nouzový fond\n• Investice (ETF, akcie)\n• Splácení dluhů nad minimum\n• Penzijní spoření"
        }
    }
};

// Export pro použití v jiných modulech
if (typeof module !== 'undefined' && module.exports) {
    module.exports = KnowledgeBase;
}
