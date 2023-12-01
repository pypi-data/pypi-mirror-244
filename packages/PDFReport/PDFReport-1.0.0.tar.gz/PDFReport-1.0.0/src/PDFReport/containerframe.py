from typing import List, cast

from .reportframe import ReportFrame


class ContainerFrame(ReportFrame):

    def __init__(self, parent, frame_id: str = ""):
        super().__init__()
        self.frame_id = frame_id
        self._currentFrameIndex = 0
        self._frames: List[ReportFrame] = []

        if parent is not None:
            self.parent_frame = parent
            idx = parent.add_frame(self)
            if self.frame_id == "":
                self.frame_id = parent.frame_id + "." + str(idx)

    def get_frame_count(self) -> int:
        return len(self._frames)

    def clear_frames(self):
        self._frames.clear()

    def reset_size(self, keep_together: bool):
        super().reset_size(keep_together)
        if keep_together:
            for i in range(0, len(self._frames)):
                self._frames[i].reset_size(True)

        else:
            if self._is_current_frame_valid():
                self._get_current_frame().reset_size(False)

    def is_endless(self, frames: []) -> bool:
        for i in range(0, len(self._frames)):
            if self._frames[i] in frames:
                return True

            frames.append(self._frames[i])
            if isinstance(self._frames[i], ContainerFrame):
                container_frame = cast(ContainerFrame, self._frames[i])
                if container_frame.is_endless(frames):
                    return True

        return False

    def reset(self):
        super().reset()
        for i in range(0, len(self._frames)):
            self._frames[i].reset()

    def add_frame(self, frame: ReportFrame) -> int:
        frame.parent_frame = self
        self._frames.append(frame)
        return len(self._frames) - 1

    def _is_current_frame_valid(self) -> bool:
        if self._currentFrameIndex < len(self._frames):
            return True
        else:
            return False

    def _get_current_frame(self) -> ReportFrame:
        if self._currentFrameIndex < len(self._frames):
            return self._frames[self._currentFrameIndex]

    def to_dict(self, data: dict, frame: dict):
        super().to_dict(data, frame)

        for i in range(0, len(self._frames)):
            f = {}
            self._frames[i].to_dict(data, f)

    def from_dict(self, frame: dict):
        super().from_dict(frame)
