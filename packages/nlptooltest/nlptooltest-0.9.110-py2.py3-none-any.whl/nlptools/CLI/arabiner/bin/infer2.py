import os
import csv
from nlptools.utils.sentence_tokenizer import sent_tokenize
from nlptools.morphology.tokenizers_words import simple_word_tokenize
import pandas as pd

"""
CSV NER Tagging Tool

Usage:
------
Run the script with the following command:

arabi_ner2  input.csv --text-columns "TextColumn1,TextColumn2" --additional-columns "Column3,Column4" --output-csv output.csv
"""

import argparse
import pandas as pd
from nlptools.utils.sentence_tokenizer import sent_tokenize
from nlptools.morphology.tokenizers_words import simple_word_tokenize
from nlptools.arabiner.bin.infer import ner

def infer(sentence):
    output = ner(sentence)
    return [word[1] for word in output]



def corpus_tokenizer_keep_columns(row_id, global_sentence_id, input_csv, output_csv, text_column, fieldnames):

    df = pd.read_csv(input_csv)
    result = df.drop_duplicates(subset=['sentence_id', text_column])[text_column]

    row_id = row_id - 1
    global_sentence_id = global_sentence_id - 1
    fieldnames = ['Row_ID', 'Docs_Sentence_Word_ID', 'Global Sentence ID', 'Sentence ID', 'Sentence', 'Word Position', 'Word', 'Ner tags']
        
    
    with open(output_csv, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in result:  
            sentences = sent_tokenize(row, dot=True, new_line=True, question_mark=False, exclamation_mark=False)
            for sentence_id, sentence in enumerate(sentences, start=1):
                words = simple_word_tokenize(sentence)
                tags = infer(sentence) 
                global_sentence_id += 1
                for word_pos, word in enumerate(words, start=1):
                    row_id += 1
                    doc_sentence_filename = input_csv.split(".csv")[0]
                    docs_sentence_word_id = f"{doc_sentence_filename}_{global_sentence_id}_{sentence_id}_{word_pos}"
    
                    writer.writerow({'Row_ID': row_id,
                                     'Docs_Sentence_Word_ID': docs_sentence_word_id,
                                     'Global Sentence ID': global_sentence_id,
                                     'Sentence ID': sentence_id,
                                     'Sentence': sentence,
                                     'Word Position': word_pos,
                                     'Word': word,
                                     'Ner tags':tags[word_pos-1]})        


    df_input = pd.read_csv(input_csv)
    df_output = pd.read_csv(output_csv)
    
    
    # Concatenate along columns (horizontally)
    result = pd.concat([df_input, df_output], axis=1)
    
    # Write the DataFrame to a CSV file
    result.to_csv(output_csv, index=False)




def main():
    parser = argparse.ArgumentParser(description="CSV NER Tagging Tool")
    parser.add_argument("--row_id", help="Path to the input CSV file")
    parser.add_argument("--global_sentence_id", help="Path to the input CSV file")
    parser.add_argument("--input_csv", help="Path to the input CSV file")
    parser.add_argument("--text_column", required=True,
                        help="Column index in the CSV file to apply NER tagging")
    parser.add_argument("--additional_columns", nargs='*', default=[],
                        help="Additional column indexes to retain in the output seperated by , ")
    parser.add_argument("--output_csv", default="output.csv",
                        help="Path to the output CSV file")

    args = parser.parse_args()
    corpus_tokenizer_keep_columns(int(args.row_id), int(args.global_sentence_id), args.input_csv, args.output_csv, args.text_column, args.additional_columns)

# arabi_ner2 --row_id "1" --global_sentence_id "1" --input_csv "Algi_Sheet1.csv" --text_column "sentence" --additional_columns "sentence id,domain,url,year,# of words" --output_csv "output_csv.csv"
if __name__ == "__main__":
    main()



