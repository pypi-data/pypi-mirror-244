from transformers import PreTrainedTokenizerFast

def get_tokenizer():
    return PreTrainedTokenizerFast(tokenizer_file="./BPE_tokenizer/BPE_tokenizer_32.0K.json")
