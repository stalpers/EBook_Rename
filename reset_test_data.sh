#!/bin/bash

export PROJECT=.
export ORG_EPUB=$PROJECT/org/books
export ORG_PDF=$PROJECT/org/pdf
export TEST_PDF=$PROJECT/pdf
export TEST_EPUB=$PROJECT/books

echo "* Cleaning epub directory - $TEST_EPUB"
rm $TEST_EPUB/*.epub
echo "* Cleaning pdf directoy - $TEST_PDF"
rm $TEST_PDF/*.pdf
echo "* Copying epub test files - $ORG_EPUB"
cp $ORG_EPUB/*.epub $TEST_EPUB/
echo "* Copying PDF testfiles - $ORG_PDF"
cp $ORG_PDF/*.pdf $TEST_PDF/

echo "*** DONE"
