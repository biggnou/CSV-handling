#! /usr/bin/python
# -*- coding: utf-8 -*-
# @author: biggnou@gmail.com
# @purpose: split and output a CSV file in a new one.

import argparse
import csv
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='CSV file spliter')
    parser.add_argument('infile', help='CSV file to import', action='store')
    parser.add_argument('-o', '--output', dest='outfile', help='CSV file to create', action='store')
    parser.add_argument('-v', '--verbose', help='Show a sample output on screen', action='store_true')
    parser.add_argument('-n', '--dryrun', help='Dry run: do nothing but produce sample output', action='store_true')

    args = parser.parse_args()

    if args.outfile and args.dryrun:  # mmm... doesn't make any sense
        parser.error("\nYou can't write an output file while performing a dry-run.\n")

    csv_INfile = args.infile
    if args.outfile:
        csv_OUTfile = args.outfile

    df = pd.read_csv(csv_INfile) # read the file to get a pandas' DataFrame

    fh = open(csv_INfile, 'r')
    reader = csv.reader(fh)
    rfd_header = reader.next()  # list from csv is easier than DataFrame from pandas to work with :-(
    fh.close()

    print "\nHere are the column in this CSV file:\n" , rfd_header

    selection_list = []  # user select

    print "\nNow please select each column you want to keep. Press <enter> (leave empty) when satisfied. The order you make your selection will be the new CSV file columns order.\n"

    while True:

        selection = raw_input('Select a CSV field: ')

        if selection is not "":
            if selection in rfd_header:  # ntui
                selection_list.append(selection)
            else:
                print "Oops," , selection , "not in the headers..."

        else:
            break

    print "\nHere is your selection: " , selection_list

    if args.verbose or args.dryrun:  # print to STDOUT (sample of 10 first lines only)
        print "\nHere is what the output will look like...\n"
        print df[selection_list].head(10) , "\n"

    if args.outfile:  # yeah, new file \o/
        with open(csv_OUTfile, 'w') as f:
            df[selection_list].to_csv(f, header=True, index=False, quoting=csv.QUOTE_ALL)

        f.close()
        print "\nDone! Please check \" {out} \".\n".format(out=csv_OUTfile)

if __name__ == "__main__":
    main()
