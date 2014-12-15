from __future__ import print_function

from IPython.core.magic import Magics, magics_class, line_magic
import csv


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
                names.append(prefix+column_name)
                ip.user_ns[prefix+column_name] = value_list

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
            quoted = ['"'+arg+'"' for arg in args]
            csvfile.write(','.join(quoted))
            csvfile.write('\n')

            for line in range(length):
                row = ['"'+str(iterable.next())+'"' for iterable in iterables]
                csvfile.write(','.join(row))
                csvfile.write('\n')


def load_ipython_extension(ipython):
    ipython.register_magics(CSVMagics)
