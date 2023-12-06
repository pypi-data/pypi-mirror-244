#!/usr/bin/bash

sphinx-apidoc -f -o source/ ../ananke --templatedir templates/
#make html
pandoc ../CHANGELOG.md --from markdown --to rst -s -o source/changelog.rst
python3 -m sphinx source/ build/
