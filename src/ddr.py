import typing
import more_itertools
from contextlib import contextmanager
from typing import Any, Iterator, Tuple

import cv2
import numpy as np


@contextmanager
def releasing(capture):
    yield capture
    capture.destroyAllWindows()


def iter_camera(
    capture: cv2.VideoCapture, end_char="q"
) -> Iterator[Tuple[Any, np.ndarray]]:
    assert len(end_char) == 1
    while capture.isOpened():
        ret, frame = capture.read()
        yield frame
        if cv2.waitKey(1) & 0xFF == ord(end_char):
            break


def main():
    with releasing(cv2.VideoCapture(0)) as capture:
        thing(capture)


def grayscale(frame: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


class Slider:
    """A slider added to the given window"""

    def __init__(self, name: str, window_name: str, max_value: int, starting_value=0):
        cv2.createTrackbar(
            name, window_name, starting_value, max_value, self.__update_value
        )
        self.value = starting_value

    def __update_value(self, new_value: int):
        self.value = new_value


def thing(capture: cv2.VideoCapture):
    cv2.namedWindow("window")
    thresh = Slider("thresh", "window", max_value=255)
    for prev_frame, frame in more_itertools.windowed(
        map(grayscale, iter_camera(capture)), 2
    ):
        diff = cv2.absdiff(frame, prev_frame)
        _, threshed = cv2.threshold(diff, thresh.value, 255, cv2.THRESH_BINARY)
        cv2.imshow("window", threshed)


if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()
