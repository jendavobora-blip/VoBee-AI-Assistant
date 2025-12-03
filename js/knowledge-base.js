/**
 * VoBee AI Assistant - Czech Financial Knowledge Base
 * Comprehensive Q&A database for cryptocurrencies, stocks, ETF, financial literacy, insolvency, and savings
 */

const KnowledgeBase = {
    // Greeting patterns
    greetings: {
        patterns: ['ahoj', 'dobrý den', 'nazdar', 'čau', 'zdravím', 'ahojky', 'čus', 'zdar', 'hey', 'hej', 'dobré ráno', 'dobré odpoledne', 'dobrý večer'],
        responses: [
            'Ahoj! 🐝 Jsem VoBee, váš finanční asistent. Jak vám mohu dnes pomoci?',
            'Dobrý den! 🐝 Vítejte u VoBee AI. Jsem tu, abych vám pomohl s finančními otázkami.',
            'Zdravím! 🐝 Jsem připraven zodpovědět vaše dotazy o financích, investicích a šetření.',
            'Čau! 🐝 Rád vás vidím. Co byste chtěli vědět o financích?'
        ]
    },

    // Farewell patterns
    farewells: {
        patterns: ['sbohem', 'nashle', 'pa', 'čau', 'ahoj', 'měj se', 'tak zatím', 'díky nashle', 'končím'],
        responses: [
            'Nashledanou! 👋 Přeji hodně úspěchů s vašimi financemi!',
            'Díky za návštěvu! 🐝 Kdykoliv se můžete vrátit.',
            'Měj se! 👋 Investuj moudře a šetři pravidelně!',
            'Ahoj! 🐝 Budu tu, kdybyste měli další dotazy.'
        ]
    },

    // Thanks patterns
    thanks: {
        patterns: ['díky', 'děkuji', 'dekuji', 'díkes', 'dík', 'děkuju', 'thanks', 'super', 'skvělé', 'výborně'],
        responses: [
            'Rádo se stalo! 😊 Pokud máte další otázky, ptejte se.',
            'Není zač! 🐝 Jsem tu pro vás.',
            'Potěšilo mě! 😊 Mohu vám ještě s něčím pomoci?',
            'Super! 🎉 Rád pomůžu kdykoliv.'
        ]
    },

    // Cryptocurrency knowledge
    crypto: {
        keywords: ['krypto', 'bitcoin', 'btc', 'ethereum', 'eth', 'blockchain', 'kryptoměn', 'altcoin', 'wallet', 'peněženk', 'těžb', 'mining', 'defi', 'nft', 'token'],
        topics: {
            'co jsou kryptoměny': {
                question: ['co jsou kryptoměny', 'co je krypto', 'co je kryptoměna', 'vysvětli krypto'],
                answer: `**Kryptoměny** jsou digitální nebo virtuální měny, které využívají kryptografii pro zabezpečení transakcí. 🔐

📌 **Hlavní vlastnosti:**
• Decentralizované - nejsou kontrolovány žádnou centrální autoritou
• Využívají technologii blockchain
• Transparentní a neměnné transakce
• Omezená nabídka (např. Bitcoin má max. 21 milionů mincí)

📌 **Nejznámější kryptoměny:**
• Bitcoin (BTC) - první a největší kryptoměna
• Ethereum (ETH) - platforma pro chytré kontrakty
• Solana, Cardano, Ripple a další

⚠️ **Rizika:** Vysoká volatilita, regulační nejistota, technická složitost.`
            },
            'jak funguje bitcoin': {
                question: ['jak funguje bitcoin', 'co je bitcoin', 'btc', 'bitcoin'],
                answer: `**Bitcoin (BTC)** je první a nejznámější kryptoměna, vytvořená v roce 2009 Satoshim Nakamotem. ₿

📌 **Jak funguje:**
• Transakce jsou ověřovány sítí uzlů (nodes)
• Těžaři řeší matematické problémy pro ověření bloků
• Každý blok obsahuje hash předchozího bloku (blockchain)
• Nový Bitcoin vzniká jako odměna za těžbu

📌 **Klíčové vlastnosti:**
• Max. 21 milionů BTC
• Halving každé 4 roky (snížení odměny o 50%)
• Decentralizovaný - žádná centrální banka
• Pseudonymní transakce

💡 **Tip:** Bitcoin se často označuje jako "digitální zlato" díky své omezené nabídce.`
            },
            'ethereum': {
                question: ['ethereum', 'eth', 'co je ethereum', 'smart contract', 'chytrý kontrakt'],
                answer: `**Ethereum (ETH)** je decentralizovaná platforma pro chytré kontrakty a decentralizované aplikace (dApps). 💎

📌 **Co umožňuje:**
• Vytváření chytrých kontraktů (smart contracts)
• Decentralizované aplikace (DeFi, NFT, hry)
• Tokenizace aktiv (ERC-20, ERC-721)
• Decentralizované finance (DeFi)

📌 **Ethereum 2.0:**
• Přechod z Proof of Work na Proof of Stake
• Výrazně nižší spotřeba energie
• Vyšší škálovatelnost
• Staking ETH pro odměny

💡 **Zajímavost:** Ethereum zpracuje mnohem více transakcí než Bitcoin díky své flexibilitě.`
            },
            'peněženka': {
                question: ['peněženka', 'wallet', 'krypto peněženka', 'kam uložit krypto', 'hot wallet', 'cold wallet'],
                answer: `**Kryptopeněženky** slouží k bezpečnému ukládání a správě kryptoměn. 👛

📌 **Typy peněženek:**

🔥 **Hot Wallets (Online):**
• MetaMask, Trust Wallet, Coinbase Wallet
• Výhody: Snadný přístup, vhodné pro obchodování
• Nevýhody: Méně bezpečné (připojené k internetu)

❄️ **Cold Wallets (Offline):**
• Ledger, Trezor, papírové peněženky
• Výhody: Maximální bezpečnost
• Nevýhody: Méně pohodlné pro časté transakce

📌 **Bezpečnostní tipy:**
• Nikdy nesdílejte svůj seed phrase (záložní frázi)
• Používejte dvoufaktorové ověření
• Větší částky ukládejte na cold wallet`
            },
            'jak investovat do krypta': {
                question: ['jak investovat do krypta', 'jak koupit bitcoin', 'kde koupit krypto', 'investice do kryptoměn'],
                answer: `**Jak začít investovat do kryptoměn:** 🚀

📌 **1. Vyberte burzu:**
• Coinbase, Binance, Kraken, Coinmate (CZ)
• Ověřte si regulace a poplatky

📌 **2. Vytvořte účet:**
• Registrace a ověření identity (KYC)
• Připojte platební metodu

📌 **3. Strategie investování:**
• **DCA (Dollar Cost Averaging)** - pravidelné nákupy
• **HODL** - dlouhodobé držení
• Nikdy neinvestujte více, než si můžete dovolit ztratit

📌 **4. Bezpečnost:**
• Používejte silná hesla
• Aktivujte 2FA
• Přesuňte krypto do vlastní peněženky

⚠️ **Varování:** Kryptotrh je vysoce volatilní. Investujte zodpovědně!`
            }
        }
    },

    // Stocks knowledge
    stocks: {
        keywords: ['akci', 'burz', 'dividenda', 'portfolio', 'broker', 'obchodování', 'p/e', 'index', 'dow', 'nasdaq', 's&p', 'px'],
        topics: {
            'co jsou akcie': {
                question: ['co jsou akcie', 'co je akcie', 'vysvětli akcie', 'akcie'],
                answer: `**Akcie** představují podíl vlastnictví ve společnosti. 📈

📌 **Co získáte koupí akcie:**
• Podíl na zisku společnosti (dividendy)
• Hlasovací práva na valné hromadě
• Potenciální růst hodnoty akcie

📌 **Typy akcií:**
• **Růstové akcie** - zaměřené na růst ceny (tech firmy)
• **Hodnotové akcie** - podhodnocené společnosti
• **Dividendové akcie** - pravidelné výplaty dividend

📌 **Kde obchodovat v ČR:**
• Fio e-Broker, Patria, DEGIRO, Interactive Brokers
• Pražská burza (BCPP) - index PX

💡 **Tip:** Diverzifikujte portfolio napříč sektory a regiony.`
            },
            'jak začít s akciemi': {
                question: ['jak začít s akciemi', 'jak investovat do akcií', 'jak koupit akcie', 'začátečník akcie'],
                answer: `**Jak začít investovat do akcií:** 🎯

📌 **1. Vzdělání:**
• Naučte se základy (P/E, dividendy, tržní kapitalizace)
• Sledujte finanční zprávy a analýzy

📌 **2. Vyberte brokera:**
• Porovnejte poplatky a nabídku
• Oblíbení v ČR: Fio, Patria, DEGIRO, XTB

📌 **3. Otevřete účet:**
• Online registrace
• Vklad prostředků

📌 **4. Strategie:**
• **Buy and Hold** - dlouhodobé držení
• **DCA** - pravidelné investice
• Začněte s menšími částkami

📌 **5. Diverzifikace:**
• Různé sektory a regiony
• Zvažte ETF pro začátek

⚠️ **Důležité:** Investování nese riziko. Minulé výnosy nezaručují budoucí.`
            },
            'dividendy': {
                question: ['dividenda', 'dividendy', 'co je dividenda', 'dividendové akcie'],
                answer: `**Dividendy** jsou podíl na zisku společnosti vyplácený akcionářům. 💵

📌 **Jak fungují:**
• Společnost rozhodne o výplatě na valné hromadě
• Výplata obvykle čtvrtletně nebo ročně
• Rozhodný den (ex-dividend date) určuje nárok

📌 **Klíčové pojmy:**
• **Dividendový výnos** = dividenda / cena akcie × 100
• **Payout ratio** = % zisku vyplaceného jako dividenda
• **Dividendový aristokrat** = 25+ let rostoucích dividend

📌 **Příklady dividendových akcií:**
• ČEZ, Komerční banka (ČR)
• Coca-Cola, Johnson & Johnson (USA)

💡 **Tip:** Reinvestice dividend může významně zvýšit dlouhodobý výnos (složené úročení).`
            },
            'p/e ratio': {
                question: ['p/e', 'p/e ratio', 'poměr cena zisk', 'valuace akcie'],
                answer: `**P/E Ratio (Price-to-Earnings)** je základní ukazatel ocenění akcie. 📊

📌 **Výpočet:**
P/E = Cena akcie / Zisk na akcii (EPS)

📌 **Interpretace:**
• **Nízké P/E (< 15):** Může být podhodnocená nebo v problémech
• **Střední P/E (15-25):** Férově oceněná
• **Vysoké P/E (> 25):** Očekáván růst nebo nadhodnocená

📌 **Varianty:**
• **Trailing P/E** - historický zisk
• **Forward P/E** - očekávaný zisk
• **PEG ratio** = P/E / růst zisku

⚠️ **Pozor:** P/E se liší podle sektoru. Porovnávejte s konkurencí!`
            }
        }
    },

    // ETF knowledge
    etf: {
        keywords: ['etf', 'fond', 'index', 'vanguard', 'ishares', 'spdr', 'ter', 'nákladovost'],
        topics: {
            'co je etf': {
                question: ['co je etf', 'etf', 'exchange traded fund', 'burzovně obchodovaný fond'],
                answer: `**ETF (Exchange Traded Fund)** je burzovně obchodovaný fond, který sleduje určitý index nebo koš aktiv. 📊

📌 **Výhody ETF:**
• Diverzifikace - jedním nákupem získáte desítky/stovky akcií
• Nízké náklady (TER obvykle 0,03% - 0,5%)
• Likvidita - obchodovatelné jako akcie
• Transparentnost - víte, co fond drží

📌 **Typy ETF:**
• **Akciové** - S&P 500, MSCI World
• **Dluhopisové** - státní, korporátní
• **Komoditní** - zlato, ropa
• **Sektorové** - technologie, zdravotnictví

📌 **Populární ETF:**
• Vanguard S&P 500 (VOO)
• iShares MSCI World (IWDA)
• Vanguard FTSE All-World (VWCE)

💡 **Tip:** ETF jsou ideální pro pasivní investory a začátečníky.`
            },
            'jak vybrat etf': {
                question: ['jak vybrat etf', 'nejlepší etf', 'které etf', 'výběr etf'],
                answer: `**Jak vybrat správné ETF:** 🎯

📌 **1. Určete strategii:**
• Geografický rozsah (svět, USA, Evropa, emerging markets)
• Sektor (celý trh vs. specifický sektor)
• Akumulační vs. distribuční

📌 **2. Klíčové metriky:**
• **TER (Total Expense Ratio)** - nižší je lepší
• **Tracking difference** - jak přesně sleduje index
• **Velikost fondu** - větší = bezpečnější
• **Likvidita** - objem obchodování

📌 **3. Domicil:**
• Irsko = výhodné pro české investory (daňové smlouvy)
• Hledejte UCITS ETF

📌 **Oblíbené volby:**
• **VWCE/IWDA** - celosvětová diverzifikace
• **VUAA** - pouze USA (S&P 500)
• **EUNL** - MSCI World`
            },
            'ter nákladovost': {
                question: ['ter', 'nákladovost', 'poplatky etf', 'total expense ratio'],
                answer: `**TER (Total Expense Ratio)** je celková roční nákladovost ETF. 💰

📌 **Co zahrnuje:**
• Manažerské poplatky
• Administrativní náklady
• Právní a auditorské služby
• Marketing

📌 **Typické hodnoty:**
• **Indexové ETF:** 0,03% - 0,25%
• **Aktivní ETF:** 0,5% - 1%
• **Specializované:** 0,3% - 0,7%

📌 **Proč záleží:**
Příklad s 10 000 Kč ročně po 30 let:
• TER 0,07%: ~785 000 Kč
• TER 0,50%: ~745 000 Kč
• Rozdíl: 40 000 Kč!

💡 **Tip:** U pasivních ETF vždy preferujte nižší TER. Malé rozdíly se sčítají!`
            }
        }
    },

    // Financial literacy
    literacy: {
        keywords: ['gramotnost', 'rozpočet', 'budget', 'dluh', 'úvěr', 'půjčk', 'hypotéka', 'úrok', 'inflac', 'spoř', 'finance'],
        topics: {
            'finanční gramotnost': {
                question: ['finanční gramotnost', 'co je finanční gramotnost', 'základy financí'],
                answer: `**Finanční gramotnost** je schopnost rozumět a efektivně spravovat osobní finance. 📚

📌 **Klíčové oblasti:**

1️⃣ **Rozpočtování:**
• Pravidlo 50/30/20 (potřeby/chtíče/spoření)
• Sledování příjmů a výdajů

2️⃣ **Spoření a investice:**
• Nouzový fond (3-6 měsíců výdajů)
• Dlouhodobé investice pro cíle

3️⃣ **Řízení dluhů:**
• Rozlišujte dobrý a špatný dluh
• Priorita: splacení drahých dluhů

4️⃣ **Ochrana:**
• Pojištění (zdravotní, životní, majetku)
• Diverzifikace rizik

💡 **Zlaté pravidlo:** Plaťte nejdřív sami sobě - automatizujte spoření!`
            },
            'rozpočet': {
                question: ['rozpočet', 'jak sestavit rozpočet', 'budget', 'osobní rozpočet', '50/30/20'],
                answer: `**Jak sestavit osobní rozpočet:** 📝

📌 **Pravidlo 50/30/20:**
• **50% na potřeby:** bydlení, jídlo, doprava, pojištění
• **30% na přání:** zábava, restaurace, koníčky
• **20% na spoření:** nouzový fond, investice, splátky dluhů

📌 **Kroky k rozpočtu:**

1️⃣ Spočítejte čistý příjem
2️⃣ Zmapujte všechny výdaje (min. 1 měsíc)
3️⃣ Kategorizujte výdaje
4️⃣ Stanovte limity pro kategorie
5️⃣ Sledujte a upravujte

📌 **Užitečné aplikace:**
• Wallet, Spendee, YNAB
• Excel/Google Sheets

💡 **Tip:** Začněte sledovat výdaje ještě dnes. Překvapí vás, kam peníze mizí!`
            },
            'inflace': {
                question: ['inflace', 'co je inflace', 'jak se chránit před inflací'],
                answer: `**Inflace** je růst cenové hladiny, který snižuje kupní sílu peněz. 📈

📌 **Jak funguje:**
• Měřeno indexem spotřebitelských cen (CPI)
• Cílová inflace ČNB: 2%
• Vysoká inflace = peníze ztrácejí hodnotu

📌 **Příčiny:**
• Růst peněžní zásoby
• Růst nákladů (energie, mzdy)
• Vysoká poptávka

📌 **Jak se chránit:**
• **Investice:** akcie, nemovitosti, komodity
• **Dluhopisy:** protiinflační dluhopisy
• **Diverzifikace:** mix aktiv
• **Vyjednávání:** růst platu

⚠️ **Pozor:** Peníze na běžném účtu při inflaci ztrácejí hodnotu!`
            },
            'nouzový fond': {
                question: ['nouzový fond', 'rezerva', 'kolik mít v rezervě', 'emergency fund'],
                answer: `**Nouzový fond** je finanční polštář pro neočekávané výdaje. 🛡️

📌 **Kolik mít:**
• Minimum: 3 měsíce výdajů
• Ideál: 6 měsíců výdajů
• Podnikatelé/OSVČ: 9-12 měsíců

📌 **Na co slouží:**
• Ztráta zaměstnání
• Zdravotní výdaje
• Opravy auta/domu
• Neočekávané situace

📌 **Kde držet:**
• Spořicí účet s okamžitým přístupem
• Nízké riziko, rychlá dostupnost
• Nepočítejte s ním jako s investicí

📌 **Jak vybudovat:**
1. Stanovte cílovou částku
2. Automatizujte měsíční převody
3. Nejdřív splaťte drahé dluhy

💡 **Tip:** Nouzový fond = klid v hlavě. Je základ každého finančního plánu!`
            }
        }
    },

    // Insolvency knowledge
    insolvency: {
        keywords: ['insolvenc', 'bankrot', 'oddluže', 'exekuc', 'dlužník', 'věřitel', 'konkurz', 'úpadek'],
        topics: {
            'co je insolvence': {
                question: ['co je insolvence', 'insolvence', 'úpadek', 'platební neschopnost'],
                answer: `**Insolvence (úpadek)** je situace, kdy dlužník není schopen plnit své závazky. ⚖️

📌 **Znaky úpadku:**
• Více věřitelů (min. 2)
• Závazky po splatnosti více než 30 dnů
• Neschopnost plnit závazky

📌 **Formy úpadku:**
• **Platební neschopnost** - nedostatek prostředků
• **Předlužení** - dluhy převyšují majetek (pouze u podnikatelů)
• **Hrozící úpadek** - očekávaná neschopnost platit

📌 **Řešení úpadku:**
• **Konkurz** - zpeněžení majetku
• **Reorganizace** - pro podniky
• **Oddlužení** - pro fyzické osoby

💡 **Tip:** Prevence je klíčová. Řešte dluhy včas, než se situace zhorší!`
            },
            'oddlužení': {
                question: ['oddlužení', 'osobní bankrot', 'jak na oddlužení', 'podmínky oddlužení'],
                answer: `**Oddlužení (osobní bankrot)** umožňuje zbavit se dluhů a začít znovu. 🆕

📌 **Podmínky pro oddlužení:**
• Poctivý záměr
• Schopnost splácet min. část dluhů
• Bez předchozího oddlužení v posledních 10 letech

📌 **Průběh:**
1. Podání návrhu k insolvenčnímu soudu
2. Rozhodnutí o úpadku
3. Schválení oddlužení
4. Splátkový kalendář (3-5 let)
5. Osvobození od zbytku dluhů

📌 **Co je chráněno:**
• Nezabavitelné minimum
• Základní vybavení domácnosti
• Pracovní pomůcky

📌 **Kolik splatit:**
• Min. tolik, kolik je možné za dobu oddlužení

⚠️ **Důležité:** Konzultujte s právníkem nebo dluhovou poradnou!`
            },
            'exekuce': {
                question: ['exekuce', 'exekutor', 'jak zastavit exekuci', 'co může exekutor zabavit'],
                answer: `**Exekuce** je nucený výkon rozhodnutí k vymožení pohledávky. ⚠️

📌 **Co může exekutor zabavit:**
• Bankovní účty (nad nezabavitelné minimum)
• Mzdu (třetinový systém)
• Movitý majetek
• Nemovitosti

📌 **Co NELZE zabavit:**
• Nezabavitelné minimum
• Základní vybavení domácnosti
• Zdravotní pomůcky
• Nástroje potřebné k práci (do hodnoty)

📌 **Jak se bránit:**
• Jednejte aktivně s věřiteli
• Sledujte insolvenční rejstřík
• Zvažte oddlužení
• Konzultujte s poradnou

📌 **Nezabavitelné minimum 2024:**
• Základní částka: ~13 638 Kč
• Na vyživovanou osobu: ~3 410 Kč

💡 **Tip:** Dluhové poradny nabízejí bezplatnou pomoc!`
            }
        }
    },

    // Savings knowledge
    savings: {
        keywords: ['šetř', 'spoř', 'uspoř', 'stavební spoř', 'penzijn', 'dluhopis', 'termínovan', 'úrok'],
        topics: {
            'jak šetřit': {
                question: ['jak šetřit', 'jak ušetřit', 'tipy na šetření', 'jak šetřit peníze'],
                answer: `**Praktické tipy jak šetřit peníze:** 💰

📌 **Automatizace:**
• Nastavte trvalý příkaz na spoření hned po výplatě
• "Platba sobě" jako první výdaj

📌 **Každodenní úspory:**
• Nakupujte s jídelníčkem a seznamem
• Porovnávejte ceny (Heureka, Idealo)
• Využívejte cashback a slevové programy
• Omezte impulzivní nákupy (pravidlo 24 hodin)

📌 **Větší úspory:**
• Refinancujte úvěry při nižších sazbách
• Změňte dodavatele energií
• Přehodnoťte předplatná a pojištění

📌 **Pravidlo 50/30/20:**
• 50% potřeby, 30% přání, 20% spoření

📌 **Motivace:**
• Stanovte konkrétní cíle
• Sledujte pokrok
• Oslavujte milníky

💡 **Tip:** I malé úspory se sčítají. 100 Kč denně = 36 500 Kč ročně!`
            },
            'kam uložit peníze': {
                question: ['kam uložit peníze', 'kde spořit', 'spořicí účet', 'termínovaný vklad'],
                answer: `**Kam uložit peníze podle účelu:** 🏦

📌 **Krátkodobě (do 1 roku):**
• **Spořicí účet** - likvidita, nižší úrok
• **Termínovaný vklad** - vyšší úrok, vázanost
• Pro: nouzový fond, plánované výdaje

📌 **Střednědobě (1-5 let):**
• **Stavební spoření** - státní podpora, stabilita
• **Dluhopisy** - státní (protiinflační), korporátní
• Pro: konkrétní cíle (auto, dovolená)

📌 **Dlouhodobě (5+ let):**
• **ETF/akcie** - vyšší potenciál výnosu
• **Penzijní spoření** - daňové výhody
• **Nemovitosti** - diverzifikace
• Pro: důchod, finanční nezávislost

📌 **Porovnání (orientačně):**
• Spořicí účet: 3-5% p.a.
• Stavební spoření: 2-3% + státní podpora
• Akcie/ETF: průměrně 7-10% p.a. (dlouhodobě)

💡 **Tip:** Kombinujte produkty podle svých cílů a horizontu!`
            },
            'stavební spoření': {
                question: ['stavební spoření', 'jak funguje stavební spoření', 'státní podpora'],
                answer: `**Stavební spoření** je oblíbený český produkt pro spoření a bydlení. 🏠

📌 **Hlavní výhody:**
• **Státní podpora:** 10% z vkladů, max. 2 000 Kč/rok
• Vkládat můžete max. 20 000 Kč/rok pro podporu
• Garantovaný úrok
• Možnost výhodného úvěru

📌 **Podmínky:**
• Vázací doba: 6 let pro státní podporu
• Min. věk: bez omezení
• Smlouva na 6 let

📌 **Využití:**
• Spoření na bydlení
• Úvěr ze stavebního spoření (nízký úrok)
• Překlenovací úvěr
• I bez účelu po vázací době

📌 **Stavební spořitelny v ČR:**
• Českomoravská stavební spořitelna
• Modrá pyramida
• Raiffeisen stavební spořitelna
• Stavební spořitelna České spořitelny

💡 **Tip:** Maximalizujte státní podporu vkladem 20 000 Kč ročně!`
            },
            'penzijní spoření': {
                question: ['penzijní spoření', 'penzijko', 'doplňkové penzijní spoření', 'iii pilíř'],
                answer: `**Penzijní spoření (III. pilíř)** je důležitá součást přípravy na důchod. 👴

📌 **Státní příspěvky:**
| Váš vklad | Státní příspěvek |
|-----------|------------------|
| 300 Kč    | 90 Kč           |
| 500 Kč    | 130 Kč          |
| 700 Kč    | 170 Kč          |
| 1000 Kč   | 230 Kč (max.)   |

📌 **Daňové výhody:**
• Odpočet od základu daně až 24 000 Kč/rok
• Úspora na dani až 3 600 Kč
• Pro příspěvky nad 1 000 Kč/měsíc

📌 **Příspěvek zaměstnavatele:**
• Často do 3% hrubé mzdy
• Daňově zvýhodněn

📌 **Strategie fondů:**
• Konzervativní, vyvážená, dynamická
• Mladší = více dynamická

⚠️ **Podmínky výplaty:**
• Důchodový věk nebo invalidita
• Předčasný výběr = ztráta podpory

💡 **Tip:** Využijte plně státní příspěvek i daňový odpočet!`
            }
        }
    },

    // Default responses
    defaults: [
        'Omlouvám se, této otázce úplně nerozumím. 🤔 Můžete se zeptat jinak? Rád pomohu s tématy jako kryptoměny, akcie, ETF, finanční gramotnost, insolvence nebo šetření.',
        'Toto téma nemám v databázi. 📚 Zkuste se zeptat na něco z oblasti financí - investice, spoření, nebo finanční plánování.',
        'Na tuto otázku bohužel neznám odpověď. 🐝 Zkuste formulovat dotaz jinak, nebo se zeptejte na jiné finanční téma.',
        'Hmm, tady si nejsem jistý. 🤷 Mohu vám pomoci s kryptoměnami, akciemi, ETF, rozpočtováním, oddlužením nebo spořením.'
    ]
};

// Export for use in chatbot.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = KnowledgeBase;
}
