import subprocess

# Step 1: Prepare your data - parallel corpus and monolingual corpus

# Filipino parallel corpus
subprocess.call("/mnt/c/smt/smt/mosesdecoder/scripts/tokenizer/tokenizer.perl -a -l en < /mnt/c/smt/smt/corpus/corpus_fil.txt > /mnt/c/smt/smt/corpus/corpus_tok.fil", shell=True)

# English parallel corpus
subprocess.call("/mnt/c/smt/smt/mosesdecoder/scripts/tokenizer/tokenizer.perl -a -l en < /mnt/c/smt/smt/corpus/corpus_eng.txt > /mnt/c/smt/smt/corpus/corpus_tok.eng", shell=True)

# Cleaning
subprocess.call("/mnt/c/smt/smt/mosesdecoder/scripts/training/clean-corpus-n.perl /mnt/c/smt/smt/corpus/corpus_tok fil eng /mnt/c/smt/smt/corpus/corpus.clean 1 22", shell=True)

# Building Language Model using KenLM
subprocess.call("/mnt/c/smt/smt/ubuntu-16.04/bin/lmplz -o 3 < /mnt/c/smt/smt/corpus/corpus_tok.eng > /mnt/c/smt/smt/corpus/corpus_arpa.eng", shell=True)

subprocess.call("/mnt/c/smt/smt/ubuntu-16.04/bin/build_binary /mnt/c/smt/smt/corpus/corpus_arpa.eng /mnt/c/smt/smt/corpus/corpus_blm.eng", shell=True)

# # Alignment
# subprocess.call("nohup nice /mnt/c/smt/smt/mosesdecoder/scripts/training/train-model.perl -root-dir train -corpus /mnt/c/smt/smt/corpus/corpus.clean -f fil -e eng -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:/mnt/c/smt/smt/corpus/corpus_blm.eng:8 -external-bin-dir /mnt/c/smt/smt/mosesdecoder/tools/ >& training.out & tail -f training.out",shell=True)

# # Translation
# subprocess.call("/mnt/c/smt/smt/mosesdecoder/tools/bin/moses -f /mnt/c/smt/smt/working/train/model/moses.ini")