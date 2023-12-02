import logging
from multiprocessing import Pool
from pathlib import Path
from typing import Callable, Sequence

import cv2
import h5py
import numpy as np

from idtrackerai import Blob
from idtrackerai.utils import Episode, remove_file, track


def segment_episode(
    inputs: tuple[Episode, list[Path], dict, Path]
) -> tuple[list[list[Blob]], Episode]:
    """Gets list of blobs segmented in every frame of the episode of the video
    given by `path` (if the video is splitted in different files) or by
    `episode_start_end_frames` (if the video is given in a single file)

    Parameters
    ----------
    session : <Session object>
        Object collecting all the parameters of the video and paths for saving and loading
    segmentation_thresholds : dict
        Dictionary with the thresholds used for the segmentation: `min_threshold`,
        `max_threshold`, `min_area`, `max_area`
    path : string
        Path to the video file from where to get the VideoCapture (OpenCV) object
    episode_start_end_frames : tuple
        Tuple (starting_frame, ending_frame) indicanting the start and end of the episode
        when the video is given in a single file

    Returns
    -------
    blobs_in_episode : list
        List of `blobs_in_frame` of the episode of the video being segmented
    """
    episode, video_paths, segmentation_parameters, segmentation_data_folder = inputs
    # Set file path to store blobs segmentation image and blobs pixels
    bbox_images_path = segmentation_data_folder / f"episode_images_{episode.index}.hdf5"
    remove_file(bbox_images_path)

    # Read video for the episode
    video_path = video_paths[episode.video_path_index]
    cap = cv2.VideoCapture(str(video_path))

    # Get the video on the starting position
    cap.set(1, episode.local_start)

    blobs_in_episode = []
    for frame_number_in_video_path, global_frame_number in zip(
        range(episode.local_start, episode.local_end),
        range(episode.global_start, episode.global_end),
    ):
        ret, frame = cap.read()
        if ret:
            blobs_in_frame = get_blobs_in_frame(
                frame, segmentation_parameters, global_frame_number, bbox_images_path
            )
        else:
            logging.error(
                "OpenCV could not read frame "
                f"{frame_number_in_video_path} of {video_path}"
            )
            blobs_in_frame = []

        # store all the blobs encountered in the episode
        blobs_in_episode.append(blobs_in_frame)

    cap.release()
    return blobs_in_episode, episode


def get_blobs_in_frame(
    frame: np.ndarray,
    segmentation_parameters: dict,
    global_frame_number: int,
    bbox_images_path: Path,
) -> list[Blob]:
    """Segments a frame read from `cap` according to the preprocessing parameters
    in `video`. Returns a list `blobs_in_frame` with the Blob objects in the frame
    and the `max_number_of_blobs` found in the video so far. Frames are segmented
    in gray scale.

    Parameters
    ----------
    segmentation_thresholds : dict
        Dictionary with the thresholds used for the segmentation: `min_threshold`,
        `max_threshold`, `min_area`, `max_area`
    global_frame_number : int
        This is the frame number in the whole video. It will be different to the frame_number
        if the video is chuncked.


    Returns
    -------
    blobs_in_frame : list
        List of <Blob object> segmented in the current frame
    """

    intensity_ths = segmentation_parameters["intensity_ths"]
    if segmentation_parameters["bkg_model"] is not None and intensity_ths[0] == 0:
        # versions < 5.2.5 used intensity ths with background as (0, value)
        # now we use (value, 255)
        segmentation_parameters["intensity_ths"] = (intensity_ths[1], 255)

    _, contours, frame = process_frame(frame, **segmentation_parameters)

    blobs_in_frame: list[Blob] = []
    with h5py.File(bbox_images_path, "a") as file:
        for i, contour in enumerate(contours):
            dataset_name = f"{global_frame_number}-{i}"
            file.create_dataset(dataset_name, data=get_bbox_image(frame, contour))
            blobs_in_frame.append(Blob(contour, global_frame_number, dataset_name))

    return blobs_in_frame


