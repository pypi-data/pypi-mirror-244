import argparse
import shutil
from pyannote.audio import Pipeline
import time
import os
import numpy as np
from collections import OrderedDict
from audiotool.get_audio_timestamp import extract_audio_to_file
from pydub import AudioSegment

# import torchaudio.lib.libtorchaudio


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default=None)
    parser.add_argument("-t", "--target", type=str, default=None, help="target folder")
    args = parser.parse_args()

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token="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",
    )
    # pipeline.to(torch.device("cuda"))
    folder = args.file

    hparams = pipeline.parameters(instantiated=True)
    print(hparams)
    hparams["clustering"]["threshold"] -= 0.14
    hparams["segmentation"]["min_duration_off"] += 0.22
    pipeline.instantiate(hparams)
    print(hparams)

    t0 = time.time()
    name = os.path.basename(folder).split(".")[0]
    diarization = pipeline(folder, min_speakers=2, max_speakers=4)

    # diarization = pipeline(audio_f, num_speakers=2)
    t1 = time.time()
    print(f"time cost: {t1 - t0}")
    #  print the result
    speakers = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        speaker_dict = {}
        speaker_dict["start"] = turn.start
        speaker_dict["end"] = turn.end
        speaker_dict["speaker"] = speaker
        speaker_dict["unit_len"] = turn.end - turn.start
        speakers.append(speaker_dict)

    # save the most speaker into a folder by the length
    speakers_lens_gather = OrderedDict()
    for sp in speakers:
        print(sp["speaker"])
        if sp["speaker"] in speakers_lens_gather.keys():
            speakers_lens_gather[sp["speaker"]] += sp["unit_len"]
        else:
            speakers_lens_gather[sp["speaker"]] = sp["unit_len"]
    print(speakers_lens_gather)

    most_speaker = np.argmax(speakers_lens_gather.values())
    most_speaker = list(speakers_lens_gather.keys())[most_speaker]
    print("most speaker: ", most_speaker)
    target_folder = f"results/{name}"
    shutil.rmtree(target_folder)
    os.makedirs(target_folder, exist_ok=True)
    for i, sp in enumerate(speakers):
        if sp["speaker"] == most_speaker:
            s = sp["start"]
            e = sp["end"]
            extract_audio_to_file(s, e, folder, f"{target_folder}/{i}.mp3")

    # concate all mp3 files into one
    mp3_files = [f for f in os.listdir(target_folder) if f.endswith(".mp3")]
    mp3_files.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
    # Initialize an empty audio segment
    combined = AudioSegment.empty()
    for mp3_file in mp3_files:
        sound = AudioSegment.from_mp3(os.path.join(target_folder, mp3_file))
        combined += sound
    combined.export(f"{target_folder}/final_concat.mp3", format="mp3")


if __name__ == "__main__":
    main()
