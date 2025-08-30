from googletrans import Translator
from functools import lru_cache
import time

class TranslationProcessor:
    def __init__(self, target_lang='hi'):
        self.translator = Translator()
        self.target_lang = target_lang
        self.cache_timeout = 300  # 5 minutes
        self._cache = {}
        
    @lru_cache(maxsize=512)
    def _translate_cached(self, text, dest):
        try:
            result = self.translator.translate(text, dest=dest)
            return result.text
        except Exception:
            return text
            
    def _clean_cache(self):
        current_time = time.time()
        expired_keys = [k for k, (_, timestamp) in self._cache.items() 
                       if current_time - timestamp > self.cache_timeout]
        for key in expired_keys:
            del self._cache[key]
            
    def process(self, ocr_results):
        if not ocr_results:
            return []
            
        self._clean_cache()
        translated_results = []
        
        for result in ocr_results:
            text = result['text']
            cache_key = f"{text}_{self.target_lang}"
            
            # Check cache first
            if cache_key in self._cache:
                translated_text = self._cache[cache_key][0]
            else:
                translated_text = self._translate_cached(text, self.target_lang)
                self._cache[cache_key] = (translated_text, time.time())
                
            translated_results.append({
                'original': text,
                'translated': translated_text,
                'bbox': result['bbox'],
                'confidence': result['confidence']
            })
            
        return translated_results
