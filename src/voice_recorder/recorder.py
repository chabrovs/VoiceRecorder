from record_producer import RecordProducer

# Interface recorder.


class Recorder:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Recorder, cls).__new__(cls)
            # Class initialization here:
            cls.record_producer = RecordProducer()

        return cls._instance


    def record(self) -> None:
        self.record_producer.produce_record()

    def start_recording(self) -> None:
        self.record_producer.start_recording()

    def stop_recording(self) -> None:
        self.record_producer.stop_recording()
