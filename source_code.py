import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLineEdit,
                             QLabel, QComboBox, QStackedWidget, QRadioButton,
                             QListWidget, QMessageBox)
from stacked_interface import Ui_StackedWidget
import json

# Klasse voor database
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def haal_vragen_op(self, moeilijkheid, onderwerp, aantal_vragen, willekeurig):
        #controleert of willekeurig knop is ingedrukt
        if willekeurig:
            query = '''
                SELECT vraag, antwoord, opties, vraag_id
                FROM quiz_vragen
                ORDER BY random()
                LIMIT ?;
            '''
            self.cursor.execute(query, (aantal_vragen,))
        else:
            query = '''
                SELECT vraag, antwoord, opties, vraag_id
                FROM quiz_vragen 
                WHERE LOWER(moeilijkheid) = ? AND LOWER(onderwerp) = ?
                ORDER BY random()
                LIMIT ?
            '''
            self.cursor.execute(query, (moeilijkheid, onderwerp, aantal_vragen))
        return self.cursor.fetchall()

    def vraag_id_verzamelen(self, naam, juiste_vraag_id, foute_vraag_id):
        #statistieken voor juiste en foute antwoorden op te slaan
        #zoek bestaande gebruiker of maak nieuwe aan
        #foute_vraag_id en juiste_vraag_id komen van de interface class en vragen_laden_frontend methode
        naam = naam.strip()
        self.cursor.execute('SELECT gebruiker_id FROM personen_info WHERE LOWER(naam) = LOWER(?)', (naam,))
        gebruiker = self.cursor.fetchone()
        if gebruiker is None:
            self.cursor.execute('INSERT INTO personen_info (naam, score) VALUES (?, 0)', (naam,))
            gebruiker_id = self.cursor.lastrowid
        else:
            gebruiker_id = gebruiker[0]

        #registreer juiste antwoord
        for vraag_id in juiste_vraag_id:
            self.cursor.execute('''
                INSERT INTO quiz_statistieken (gebruiker_id, vraag_id, aantal_keren_juist, aantal_keren_fout)
                VALUES (?, ?, 1, 0)
                ON CONFLICT(gebruiker_id, vraag_id)
                DO UPDATE SET aantal_keren_juist = aantal_keren_juist + 1;
            ''', (gebruiker_id, vraag_id))
        #ON Conflict voorkomt duplicaten en werkt bestaande records bij i.p.v. eerst te checken en dan updaten

        #registreer foute antwoord
        for vraag_id in foute_vraag_id:
            self.cursor.execute('''
                INSERT INTO quiz_statistieken (gebruiker_id, vraag_id, aantal_keren_juist, aantal_keren_fout)
                VALUES (?, ?, 0, 1)
                ON CONFLICT(gebruiker_id, vraag_id)
                DO UPDATE SET aantal_keren_fout = aantal_keren_fout + 1;
            ''', (gebruiker_id, vraag_id))

        self.conn.commit()

    def score_berekenen(self, naam, score):
        # Controleer of de gebruiker al bestaat
        self.cursor.execute('SELECT 1 FROM personen_info WHERE naam = ?', (naam,))
        if self.cursor.fetchone():
        #update score
            self.cursor.execute('UPDATE personen_info SET score = ? WHERE naam = ?', (score, naam))
        else:
        # voeg nieuwe gebruiker toe met score
            self.cursor.execute('INSERT INTO personen_info (naam, score) VALUES (?, ?)', (naam, score))
        self.conn.commit()

    def top_score(self):
        self.cursor.execute('SELECT naam, score FROM personen_info ORDER BY score DESC LIMIT 3')
        return self.cursor.fetchall()
    #om de top 3 scores op te halen van de database

    def update_antwoord_statistieken(self):
        # voer de query uit om antwoord_statistieken bij te werken
        self.cursor.execute('''
            UPDATE antwoord_statistieken
            SET totaal_keren_juist = (
                SELECT COUNT(*) 
                FROM quiz_statistieken 
                WHERE quiz_statistieken.vraag_id = antwoord_statistieken.vraag_id 
                AND quiz_statistieken.aantal_keren_juist > 0
            ),
            totaal_keren_fout = (
                SELECT COUNT(*) 
                FROM quiz_statistieken 
                WHERE quiz_statistieken.vraag_id = antwoord_statistieken.vraag_id 
                AND quiz_statistieken.aantal_keren_fout > 0
            )
            WHERE EXISTS (
                SELECT 1
                FROM quiz_statistieken 
                WHERE quiz_statistieken.vraag_id = antwoord_statistieken.vraag_id
            );
        ''')
        self.conn.commit()
        #subqueries gebruikt

    def close(self):
        self.conn.close()

