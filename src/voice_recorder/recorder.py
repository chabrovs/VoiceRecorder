from record_producer import RecordProducer

# Interface recorder.


class Recorder:
    def __init__(self) -> None:
        self.record_producer = RecordProducer()

    def record(self) -> None:
        self.record_producer.produce_record()

    def start_recording(self) -> None:
        self.record_producer.start_recording()

    def stop_recording(self) -> None:
        self.record_producer.stop_recording()
