from dataclasses import dataclass
from moviepy import *
import math
from helpers import resolve_clip_time, resolve_path

@dataclass(frozen=True) #Now using dataclasses for paramaters instead of passing in method.
class ImageWatermarkParamaters:
    """
    :param image_name Filename of the image
    """
    image_name: str #Filename of the image
    size: tuple | tuple[str, str] | None = None
    position: tuple[str, str] | str | tuple[int, int] = ("center", "center")

    opacity: float = 1.0
    rotation_speed: float = 0.0
    rotation_phase: float = 0.0

    begin_time: float = 0
    end_time: float = None
    watermark_duration: float = None


class ImageWatermarkEffect(Effect):
    def __init__(self, params: ImageWatermarkParamaters):
        self.params = params

    def apply(self, editor):
        # Gets the path of the image to use to create the watermark.
        image_path = resolve_path(self.params.image_name, editor.image_dir)
        begin_time, duration = resolve_clip_time(editor.clip.duration, self.params.begin_time, self.params.end_time, self.params.watermark_duration)


        image_watermark = (
            ImageClip(image_path)
            .with_duration(editor.clip.duration)
            .with_position(self.params.position)
            .with_opacity(self.params.opacity)
        )
        image_watermark = image_watermark.with_start(begin_time).with_duration(duration)
        if self.params.size is not None: #If a size is given, resize the watermark to fit that.
            image_watermark = image_watermark.resized(self.params.size)

        if self.params.rotation_phase != 0 or self.params.rotation_speed != 0:
            image_watermark = image_watermark.rotated(lambda t: (self.params.rotation_speed * t) + self.params.rotation_phase)

        editor.clip = CompositeVideoClip(
            [editor.clip, image_watermark],
            size = editor.clip.size
        )
        return editor

