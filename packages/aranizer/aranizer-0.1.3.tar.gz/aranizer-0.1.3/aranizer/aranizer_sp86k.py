
from transformers import PreTrainedTokenizerFast

def get_tokenizer():
    return PreTrainedTokenizerFast(tokenizer_file="aranizer/sentence_peice_tokenizers/SP_tokenizer_86.0K.json")


