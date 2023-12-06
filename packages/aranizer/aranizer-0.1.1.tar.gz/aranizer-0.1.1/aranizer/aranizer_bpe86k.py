# tokenizer_fast1.py
from transformers import PreTrainedTokenizerFast

def get_tokenizer():
    return PreTrainedTokenizerFast(tokenizer_file="./BPE_tokenizer/BPE_tokenizer_86.0K.json")
