import psycopg2


class DB_Editor:
    def __init__(self):
        self.connection = psycopg2.connect("dbname=lotr_database user=grahambrown host=/tmp/")
        self.cur = self.connection.cursor()

    def menu(self):
        while True:
            menu_select = input("Would you like to add(1) a character, \
delete(2) a character, edit(3) a character, or view(4) characters: ")
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
        self.cur.execute('DELETE from character WHERE name =  %s', (input_name,))
        self.connection.commit()

    def edit_info(self):
        input_name = input("Whose info would you like to edit: ")
        input_field = False
        input_field = input("Which field to edit? name(1), home_city(2), age(3), race(4): ")
        if input_field == "1":
            input_field = 'name'
        elif input_field == "2":
            input_field = 'home_city'
        elif input_field == "3":
            input_field = 'age'
        elif input_field == "4":
            input_field = 'race'
        input_change = input("What to change it to: ")
        self.cur.execute('UPDATE character SET {} = %s WHERE name = %s'.format(input_field), (input_change, input_name))
        self.connection.commit()

    def view_character(self):
        while True:
            what_to_view = input("what do you want to lookup? name(1) , home city(2), race(3): ")
            if what_to_view == "1":
                what_to_view = 'name'
                search = input("what name do you want to view: ")
                break
            elif what_to_view == "2":
                what_to_view = 'home_city'
                search = input("what city do you want to view: ")
                break
            elif what_to_view == "3":
                what_to_view = 'race'
                search = input("what race do you want to view: ")
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
    while True:
        db_edit.menu()
    db_edit.cur.close()
    db_edit.connection.close()


main()
