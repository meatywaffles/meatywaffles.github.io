#Charles Morales
#Artifact 3
#11/30/25

import sqlite3
from collections import Counter

class ItemTracker:
    def __init__(self, text_file="Input.txt", db_file="groceries.db"):
        self.filename = text_file
        self.db_filename = db_file
        self._cache = None # Cache for frequencies
    
    def _read_items(self):
        #Reads all items from the file and returns a list
        items = []
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    # Makes things normalized by making everything lowercase
                    cleaned = line.strip().lower()
                    if cleaned:
                        items.append(cleaned)
        except FileNotFoundError:
            print(f"Error: Could not find {self.filename}")
        return items

    def get_all_frequencies(self):
        #Returns a dictionary of item count with counts
        if self._cache is not None:
            return self._cache

        # Try loading from database
        if self._load_from_database() and self._cache:
            return self._cache

        # Fallback read from file
        print("No database data found, Migrating from text file")
        items = self._read_items()

        if not items: 
            self._cache = {}
            return self._cache

        self._cache = dict(Counter(items))
        self._save_to_database() # one-time migration
        return self._cache

    def get_frequency(self, item_name):
        #Returns frequency of specific item
        frequencies = self.get_all_frequencies()
        return frequencies.get(item_name.lower(), 0)
    
    def get_histogram(self):
        #Returns dictionary where values are '*' for count
        frequencies = self.get_all_frequencies()
        return {item: '*' * count for item, count in frequencies.items()}

    # SQLite functions
    def _connect(self):
        #Secure connection
        return sqlite3.connect(self.db_filename)

    def _ensure_initialization(self):
        # Create inventory table if it doesn't exist
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS inventory
        (item_name TEXT PRIMARY KEY, 
        quantity INTEGER NOT NULL
        )
        """)
        conn.commit()
        conn.close()

    def _load_from_database(self):
        # Load frequencies from database into cache
        try:
            self._ensure_initialization()
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT item_name, quantity FROM inventory")
            results = cursor.fetchall()
            self._cache = {name: qty for name, qty in results}
            conn.close()
            return True
        except Exception as e:
            print(f"Database load error: {e}")
            return False

    def _save_to_database(self):
        # Save current cache to database
        if self._cache is None:
            return False

        try:
            self._ensure_initialization()
            conn = self._connect()
            cursor = conn.cursor()

            for item, count in self._cache.items():
                cursor.execute("""
                    INSERT OR REPLACE INTO inventory (item_name, quantity)
                    VALUES (?, ?)
                    """, (item,count))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Database save error: {e}")
            return False


    #Functions for Source.cpp
_tracker = ItemTracker()

def CountUser(item):
    return _tracker.get_frequency(item)

def CountItems():
    return _tracker.get_all_frequencies()

def PrintHistogram():
    return _tracker.get_histogram()
