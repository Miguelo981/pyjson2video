import math, os, random, string, numpy

from PIL import Image, ImageFilter
from moviepy.video.fx.resize import resize
from conf import IMAGE_EXPORTS_PATH


def drop_shadow(image, iterations=3, border=8, offset=(5,5), background_colour=0xffffff, shadow_colour=0x444444):
    shadow_width = image.size[0] + abs(offset[0]) + 2 * border
    shadow_height = image.size[1] + abs(offset[1]) + 2 * border

    shadow = Image.new(image.mode, (shadow_width, shadow_height), background_colour)

    shadow_left = border + max(offset[0], 0)
    shadow_top = border + max(offset[1], 0)
    shadow.paste(shadow_colour, [shadow_left, shadow_top, shadow_left + image.size[0], shadow_top + image.size[1]])

    for i in range(iterations):
        shadow = shadow.filter(ImageFilter.BLUR)

    img_left = border - min(offset[0], 0)
    img_top = border - min(offset[1], 0)
    shadow.paste(image, (img_left, img_top))

    return shadow

def prepare_image(route):
    shadowed_img = drop_shadow(route)
    shadowed_img_route = os.path.join(IMAGE_EXPORTS_PATH, ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9)) + '.png')
    shadowed_img.save(shadowed_img_route)

    return shadowed_img_route

def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)

        result = numpy.array(img)
        img.close()

        return result

    return clip.fl(effect)

def resize_zoomin_func(clip, ratio=0.04):
    clip = resize(clip, lambda t: 1 + ratio * t)
    return clip

def resize_zoomout_func(clip, duration, ratio=0.04):
    clip = resize(clip, lambda t: 1 + ratio * (duration-t))
    return clip