import argparse
import os
from os import listdir
from os.path import isfile, join
from ebooklib import epub
import pikepdf
from pathvalidate import sanitize_filename
import shutil
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def check_path(path):
    print(f'{bcolors.OKBLUE}[INF] Verifying path ({path}){bcolors.ENDC}')
    if os.path.exists(path) and os.path.isdir(path):
        print(f'{bcolors.OKGREEN}[OK ] Directory ({path}) exists{bcolors.ENDC}')
        if os.access(path, os.W_OK):
            print(f'{bcolors.OKGREEN}[OK ] Path ({path}) is writeable{bcolors.ENDC}')
        else:
            print(f'{bcolors.FAIL}[ERR] Path ({path}) is NOT writeable{bcolors.ENDC}')
            exit(99)
    else:
        print(f'{bcolors.FAIL}[ERR] Directory ({path}) does NOT exists{bcolors.ENDC}')
        exit(99)

def do_backup(source, dest):
    print(f'{bcolors.OKCYAN}[INF] Backup {source} => {dest}{bcolors.ENDC}')
    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        if os.path.isfile(file_path):
            shutil.copy2(file_path, dest)
            print(f'[OK ] Copied {file_path} to {dest}')

parser = argparse.ArgumentParser(
                    prog='rename_books.py',
                    description='Rename PDF and EPUB based on their meta data')
parser.add_argument('path', type=str, help="Path to the directory conatining the files to be renamed")
group = parser.add_mutually_exclusive_group()
parser.add_argument("--backup_dir", type=str, help="Directory to backup the files")
group.add_argument("--pdf", action="store_true", help="rename PDF Files")
group.add_argument("--epub", action="store_true", help="rename EPUB Files")
parser.add_argument("--dry", action="store_true", help="Dry run - do not rename")
args = parser.parse_args()

enable_epub = False
enable_pdf = False
do_rename = True
path=''
pdf_path=''
OK='[OK ]'


if args.epub:
    enable_epub = True
if args.pdf:
    enable_pdf = True
if args.dry:
    do_rename = False
    OK='[DRY]'

if args.path:
    check_path(args.path)
    if enable_epub:
        path=args.path
    if enable_pdf:
        pdf_path = args.path

if not enable_epub and not enable_pdf:
    print('{bcolors.FAIL}[ERR] Please specify either --epub or --pdf option{bcolors.ENDC}')
    exit(99)


if args.backup_dir:

    check_path(args.backup_dir)
    if enable_epub:
        do_backup(path, args.backup_dir)
    elif enable_pdf:
        do_backup(pdf_path, args.backup_dir)

if __name__ == '__main__':


    if enable_epub:
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for file in files:
            book = epub.read_epub(f'{path}/{file}')
            result = book.get_metadata('DC', 'title')
            if result:
                dest_file = sanitize_filename(f'{result[0][0]}.epub')
                print (f'{OK} Rename {file} =>  {dest_file}')
                if do_rename:
                    os.rename(f'{path}/{file}', f'{path}/{dest_file}')

    elif enable_pdf:
        for pdf_file in [f for f in listdir(pdf_path) if isfile(join(pdf_path, f))]:
            pdf = pikepdf.Pdf.open(f'{pdf_path}/{pdf_file}')
            docinfo = pdf.docinfo
            has_title=False
            for key, value in docinfo.items():
                if key == "/Title":
                    dest_file = sanitize_filename(f'{value}.pdf')
                    print(f'{OK} Rename {pdf_file} =>  {dest_file}')
                    if do_rename:
                        os.rename(f'{pdf_path}/{pdf_file}', f'{pdf_path}/{dest_file}')
                    has_title = True
                # print(key, ":", value)
            if has_title:
                print ('[OK ] Title Found')
            else:
                print (f'{bcolors.WARNING}[!!!] Title missing for {pdf_file}{bcolors.ENDC}')
    else:
        print (f"{bcolors.FAIL}[ERR] Nothing to do...{bcolors.ENDC}")