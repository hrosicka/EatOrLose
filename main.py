import tkinter as tk
import sqlite3

# Vytvoření databáze (pokud neexistuje)
conn = sqlite3.connect('potraviny.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS potraviny
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              nazev TEXT NOT NULL,
              datum_spotreby TEXT NOT NULL)''')
conn.commit()

# Funkce pro přidání potraviny
def pridej_potravinu():
    nazev = entry_nazev.get()
    datum = entry_datum.get()
    cursor.execute("INSERT INTO potraviny (nazev, datum_spotreby) VALUES (?, ?)", (nazev, datum))
    conn.commit()
    zobraz_potraviny()

# Funkce pro zobrazení potravin
def zobraz_potraviny():
    for item in listbox.get(0, tk.END):
        listbox.delete(item)
    cursor.execute("SELECT * FROM potraviny")
    results = cursor.fetchall()
    for row in results:
        listbox.insert(tk.END, f"{row[1]} ({row[2]})")

# Funkce pro odstranění potraviny
def odstran_potravinu():
    index = listbox.curselection()
    if index:
        item = listbox.get(index)
        cursor.execute("DELETE FROM potraviny WHERE nazev=?", (item.split(' (')[0],))
        conn.commit()
        zobraz_potraviny()

# Vytvoření hlavního okna
okno = tk.Tk()
okno.title("Sledování spotřeby potravin")

# Vytvoření prvků GUI
label_nazev = tk.Label(okno, text="Název potraviny:")
entry_nazev = tk.Entry(okno)
label_datum = tk.Label(okno, text="Datum spotřeby:")
entry_datum = tk.Entry(okno)
button_pridej = tk.Button(okno, text="Přidat", command=pridej_potravinu)
button_odstran = tk.Button(okno, text="Odstranit", command=odstran_potravinu)
listbox = tk.Listbox(okno)

# Umístění prvků na okno
label_nazev.pack()
entry_nazev.pack()
label_datum.pack()
entry_datum.pack()
button_pridej.pack()
button_odstran.pack()
listbox.pack()

# Zobrazení potravin při spuštění aplikace
zobraz_potraviny()

# Spuštění aplikace
okno.mainloop()