def process_frame(
    frame: np.ndarray,
    intensity_ths: Sequence[float],
    area_ths: Sequence[float],
    ROI_mask: np.ndarray | None = None,
    bkg_model: np.ndarray | None = None,
    resolution_reduction: float = 1.0,
) -> tuple[list[int], list[np.ndarray], np.ndarray]:
    # Apply resolution reduction
    if resolution_reduction != 1:
        frame = cv2.resize(
            frame,
            None,  # type: ignore
            fx=resolution_reduction,
            fy=resolution_reduction,
            interpolation=cv2.INTER_AREA,
        )

    # Convert the frame to gray scale
    frame = to_gray_scale(frame)

    if bkg_model is None:
        segmented_frame = cv2.inRange(frame, *intensity_ths)
    else:
        segmented_frame = (cv2.absdiff(bkg_model, frame) > intensity_ths[0]).astype(
            np.uint8, copy=False
        )

    # Applying the mask
    if ROI_mask is not None:
        cv2.bitwise_and(segmented_frame, ROI_mask, segmented_frame)

    # Extract blobs info
    contours = cv2.findContours(
        segmented_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS
    )[0]

    # Filter contours by size
    areas = []
    good_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area_ths[0] <= area <= area_ths[1]:
            good_contours.append(np.squeeze(contour))
            areas.append(area)
    return areas, good_contours, frame


def segment(
    segmentation_parameters: dict,
    episodes: list[Episode],
    bbox_images_path: Path,
    video_paths: list[Path],
    number_of_frames: int,
    n_jobs: int,
) -> list[list[Blob]]:
    """Computes a list of blobs for each frame of the video and the maximum
    number of blobs found in a frame."""
    logging.info(
        f"Segmenting video, {len(episodes)} episodes in {n_jobs} parallel jobs"
    )
    # avoid computing with all the cores in very large videos. It fills the RAM.

    inputs = [
        (episode, video_paths, segmentation_parameters, bbox_images_path.parent)
        for episode in episodes
    ]

    blobs_in_video: list[list[Blob]] = [[]] * number_of_frames

    if n_jobs == 1:
        for input in track(inputs, "Segmenting video"):
            blobs_in_episode, episode = segment_episode(input)
            blobs_in_video[episode.global_start : episode.global_end] = blobs_in_episode
    else:
        with Pool(n_jobs, maxtasksperchild=1) as p:
            for blobs_in_episode, episode in track(
                p.imap_unordered(segment_episode, inputs),
                "Segmenting video",
                len(inputs),
            ):
                blobs_in_video[episode.global_start : episode.global_end] = (
                    blobs_in_episode
                )

    return blobs_in_video


