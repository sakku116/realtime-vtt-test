import os
import subprocess
import ffmpeg
import requests
import logging
import speech_recognition as sr


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s\t| %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
)

logger = logging.getLogger(__name__)
recognizer = sr.Recognizer()

# def downloadHslToWav(hls_url, output_file):
#     response = requests.get(hls_url, stream=True)
#     if not response.ok:
#         raise Exception(
#             f"failed to download hsl content, \nstatus_code: {response.status_code} \nraw: {response.text}"
#         )

#     # temp file for hsl
#     temp_file = "temp.ts"
#     with open(temp_file, "wb") as f:
#         for chunk in response.iter_content(chunk_size=1024):
#             f.write(chunk)

#     # convert hsl to wav using ffmpeg
#     command = [
#         "ffmpeg",
#         "-i",
#         temp_file,
#         "-vn",
#         "-acodec",
#         "pcm_s16le",
#         "-ar",
#         "44100",
#         "-ac",
#         "2",
#         output_file,
#     ]
#     subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#     # clean temp file
#     # os.remove(temp_file)


def downloadHslToWav(hls_url, output_file):
    try:
        ffmpeg.input(hls_url).output(output_file, acodec='pcm_s16le', ar='44100').run()
    except ffmpeg.Error as e:
        raise Exception(f"failed to download hsl content, err: {e}")

def transcript(audio):
    with sr.AudioData(audio) as source:
        try:
            text = recognizer.recognize_google_cloud(source)
        except sr.UnknownValueError as e:
            raise Exception(f"Could not understand audio, err: {e}")
        except sr.RequestError:
            raise Exception(f"Could not request results, err: {e}")
        except Exception as e:
            raise Exception(
                f"something went wrong when trying to transcript the audio, err: {e}"
            )

        return text

if __name__ == "__main__":
    logger.info("downloading hsl to wav")
    hsl = "http://op-group1-swiftservehd-1.dens.tv/h/h40/01.m3u8"

    downloadHslToWav(hsl, "hsl_output.wav")