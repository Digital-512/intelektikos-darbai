import json

# 1 uzduotis

"""
1. Paprasyti vartotojo, kad surasytu, kokiu duomenu reikes.
2. Vartotojas suveda reikiamus duomenis.
3. Paklausti vartotojo, ar reikia ivesti nauja duomenu irasa.
4. Visa duomenu baze irasyti i tekstini faila.
5. Irasyti i JSON faila.
"""

menu_select = {
    1: "Sukurti duomenu baze",
    2: "Rodyti sukurtas duomenu bazes ir ju skaiciu",
    3: "Rodyti pasirinktos duomenu bazes duomenis",
    4: "Irasyti duomenu bazes i tekstini (.txt) faila",
    5: "Irasyti duomenu bazes i JSON faila",
    6: "Irasyti duomenu bazes i SQL faila",
    7: "Iseiti is programos"
}

schemas = list()


def create_schema():
    # prasyti pavadinimo
    schema = dict()
    schema["schema_name"] = input("Irasykite duomenu bazes pavadinima: ")
    schema["data"] = list()

    # prasyti duomenu bazes strukturos sukurimo
    schema_struct = list()
    while True:
        name = input("Irasykite laukelio pavadinima: ")
        schema_struct.append(name)

        if input("Ar norite sukurti dar viena laukeli? [Y/n]: ").lower() == "n":
            break

    # prasyti duomenu surasymo i sukurta duomenu bazes struktura
    num = 0
    while True:
        num += 1
        entity = dict()

        print("\nSukuriamas", str(num), "duomenu bazes irasas\n")

        for field in schema_struct:
            entity[field] = input("Iveskite laukelio `" + field + "` reiksme: ")

        schema["data"].append(entity)

        if input("Ar norite sukurti dar viena irasa? [Y/n]: ").lower() == "n":
            break

    # irasyti duomenu baze
    print("\nSukurta duomenu baze `" + schema["schema_name"] + "`")
    schemas.append(schema)


def show_schemas():
    # atspausdinti, kiek yra sukurta duomenu baziu ir ju pavadinimus
    print("\nSukurta duomenu baziu:", len(schemas))
    print("Sukurtu duomenu baziu sarasas:")

    # rodyti duomenu baziu pavadinimus
    dbs = list()
    for db in schemas:
        dbs.append(db["schema_name"])

    print("[", ", ".join(dbs), "]")


def show_schema_data():
    selected_schema = input("Iveskite duomenu bazes pavadinima, kuria norite perziureti: ")
    found = False
    for schema in schemas:
        if schema["schema_name"] == selected_schema:
            print(json.dumps(schema["data"], indent=4))
            found = True
            break
    if not found:
        print("Nera sukurtos tokios duomenu bazes `" + selected_schema + "`")


def export_txt():
    # prasyti failo pavadinimo
    file_name = input("Irasykite TXT failo pavadinima: ")

    # sukuriamas failas
    file = open(file_name + ".txt", "w")

    # irasomos duomenu bazes i TXT faila
    for schema in schemas:
        keys = schema["data"][0].keys()

        file.write("\n----------------------------------\n")
        file.write(schema["schema_name"])
        file.write("\n----------------------------------\n\n")
        file.write(" | ".join(keys))
        file.write("\n----------------------------------\n")

        for row in schema["data"]:
            for col in keys:
                file.write(row[col] + " | ")
            file.write("\n")

        file.write("\n")

    # uzdaromas failas
    file.close()

    print("Sukurtas failas `" + file_name + ".txt`")


def export_json():
    # prasyti failo pavadinimo
    file_name = input("Irasykite JSON failo pavadinima: ")

    # sukuriamas failas
    file = open(file_name + ".json", "w")

    # irasomos duomenu bazes i JSON faila
    file.write(json.dumps(schemas, indent=4))

    # uzdaromas failas
    file.close()

    print("Sukurtas failas `" + file_name + ".json`")


def get_sql_type(key, data):
    if key.lower() == "id":
        return "`" + key + "` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY"
    if data.isnumeric():
        return "`" + key + "` INT NOT NULL"
    if "." in data:
        try:
            float(data)
            return "`" + key + "` FLOAT NOT NULL"
        except ValueError:
            pass
    if data == "True" or data == "False":
        return "`" + key + "` BOOLEAN NOT NULL"
    if type(data) is str:
        return "`" + key + "` VARCHAR(255) NOT NULL" if len(data) <= 255 else "`" + key + "` TEXT NOT NULL"


def export_sql():
    # prasyti failo pavadinimo
    file_name = input("Irasykite SQL failo pavadinima: ")

    # sukuriamas failas
    file = open(file_name + ".sql", "w")

    # irasomos duomenu bazes i SQL faila
    file.write("-- Duomenu bazes sukurimas\n\n")
    file.write("CREATE SCHEMA `" + file_name + "` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n")
    file.write("USE `" + file_name + "`;\n")
    file.write("\n-- Sukuriamos lenteles duomenu bazeje\n\n")

    # sukuriamos lenteles
    for schema in schemas:
        keys = schema["data"][0].keys()
        file.write("CREATE TABLE `" + schema["schema_name"] + "` (\n")
        for col in keys:
            file.write("    " + get_sql_type(col, schema["data"][0][col]) + ",\n")
        file.write(");\n\n")

    # irasomi duomenys i lenteles
    file.write("-- Duomenu bazes pildymas duomenimis\n\n")
    for schema in schemas:
        file.write("INSERT INTO `" + schema["schema_name"] + "` VALUES\n")
        for data in schema["data"]:
            file.write("(" + ", ".join(data.values()) + "),\n")
        file.write("\n")

    # uzdaromas failas
    file.close()

    print("Sukurtas failas `" + file_name + ".sql`")


def main_script():
    while True:
        print("\nPasirinkite veiksma, kuri norite atlikti:\n")

        # atspausdinti visus meniu pasirinkimus
        for key in menu_select.keys():
            print("[" + str(key) + "]", menu_select[key])

        # nuskaityti vartotojo pasirinkima
        try:
            select = int(input())
        except ValueError:
            print("Neteisinga ivestis. Irasykite skaiciu.")
            continue

        # isvalyti konsoles langa (priraso daug tusciu eiluciu)
        print("\n" * 100)

        # ivykdyti vartotojo pasirinkta komanda
        if select == 1:
            create_schema()
        elif select == 2:
            show_schemas()
        elif select == 3:
            show_schema_data()
        elif select == 4:
            export_txt()
        elif select == 5:
            export_json()
        elif select == 6:
            export_sql()
        elif select == 7:
            exit()
        else:
            print("Nera tokio pasirinkimo. Irasykite skaiciu nuo 1 iki", len(menu_select))


if __name__ == "__main__":
    main_script()
