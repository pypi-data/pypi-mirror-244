
from transformers import PreTrainedTokenizerFast

def get_tokenizer():
    return PreTrainedTokenizerFast(tokenizer_file="./sentence peice tokenizers/SP_tokenizer_86.0K.json")


