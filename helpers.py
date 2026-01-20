from pathlib import Path
from moviepy import *
def time_stamp(seconds: float|int, minutes:float|int =0 , hours:float|int =0,
               miliseconds:float|int=0) -> float:
    """

    :param seconds: Time in seconds (float or int)
    :param minutes: Time in minutes (float or int)
    :param hours: Time in hours (float or int)
    :param miliseconds: Time in milliseconds (float or int)
    :return: Given time in seconds (float)
    """
    # Takes in time units and outputs a time in seconds for ease of use.
    return (seconds) + (minutes * 60) + (hours * 3600) + (miliseconds / 1000)


def resolve_path(file_path: str | Path, base_dir:Path=None)-> Path: #Take in either absolute (within PC) or relative (in resources directory in script) paths for resources.
    """
    :param file_path: The path of the file desired to be used, either absolute or relative.
    :param base_dir: Base directory of the file itself. Defaults to None, primarily used if the path will be absolute
    :return: The directory of the file as a Path object.
    """
    path_to_process = Path(file_path)
    return path_to_process if path_to_process.is_absolute() else base_dir / path_to_process

def clip_speed(clip, speed_multiplier:float):
    """
    :param clip: Base clip to be sped up or slowed down
    :param speed_multiplier: How much faster or slower clip is desired to be. If >1.0, speeds up. If <1.0, slows down. Must be positive.
    :return: clip edited with audio and video adjusted with the multiplier.
    """
    if speed_multiplier <=0:
        raise ValueError("Speed must be positive.")
    clip = clip.time_transform(lambda t: t * speed_multiplier).with_duration(clip.duration / speed_multiplier)
    if clip.audio: #If the clip has audio, also apply the multiplier to it.
        clip = clip.with_audio(
            clip.audio.time_transform(lambda t: t * speed_multiplier).with_duration(clip.duration)
        )
    return clip

def resolve_clip_time(base_clip_duration, begin_time=0, end_time=None, desired_duration=None):
    """

    :param base_clip_duration: The duration of the base clip to be analyzed; intened to be a self.clip.duratiion for MoviePy Clip clases
    :param begin_time: Desired begin time for clip: Default to 0 seconds
    :param end_time: Desired end time for clip: Default to None; Mutually exclusive with desired_duration
    :param desired_duration: Desired duration of clip, relative to begin_time: Default to None; mutually exclusive with end_time
    :return: Floats for the begin time, and the interval desired for clip.
    """
    if begin_time < 0:
        raise ValueError("Begin time of clip cannot be negative.")
    # If both end time and duration are provided in dataclass
    if end_time is not None and desired_duration is not None:
        raise ValueError("Cannot have both end time and duration paramaters at the same time")
    # If watermark duration is provided:
    elif desired_duration is not None:
        duration = desired_duration
        if begin_time + duration > base_clip_duration:
            raise ValueError("Duration of watermark cannot be longer than the duration of the clip being edited.")

    else: # With end time
        end_time = end_time if end_time is not None else base_clip_duration #Checks if there is a value for end_time. If None, assumes the duration of the base clip to be the end time.
        if begin_time > end_time:
            raise ValueError("Begin time cannot be greater than end time")
        else:
            duration = end_time - begin_time
    if duration <=0:
        raise ValueError("Duration must be positive")
    return begin_time, duration