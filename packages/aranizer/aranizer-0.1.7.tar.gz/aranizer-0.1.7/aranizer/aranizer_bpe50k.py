import pkg_resources
from transformers import PreTrainedTokenizerFast

def get_tokenizer():
    tokenizer_file = pkg_resources.resource_filename(
        'aranizer', 'BPE_tokenizer/BPE_tokenizer_50.0K.json')
    return PreTrainedTokenizerFast(tokenizer_file=tokenizer_file)