# Spelersklasse
class Speler:
    def __init__(self, naam):
        self.naam = naam
        self.score = 0

    def update_score(self, nieuwe_score):
        self.score = nieuwe_score
        #dit scheidt spelgegevens van UI en database logica

# Klasse voor quizvragen
class QuizVragen:
    def __init__(self, vragen, antwoorden, opties, vraag_id_lijst):
        self.vragen = vragen
        self.antwoorden = antwoorden
        self.opties = opties
        self.vraag_id_lijst = vraag_id_lijst
        self.vraag_index = 0
        self.aangeklikte_opties = [None] * len(vragen)

    def volgende_vraag(self):
        #naar de volgende vraag als die bestaat
        if self.vraag_index < len(self.vragen) - 1:
            self.vraag_index += 1
            return self.vragen[self.vraag_index], self.opties[self.vraag_index]
        return None, None
        # geen volgende vraag meer door None op beide indexen van vraag en opties

    def controleer_antwoord(self, gekozen_optie):
        self.aangeklikte_opties[self.vraag_index] = gekozen_optie
        return self.antwoorden[self.vraag_index] == gekozen_optie

    def verzamel_vraag_ids(self):
        #IDs van juiste en foute antwoorden in list (list comprehension)
        juiste_vraag_id = [self.vraag_id_lijst[i] for i in range(len(self.vragen))
                          if self.antwoorden[i] == self.aangeklikte_opties[i]]
        foute_vraag_id = [self.vraag_id_lijst[i] for i in range(len(self.vragen))
                         if self.antwoorden[i] != self.aangeklikte_opties[i]]
        return juiste_vraag_id, foute_vraag_id

