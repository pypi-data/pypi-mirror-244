import pkg_resources
from transformers import PreTrainedTokenizerFast

def get_tokenizer():
    tokenizer_file = pkg_resources.resource_filename(
        'aranizer', 'sentence_peice_tokenizers/SP_tokenizer_32.0K.json')
    return PreTrainedTokenizerFast(tokenizer_file=tokenizer_file)
