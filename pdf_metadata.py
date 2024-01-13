import argparse
import os
from os import listdir
from os.path import isfile, join
from ebooklib import epub
import pikepdf
from pathvalidate import sanitize_filename
import sys

enable_epub = True
enable_pdf = True
do_rename = True



pdf_file='hands-ondataanalysiswithpandassecondedition.pdf'
pdf_path = 'pdf'
if __name__ == '__main__':


    pdf = pikepdf.Pdf.open(f'{pdf_path}/{pdf_file}')
    docinfo = pdf.docinfo
    has_title=False
    for key, value in docinfo.items():
        print(f'{key} =>  {value}')

