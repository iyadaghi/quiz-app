import sqlite3

# Verbinden met de database
conn = sqlite3.connect('quiz_vragen.db')
cursor = conn.cursor()

cursor.execute(''' 

CREATE TABLE IF NOT EXISTS personen_info (
    gebruiker_id INTEGER PRIMARY KEY,
    naam VARCHAR(255) NOT NULL,
    score DECIMAL(2)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz_vragen (
    vraag_id INTEGER PRIMARY KEY,
    vraag varchar(255) NOT NULL,
    antwoord varchar(255) NOT NULL,
    opties JSON,
    onderwerp VARCHAR(25),
    moeilijkheid VARCHAR(25)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz_statistieken (
    id INTEGER PRIMARY KEY,
    gebruiker_id INTEGER,
    vraag_id INTEGER,
    aantal_keren_juist INTEGER DEFAULT 0,
    aantal_keren_fout INTEGER DEFAULT 0,
    FOREIGN KEY (gebruiker_id) REFERENCES personen_info(gebruiker_id),
    FOREIGN KEY (vraag_id) REFERENCES quiz_vragen(vraag_id),
    UNIQUE (gebruiker_id, vraag_id)

);
''')


conn.commit()




# Invoegen van de gegevens
cursor.executemany('''
INSERT INTO quiz_vragen (vraag, antwoord, opties, onderwerp, moeilijkheid)
VALUES (?, ?, ?, ?, ?)
''',
(
    ("In welk jaar werd de Verenigde Naties opgericht?", "1945", '["1945", "1939", "1950"]', "geschiedenis", "beginner"),
    ("Wie was de eerste president van de Verenigde Staten?", "George Washington", '["George Washington", "Abraham Lincoln", "Thomas Jefferson"]', "geschiedenis", "beginner"),
    ("Welke gebeurtenis leidde tot de Eerste Wereldoorlog?", "De moord op Franz Ferdinand", '["De moord op Franz Ferdinand", "De ondergang van de Titanic", "De aanval op Pearl Harbor"]', "geschiedenis", "beginner"),
    ("Wat was de oorzaak van de Franse Revolutie?", "Sociale en economische ongelijkheid", '["Sociale en economische ongelijkheid", "De wens voor macht", "De invasie van Engeland"]', "geschiedenis", "beginner"),
    ("In welk jaar werd Nederland onafhankelijk van Spanje?", "1648", '["1648", "1581", "1700"]', "geschiedenis", "beginner"),
    ("Wie was de belangrijkste figuur in de Amerikaanse burgeroorlog?", "Abraham Lincoln", '["Abraham Lincoln", "Ulysses S. Grant", "Robert E. Lee"]', "geschiedenis", "beginner"),
    ("Welke stad werd getroffen door de eerste atoombom?", "Hiroshima", '["Hiroshima", "Nagasaki", "Tokyo"]', "geschiedenis", "beginner"),
    ("Wat was de belangrijkste oorzaak van de val van het Romeinse Rijk?", "Barbaarse invasies", '["Barbaarse invasies", "Corruptie van de heersers", "Interne burgeroorlogen"]', "geschiedenis", "beginner"),
    ("Wie ontdekte Amerika in 1492?", "Christopher Columbus", '["Christopher Columbus", "Marco Polo", "Amerigo Vespucci"]', "geschiedenis", "beginner"),
    ("In welk jaar werd de Berlijnse Muur neergehaald?", "1989", '["1989", "1961", "1975"]', "geschiedenis", "beginner"),
    ("In welk jaar eindigde de Tweede Wereldoorlog?", "1945", '["1945", "1944", "1939"]', "geschiedenis", "medium"),
    ("Wat was het doel van de Russische Revolutie van 1917?", "De afzetting van de tsaar en de opkomst van het communisme", '["De afzetting van de tsaar en de opkomst van het communisme", "De vestiging van een monarchie", "De opkomst van de nazis"]', "geschiedenis", "medium"),
    ("Wie was de koning van Frankrijk tijdens de Franse Revolutie?", "Lodewijk XVI", '["Lodewijk XVI", "Lodewijk XIV", "Karel X"]', "geschiedenis", "medium"),
    ("Welke stad werd in 79 na Christus verwoest door een vulkaanuitbarsting?", "Pompeii", '["Pompeii", "Rome", "Athene"]', "geschiedenis", "medium"),
    ("Wat was het belangrijkste middel van communicatie in de oude Griekse stadstaten?", "Het orakel", '["Het orakel", "Brieven", "De mondelinge overlevering"]', "geschiedenis", "medium"),
    ("Welke beroemde leider werd in 323 v.Chr. in Babylon begraven?", "Alexander de Grote", '["Alexander de Grote", "Julius Caesar", "Nero"]', "geschiedenis", "medium"),
    ("Wie was de leider van de Franse Revolutie?", "Maximilien Robespierre", '["Maximilien Robespierre", "Napoleon Bonaparte", "Georges Danton"]', "geschiedenis", "medium"),
    ("Welke veldslag leidde tot de ondergang van het Franse koninkrijk in 1815?", "Slag bij Waterloo", '["Slag bij Waterloo", "Slag bij Austerlitz", "Slag bij Leipzig"]', "geschiedenis", "medium"),
    ("Wie was de leider van de Mongoolse invasie van Europa?", "Dzjengis Khan", '["Dzjengis Khan", "Kublai Khan", "Tamerlane"]', "geschiedenis", "medium"),
    ("Wat was de belangrijkste oorzaak van de Amerikaanse Burgeroorlog?", "Slavernij", '["Slavernij", "Economische problemen", "De strijd om de onafhankelijkheid"]', "geschiedenis", "medium"),
    ("Wie was de laatste keizer van China?", "Pu Yi", '["Pu Yi", "Qin Shi Huang", "Kangxi"]', "geschiedenis", "gevorderd"),
    ("Wie was de leider van de Sovjetunie tijdens de Tweede Wereldoorlog?", "Joseph Stalin", '["Joseph Stalin", "Leon Trotsky", "Vladimir Lenin"]', "geschiedenis", "gevorderd"),
    ("In welk jaar werd de Titanic gezonken?", "1912", '["1912", "1905", "1915"]', "geschiedenis", "gevorderd"),
    ("Welke strijd leidde tot de val van het Franse Imperium in 1815?", "De Slag bij Waterloo", '["De Slag bij Waterloo", "De Slag bij Leipzig", "De Slag bij Austerlitz"]', "geschiedenis", "gevorderd"),
    ("Wat was de belangrijkste oorzaak van de val van het Byzantijnse Rijk?", "Ottomaanse verovering", '["Ottomaanse verovering", "Interne conflicten", "De kruistochten"]', "geschiedenis", "gevorderd"),
    ("Wie was de eerste Romeinse keizer?", "Augustus", '["Augustus", "Nero", "Julius Caesar"]', "geschiedenis", "gevorderd"),
    ("Wat was de belangrijkste oorzaak van de Engelse Burgeroorlog?", "Strijd om politieke macht", '["Strijd om politieke macht", "Religieuze onenigheid", "Grondbezit"]', "geschiedenis", "gevorderd"),
    ("In welk jaar werd de Berlin Muur gebouwd?", "1961", '["1961", "1958", "1970"]', "geschiedenis", "gevorderd"),
    ("Wat was het belangrijkste resultaat van de Vrede van Versailles?", "Einde van de Eerste Wereldoorlog", '["Einde van de Eerste Wereldoorlog", "Einde van het Ottomaanse Rijk", "Het herstel van Frankrijk"]', "geschiedenis", "gevorderd"),
    ("Wat was de belangrijkste oorzaak van de Amerikaanse Burgeroorlog?", "Slavernij", '["Slavernij", "Economische problemen", "De strijd om de onafhankelijkheid"]', "geschiedenis", "gevorderd"),
    ("Wie is de grondlegger van het existentialisme?", "Søren Kierkegaard", '["Søren Kierkegaard", "Jean-Paul Sartre", "Friedrich Nietzsche"]', "filosofie", "beginner"),
    ("Wat betekent 'cogito ergo sum'?", "Ik denk dus ik ben", '["Ik denk dus ik ben", "Ik ben, dus ik leef", "De waarheid ligt in de rede"]', "filosofie", "beginner"),
    ("Wie ontwikkelde het concept van de 'overmens'?", "Friedrich Nietzsche", '["Friedrich Nietzsche", "Jean-Paul Sartre", "Martin Heidegger"]', "filosofie", "beginner"),
    ("Wat is het belangrijkste idee in de ethiek van Immanuel Kant?", "Het categorisch imperatief", '["Het categorisch imperatief", "Het principe van utilitarisme", "Het idee van de deugd"]', "filosofie", "beginner"),
    ("Wie ontwikkelde het sociaal contract?", "Jean-Jacques Rousseau", '["Jean-Jacques Rousseau", "John Locke", "Karl Marx"]', "filosofie", "beginner"),
    ("Wat is de theorie van 'tabula rasa'?", "Het idee dat mensen als een onbeschreven blad worden geboren", '["Het idee dat mensen als een onbeschreven blad worden geboren", "De menselijke geest is voorgeprogrammeerd", "Mensen worden geboren met instincten"]', "filosofie", "beginner"),
    ("Wat betekent empirisme?", "Kennis komt uit zintuiglijke ervaring", '["Kennis komt uit zintuiglijke ervaring", "Kennis komt uit logica", "Kennis is aangeboren"]', "filosofie", "beginner"),
    ("Wie was de grondlegger van de pragmatisme?", "Charles Peirce", '["Charles Peirce", "John Dewey", "William James"]', "filosofie", "beginner"),
    ("Wat is het verschil tussen empirisme en rationalisme?", "Empirisme komt uit ervaring, rationalisme uit rede", '["Empirisme komt uit ervaring, rationalisme uit rede", "Empirisme is gebaseerd op logica", "Rationalisme is de basis van alle kennis"]', "filosofie", "beginner"),
    ("Wat is het idee van de 'wil tot macht'?", "De fundamentele drijfveer van de mens is de wil om te heersen", '["De fundamentele drijfveer van de mens is de wil om te heersen", "Het streven naar geluk", "De zoektocht naar kennis"]', "filosofie", "beginner"),
    ("Wat houdt het idee van het 'categorisch imperatief' in?", "Acties moeten universeel toepasbaar zijn", '["Acties moeten universeel toepasbaar zijn", "Het is moreel goed als het geluk oplevert", "Het is moreel goed als het leidt tot vooruitgang"]', "filosofie", "medium"),
    ("Wie zei 'De staat is de vijand van de vrijheid'?", "Karl Marx", '["Karl Marx", "Friedrich Nietzsche", "Jean-Paul Sartre"]', "filosofie", "medium"),
    ("Wat was de belangrijkste stelling in de theorie van Plato?", "De fysieke wereld is slechts een imperfecte afspiegeling van de ideale vormen", '["De fysieke wereld is slechts een imperfecte afspiegeling van de ideale vormen", "De werkelijkheid is gebaseerd op zintuiglijke ervaring", "Mensen zijn van nature goed"]', "filosofie", "medium"),
    ("Wat is het belangrijkste principe in het utilitarisme?", "Het grootste geluk voor het grootste aantal", '["Het grootste geluk voor het grootste aantal", "Het naleven van de deugd", "De rechten van de mens"]', "filosofie", "medium"),
    ("Wat was het belangrijkste doel van Aristoteles' ethiek?", "Het bereiken van de deugd en het goede leven", '["Het bereiken van de deugd en het goede leven", "Het verkrijgen van rijkdom", "Het verzamelen van kennis"]', "filosofie", "medium"),
    ("Welke filosoof ontwikkelde de theorie van het 'maatschappelijk contract'?", "John Locke", '["John Locke", "Jean-Jacques Rousseau", "Thomas Hobbes"]', "filosofie", "medium"),
    ("Wat stelde Karl Marx over de economie?", "De economie bepaalt de samenleving", '["De economie bepaalt de samenleving", "Politieke vrijheid leidt tot economische vooruitgang", "De staat moet alle bezittingen beheersen"]', "filosofie", "medium"),
    ("Wie was de grondlegger van de fenomenologie?", "Edmund Husserl", '["Edmund Husserl", "Martin Heidegger", "Jean-Paul Sartre"]', "filosofie", "medium"),
    ("Wat is het doel van epistemologie?", "Het begrijpen van de aard en bronnen van kennis", '["Het begrijpen van de aard en bronnen van kennis", "Het onderzoeken van de menselijke geest", "Het begrijpen van de werkelijkheid"]', "filosofie", "medium"),
    ("Wat bedoelt Kant met het 'noumenale'?", "De werkelijkheid zoals die is, onafhankelijk van onze ervaring", '["De werkelijkheid zoals die is, onafhankelijk van onze ervaring", "De zintuiglijke wereld zoals wij die ervaren", "Het idee van de objectieve waarheid"]', "filosofie", "medium"),
    ("Wat bedoelt Heidegger met 'Dasein'?", "Het begrip dat menselijk bestaan altijd verbonden is met de wereld", '["Het begrip dat menselijk bestaan altijd verbonden is met de wereld", "Het idee van de eeuwige waarheid", "De zoektocht naar kennis"]', "filosofie", "gevorderd"),
    ("Wat is het idee van het 'übermensch'?", "De idealistische mens die zijn eigen waarden creëert", '["De idealistische mens die zijn eigen waarden creëert", "De mens die boven anderen staat", "De mens die zijn lot accepteert"]', "filosofie", "gevorderd"),
    ("Wat is de 'wil tot macht' in Nietzsche's filosofie?", "De fundamentele drijfveer van mensen is de wil om te heersen", '["De fundamentele drijfveer van mensen is de wil om te heersen", "De zoektocht naar het hogere zelf", "De wil om te overleven"]', "filosofie", "gevorderd"),
    ("Wat is de 'ontologische' filosofie?", "De studie van het wezen van het bestaan", '["De studie van het wezen van het bestaan", "De studie van de menselijke geest", "De studie van kennis"]', "filosofie", "gevorderd"),
    ("Wat was het belangrijkste idee in het werk van Michel Foucault?", "De invloed van macht en kennis op de samenleving", '["De invloed van macht en kennis op de samenleving", "Het idee van objectieve waarheid", "De zoektocht naar de menselijke vrijheid"]', "filosofie", "gevorderd"),
    ("Wie ontwikkelde het idee van de 'willen tot macht'?", "Friedrich Nietzsche", '["Friedrich Nietzsche", "Karl Marx", "Jean-Paul Sartre"]', "filosofie", "gevorderd"),
    ("Wat is de 'fenomenologie' volgens Edmund Husserl?", "De studie van de structuur van ervaring", '["De studie van de structuur van ervaring", "Het zoeken naar objectieve waarheid", "De studie van de menselijke geest"]', "filosofie", "gevorderd"),
    ("Wat was het idee van de 'narratieve identiteit' volgens Paul Ricoeur?", "Identiteit ontstaat uit verhalen die we vertellen over onszelf", '["Identiteit ontstaat uit verhalen die we vertellen over onszelf", "Identiteit is gebaseerd op de genezen ziel", "Identiteit is een constante staat van verandering"]', "filosofie", "gevorderd"),
    ("Wie won de FIFA Wereldbeker in 2014?", "Duitsland", '["Duitsland", "Brazilië", "Argentinië"]', "sport", "medium"),
    ("Wie heeft de meeste Formule 1 Wereldkampioenschappen gewonnen?", "Michael Schumacher", '["Michael Schumacher", "Lewis Hamilton", "Juan Manuel Fangio"]', "sport", "gevorderd"),
    ("Wie won de eerste FIFA Wereldbeker in 1930?", "Uruguay", '["Uruguay", "Brazilië", "Duitsland"]', "sport", "beginner"),
    ("Wie is de bekendste voetballer uit Brazilië?", "Pelé", '["Pelé", "Zico", "Neymar"]', "sport", "beginner"),
    ("Hoeveel spelers staan er op het veld in een voetbalteam?", "11", '["11", "9", "13"]', "sport", "beginner"),
    ("In welke stad werden de Olympische Spelen van 2008 gehouden?", "Peking", '["Peking", "Londen", "Rio de Janeiro"]', "sport", "beginner"),
    ("Wat is de maximale score in een perfect potje bowlen?", "300", '["300", "250", "200"]', "sport", "beginner"),
    ("Wie won de Tour de France in 2010?", "Alberto Contador", '["Alberto Contador", "Lance Armstrong", "Chris Froome"]', "sport", "beginner"),
    ("Wie is de snelste man ter wereld?", "Usain Bolt", '["Usain Bolt", "Carl Lewis", "Michael Johnson"]', "sport", "beginner"),
    ("Wat is de lengtemaat voor een marathonschaatswedstrijd?", "42,195 km", '["42,195 km", "50 km", "30 km"]', "sport", "beginner"),
    ("Welke sport wordt gespeeld op Wimbledon?", "Tennis", '["Tennis", "Golf", "Voetbal"]', "sport", "beginner"),
    ("In welke sport wordt de Stanley Cup uitgereikt?", "Ijshockey", '["Ijshockey", "Basketbal", "American Football"]', "sport", "beginner"),
    ("Wie heeft de meeste Grand Slam-titels in het tennis?", "Roger Federer", '["Roger Federer", "Rafael Nadal", "Novak Djokovic"]', "sport", "medium"),
    ("Welke Formule 1-coureur heeft het meeste aantal wereldtitels?", "Michael Schumacher", '["Michael Schumacher", "Lewis Hamilton", "Juan Manuel Fangio"]', "sport", "medium"),
    ("Wie won de gouden medaille voor de 100 meter op de Olympische Spelen van 2008?", "Usain Bolt", '["Usain Bolt", "Tyson Gay", "Asafa Powell"]', "sport", "medium"),
    ("Welke sporter heeft de meeste Olympische medailles aller tijden?", "Michael Phelps", '["Michael Phelps", "Larisa Latynina", "Carl Lewis"]', "sport", "medium"),
    ("Wie won de Champions League in 2019?", "Liverpool", '["Liverpool", "Barcelona", "Real Madrid"]', "sport", "medium"),
    ("Welke Nederlandse schaatser heeft de meeste wereldtitels?", "Sven Kramer", '["Sven Kramer", "Jorrit Bergsma", "Ireen Wüst"]', "sport", "medium"),
    ("In welk jaar werd de eerste Super Bowl gespeeld?", "1967", '["1967", "1950", "1975"]', "sport", "medium"),
    ("Wie won de FIFA Wereldbeker 2018?", "Frankrijk", '["Frankrijk", "Brazilië", "Duitsland"]', "sport", "medium"),
    ("Welke sporter heeft de meeste overwinningen in de Tour de France?", "Lance Armstrong", '["Lance Armstrong", "Eddy Merckx", "Miguel Indurain"]', "sport", "medium"),
    ("Wie is de snelste man ooit op de 100 meter?", "Usain Bolt", '["Usain Bolt", "Tyson Gay", "Asafa Powell"]', "sport", "medium"),
    ("Wie schilderde de beroemde 'Guernica', een kunstwerk over de Spaanse Burgeroorlog?", "Pablo Picasso", '["Pablo Picasso", "Salvador Dalí", "Henri Matisse"]', "cultuur", "gevorderd"),
    ("Wie won de Olympische gouden medaille op de 200 meter in 2008?", "Usain Bolt", '["Usain Bolt", "Michael Johnson", "Frank Fredericks"]', "sport", "gevorderd"),
    ("Wie heeft de meeste Formule 1-races gewonnen?", "Lewis Hamilton", '["Lewis Hamilton", "Michael Schumacher", "Ayrton Senna"]', "sport", "gevorderd"),
    ("Welke sporter heeft het meeste aantal Wimbledon-titels behaald?", "Roger Federer", '["Roger Federer", "Pete Sampras", "Björn Borg"]', "sport", "gevorderd"),
    ("Wie heeft het meeste aantal gouden medailles gewonnen op de Olympische Spelen?", "Michael Phelps", '["Michael Phelps", "Larisa Latynina", "Paavo Nurmi"]', "sport", "gevorderd"),
    ("Wie won de Tour de France in 1998?", "Marco Pantani", '["Marco Pantani", "Lance Armstrong", "Miguel Indurain"]', "sport", "gevorderd"),
    ("Wat is de langste afstand die ooit werd gerend in een ultramarathon?", "565 km", '["565 km", "500 km", "600 km"]', "sport", "gevorderd"),
    ("Wie is de oudste Formule 1-kampioen?", "Luigi Fagioli", '["Luigi Fagioli", "Juan Manuel Fangio", "Alain Prost"]', "sport", "gevorderd"),
    ("Wie was de eerste vrouwelijke sporter die een gouden medaille won op de Olympische Spelen?", "Hélène de Pourtalès", '["Hélène de Pourtalès", "Charlotte Cooper", "Stella Walsh"]', "sport", "gevorderd"),
    ("In welk jaar won Nederland de eerste Europese Voetbalkampioenschap?", "1988", '["1988", "1974", "1992"]', "sport", "gevorderd"),
    ("Wie won de wereldcup in Zuid-Afrika?", "spanje", '["duitsland","Engeland", "België"]', "sport", "gevorderd"),
    ("Wat is de naam van de beroemdste Japanse filmregisseur?", "Akira Kurosawa", '["Akira Kurosawa", "Hayao Miyazaki", "Yasujiro Ozu"]', "cultuur", "beginner"),
    ("Wat is de naam van de beroemde toren in Parijs?", "Eiffeltoren", '["Eiffeltoren", "Big Ben", "Vrijheidsbeeld"]', "cultuur", "beginner"),
    ("Welke beroemde Nederlandse kunstenaar schilderde 'De Sterrennacht'?", "Vincent van Gogh", '["Vincent van Gogh", "Rembrandt", "Johannes Vermeer"]', "cultuur", "beginner"),
    ("Welke Franse kunstenaar is bekend vanwege de 'waterlelies' schilderijen?", "Claude Monet", '["Claude Monet", "Pablo Picasso", "Edgar Degas"]', "cultuur", "beginner"),
    ("Wat is de naam van de wereldberoemde Italiaanse modehuis?", "Gucci", '["Gucci", "Versace", "Chanel"]', "cultuur", "beginner"),
    ("Welke beroemde Italiaanse schilder schilderde de 'Aankondiging van de Heilige Maagd'?", "Leonardo da Vinci", '["Leonardo da Vinci", "Raphael", "Michelangelo"]', "cultuur", "beginner"),
    ("Welke stad staat bekend om de beroemde 'Venetiaanse gondels'?", "Venetië", '["Venetië", "Rome", "Florence"]', "cultuur", "beginner"),
    ("In welk land werd de film 'Parasite' geproduceerd?", "Zuid-Korea", '["Zuid-Korea", "Japan", "China"]', "cultuur", "beginner"),
    ("Wat is de naam van de beroemde Engelse schrijver van 'Romeo en Julia'?", "William Shakespeare", '["William Shakespeare", "Charles Dickens", "Jane Austen"]', "cultuur", "beginner"),
    ("Wat is de naam van de beroemde Londense opera?", "Royal Opera House", '["Royal Opera House", "La Scala", "Metropolitan Opera House"]', "cultuur", "beginner"),
    ("Wie schilderde de beroemde 'Guernica'?", "Pablo Picasso", '["Pablo Picasso", "Salvador Dalí", "Henri Matisse"]', "cultuur", "medium"),
    ("Wat is de naam van de bekende Italiaanse opera die zich afspeelt in een operahuis?", "La Traviata", '["La Traviata", "Carmen", "Madama Butterfly"]', "cultuur", "medium"),
    ("Wie schreef het boek '1984'?", "George Orwell", '["George Orwell", "Aldous Huxley", "Ray Bradbury"]', "cultuur", "medium"),
    ("Welke muziekstijl komt oorspronkelijk uit Jamaica?", "Reggae", '["Reggae", "Blues", "Jazz"]', "cultuur", "medium"),
    ("Wie was de beroemde Franse modeontwerper die het 'kleine zwarte jurkje' introduceerde?", "Coco Chanel", '["Coco Chanel", "Christian Dior", "Yves Saint Laurent"]', "cultuur", "medium"),
    ("Wat is de naam van de beroemde Russische schrijver die 'Oorlog en Vrede' schreef?", "Leo Tolstoy", '["Leo Tolstoy", "Anton Tsjechov", "Fyodor Dostojewski"]', "cultuur", "medium"),
    ("Wat is de beroemde schilderij van Leonardo da Vinci?", "Mona Lisa", '["Mona Lisa", "Het Laatste Avondmaal", "De Geboorte van Venus"]', "cultuur", "medium"),
    ("Wat is de naam van de beroemde Franse stad waar het festival 'Cannes Film Festival' wordt gehouden?", "Cannes", '["Cannes", "Parijs", "Lyon"]', "cultuur", "medium"),
    ("Wat is het belangrijkste werk van de Franse schrijver Victor Hugo?", "Les Misérables", '["Les Misérables", "De klokkenluider van de Notre-Dame", "De Ketter"]', "cultuur", "medium"),
    ("Welke beroemde schilder wordt geassocieerd met het surrealisme?", "Salvador Dalí", '["Salvador Dalí", "Pablo Picasso", "Vincent van Gogh"]', "cultuur", "medium"),
    ("Wie was de belangrijkste vertegenwoordiger van de abstracte schilderkunst?", "Wassily Kandinsky", '["Wassily Kandinsky", "Jackson Pollock", "Piet Mondriaan"]', "cultuur", "gevorderd"),
    ("Wat is de naam van de beroemde Franse schrijver die 'De Fles' schreef?", "Albert Camus", '["Albert Camus", "Jean-Paul Sartre", "Simone de Beauvoir"]', "cultuur", "gevorderd"),
    ("Wat is de naam van de beroemde Duitse componist die 'Symfonie nr. 9' componeerde?", "Ludwig van Beethoven", '["Ludwig van Beethoven", "Johann Sebastian Bach", "Wolfgang Amadeus Mozart"]', "cultuur", "gevorderd"),
    ("Wie was de beroemde Engelse schrijver van 'Moby-Dick'?", "Herman Melville", '["Herman Melville", "Charles Dickens", "Jane Austen"]', "cultuur", "gevorderd"),
    ("Wat is de naam van de beroemde operazanger die 'Nessun Dorma' zong?", "Luciano Pavarotti", '["Luciano Pavarotti", "Enrico Caruso", "Placido Domingo"]', "cultuur", "gevorderd"),
    ("Wie schilderde het beroemde schilderij 'De Nachtwacht'?", "Rembrandt", '["Rembrandt", "Johannes Vermeer", "Pieter Bruegel de Oude"]', "cultuur", "gevorderd"),
    ("Wat is het belangrijkste werk van de Franse filosoof René Descartes?", "Meditaties over de Eerste Filosofie", '["Meditaties over de Eerste Filosofie", "Discours de la méthode", "Les Pensées"]', "cultuur", "gevorderd"),
    ("Wie was de oprichter van de Italiaanse Renaissance?", "Leonardo da Vinci", '["Leonardo da Vinci", "Michelangelo", "Raphael"]', "cultuur", "gevorderd"),
    ("Wie schreef 'Het Kapitaal', een invloedrijk werk over het marxisme?", "Karl Marx", '["Karl Marx", "Friedrich Engels", "Mao Zedong"]', "cultuur", "gevorderd"),
    ("Welke schrijver ontwikkelde de existentialistische filosofie in zijn werk 'Zijn en Niets'?", "Jean-Paul Sartre", '["Jean-Paul Sartre", "Simone de Beauvoir", "Maurice Merleau-Ponty"]', "cultuur", "gevorderd")
))



conn.commit()

# Sluit de verbinding
conn.close()