def generate_frame_stack(
    video_paths: Sequence[str | Path],
    episodes: list[Episode],
    n_frames_for_background: int,
    progress_bar=None,
    abort: Callable = lambda: False,
) -> np.ndarray | None:
    logging.info(
        "Generating frame stack for background subtraction with"
        f" {n_frames_for_background} samples"
    )

    list_of_frames: list[tuple[int, int]] = []
    for e in episodes:
        list_of_frames += [
            (frame, e.video_path_index) for frame in range(e.local_start, e.local_end)
        ]

    frames_to_take = np.linspace(
        0, len(list_of_frames) - 1, n_frames_for_background, dtype=int
    )

    frames_to_sample: list[tuple[int, int]] = [
        list_of_frames[i] for i in frames_to_take
    ]

    cap = cv2.VideoCapture(str(video_paths[0]))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    if abort():
        return None
    frame_stack = np.empty((len(frames_to_sample), height, width), np.uint8)
    current_video = 0
    error_frames: list[int] = []
    for i, (frame_number, video_idx) in enumerate(
        track(frames_to_sample, "Computing background")
    ):
        if video_idx != current_video:
            cap.release()
            cap = cv2.VideoCapture(str(video_paths[video_idx]))
            current_video = video_idx
        if frame_number != int(cap.get(cv2.CAP_PROP_POS_FRAMES)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:
            frame_stack[i] = to_gray_scale(frame)
        else:
            logging.error(
                f"OpenCV could not read frame {frame_number} of"
                f" {video_paths[video_idx]} while computing the background"
            )
            error_frames.append(i)
        if abort():
            return None
        if progress_bar:
            progress_bar.emit(i)

    if error_frames:
        return np.delete(frame_stack, error_frames, 0)
    return frame_stack


def generate_background_from_frame_stack(
    frame_stack: np.ndarray | None, stat: str
) -> np.ndarray | None:
    if frame_stack is None:
        return None

    logging.info(f"Computing background from a frame stack using '{stat}'")

    if stat == "median":
        bkg = np.median(frame_stack, axis=0, overwrite_input=True)
    elif stat == "mean":
        bkg = np.mean(frame_stack, axis=0)
    elif stat == "max":
        bkg = np.max(frame_stack, axis=0)
    elif stat == "min":
        bkg = np.min(frame_stack, axis=0)
    else:
        raise ValueError(
            f"Stat '{stat}' is not one of ('median', 'mean', 'max' or 'min')"
        )
    return bkg.astype(np.uint8)


def compute_background(
    video_paths,
    episodes: list[Episode],
    n_frames_for_background: int,
    stat: str,
    progress_bar=None,
) -> np.ndarray | None:
    """
    Computes the background model by sampling `n_frames_for_background` frames
    from the video and computing the stat ('median', 'mean', 'max' or 'min')
    across the sampled frames.

    Parameters
    ----------
    video_paths : list[str]
    original_ROI: np.ndarray
    episodes: list[tuple(int, int, int, int, int)]
    stat: str
        statistic to compute over the sampled frames
        ('median', 'mean', 'max' or 'min')

    Returns
    -------
    bkg : np.ndarray
        Background model
    """

    frame_stack = generate_frame_stack(
        video_paths, episodes, n_frames_for_background, progress_bar
    )

    if frame_stack is None:
        return None

    background = generate_background_from_frame_stack(frame_stack, stat)

    return background


def to_gray_scale(frame: np.ndarray) -> np.ndarray:
    if frame.ndim > 2:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame


def get_bbox_image(frame: np.ndarray, cnt: np.ndarray) -> np.ndarray:
    """Computes the `bbox_image`from a given frame and contour. It also
    returns the coordinates of the `bbox`, the ravelled `pixels`
    inside of the contour and the diagonal of the `bbox` as
    an `estimated_body_length`

    Parameters
    ----------
    frame : nd.array
        frame from where to extract the `bbox_image`
    cnt : list
        List of the coordinates that defines the contour of the blob in the
        full frame of the video

    Returns
    -------
    bbox : tuple
        Tuple with the coordinates of the bounding box (x, y),(x + w, y + h))
    bbox_image : nd.array
        Part of the `frame` defined by the coordinates in `bbox`
    pixels_in_full_frame_ravelled : list
        List of ravelled pixels coordinates inside of the given contour
    estimated_body_length : int
        Estimated length of the contour in pixels.

    See Also
    --------
    _get_bbox
    _cnt2BoundingBox
    _get_pixels
    """
    # extra padding for future image eroding
    pad = 1
    # Coordinates of an expanded bounding box
    frame_w, frame_h = frame.shape
    x0, y0, w, h = cv2.boundingRect(cnt)
    w -= 1  # cv2 adds an extra pixel on width and height
    h -= 1
    x0 -= pad
    y0 -= pad
    x1 = x0 + w + 2 * pad
    y1 = y0 + h + 2 * pad

    if x0 < 0:
        x0_margin = -x0
        x0 = 0
    else:
        x0_margin = 0

    if y0 < 0:
        y0_margin = -y0
        y0 = 0
    else:
        y0_margin = 0

    if x1 > frame_h:
        x1_margin = frame_h - x1
        x1 = frame_h
    else:
        x1_margin = None

    if y1 > frame_w:
        y1_margin = frame_w - y1
        y1 = frame_w
    else:
        y1_margin = None

    bbox_image = np.zeros((h + 2 * pad, w + 2 * pad), np.uint8)

    # the estimated body length is the diagonal of the original bbox
    # Get bounding box from frame
    bbox_image[y0_margin:y1_margin, x0_margin:x1_margin] = frame[y0:y1, x0:x1]
    return bbox_image
