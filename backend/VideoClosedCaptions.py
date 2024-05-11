import assemblyai as aai

def closed_captions(videofilepath):
    aai.settings.api_key = "3d562e41f9c045b591814f2243585398"

    transcript = aai.Transcriber().transcribe(videofilepath)

    subtitles = transcript.export_subtitles_srt(chars_per_caption=20)

    print(subtitles)



