import subprocess

# Step 1: Prepare your data - parallel corpus and monolingual corpus

# Assuming you have parallel corpora and monolingual corpora files in the following format:
parallel_corpus = [
    ("Ikaw", "You"),
    ("At", "And"),
    # Add more pairs
]

# Create parallel corpus files
with open("corpus.fil", "w", encoding="utf-8") as fil_corpus, open("corpus.eng", "w", encoding="utf-8") as eng_corpus:
    for filipino, english in parallel_corpus:
        fil_corpus.write(filipino + "\n")
        eng_corpus.write(english + "\n")

# Create monolingual English corpus file
# Assuming you have a list of English sentences in the following format:
english_corpus = [
    "You",
    "And",
    # Add more sentences
]

with open("corpus.eng.monolingual", "w", encoding="utf-8") as eng_monolingual_corpus:
    for sentence in english_corpus:
        eng_monolingual_corpus.write(sentence + "\n")

# Step 2: Tokenization and Preprocessing using Moses Tokenizer

# Tokenize parallel corpus using Moses tokenizer
subprocess.call("/mnt/c/smt/smt/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en -no-escape < corpus.eng > corpus.eng.tok", shell=True)

# subprocess.call(["/mnt/c/smt/smt/mosesdecoder/scripts/tokenizer/tokenizer.perl", "-l", "en", "-no-escape", "<", "/mnt/c/smt/smt/corpus.eng", ">", "/mnt/c/smt/smt/corpus.eng.tok"])

# Tokenize English monolingual corpus using Moses tokenizer
# subprocess.call(["/mnt/c/smt/smt/mosesdecoder/scripts/tokenizer/tokenizer.perl", "-l", "en", "-no-escape", "<", "/mnt/c/smt/smt/corpus.eng.monolingual", ">", "/mnt/c/smt/smt/corpus.eng.monolingual.tok"])

# Step 3: Alignment with Giza++

# Assuming you've already installed Giza++

# Perform word alignment for both directions (Filipino to English and vice versa)
subprocess.call(["/mnt/c/smt/smt/giza-pp/GIZA++-v2/plain2snt.out", "corpus.fil", "corpus.eng"])
subprocess.call(["/mnt/c/smt/smt/giza-pp/GIZA++-v2/plain2snt.out", "corpus.eng", "corpus.fil"])

# Run GIZA++ for word alignment
subprocess.call(["/mnt/c/smt/smt/mosesdecoder/tools/snt2cooc.out", "-snt", "corpus.fil-eng.snt", "-coocurrence-fil", "corpus.fil-eng.coocurrence"])
subprocess.call(["/mnt/c/smt/smt/mosesdecoder/tools/snt2cooc.out", "-snt", "corpus.eng-fil.snt", "-coocurrence-fil", "corpus.eng-fil.coocurrence"])

subprocess.call(["/mnt/c/smt/smt/giza-pp/GIZA++-v2/GIZA++", "-S", "corpus.fil-eng.coocurrence", "-T", "corpus.fil-eng.coocurrence", "-C", "corpus.fil-eng.snt", "-o", "alignment", "-outputpath", "."])
subprocess.call(["/mnt/c/smt/smt/giza-pp/GIZA++-v2/GIZA++", "-S", "corpus.eng-fil.coocurrence", "-T", "corpus.eng-fil.coocurrence", "-C", "corpus.eng-fil.snt", "-o", "alignment", "-outputpath", "."])

# Step 4: Create Phrase Table with Moses

# Create a working directory for Moses
subprocess.call(["mkdir", "-p", "working_dir"])

# Create the phrase table for both directions
subprocess.call(["/mnt/c/smt/smt/mosesdecoder/scripts/training/train-model.perl", "-root-dir", "working_dir", "-corpus", "corpus", "-e", "en", "-e", "en", "-alignment", "alignment", "-reordering", "msd-bidirectional-fe", "-lm", "0:5:/mnt/c/smt/smt/giza-pp/GIZA++-v2/", "-external-bin-dir", "/mnt/c/smt/smt/mosesdecoder/tools"])
# subprocess.call(["/mnt/c/smt/smt/mosesdecoder/scripts/training/train-model.perl", "-root-dir", "working_dir", "-corpus", "corpus", "-f", "eng", "-e", "fil", "-alignment", "alignment", "-reordering", "msd-bidirectional-fe", "-lm", "0:5:/mnt/c/smt/smt/giza-pp/GIZA++-v2", "-external-bin-dir", "/mnt/c/smt/smt/mosesdecoder/tools"])

# # Step 5: Translation
 
# # Translate a Filipino idiom to English
# translate_command = ["D:/smt/moses/bin/moses", "-f", "working_dir/model/moses.ini"]
# with open("input.txt", "r", encoding="utf-8") as input_file:
#     with open("output.txt", "w", encoding="utf-8") as output_file:
#         subprocess.call(translate_command, stdin=input_file, stdout=output_file)

