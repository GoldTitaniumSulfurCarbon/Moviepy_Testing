from clip_editor import ClipEditor
from effects.text_watermark import TextWatermarkParamaters, TextWatermarkEffect
from effects.image_watermark import ImageWatermarkParamaters, ImageWatermarkEffect


def testing_text_time(): #Testing if each of the 6 scenarios I want do in fact work.
    fox = ClipEditor("video_2025-05-25_02-02-44.mp4")
    fox_params = TextWatermarkParamaters("Cute boy", end_time = 3)
    fox_image = ImageWatermarkParamaters("E:\Pictures/500px-Fisheyejak_original.jpg", position=("right","top"))
    fox.apply(TextWatermarkEffect(fox_params))
    fox.apply(ImageWatermarkEffect(fox_image))
    fox.preview()

#testing_text_time()

def FAFO():
    FAFO = ClipEditor("E:\PICTURES\libtard_FAFO.mp4").crop(12,17)
    FAFO_half = FAFO.duplicate().speed(.5)
    FAFO.concatenate(FAFO_half)


    FAFO.preview()
FAFO()