# Interfaceklasse
class Interface(QMainWindow):
    def __init__(self):
        super().__init__() #inheritance van de Pyqt Qmainwindow class
        self.ui = Ui_StackedWidget()
        self.stacked_widget = QStackedWidget()
        self.ui.setupUi(self.stacked_widget)
        self.setCentralWidget(self.stacked_widget)
        self.database = Database('quiz_vragen_3.db')
        self.speler = None
        self.quiz_vragen = None
        self.dragging = False
        self.old_pos = None
        self.init_ui()
        self.stacked_widget.setCurrentIndex(0)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def init_ui(self):
        #ui elementen koppellen
        self.naam_input = self.stacked_widget.findChild(QLineEdit, 'naam_input')
        self.onderwerp_input = self.stacked_widget.findChild(QComboBox, 'onderwerp_input')
        self.moeilijkheid_input = self.stacked_widget.findChild(QComboBox, 'moeilijkheid_input')
        self.hoeveelheid = self.stacked_widget.findChild(QComboBox, 'comboBox')
        self.start_quiz2 = self.stacked_widget.findChild(QPushButton, "start_quiz2")
        self.willekeurig = self.stacked_widget.findChild(QRadioButton, 'willeukerig')
        self.next_vraag = self.stacked_widget.findChild(QPushButton, 'next_vraag')
        self.vraag_input = self.stacked_widget.findChild(QLabel, 'vraag_input')
        self.optie_input = self.stacked_widget.findChild(QListWidget, 'optie_input')
        self.feedback_button = self.stacked_widget.findChild(QPushButton, 'feedback_button')
        self.foute_vraag = self.stacked_widget.findChild(QLabel, 'foute_vraag')
        self.juiste_antwoord = self.stacked_widget.findChild(QLabel, 'juiste_antwoord')
        self.herstart_quiz = self.stacked_widget.findChild(QPushButton, 'herstart_quiz')
        self.score_gebruiker_label = self.stacked_widget.findChild(QLabel, 'score_gebruiker')
        self.feedback_knop_2 = self.stacked_widget.findChild(QPushButton, 'feedback_button_2')
        self.topscore_1 = self.stacked_widget.findChild(QLabel, 'topscore_1')
        self.topscore_2 = self.stacked_widget.findChild(QLabel, 'topscore_2')
        self.topscore_3 = self.stacked_widget.findChild(QLabel, 'topscore_3')

        # groepeer verberg- en sluitknoppen
        verberg_knoppen = [
            self.stacked_widget.findChild(QPushButton, 'verberg_page1'),
            self.stacked_widget.findChild(QPushButton, 'verberg_page2'),
            self.stacked_widget.findChild(QPushButton, 'verberg_page3'),
            self.stacked_widget.findChild(QPushButton, 'verberg_page4')
        ]
        sluit_knoppen = [
            self.stacked_widget.findChild(QPushButton, 'close_page1'),
            self.stacked_widget.findChild(QPushButton, 'close_page2'),
            self.stacked_widget.findChild(QPushButton, 'close_page3'),
            self.stacked_widget.findChild(QPushButton, 'close_page4')
        ]

        self.start_quiz2.clicked.connect(self.start_quiz)
        self.next_vraag.clicked.connect(self.vragen_laden_frontend)
        self.herstart_quiz.clicked.connect(self.herstart_quiz_functie)
        self.feedback_button.clicked.connect(self.fouten_laden)
        self.feedback_knop_2.clicked.connect(self.fouten_laden_rest)

        for knop in verberg_knoppen:
            knop.clicked.connect(self.verberg_page1)
        for knop in sluit_knoppen:
            knop.clicked.connect(self.sluit_page1)

        self.naam_input.setText("vul je naam in:")
        self.naam_input.mousePressEvent = self.wis_naam_input
        self.naam_input.focusOutEvent = self.terugzetten_naam_input

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.dragging and self.old_pos is not None:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def wis_naam_input(self, event):
        if self.naam_input.text() == "vul je naam in:":
            self.naam_input.clear()
        QLineEdit.mousePressEvent(self.naam_input, event)

    def terugzetten_naam_input(self, event):
        if not self.naam_input.text().strip():
            self.naam_input.setText("vul je naam in:")
        QLineEdit.focusOutEvent(self.naam_input, event)

    #helper functie om inputs op te schonen
    def clean_input(self, text, placeholder):
        return text.strip().lower().replace(placeholder, "")

    def start_quiz(self):
        #inputs van de quiz bij te houden in variabelen
        naam = self.clean_input(self.naam_input.text(), "vul je naam in:")
        onderwerp = self.clean_input(self.onderwerp_input.currentText(), "keuze thema:")
        moeilijkheid = self.clean_input(self.moeilijkheid_input.currentText(), "keuze niveau:")
        aantal_vragen = int(self.hoeveelheid.currentText().strip())
        is_willekeurig = self.willekeurig.isChecked()

        #validaties
        if not naam:
            self.toon_foutmelding("Naam vereist!")
            return
        if is_willekeurig and (onderwerp or moeilijkheid):
            self.toon_foutmelding("Kies geen Thema of moeilijkheid voor willekeurige vragen!")
            return

        resultaten = self.database.haal_vragen_op(moeilijkheid, onderwerp, aantal_vragen, is_willekeurig)
        if not resultaten:
            self.toon_foutmelding("Geen vragen gevonden!")
            return

        vragen, antwoorden, opties, vraag_id_lijst = self.vragen_klaar_zetten(resultaten)
        self.quiz_vragen = QuizVragen(vragen, antwoorden, opties, vraag_id_lijst)
        self.speler = Speler(naam)
        self.toon_vraag(vragen[0], opties[0])
        self.stacked_widget.setCurrentIndex(1)

    def vragen_laden_frontend(self):
        if not self.optie_input.currentItem():
            self.toon_foutmelding("Selecteer een optie!")
            return
        #laad volgende vraag
        gekozen_optie = self.optie_input.currentItem().text()
        if self.quiz_vragen.controleer_antwoord(gekozen_optie):
            self.speler.update_score(self.speler.score + 1)

        volgende_vraag, volgende_opties = self.quiz_vragen.volgende_vraag()
        #eindig quiz
        if volgende_vraag is None:
            juiste_vraag_id, foute_vraag_id = self.quiz_vragen.verzamel_vraag_ids()
            self.database.vraag_id_verzamelen(self.speler.naam, juiste_vraag_id, foute_vraag_id)
            self.eindig_quiz()
            return

        self.toon_vraag(volgende_vraag, volgende_opties)

    def bereken_score(self):
        if not self.quiz_vragen:
            return 0
        score = sum(1 for i in range(len(self.quiz_vragen.vragen))
                   if self.quiz_vragen.antwoorden[i] == self.quiz_vragen.aangeklikte_opties[i])
        return int(round((score * 10 / len(self.quiz_vragen.vragen)), 1))
        # het geeft een score op 10, gebaseerd op het percentage correcte antwoorden

    def toon_score(self):
        #toon score en werk statistieken bij
        self.database.update_antwoord_statistieken()
        score = self.bereken_score()
        self.score_gebruiker_label.setText(str(score))
        return str(score)

    def inject_score(self, naam, score):
        self.database.score_berekenen(naam, score)

    def toon_top_scores(self):
        topscores = self.database.top_score()
        topscore_labels = [self.topscore_1, self.topscore_2, self.topscore_3]
        for i, label in enumerate(topscore_labels):
            if i < len(topscores):
                naam, score = topscores[i]
                label.setText(f"{naam} = {score}")
            else:
                label.setText("Geen scores beschikbaar" if i == 0 else "")

    def eindig_quiz(self):
        score = self.bereken_score()
        self.toon_score()
        self.inject_score(self.speler.naam, score)
        self.toon_top_scores()
        self.stacked_widget.setCurrentIndex(2)

    def toon_vraag(self, vraag, opties):
        self.vraag_input.setText(vraag)
        self.optie_input.clear()
        self.optie_input.addItems(opties)
        #additems is van pyqt5 om items in een qlist widget toe te voegen

    def vragen_klaar_zetten(self, resultaten):
        vragen, antwoorden, opties, vraag_id_lijst = [], [], [], []
        for resultaat in resultaten:
            vraag, antwoord, optie_set, vraag_id = resultaat
            vragen.append(vraag)
            antwoorden.append(antwoord)
            #de vragen laden als Json sommige vragen hebben een ', ' en kunnen dan de vraag of optie niet volledig laden en moet in een json formaat geladen worden
            try:
                opties_lijst = json.loads(optie_set)
            except json.JSONDecodeError as e:
                opties_lijst = []
                #errorhandeling bij ongeldige JSON
            opties.append(opties_lijst)
            vraag_id_lijst.append(vraag_id)
        return vragen, antwoorden, opties, vraag_id_lijst

    def fouten_laden(self):
        #feedback welke vragen juist en fout waren
        fouten = [(vraag, antwoord) for vraag, antwoord in zip(self.quiz_vragen.vragen, self.quiz_vragen.antwoorden)
                 if antwoord != self.quiz_vragen.aangeklikte_opties[self.quiz_vragen.vragen.index(vraag)]]
        if not fouten:
            self.toon_informatie("Proficiat!", "Je hebt alle vragen correct beantwoord!")
            return
        self.toon_fout(fouten[0][0], fouten[0][1])
        self.fouten = fouten[1:]
        self.stacked_widget.setCurrentIndex(3)

    def fouten_laden_rest(self):
        #laad volgende fout of herstart
        if not hasattr(self, 'fouten') or not self.fouten:
            #controleert of object de 'fouten' attribute niet heeft
            self.toon_informatie("Proficiat!", "Er zijn geen foute vragen meer!")
            self.herstart_quiz_functie()
            return
        self.toon_fout(self.fouten[0][0], self.fouten[0][1])
        self.fouten = self.fouten[1:]

    def toon_fout(self, fout_vraag, correct_antwoord):
        self.foute_vraag.setText(fout_vraag)
        self.juiste_antwoord.setText(correct_antwoord)

    def herstart_quiz_functie(self):
        self.naam_input.setText("vul je naam in:")
        self.onderwerp_input.setCurrentIndex(0)
        self.moeilijkheid_input.setCurrentIndex(0)
        self.hoeveelheid.setCurrentIndex(0)
        self.stacked_widget.setCurrentIndex(0)

    def verberg_page1(self):
        self.showMinimized()

    def sluit_page1(self):
        self.close()

    def toon_foutmelding(self, tekst):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Foutmelding")
        msg.setText(tekst)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def toon_informatie(self, titel, tekst):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(titel)
        msg.setText(tekst)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    interface = Interface()
    interface.show()
    sys.exit(app.exec_())