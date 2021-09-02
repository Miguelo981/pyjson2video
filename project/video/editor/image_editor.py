from moviepy.video.VideoClip import TextClip

def create_text_clip(text_content, size):
    txt_clip = TextClip(text_content, fontsize=size, color='white', align='West', size=(1280, size), stroke_color='black', stroke_width=5)
    txt_clip = txt_clip.set_fps(30).set_position(("center"))
    return txt_clip