#Charles Morales
#Artifact 2 
#11/23/25

from collections import Counter

class ItemTracker:
    def __init__(self, filename="Input.txt"):
        self.filename = filename
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

        items = self._read_items()
        if not items: 
            self._cache = {}
            return self._cache

        self._cache = dict(Counter(items))
        return self._cache

    def get_frequency(self, item_name):
        #Returns frequency of specific item
        frequencies = self.get_all_frequencies()
        return frequencies.get(item_name.lower(), 0)
    
    def get_histogram(self):
        #Returns dictionary where values are '*' for count
        frequencies = self.get_all_frequencies()
        return {item: '*' * count for item, count in frequencies.items()}

    # Prep for SQLite
    def load_from_database(self):
        raise NotImplementedError("Not implemented")

    def save_to_database(self, frequencies):
        raise NotImplementedError("Not implemented")

    #Functions for Source.cpp
_tracker = ItemTracker()

def CountUser(item):
    return _tracker.get_frequency(item)

def CountItems():
    return _tracker.get_all_frequencies()

def PrintHistogram():
    return _tracker.get_histogram()
