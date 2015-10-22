from ngram import NGram
from db import DB

ngrams = NGram()
mydb = DB()

ngrams.input_data(mydb)
ngrams.get_synonym_list('take')

# ngrams.num_abbreviations(mydb)
