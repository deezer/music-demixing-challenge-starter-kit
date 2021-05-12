#!/usr/bin/env python
#
# This file uses spleeter for music demixing.
#
# NOTE: spleeter need checkpoints to be submitted along with your code.
#
# Making submission using openunmix:
# 1. Run this file locally with `python test.py`.
# 3. Submit your code using git-lfs
#    #> git lfs install
#    #> git lfs track "pretrained_models/*"
#    #> git add .gitattributes
#    #> mkdir -p pretrained_models/pretrained_models/
#    #> ln -s ../4stems/ pretrained_models/pretrained_models/4stems
#    #> git add pretrained_models/


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
        print("%s: prediction completed." % mixture_file_path)


if __name__ == "__main__":
    submission = SpleeterPredictor()
    submission.run()
    print("Successfully generated predictions!")
