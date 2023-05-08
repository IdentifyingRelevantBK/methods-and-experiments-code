python3 ../Popper/popper.py --stats --timeout 600 $1/$2/train/ > $1/$2/output.txt 2> $1/$2/debug.txt &&
cat $1/$2/output.txt | grep "pharma(A)" > $1/$2/solution.pl &&
cd ../testing/ &&
python3 hypothesis_testing.py ../pharma/$1/$2/solution.pl ../pharma/$1/$2/test/bk.pl ../pharma/$1/$2/test/exs.pl >> ../pharma/$1/$2/output.txt &&
cd ../pharma
cat $1/$2/output.txt 
