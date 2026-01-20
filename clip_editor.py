from moviepy import *
from helpers import *
from effects.text_watermark import TextWatermarkParamaters, TextWatermarkEffect
from effects.image_watermark import ImageWatermarkParamaters, ImageWatermarkEffect
import datetime
import math
"""
PATTERN FOR ANY CLIP METHODS:
1: CALL self.clip, as that is the VideoFileClip itself to be edited (NOT self, which is the ClipEditor object used to edit the base clip).
2: IF ITS BEING EDITED, USE self.clip = self.clip.{EDITING_METHOD}
3: RETURN SELF
"""

class ClipEditor:
    def __init__(self, base_clip_filename_or_base_clip):
        """
        :param base_clip_filename_or_base_clip: Takes in either a path of a video or an existing VideoFileClip object to be edited.
        """
      #Initializes the directories, then creates them if they dont already exist.
        self.base_dir = Path(__file__).resolve().parent #Directory where the script is located
        self.resource_dir = self.base_dir / "resources" #Directory where resources (ie: input videos, watermark fonts), go.
        self.image_dir = self.resource_dir / "images"
        self.font_dir = self.resource_dir / "fonts" #Directory where fonts for watermarks go
        self.input_dir = self.resource_dir / "inputs" #Directory where videos to be edited go
        self.output_dir = self.base_dir / "outputs" #Directory where the edited videos go to.

        self.ensure_dirs(self.resource_dir, self.image_dir, self.input_dir, self.font_dir, self.output_dir) #Makes directories
        #Declaring input path

        if isinstance(base_clip_filename_or_base_clip, VideoFileClip):
            self.base_clip_path = None
            self.base_clip = base_clip_filename_or_base_clip
        else:
            self.base_clip_path = resolve_path(base_clip_filename_or_base_clip, base_dir=self.input_dir)
            self.base_clip = VideoFileClip(
                str(self.base_clip_path)
            )  # Path works, but some weird bugs can occur on Windows with path vs string.
            if not self.base_clip_path.exists():
                raise FileNotFoundError(self.base_clip_path)

        self.clip = self.base_clip #Defining the clip object that is to be mutated over time to not cause bugs with changing duration and time of the clip.

        #Declaring output path
        self.output_clip_filename =  f"{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}_{base_clip_filename_or_base_clip}"
        self.output_clip = resolve_path(self.output_clip_filename, base_dir=self.output_dir)





    def get_clip_duration(self, base_clip=False):
        return self.base_clip.duration if base_clip else self.clip.duration

    def ensure_dirs(self, *dirs: Path | str):
        """
        Creates directories with the desired paths given.
        :param dirs: Paths to be passed through for desired directories
        """
        for d in dirs:
            d.mkdir(exist_ok=True)

    def apply(self, effect: Effect):
        """
        Takes in any of the above effects and applies it to the clip. Wrapper method used to make it easier versus just calling the creation methods itself.
        """
        return effect.apply(self)

    def speed(self, multiplier:float):
        """
        Uses the clip_speed method in helpers.py
        :param multiplier: Multiplier in how fast (or slow) the edited clip should be. >1: Speeds up. <1: Slows down. Must be greater than 0.
        :return: the clip, sped or slowed by the given multiplier
        """
        self.clip = clip_speed(self.clip, multiplier)
        return self

    def preview(self):
        """
        Calls the preview() method of MoviePy clips.
        :return: Preview of the clip.
        """
        self.clip.preview()

    def save(self, filename=None):
        if filename is None:
            self.clip.write_videofile(self.output_clip) #Default name for output
        else:
            self.clip.write_videofile(str(resolve_path(filename, base_dir=self.output_dir)))#If a filename is given, use this instead for saving.

    def crop(self, begin_time, end_time): #Crops the given clip from begin time to end time
        """
        :param begin_time: Time(in seconds) where the cropping begins
        :param end_time: Time(in seconds) where the cropping ends
        :return: Base clip with the desired crop
        """
        self.clip = self.clip.subclipped(begin_time, end_time)
        return self
    def concatenate(self,clip_to_concat):
        """
        :param clip_to_concat: Clip or ClipEditor to append to the end of the input clip. If a ClipEditor object is passed, it will take its clip attribute and set that as the clip to be concatenated.
        :return: Clip with self and clip_to_concat at the end.
        """
        #If a ClipEditor is passed instead of a Clip
        if hasattr(clip_to_concat, "clip"):
            clip_to_concat = clip_to_concat.clip
        #Concatenates the two clips together.
        self.clip = concatenate_videoclips([self.clip, clip_to_concat], method="compose")
        return self

    def duplicate(self):
        """
        :return: Creates a copy of the clip into a new ClipEditor object.
        """
        return ClipEditor(self.clip.copy())



