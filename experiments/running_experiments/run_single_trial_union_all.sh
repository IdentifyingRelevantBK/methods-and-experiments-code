cd ../methods/ &&
cp ../pharma/$1/$2/train/bk.pl bk_copy_1.pl &&
python3 methods.py --bk-file bk_copy_1.pl --bias-file-popper ../zendo/$1/$2/train/bias_orig.pl --bias-file-aleph ../zendo/$1/$2/train/bias_aleph.pl --bias-file-new ../zendo/$1/$2/train/bias.pl --examples-file ../zendo/$1/$2/train/exs.pl --method BC-union-all > ../zendo/$1/$2/bottom_clause.txt &&
cd ../pharma/ &&
python3 ../Popper/popper.py --stats --timeout 300 $1/$2/train/ > $1/$2/output.txt 2> $1/$2/debug.txt &&
cat $1/$2/output.txt | grep "pharma(A)" > $1/$2/solution.pl &&
cd ../testing/ &&
python3 hypothesis_testing.py ../pharma/$1/$2/solution.pl ../pharma/$1/$2/test/bk.pl ../pharma/$1/$2/test/exs.pl >> ../pharma/$1/$2/output.txt &&
cd ../pharma
cat $1/$2/output.txt
cat $1/$2/bottom_clause.txt | grep "Total time"
cat $1/$2/bottom_clause.txt | grep "Removed"

