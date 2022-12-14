# Blockchain Demo
This project contains a mainly OOP implementation of a basic blockchain logic. 
Inspired by [this](http://ecomunsing.com/build-your-own-blockchain) article.
Implementation is meant to work with python-3.11. Core logic remained largery
the same but has been transformed into an OOP approach. Some minor functions
have been added and export/import logic has been tweaked a little bit in order
to avoid having to use default dictionaries with potential key errors everywhere.

# Run tests:
```
cd Python
python -m venv venv
./venv/Scripts/activate
pip install -e .
python -m unittest discover --verbose
```

# Room for improvement:

* Description of functionality and enhancing this readme of better running instrucitons.
* Better unittests - finishing testing of all the methods concerning chain checking at the very least. 
* Setting up some sort of automatic CI pipeline in order to run tests on push and analyze the code quality.
* Possible refactoring of class SimpleBlockchain due to it's size - some methods may not necessary be there (hash_msg) 