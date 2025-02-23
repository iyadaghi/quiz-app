In de file databank.py worden vier tabellen aangemaakt en beheerd. Hieronder een korte uitleg van elke tabel:

personen_info
Deze tabel slaat de persoonlijke gegevens van gebruikers op, zoals hun naam en een score. Hiermee kun je bijhouden wie er de quiz heeft gespeeld.

quizvragen
In deze tabel staan alle quizvragen die in de applicatie worden gebruikt. 

quiz_statistieken
Deze tabel houdt per gebruiker en per vraag bij hoeveel keer een vraag juist of fout beantwoord is. Dit maakt het mogelijk om gedetailleerde statistieken te genereren over individuele prestaties.

antwoord_statistieken
(Optioneel, indien aanwezig) Deze tabel aggregeert de gegevens uit de quiz_statistieken. Hierin wordt per vraag een totaaloverzicht bijgehouden, zoals het totale aantal keren dat een vraag fout (of juist) beantwoord is over alle gebruikers heen.

source_code.py
Deze file vormt de kern van de applicatie. In source_code.py worden de verschillende componenten met elkaar verbonden:

Databaseverbinding: De file importeert de databasefunctionaliteit uit databank.py en maakt een verbinding met de database waarin de tabellen (personen_info, quizvragen, quiz_statistieken, etc.) zijn aangemaakt.
Interface-integratie: De interface (bijvoorbeeld gedefinieerd in interface.py) wordt geïmporteerd, zodat de applicatie de vragen kan tonen en gebruikersinput kan verwerken.
Gebruikersinput en vraaggeneratie: Aan de hand van de input van de gebruiker worden de quizvragen uit de databank geladen, de logica toegepasen de gegenereerde vragen in de interface getoond.

stacked_interface.py
Deze file bevat de interface code en wordt geïmporteerd via klasses in de source_code file.
