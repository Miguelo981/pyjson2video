import platform

drivers = { "Linux": "espeak", "Darwin": "nsss", "Windows": "sapi5" }

def voice_driver_by_os():
    return drivers[platform.system()]

def use_lang(short_lang, long_lang):
    if platform.system() == 'Linux':
        return long_lang
    elif platform.system() == 'Windows':
        return short_lang
    elif platform.system() == 'Darwin':
        pass