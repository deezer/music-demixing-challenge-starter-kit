#!/usr/bin/env python
from evaluator.music_demixing import MusicDemixingPredictor

from spleeter.audio.ffmpeg import FFMPEGProcessAudioAdapter
from spleeter.separator import Separator


class SpleeterPredictor(MusicDemixingPredictor):
    """ Predictor based on Spleeter separator instance. """

    def prediction_setup(self) -> None:
        self.audio = FFMPEGProcessAudioAdapter()
        self.separator = Separator("spleeter:4stems")
        # NOTE: call manually internal to ensure model is
        #       not lazy loaded.
        self.separator._get_prediction_generator()

    def prediction(
        self,
        music_name: str,
        mixture_file_path: str,
        bass_file_path: str,
        drums_file_path: str,
        other_file_path: str,
        vocals_file_path: str,
    ) -> None:
        y, _ = self.audio.load(mixture_file_path)
        prediction = self.separator.separate(y)
        instruments = {
            "bass": bass_file_path,
            "drums": drums_file_path,
            "other": other_file_path,
            "vocals": vocals_file_path,
        }
        for instrument, path in instruments.items():
            self.audio.save(path, prediction[instrument], 44100)
        print("%s: prediction completed." % music_name)


if __name__ == "__main__":
    submission = SpleeterPredictor()
    submission.run()
    print("Successfully generated predictions!")
