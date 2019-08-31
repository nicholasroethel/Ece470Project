This project contains a genetic algorithm that attempts to decrypt a cipher text that hsa been encoded using a Vignere Cipher. 

Our code is contained in GADecrypt, it is currently setup to test parameters.

To run:
1. Install python3 
2. Install dependencies with pip `pip install -r requirements.txt`
3. Run the code with `py ./GADecrypt.py`

It will take a few minutes to run and then generate a graph by varying the parameter designated parameter.
All parameters can be seen with `py ./GADecrypt.py --h`.

Additionally GADPasswordSelection.py is a program used to choose a strong password for the vignere cipher. Full details can be found in the report. The code can be run with `py ./GADPasswordSelection.py`
