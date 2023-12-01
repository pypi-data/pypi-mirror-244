
from .containerframe import ContainerFrame
from .reportframe import ReportFrame


class SimpleFrame(ReportFrame):

    def __init__(self, parent: ContainerFrame, frame_id: str = ""):
        """
        Baseclass for simple frame types e.g. TextFrame or ImageFrame

        :param parent: Container into which the simple frame will be added
        :param frame_id: Unique id for the frame (optional)
        """
        super().__init__()
        self.frame_id = frame_id
        self.parent_frame = parent
        idx = parent.add_frame(self)
        if self.frame_id == "":
            self.frame_id = parent.frame_id + "." + str(idx)

    def to_dict(self, data: dict, frame: dict):
        super().to_dict(data, frame)

    def from_dict(self, frame: dict):
        super().from_dict(frame)
