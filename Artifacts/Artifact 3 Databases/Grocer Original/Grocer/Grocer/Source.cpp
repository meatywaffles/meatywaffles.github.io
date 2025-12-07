///Charles Morales
//Project 3 Corner Grocer
//8/18/24



#include<Python.h>
#include<iostream>
#include<fstream>
#include<string>
#include<vector>

using namespace std;

class Item {
private:
	string itemName;
	int frequency;

public:
	Item(string name, int freq) : itemName(name), frequency(freq) {}

	string getName() {
		return itemName;
	}
	int getFrequency() {
		return frequency;
	}
	void setFrequency(int freq) {
		frequency = freq;
	}
};

int userInput;
string userItem;
void displayMenu();
int validateOption();
void GetUserItem();
void CallPrintFrequencies();
void CallPrintHistogram();
vector<Item> populateItemsFromPython(PyObject* pResut);

// takes the items from python and puts them in Item class
vector<Item> populateItemsFromPython(PyObject* pResult) {
	vector<Item> items;

	if (PyDict_Check(pResult)) {
		PyObject* key;
		PyObject* value;
		Py_ssize_t pos = 0;

		while (PyDict_Next(pResult, &pos, &key, &value)) {
			string itemName = PyUnicode_AsUTF8(key);
			int frequency = PyLong_AsLong(value);
			items.push_back(Item(itemName, frequency));
		}
	}
	return items;

}


void displayMenu() {
	cout << "**************************************" << endl;
	cout << "                Corner Grocer         " << endl;
	cout << "**************************************" << endl;
	cout << "Please pick from the following options" << endl;
	cout << "1: Count a specific item" << endl;
	cout << "2: Display all item quantities" << endl;
	cout << "3: Display histogram of item counts" << endl;
	cout << "4: Exit" << endl;
	cout << "**************************************" << endl;
	userInput = validateOption();
}

int validateOption() {
	int x;

	while (true) {
		if (cin >> x) {
			if (x >= 1 && x <= 4) {
				//valid number
				break;
			}
			else {
				//Number not valid
				cout << "Invalid input" << endl;
				cin.clear();
				cin.ignore(100000, '\n');
			}
		}
		else {
			//Not a number
			cout << "Invalid input" << endl;
			cin.clear();
			cin.ignore(100000, '\n');
		}
	}
	return x;
}
// calls the python function CountUser
void GetUserItem() {
	cout << "Which item are you searching for" << endl;
	cin.ignore(numeric_limits<streamsize>::max(), '\n');
	getline(cin, userItem);
	//initialize the python interpreter
	Py_Initialize();
	PyObject* pModule = PyImport_ImportModule("PythonCode");

	// import CountUser function from python
	PyObject* pFunc = PyObject_GetAttrString(pModule, "CountUser");

	// call CountUser function
	PyObject* pInput = PyTuple_Pack(1, PyUnicode_FromString(userItem.c_str()));
	PyObject* pResult = PyObject_CallObject(pFunc, pInput);
	Py_DECREF(pInput);

	//displaying
	int count = PyLong_AsLong(pResult);
	cout << "The frequency of " << userItem << " is: " << count << endl;


}
//calls the python function CountItems
void CallPrintFrequencies() {
	//initialize the python interpreter
	Py_Initialize();

	PyObject* pModule = PyImport_ImportModule("PythonCode");
	PyObject* pFunc = PyObject_GetAttrString(pModule, "CountItems");

	PyObject* pResult = PyObject_CallObject(pFunc, NULL);
	if (pResult != NULL) {
		vector<Item> items = populateItemsFromPython(pResult);
		for (auto& item : items) {
			cout << item.getName() << ": " << item.getFrequency() << endl;
		}
		Py_DECREF(pResult);
	}
	else {
		PyErr_Print(); // prints python error if pResult is empty
	}

	Py_DECREF(pFunc);
	Py_DECREF(pModule);
	Py_Finalize(); // finalize python interpreter
}
// calls the python function PrintHistogram
void CallPrintHistogram() {

	//initialize python interpeter
	Py_Initialize();

	PyObject* pModule = PyImport_ImportModule("PythonCode");
	PyObject* pFunc = PyObject_GetAttrString(pModule, "PrintHistogram");

	PyObject* pResult = PyObject_CallObject(pFunc, NULL);
	if (pResult != NULL) {
		vector<Item> items = populateItemsFromPython(pResult);
		for (auto& item : items) {
			cout << item.getName() << ": " << string(item.getFrequency(), '*') << endl;
		}
	}
	else {
		PyErr_Print();// print python error if function not called
	}
	Py_DECREF(pFunc);
	Py_DECREF(pModule);
	Py_Finalize();//finalize python interpreter
}

int main() {

	displayMenu();
	switch (userInput) {
	case 1:
		// Option 1 to count a specific item
		GetUserItem();

		system("pause");
		break;
	case 2:
		// Option 2 to display all items and quantities
		CallPrintFrequencies();

		system("pause");
		break;
	case 3:
		// Option 3 to display histogram
		CallPrintHistogram();

		system("pause");
		break;

	case 4:
		// ends the switch statement
		break;

	default:
		cout << "Invalid selection." << endl;
		system("pause");
		break;
	}

}