ipython-csvmagic
================

Tools for working with CSV files in IPython.

To install:

%install_ext https://raw.githubusercontent.com/FrankSalad/ipython-csvmagic/master/csvtools.py

##Example Usage:
a.csv
```
"n","order_number","name"
"0","389","John Snow"
"1","405","Princess Bubblegum"
```

iPython:
```
In [7]: %loadcsv /Users/frank/foo.csv
Loaded 2 values in n,order_number,name

In [8]: n
Out[8]: ['0', '1']
In [9]: order_number
Out[9]: ['389', '405']
In [10]: name
Out[10]: ['John Snow', 'Princess Bubblegum']
```
