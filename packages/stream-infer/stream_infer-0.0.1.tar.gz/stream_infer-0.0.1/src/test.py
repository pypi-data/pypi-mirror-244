from stream_infer import Inference, FrameTracker, TrackerManager, Player
from stream_infer.algo import BaseAlgo
from stream_infer.exporter import BaseExporter
from stream_infer.producer import PyAVProducer, OpenCVProducer
from stream_infer.log import logger

import time


class ExampleAlgo(BaseAlgo):
    def init(self):
        logger.info(f"{self.name} inited")

    def run(self, frames):
        logger.debug(f"{self.name} running with {len(frames)} frames")
        time.sleep(0.3)
        result = {"name": self.name}
        logger.debug(f"{self.name} finished: {result}")
        return result


class Exporter(BaseExporter):
    def send(self):
        if len(self.results) == 0:
            return
        logger.debug(self.results[-1])


INFER_FRAME_WIDTH = 1920
INFER_FRAME_HEIGHT = 1080
OFFLINE = False

video = "/Users/zaigie/Downloads/small/stu.mov"
fps = 30

producer = PyAVProducer(INFER_FRAME_WIDTH, INFER_FRAME_HEIGHT)
exporter = Exporter()

if __name__ == "__main__":
    max_size = 300
    frame_tracker = (
        FrameTracker(max_size) if OFFLINE else TrackerManager().create(max_size)
    )

    inference = Inference(frame_tracker, exporter)
    inference.load_algo(ExampleAlgo(), frame_count=1, frame_step=fps, interval=1)
    inference.load_algo(ExampleAlgo("emotion"), 5, 6, 60)

    player = Player(producer, frame_tracker, video)
    inference.start(player, fps=fps, is_offline=OFFLINE)
