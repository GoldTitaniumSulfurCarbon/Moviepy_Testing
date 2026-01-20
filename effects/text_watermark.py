from dataclasses import dataclass
from moviepy import *
import math
from helpers import resolve_clip_time, resolve_path
@dataclass(frozen=True)
class TextWatermarkParamaters:
    watermark_text: str
    text_color: str = "white"
    text_size: int = 64
    font: str = None
    position: tuple[str, str] | str | tuple[int, int] = ("center", "center")
    opacity: float = 1.0
    rotation_speed: float = 0.0
    rotation_phase: float = 0.0

    begin_time: float = 0 #When the clip begins
    end_time: float = None #When the clip ends, if not given a duration; cannot be used at same time as clip_duration
    watermark_duration: float = None #How long the clip lasts, if not given an end time. cannot be used at same time as end_time

class TextWatermarkEffect(Effect):
    def __init__(self, params: TextWatermarkParamaters):
        """
        :param params: Paramaters passed from TextWatermarkParamaters dataclass object.
        """
        self.params = params

    def apply(self, editor: "ClipEditor"):
        """
        :param editor: ClipEditor object to apply the effect to the clip
        :return: ClipEditor object passed through editor with the desired text effects applied.
        """
        # Using Pythagorean Theorem to create an area for the text to rotate without clipping, used in the clip_size argument for the watermark constructor.
        length, width = editor.clip.size
        diagonal = int(math.hypot(length, width))
        clip_size = (diagonal, diagonal)
        # Setting the font type. If the font is None, TextClip constructor will ignore it.
        if self.params.font is not None:
            font_path = resolve_path(self.params.font, base_dir=editor.font_dir)
            if not font_path.exists():
                raise FileNotFoundError(f"Font not found: {font_path}")
        else:
            font_path = None

        # Logic for determining the duration:
        # 3 main cases. No duration/interval specified, Begin time and end time, Begin time and duration,.
        begin_time, duration = resolve_clip_time(editor.clip.duration, self.params.begin_time, self.params.end_time,
                                                 self.params.watermark_duration)
        watermark = (
            TextClip(
                text=self.params.watermark_text,
                font_size=self.params.text_size,
                font=font_path,
                color=self.params.text_color,
                size=clip_size
            )
            .with_position(self.params.position)
            .with_opacity(self.params.opacity)
        )
        watermark = watermark.with_start(begin_time).with_duration(duration)

        if self.params.rotation_phase != 0 or self.params.rotation_speed != 0:  # Making it run faster if there is no rotation at all.
            watermark = watermark.rotated(lambda t: (self.params.rotation_speed * t) + self.params.rotation_phase)

        editor.clip = CompositeVideoClip(
            [editor.clip, watermark],
            size=editor.clip.size
        )
        return editor