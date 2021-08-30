import os

def change_volume(media, volume):
    return media + volume

def join_media(media1, media2):
    return media1 + media2

def overlay_media(media1, media2):
    return media1.overlay(media2, position=0)

def export_media(media, file_name, format = "wav"):
    media.export(file_name, format=format)

def get_audio_duration(audio_route):
    f = open(audio_route, encoding = 'cp850')

    f.seek(28)
    a = f.read(4)

    byteRate = 0
    for i in range(4):
        byteRate = byteRate + ord(a[i]) * pow(256, i)

    fileSize = os.path.getsize(audio_route)
    f.close()

    return ((fileSize - 44) * 1000) / byteRate
