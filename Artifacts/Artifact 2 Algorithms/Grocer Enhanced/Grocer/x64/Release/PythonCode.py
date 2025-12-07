#Charles Morales
#Artifact 1 
#11/16/25

from collections import Counter

class ItemTracker:
    def __init__(self, filename="Input.txt"):
        self.filename = filename
    
    def _read_items(self):
        #Reads all items from the file and returns a list
        try:
            with open(self.filename, "r") as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"Error: Could not find {self.filename}")
            return []

    def get_all_frequencies(self):
        #Returns a dictionary of item count with counts
        items = self._read_items()
        return dict(Counter(items))

    def get_frequency(self, item_name):
        #Returns frequency of specific item
        frequencies = self.get_all_frequencies()
        return frequencies.get(item_name, 0)
    
    def get_histogram(self):
        #Returns dictionary where values are '*' for count
        frequencies = self.get_all_frequencies()
        return {item: '*' * count for item, count in frequencies.items()}

    #Functions for current Source.cpp
_tracker = ItemTracker()

def CountUser(item):
    return _tracker.get_frequency(item)

def CountItems():
    return _tracker.get_all_frequencies()

def PrintHistogram():
    return _tracker.get_histogram()
