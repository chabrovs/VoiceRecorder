from record_producer import RecordProducer

# BASE_DIR = '/home/sergei/VoiceRecorder/src/voice_recorder/records'


# def generate_unique_filename(base_filename: str, directory: str = None) -> str:
#     """
#     Generates a unique filename, in case if there is already
#     a file with the same filename is the directory.
#     """

#     if not directory:
#         directory = BASE_DIR

#     count = 1

#     while True:
#         filename = f"{base_filename}_{count}.wav"
#         full_path = path.join(directory, filename)
#         if not path.exists(full_path):
#             return full_path

#         count += 1


# def record():
#     freq = 44100
#     duration = 5

#     recording = sd.rec(int(freq * duration), samplerate=freq, channels=2)
#     sd.wait()

#     full_path: str = generate_unique_filename('test')
#     write(full_path, freq, recording)


class Main:
    def __init__(self) -> None:
        self.record_producer = RecordProducer()

    def record(self) -> None:
        self.record_producer.produce_record()


def main():
    main = Main()
    main.record()
