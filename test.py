#!/usr/bin/env python
# This file is the entrypoint for your submission.
# You can modify this file to include your code or directly call your functions/modules from here.
from evaluator.music_demixing import MusicDemixingPredictor

from spleeter import Separator
from spleeter.audio.ffmpeg import FFMPEGProcessAudioAdapter


class SpleeterPredictor(MusicDemixingPredictor):
    """ Predictor based on Spleeter separator instance. """

    def prediction_setup(self) -> None:
        self.audio = FFMPEGProcessAudioAdapter()
        self.separator = Separator("spleeter:4stems")
        # TODO: Force model downloading.

    def prediction(
        self,
        mixture_file_path: str,
        bass_file_path: str,
        drums_file_path: str,
        other_file_path: str,
        vocals_file_path: str,
    ) -> None:
        y, _ = self.audio.load(mixture_file_path)
        prediction = self.separator.separate(y)
        # TODO: map proper output name.
        instruments = {
            "bass": bass_file_path,
            "drums": drums_file_path,
            "others": other_file_path,
            "vocals": vocals_file_path,
        }
        for instrument, path in instruments.items():
            self.audio.save(path, prediction[instrument], 44100)
        print("%s: prediction completed." % mixture_file_path)


if __name__ == "__main__":
    submission = SpleeterPredictor()
    submission.run()
    print("Successfully generated predictions!")
