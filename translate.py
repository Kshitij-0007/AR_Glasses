from googletrans import Translator
from functools import lru_cache

translator = Translator()

@lru_cache(maxsize=1024)
def translate_text(text, dest='hi'):
    # dest default is Hindi for example; change as needed
    if not text:
        return ''
    try:
        res = translator.translate(text, dest=dest)
        return res.text
    except Exception as e:
        # On API/network failure, return original text
        return text
