from neo4j import GraphDatabase
import PySimpleGUI as sg
import py2neo as p2n

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, text):
        with self.driver.session() as session:
            result = session.read_transaction(self._query, text)
            return result

    @staticmethod
    def _query(tx, text):
        result = tx.run(text)
        return [row["name"] for row in result]
uri = "neo4j+s://2e12b79b.databases.neo4j.io:7687"
user = "neo4j"
password = "ow9OU3dGFRsP6nOmUjZCWWOr3BeWw8GOhpp7CPpxcBU"
app = App(uri, user, password)
screens = app.query("MATCH (n:Win) RETURN n.name AS name")
fun = app.query("MATCH (n:Function) RETURN n.name AS name")
al = app.query("Match (al:Alisa) RETURN al.name AS name")



layout = [
    [sg.Button('Главный экран')],
    [sg.Text('Вывести события функций:')],
    [sg.Listbox(values=fun, size=(35, 3), enable_events=True, key='selected_key')],
    [sg.Text('Список :')],
    [sg.Listbox(values=["Функции", "Всё"], size=(35, 3), enable_events=True, key='selected_key_el')],
    [sg.Output(size=(88, 20),key = '_output_')],
    [sg.Button('Выход'), sg.Button('Очистить')]
]

window = sg.Window('pythonProject', layout)
while True:
    event, values = window.read()
  ###
    if event == 'Главный экран':
        path = ['AliseScr']
        while len(app.query(f"MATCH (w1)-[r:RELTYPE]->(Win) WHERE w1.name = '{path[-1]}' RETURN Win.name AS name;")) > 0:
            path.append(app.query(f"MATCH (w1)-[r:RELTYPE]->(Win) WHERE w1.name = '{path[-1]}' RETURN Win.name AS name;"))
            path[-1].append(0)
            path[-1] = path[-1][0]
            if path[-1] == "AliseScr":
                break
        b = []
        for i in path:
            if i in screens:
                b.append(i)
        print(' -> '. join(b))
        print('----------------------------------------------------------------------------------------------------')
###
    ###
    elif event == 'selected_key':
        screen = app.query(f"MATCH (Function)-[r]->(Event) WHERE Function.name='{   values[event][0]}' RETURN Event.name AS name")
        print(f'События функций {values[event][0]}:')
        for i in range(len(screen)):
            print('\t' + screen[i])
        print('----------------------------------------------------------------------------------------------------')
    ###
    elif event == 'selected_key_el':
        if values['selected_key_el'][0] == 'Функции':
            screen = app.query("MATCH (Function) RETURN [Function.name, Function.alias, Function.discription] AS name")
            print(screen)
            print('----------------------------------------------------------------------------------------------------')
        elif values['selected_key_el'][0] == 'Всё':
            screen = app.query("MATCH (n) RETURN [n.name, n.alias, n.discription] AS name")
            print(screen)
            print('----------------------------------------------------------------------------------------------------')
    if event in (None, 'Выход'):
        break
    if event == 'Очистить':
        window.FindElement('_output_').Update('')