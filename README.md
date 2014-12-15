ipython-csvmagic
================

Tools for working with CSV files in IPython.

To install, in iPython shell:
```
%install_ext https://raw.githubusercontent.com/FrankSalad/ipython-csvmagic/master/csvtools.py
```

##Importing Data:
a.csv
```
"n","order_number","name"
"0","389","John Snow"
"1","405","Princess Bubblegum"
```

iPython:
```
In [7]: %loadcsv a.csv
Loaded 2 values in n,order_number,name

In [8]: n
Out[8]: ['0', '1']
In [9]: order_number
Out[9]: ['389', '405']
In [10]: name
Out[10]: ['John Snow', 'Princess Bubblegum']
```

Also supports prefixing headers:
```
In [13]: %loadcsv a.csv col_
Loaded 2 values in col_n,col_order_number,col_name

In [14]: col_n
Out[14]: ['0', '1']

In [15]: col_order_number
Out[15]: ['389', '405']

In [16]: col_name
Out[16]: ['John Snow', 'Princess Bubblegum']
```

Exporting Data:
```
In [23]: title = ['The Origin of Species', 'Oryx and Crake', 'Fahrenheit 451']

In [24]: name = ['Charles Darwin', 'Margaret Atwood', 'Ray Bradbury']

In [25]: n = range(len(title))

In [26]: %storecsv b.csv n name title
```

```
$ cat b.csv 
"n","name","title"
"0","Charles Darwin","The Origin of Species"
"1","Margaret Atwood","Oryx and Crake"
"2","Ray Bradbury","Fahrenheit 451"
```
