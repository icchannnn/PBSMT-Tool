import nltk
from nltk import pos_tag
import subprocess

# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.data.path.append('/mnt/c/Users/itcha/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0/LocalCache/Roaming/nltk_data')

class PhraseBasedSMT:
    def __init__(self, parallel_corpus_path, monolingual_corpus_path):
        self.parallel_corpus_path = parallel_corpus_path
        self.monolingual_corpus_path = monolingual_corpus_path
        self.parallel_corpus = self.read_corpus(parallel_corpus_path)
        self.monolingual_corpus = self.read_corpus(monolingual_corpus_path)
        self.source_tokenized = [nltk.word_tokenize(sentence.lower()) for sentence in self.parallel_corpus]
        self.target_tokenized = [nltk.word_tokenize(sentence.lower()) for sentence in self.parallel_corpus]
        self.monolingual_tokenized = [nltk.word_tokenize(sent.lower()) for sent in self.monolingual_corpus]

        # Save the tokenized monolingual data to a text file
        self.save_tokenized_to_file()

        # Initialize components
        self.source_pos_tags = None
        self.target_pos_tags = None
        self.source_word_alignment = None
        self.phrase_table = None

    def read_corpus(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            corpus = [line.strip() for line in f]
        return corpus

    def save_tokenized_to_file(self):
        # Join the tokenized sentences into a single string
        tokenized_text = ' '.join([' '.join(sent) for sent in self.monolingual_tokenized])

        # Write the tokenized text to a file
        with open('/mnt/c/smt/pbsmt/monolingual_tokenized.txt', 'w', encoding='utf-8') as file:
            file.write(tokenized_text)

    def train(self):
        # Train the language model
        self.train_language_model()

        # Extract POS features
        self.extract_pos_features()

        # Perform word alignment
        self.word_alignment()

        # Extract phrases from word alignment
        self.extract_phrases()

    def train_language_model(self):
        # Train a language model using an external tool (e.g., KenLM)
        subprocess.call(f"/mnt/c/smt/pbsmt/ubuntu-16.04/bin/lmplz -o 3 < /mnt/c/smt/pbsmt/monolingual_tokenized.txt > /mnt/c/smt/pbsmt/language_model.arpa", shell=True)

        subprocess.call(f"/mnt/c/smt/pbsmt/ubuntu-16.04/bin/build_binary /mnt/c/smt/pbsmt/language_model.arpa /mnt/c/smt/pbsmt/language_eng.bin", shell=True)

    def extract_pos_features(self):
        # POS tagging for source and target sentences
        self.source_pos_tags = [pos_tag(sent) for sent in self.source_tokenized]
        self.target_pos_tags = [pos_tag(sent) for sent in self.target_tokenized]

    def word_alignment(self):
        # Use GIZA++ for word alignment
        # (Example command, adjust paths and parameters as needed)
        subprocess.call("/mnt/c/smt/pbsmt/tools/plain2snt.out corpus_fil.txt corpus_eng.txt", shell=True)

        subprocess.call("/mnt/c/smt/pbsmt/tools/snt2cooc.out corpus_fil.vcb corpus_eng.vcb corpus_fil_corpus_eng.snt > cooc.cooc", shell=True)

        subprocess.call("/mnt/c/smt/pbsmt/giza-pp/GIZA++-v2/GIZA++ -S corpus_fil.vcb -T corpus_eng.vcb -C corpus_fil_corpus_eng.snt -CoocurrenceFile cooc.cooc -output alignment -outputpath /mnt/c/smt/pbsmt/myout", shell=True)


        # Read the original alignment file
        with open('/mnt/c/smt/pbsmt/output', 'r') as f:
            lines = f.readlines()

        # Extract the alignment pairs and create the desired format
        alignment_pairs = []
        for line in lines:
            if line.startswith('Word Alignment:'):
                continue
            tokens = line.strip().split()
            alignment_pairs.extend(tokens)

        # Convert the list of alignment pairs to a string
        alignment_string = ' '.join(alignment_pairs)

        # Write the alignment string to a new file
        with open('/mnt/c/smt/pbsmt/alignment_output.txt', 'w') as f:
            f.write(alignment_string)


    def extract_phrases(self):
        # Extract phrases from word alignment
        self.phrase_table = self.extract_phrases_from_alignment(self.source_word_alignment)

    def extract_phrases_from_alignment(self, alignment):
        phrase_table = {}

        for line in alignment:
            source_index, target_index = map(int, line.split())

            # Extract source and target phrases
            source_phrase = self.extract_contiguous_phrase(self.source_tokenized, source_index)
            target_phrase = self.extract_contiguous_phrase(self.target_tokenized, target_index)

            # Store the mapping in the phrase table
            phrase_table[source_phrase] = target_phrase

        return phrase_table

    def extract_contiguous_phrase(self, tokens, start_index):
        # Find the end index of the contiguous phrase
        end_index = start_index
        while end_index < len(tokens) and tokens[end_index].isalpha():
            end_index += 1

        # Extract the contiguous phrase
        phrase = " ".join(tokens[start_index:end_index])

        return phrase

    def translate(self, source_sentence):
        # Tokenize the source sentence
        source_tokens = nltk.word_tokenize(source_sentence.lower())

        # Placeholder for translation logic
        translation = []

        # Iterate through source tokens and look up translations in the phrase table
        for i, source_token in enumerate(source_tokens):
            # Assume source_token is a phrase for simplicity (actual implementation would handle multi-word phrases)
            if source_token in self.phrase_table:
                translation.append(self.phrase_table[source_token])
            else:
                # If the token is not in the phrase table, use a fallback translation strategy
                # (e.g., use the token itself as a translation)
                translation.append(source_token)

        # Join the translated tokens to form the final translation
        translated_sentence = " ".join(translation)

        return translated_sentence

# Example usage:
parallel_corpus_path = "/mnt/c/smt/pbsmt/parallel_corpus.txt"
monolingual_corpus_path = "/mnt/c/smt/pbsmt/monolingual_corpus.txt"

smt_model = PhraseBasedSMT(parallel_corpus_path, monolingual_corpus_path)
smt_model.train()

# Translate a new sentence
new_filipino_sentence = "Isang kahig, isang tuka."
translated_sentence = smt_model.translate(new_filipino_sentence)

print("Input Sentence:", new_filipino_sentence)
print("Translated Sentence:", translated_sentence)
