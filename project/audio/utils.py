import platform

drivers = { "Linux": "espeak", "Darwin": "nsss", "Windows": "sapi5" }

def voice_driver_by_os():
    return drivers[platform.system()]