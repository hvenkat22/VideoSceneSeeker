import assemblyai as aai

def closed_captions(videofilepath):
    aai.settings.api_key = ""

    transcript = aai.Transcriber().transcribe(videofilepath)

    subtitles = transcript.export_subtitles_srt(chars_per_caption=20)

    print(subtitles)



