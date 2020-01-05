import typing
from contextlib import contextmanager
from typing import Any, Iterator, Tuple

import cv2
import numpy as np


@contextmanager
def releasing(capture):
    yield capture
    capture.destroyAllWindows()


cap = cv2.VideoCapture(0)


def iter_camera(capture: cv2.VideoCapture) -> Iterator[Tuple[Any, np.ndarray]]:
    while cap.isOpened():
        ret, frame = cap.read()
        yield frame
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break


def main():
    with releasing(cv2.VideoCapture()) as cap:
        thing(cap)


def prev_and_current(iterator: typing.Iterable):
    iterator = iter(iterator)
    previous = next(iterator)
    for current in iterator:
        yield previous, current
        previous = current


def gray_make(iterator: typing.Iterable[np.ndarray]):
    return (cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) for frame in iterator)


def thing(cap):
    for prev_frame, frame in prev_and_current(gray_make(iter_camera(cap))):
        # Our operations on the frame come here
        diff = cv2.absdiff(frame, prev_frame)
        # Display the resulting frame
        # cv2.imshow("frame", frame)
        cv2.imshow("diff", diff)


if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()
