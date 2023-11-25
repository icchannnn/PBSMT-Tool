/mnt/c/smt/pbsmt/tools/plain2snt.out '/mnt/c/smt/pbsmt/corpus/Source.txt' '/mnt/c/smt/pbsmt/corpus/Target.txt' 

/mnt/c/smt/pbsmt/tools/mkcls -p'/mnt/c/smt/pbsmt/corpus/Source.txt' -V'/mnt/c/smt/pbsmt/corpus/Source.vcb.classes'

/mnt/c/smt/pbsmt/tools/mkcls -p'/mnt/c/smt/pbsmt/corpus/Target.txt' -V'/mnt/c/smt/pbsmt/corpus/Target.vcb.classes'

/mnt/c/smt/pbsmt/tools/snt2cooc.out '/mnt/c/smt/pbsmt/corpus/Source.vcb' '/mnt/c/smt/pbsmt/corpus/Target.vcb' '/mnt/c/smt/pbsmt/corpus/Source_Target.snt' > 'Source_Target.cooc'

/mnt/c/smt/pbsmt/tools/GIZA++ -S /'mnt/c/smt/pbsmt/corpus/Source.vcb' -T '/mnt/c/smt/pbsmt/corpus/Target.vcb' -C '/mnt/c/smt/pbsmt/corpus/Source_Target.snt' -CoocurrenceFile '/mnt/c/smt/pbsmt/Source_Target.cooc' -o Result -outputpath ''