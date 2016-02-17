from __future__ import print_function

from IPython.core.magic import Magics, magics_class, line_magic
import csv
import string
import keyword


def ident_escape(header, fill='_'):
    """ Escapes the column header string to make it a valid Python identifier.
    """
    # Reference: https://docs.python.org/2/reference/lexical_analysis.html#identifiers
    # Starts with a number
    if header[0] in string.digits:
        header = fill + header

    if keyword.iskeyword(header):
        header = fill + header

    mut = bytearray(header)
    valid = set(string.ascii_letters+string.digits)
    for i, c in enumerate(header):
        if c not in valid:
            mut[i] = fill
    return str(mut)


@magics_class
class CSVMagics(Magics):
    @line_magic
    def loadcsv(self, line):
        """ Loads columns from a CSV into python variables.
        Column headers are used as the variable names.

        Usage:
        * ``%loadcsv a.csv``        - Loads values of a.csv into lists
                                      named each column header.
        * ``%loadcsv a.csv col_``   - Loads values of a.csv into lists
                                      named each column header, prefixed by ``col_``
        """
        ip = self.shell
        opts, argsl = self.parse_options(line, 'drz', mode='string')
        args = argsl.split()
        filepath = args.pop(0)
        prefix = args[0] if args else ''
        with open(filepath, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            header = reader.next()
            lists = []
            names = []
            for column_name in header:
                value_list = []
                lists.append(value_list)
                identifier = ident_escape(prefix+column_name)
                names.append(identifier)
                ip.user_ns[identifier] = value_list

            for row in reader:
                for i, val in enumerate(row):
                    value_list = lists[i]
                    value_list.append(val)

            print('Loaded', len(lists[0]), 'values in', ','.join(names))

    @line_magic
    def storecsv(self, line):
        """ Stores lists of values as columns in a csv file.

        Usage:
        ``storecsv a.csv col1 col2 col3``  - Creates a.csv, populates the file
                                             with a header line `"col1","col2","col3"`
                                             and each subsequent line the value
                                             corresponding to that index in each list.
                                             Each list must be the same length.
        """

        ip = self.shell

        opts, argsl = self.parse_options(line, 'drz', mode='string')
        args = argsl.split()
        filepath = args.pop(0)

        # Check if all args are same length
        length = len(ip.user_ns[args[0]])
        for arg in args:
            iterable = ip.user_ns[arg]
            if len(iterable) != length:
                print('len('+arg+') != len('+args[0]+')')
                return

        iterables = []
        for arg in args:
            iterable = iter(ip.user_ns[arg])
            iterables.append(iterable)

        with open(filepath, 'wb') as csvfile:
            quoted = [u'"'+arg+u'"' for arg in args]
            csvfile.write(u','.join(quoted).encode('utf8'))
            csvfile.write('\n')

            for line in range(length):
                row = [u'"'+unicode(iterable.next())+u'"' for iterable in iterables]
                csvfile.write(u','.join(row).encode('utf8'))
                csvfile.write('\n')


def load_ipython_extension(ipython):
    ipython.register_magics(CSVMagics)
