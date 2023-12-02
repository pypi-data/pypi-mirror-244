import os
import time

import replicate

from replicate_whisper_diarization.logger import get_logger
from replicate_whisper_diarization.diarization.utils import (
    language_mapping,
    convert_to_miliseconds,
    get_words_speaker_mapping,
    get_sentences_speaker_mapping,
)

logger = get_logger(__name__)

MODEL_NAME = os.getenv(
    "DIARIZATION_MODEL_NAME",
    "collectiveai-team/speaker-diarization-3",
)
MODEL_VERSION = os.getenv(
    "DIARIZATION_MODEL_VERSION",
    "f7425066750cd06fdf95b831c08bba1530f222a2eb4145f40493f431b7483b95",
)


def parse_diarization_segments(segments: list[dict]) -> list:
    speaker_ts = []
    for segment in segments:
        speaker_ts.append(
            [
                convert_to_miliseconds(segment["start"]),
                convert_to_miliseconds(segment["stop"]),
                segment["speaker"],
            ]
        )
    return speaker_ts


def run_segmentation(
    audio_url: str,
    webhook_url: str | None = None,
    replicate_model_name: str | None = None,
    replicate_model_version: str | None = None,
) -> dict:
    """
    Run diarization on audio file

    Args:
        audio_url (str): url of audio file
        webhook_url (str, optional): url to send webhook. Defaults to None.
        replicate_model_name (str, optional): name of model. Defaults to None.
        replicate_model_version (str, optional): version of model. Defaults to None.
    """

    model_name = replicate_model_name or MODEL_NAME
    model_version = replicate_model_version or MODEL_VERSION
    model = replicate.models.get(model_name)
    version = model.versions.get(model_version)

    replicate_input = {"audio_url": audio_url}
    if webhook_url:
        prediction = replicate.predictions.create(
            version=version,
            input=replicate_input,
            webhook=webhook_url,
        )
    else:
        prediction = replicate.predictions.create(
            version=version,
            input=replicate_input,
        )

    while prediction.status not in ["failed", "succeeded"] and not webhook_url:
        time.sleep(5)
        prediction.reload()
    if prediction.status == "failed":
        logger.error("Diarization failed")
    output = prediction.output
    return output


def run_diarization(
    segements: list[dict],
    word_timestamps: list[dict[str, float]],
    language: str,
):
    language = language_mapping.get(language, "en")
    segements = parse_diarization_segments(segements)
    wsm = get_words_speaker_mapping(word_timestamps, segements, "start")
    ssm = get_sentences_speaker_mapping(wsm, segements)
    return ssm
