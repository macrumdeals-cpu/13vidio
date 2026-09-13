from datetime import datetime
import os
import random
from app import Video, app, db
from gtts import gTTS
from moviepy.editor import ColorClip  # أو الاستيراد المباشر


def create_video_file(output_filename="static/generated_video.mp4"):
  print("--- بدأ توليد الفيديو أوتوماتيكياً ---")
  selected = random.choice(TOPICS) if "TOPICS" in globals() else {
      "title": "أحدث تقنيات الذكاء الاصطناعي والأتمتة في 2026",
      "desc": "فيديو تكنولوجي سريع.",
  }

  # 1. توليد الصوت
  tts = gTTS(text=selected["title"], lang="ar")
  audio_path = "temp_audio.mp3"
  tts.save(audio_path)

  # 2. إنشاء خلفية فيديو
  video = ColorClip(size=(720, 1280), color=(15, 23, 42), duration=5)

  os.makedirs("static", exist_ok=True)
  video.write_videofile(
      output_filename, fps=24, codec="libx264", audio_codec="aac"
  )

  if os.path.exists(audio_path):
    os.remove(audio_path)

  print("--- تم الانتهاء من رندر الفيديو بنجاح ---")
  return selected["title"], selected["desc"], output_filename
