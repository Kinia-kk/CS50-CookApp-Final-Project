import sqlite3

class Database():
    def __init__(self):
        self.con = sqlite3.connect("cooking_database.db")
        self.cursor = self.con.cursor()
        self.create_tables() 

    def create_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS list(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, item TEXT NOT NULL, quantity TEXT, status INTEGER NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS recipe(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, picture TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS ingredients(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, quantity TEXT, where_used INTEGER Not NULL)")
        self.con.commit()

    def add_item(self, item, quantity):
        self.cursor.execute("INSERT INTO list(item, quantity, status) VALUES(?,?,?)", (item, quantity, 0))
        self.con.commit()

        added_item = self.cursor.execute("SELECT * FROM list WHERE item = ?", (item,)).fetchall()
        return added_item[-1]
    
    def get_items(self):
        unowned = self.cursor.execute("SELECT * FROM list WHERE status = 0").fetchall()
        owned = self.cursor.execute("SELECT * FROM list WHERE status = 1").fetchall()

        return owned, unowned
    
    def check_shopping_completed(self, id):
        self.cursor.execute("UPDATE list SET status = 1 WHERE id = ?", (id,))
        self.con.commit()

    def check_shopping_incompleted(self, id):
        self.cursor.execute("UPDATE list SET status = 0 WHERE id = ?", (id,))
        self.con.commit()

    def delete_item(self, id):
        name = self.cursor.execute("SELECT item FROM list WHERE id = ?", (id,)).fetchall()
        self.cursor.execute("DELETE FROM list WHERE id = ?", (id,))
        self.con.commit()
        return name

    def add_recipe(self, name, description, picture):
        self.cursor.execute("INSERT INTO recipe(name, description, picture) VALUES(?,?,?)", (name, description, picture))
        self.con.commit()
        
        added_recipe = self.cursor.execute("SELECT * FROM recipe WHERE name = ?", (name,)).fetchall()
        return added_recipe[-1]
    
    def delete_recipe(self, id):
        self.cursor.execute("DELETE FROM ingredients WHERE where_used = ?", (id,))
        self.cursor.execute("DELETE FROM recipe WHERE id = ?", (id,))
        self.con.commit()

    def add_ingredient(self, name, quantity, recipe_id):
        self.cursor.execute("INSERT INTO ingredients(name, quantity, where_used) VALUES(?,?,?)", (name, quantity, recipe_id))
        self.con.commit()

    def get_recipies(self):
        recipies = self.cursor.execute("SELECT * FROM recipe").fetchall()
        return recipies
    
    def show_recipie(self, id):
        info = self.cursor.execute("SELECT * FROM recipe WHERE id = ?", id)
        return info

    def search(self, word):
        search = self.cursor.execute("SELECT * FROM recipe WHERE name LIKE ? OR description LIKE ?", ("%" + word + "%","%" + word + "%",)).fetchall()
        return search
    
    def get_ingredients(self, id):
        ingredients = self.cursor.execute("SELECT id,name, quantity FROM ingredients WHERE where_used = ?", (id,)).fetchall()
        return ingredients
    
    def recipe_details(self, id):
        rec = self.cursor.execute("SELECT * FROM recipe WHERE id = ?", (id,)).fetchall()
        return rec
    
    def change_amount(self, name, quantity):
        past_amount = self.cursor.execute("SELECT quantity FROM list WHERE item = ?", (name,)).fetchall()
        self.cursor.execute("UPDATE list SET quantity = ? WHERE item = ?", ((past_amount[0][0] + ", " + quantity), name,))
        self.con.commit()

    
    def close_database_connection(self):
        self.con.close()

    