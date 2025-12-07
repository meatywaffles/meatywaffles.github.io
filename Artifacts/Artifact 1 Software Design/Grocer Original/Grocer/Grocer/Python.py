#Charles Morales
#Project 3 Corner Grocer
#8/18/24


import re
import string

# Function that counts the frequency of the item the user specifies
def CountUser(userItem):
    # opens Input.txt and reads it
    source = open("Input.txt", "r").read()
    itemCount = 0 #starting counter
    
    # Loop through each line in the file
    for item in source.split("\n"):
        if(userItem == item):
          itemCount += 1 # adds 1 each time the user's item is found
    return itemCount # returns the total

# Function that counts all items and returns the frequecies
def CountItems():
   # opens Input.txt and reads it
   source = open("Input.txt", "r").read()
   listItems = {} # stores the items
   
   # loops through each item in the file
   for item in source.split("\n"):
      if item in listItems:
         listItems[item]+= 1 # increments addional times item is found
      else:
         listItems[item] = 1 # finds a new item and starts it at 1
   
   WriteToFile(listItems)
         
   return listItems

# Function to write the frequency to a file
def WriteToFile(listItems):
   #open the output file and get ready to write to it
   output = open("frequency.dat", "w")
   
   #write listItems to frequency.dat
   for item in listItems:
       output.write(item + ": " + str(listItems[item]) + "\n")
      
   output.close() #closes frequency.dat
   

# Function to print a histogram of item frequencies
def PrintHistogram():
   # open Input.txt and read it
   source = open("Input.txt", "r").read()
   listItems = {} # stores the items
   
   #loop through each item in the file
   for item in source.split("\n"):
      if item in listItems:
         listItems[item] += 1 # Increments additional times item is found
      else:
         listItems[item] = 1 # Add the item to the dictionary with a count of 1
         
   # Print each item and its freuency as a histogram
   for item in listItems:
      print(item + ": " + '*' * listItems[item])