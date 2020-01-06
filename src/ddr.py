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


def iter_camera(capture: cv2.VideoCapture) -> Iterator[Tuple[Any, np.ndarray]]:
    while capture.isOpened():
        ret, frame = capture.read()
        yield frame
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break


def main():
    with releasing(cv2.VideoCapture(0)) as capture:
        thing(capture)



def gray_make(iterator: typing.Iterable[np.ndarray]) -> typing.Iterator[np.ndarray]:
    return (cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) for frame in iterator)


def thing(capture: cv2.VideoCapture):
    for prev_frame, frame in more_itertools.windowed(
        gray_make(iter_camera(capture)), 2
    ):
        # Our operations on the frame come here
        diff = cv2.absdiff(frame, prev_frame)
        # Display the resulting frame
        # cv2.imshow("frame", frame)
        cv2.imshow("diff", diff)


if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()
