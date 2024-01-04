# Annotations
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Mapping
from typing import Any
from numpy import ndarray, float64

# OS
from os import path, makedirs
import queue
from threading import Thread, Event

# Libs
import sounddevice as sd
from scipy.io.wavfile import write
import wave
import pyaudio
from manager import settings_manager


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
    def record(self) -> tuple[int, ndarray[float64] | Any]:
        """
        Record voce from a sound device with a certain frequency 
        for the certain duration.
        """
        ...


class Generator(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.save_records_path: str
        self.default_filename: str

    @abstractmethod
    def generate_unique_name(self) -> str:
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
        self.freq = settings_manager.get_setting('recorder.freq')
        self.duration = settings_manager.get_setting('recorder.duration')
        self.channels = settings_manager.get_setting('recorder.channels')

    def record(self) -> tuple[int, ndarray[float64] | Any]:
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
        self.save_records_path = settings_manager.get_setting(
            'save_records_path')
        self.default_filename = settings_manager.get_setting(
            'recorder.default_filename')

    def generate_unique_name(self) -> str:
        directory = self.save_records_path

        count = 1
        while True:
            file_name = f"{self.default_filename}_{count}.wav"
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
        raise NotImplemented

    def write_continues_record_wave(self, record: tuple[pyaudio.PyAudio, list[bytes]], full_path: str) -> None:
        audio, frames = record
        # Open audio file
        audio_file = wave.open(full_path, 'wb')

        # Set setting to the audio file
        audio_file.setnchannels(settings_manager.get_setting('recorder.channels'))
        audio_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        audio_file.setframerate(settings_manager.get_setting('recorder.freq'))

        # Write data to the audio file
        audio_file.writeframes(b''.join(frames))

        # Close the audio file
        audio_file.close()


class ContinuesRecording(Thread):
    # TODO: Refactor the implementation so it would be more OOP designed.

    def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._target = target
        self._stop_recording = Event()
        self.daemon = True
        # self._result_queue = queue.Queue()
        self.full_name_generator = PathNameGenerator()
        self.record_writer = RecordWriter()

    def run(self):
        # Start recording
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=settings_manager.get_setting('recorder.channels'),
            rate=settings_manager.get_setting('recorder.freq'),
            input=True,
            frames_per_buffer=settings_manager.get_setting(
                'recorder.frames_per_buffer')
        )
        frames = []
        while not self._stop_recording.is_set():
            data = stream.read(1024)
            frames.append(data)

        # Stop recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save audio record
        self.record_writer.write_continues_record_wave(
            (audio, frames), self.full_name_generator.generate_unique_name()
        )

    def stop(self):
        self._stop_recording.set()


class RecordProducer(Producer):
    def __init__(self) -> None:
        super().__init__()
        self.voice_recorder = VoiceRecorder()
        self.path_name_generator = PathNameGenerator()
        self.record_writer = RecordWriter()
        self.continues_recording = None

    def produce_record(self) -> None:
        self.record_writer.write_record_scrip(
            self.voice_recorder.record(),
            self.path_name_generator.generate_unique_name()
        )

    def start_recording(self) -> None:
        self.continues_recording = ContinuesRecording()
        self.continues_recording.start()

    def stop_recording(self) -> None:
        self.continues_recording.stop()
        self.continues_recording.join()
