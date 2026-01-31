from clip_editor import ClipEditor
from effects.text_watermark import TextWatermarkParamaters, TextWatermarkEffect
from effects.image_watermark import ImageWatermarkParamaters, ImageWatermarkEffect
from helpers import *

def testing_text_time(): #Demonstration with relative path.
    fox = ClipEditor("video_2025-05-25_02-02-44.mp4")
    fox_params = TextWatermarkParamaters("Cute boy", end_time = 3)
    fox_image = ImageWatermarkParamaters("E:\Pictures/500px-Fisheyejak_original.jpg", position=("right","top"))
    fox.apply(TextWatermarkEffect(fox_params))
    fox.apply(ImageWatermarkEffect(fox_image))
    fox.preview()

#testing_text_time()

def FAFO(): #Demonstration with absolute path for ClipEditor
    FAFO = ClipEditor("E:\PICTURES\FAFO.mp4").crop(12,17)
    FAFO_half = FAFO.duplicate().speed(.5)
    FAFO.concatenate(FAFO_half)
    FAFO.preview()



def controlled_op():
    COP = ClipEditor("E:\Documents\Pixel 6 FTP\Christian Controlled Op Cope on Instagram _ Know More News w_ Adam Green.mp4")
    FOCUS = COP.crop(begin_time=time_stamp(minutes=22, seconds=10),end_time=time_stamp(minutes=25, seconds=35))
    #FOCUS_2 = COP.duplicate()
    FOCUS.save(filename="ericmoutsos_stealing_from_adam_green.mp4")
controlled_op()