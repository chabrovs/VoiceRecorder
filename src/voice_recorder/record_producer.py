# Annotations
from abc import ABC, abstractmethod
from typing import Any
from numpy import ndarray, float64

# OS
from os import path

# Libs
import sounddevice as sd
from scipy.io.wavfile import write


#
# ABSTRACT DESIGN / DOCUMENTATION
#
class Recorder(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.freq: int
        self.duration: int
        self.channels: int

    @abstractmethod
    def record(self) -> (int, ndarray[float64] | Any):
        """
        Record voce from a sound device with a certain frequency 
        for the certain duration.
        """
        ...


class Generator(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.base_dir: str
        self.default_name: str

    @abstractmethod
    def generate_unique_name(self, name: str, directory: str = None) -> str:
        """
        Generate a unique name for the record and construct a full path where the record
        will be saved. Should return a full path.
        """
        ...


class Writer(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def write_record(self, record: ndarray, full_path: str) -> None:
        """
        Saves the record on the hard drive to a specific path.
        """
        ...


class Producer(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.recorder = None
        self.path_generator = None
        self.record_writer = None
        self.settings: dict

    @abstractmethod
    def produce_record(self) -> None:
        """
        Start record production.
        1. Produce record
        2. Generate a filename for the record
        3. Save the record as a "wav" file.
        """
        ...


#
# IMPLEMENTATION
#

class VoiceRecorder(Recorder):
    def __init__(self) -> None:
        super().__init__()
        self.freq = 44100
        self.duration = 5
        self.channels = 2

    def record(self) -> (ndarray[float64] | Any):
        recording = sd.rec(
            int(self.freq * self.duration),
            samplerate=self.freq,
            channels=self.channels
        )
        sd.wait()
        return self.freq, recording


class PathNameGenerator(Generator):
    def __init__(self) -> None:
        super().__init__()
        self.base_dir = '/home/sergei/VoiceRecorder/src/voice_recorder/records'
        self.default_name = 'test_default'

    def generate_unique_name(self, name: str, directory: str = None) -> str:
        if not directory:
            directory = self.base_dir

        count = 1
        while True:
            file_name = f"{name}_{count}.wav"
            full_path = path.join(directory, file_name)
            if not path.exists(full_path):
                return full_path

            count += 1


class RecordWriter(Writer):
    def __init__(self) -> None:
        super().__init__()

    def write_record(self, record: tuple[int, ndarray], full_path: str) -> None:
        self.write_record_scrip(record, full_path)

    def write_record_scrip(self, record: tuple[int], full_path: str) -> None:
        freq, recording = record
        write(full_path, freq, recording)

    def write_record_wavio(self, record: tuple[int, ndarray], full_path: str) -> None:
        ...


class RecordProducer(Producer):
    def __init__(self) -> None:
        super().__init__()
        self.voice_recorder = VoiceRecorder()
        self.path_name_generator = PathNameGenerator()
        self.record_writer = RecordWriter()

    def produce_record(self, name: str = None) -> None:
        if not name:
            name = None

        self.record_writer.write_record_scrip(
            self.voice_recorder.record(),
            self.path_name_generator.generate_unique_name(name)
        )