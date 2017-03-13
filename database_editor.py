import psycopg2


class DB_Editor:
    def __init__(self):
        self.connection = psycopg2.connect("dbname=lotr_database user=grahambrown host=/tmp/")
        self.cur = self.connection.cursor()

    def menu(self):
        while True:
            menu_select = input("Would you like to add(1) a character, \
delete(2) a character, edit(3) a character, view(4) characters, or quit(Q): ")
            if menu_select == "1":
                self.add_character()
                break
            elif menu_select == "2":
                self.del_character()
                break
            elif menu_select == "3":
                self.edit_info()
                break
            elif menu_select == "4":
                self.view_character()
                break
            elif menu_select == "Q":
                return "Quit"

    def add_character(self):
        name = input("Character name: ")
        home = input("Character's home city: ")
        age = int(input("Character age(0 for unknown): "))
        race = input("Character race: ")
        self.cur.execute('INSERT INTO character(name, home_city, age, race) \
VALUES(%s, %s, %s, %s)', (name, home, age, race))
        self.connection.commit()

    def del_character(self):
        input_name = input("Name of character to remove: ")
        sure = "?"
        while sure:
            sure = input("Are you sure(Y,N): ")
            if sure == "Y":
                self.cur.execute('DELETE from character WHERE name =  %s', (input_name,))
                break
            if sure == "N":
                sure = False
        self.connection.commit()

    def edit_info(self):
        input_name = input("Whose info would you like to edit: ")
        input_field = False
        input_change = False
        choices = {"1": "name", "2": "home_city", "3": "age", "4": "race"}
        while input_field not in choices.keys():
            input_field = input("Which field to edit? name(1), home_city(2), age(3), race(4): ")
        input_field = choices[input_field]
        while not input_change:
            input_change = input("What to change it to: ")
        self.cur.execute('UPDATE character SET {} = %s WHERE name = %s'.format(input_field), (input_change, input_name))
        self.connection.commit()

    def view_character(self):
        choices = {"1": 'name', "2": 'home_city', "3": 'race'}
        while True:
            what_to_view = input("what do you want to lookup? name(1) , home city(2), race(3): ")
            what_to_view = choices[what_to_view]
            search = input("what {} do you want to view: ".format(what_to_view))
            break
        self.cur.execute("SELECT * from character WHERE {} = %s".format(what_to_view), (search,))
        print("\n")
        while True:
            try:
                searcher = self.cur.fetchone()
                print("Name: " + searcher[1])
                print("Home city: " + searcher[2])
                print("Age(0 for unknown): " + str(searcher[3]))
                print("Race: " + searcher[4])
                print("\n")
            except:
                break


def main():
    print("Welcome to the Tolkien database!")
    db_edit = DB_Editor()
    while not db_edit.menu():
        pass
    db_edit.cur.close()
    db_edit.connection.close()


main()
