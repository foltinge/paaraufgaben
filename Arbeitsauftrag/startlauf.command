#! /bin/zsh
mydir=${0:a:h}
cd $mydir
pwd

python3 paaraufgaben.py
lualatex auftraege.tex
lualatex ergebnisse.tex
pdfjam --nup 1x2 auftraege.pdf --outfile auftraege2.pdf
cp auftraege.pdf /Volumes/FOLTIN_USB/AAA_Kopien/.
cp auftraege2.pdf /Volumes/FOLTIN_USB/AAA_Kopien/.
cp ergebnisse.pdf /Volumes/FOLTIN_USB/AAA_Kopien/.
