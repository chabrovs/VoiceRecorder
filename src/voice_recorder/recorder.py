from record_producer import RecordProducer

# Interface recorder.

class Recorder:
    def __init__(self) -> None:
        self.record_producer = RecordProducer()

    def record(self) -> None:
        self.record_producer.produce_record()
