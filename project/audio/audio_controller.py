from pydub import AudioSegment


def change_volume(media, volume):
    return media + volume

def overlay_media(media1, media2):
    return media1.overlay(media2, position=0)

def import_media(file_route, format = "wav"):
    return AudioSegment.from_file(file_route, format=format)

def export_media(media, file_name, format="wav"):
    media.export(file_name, format=format)
