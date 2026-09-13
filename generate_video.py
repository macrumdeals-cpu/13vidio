from datetime import datetime
import os
import random
from app import Video, app, db
from gtts import gTTS
from moviepy.video.VideoClip import ColorClip

TOPICS = [
    {
        "title": (
            "أحدث تقنيات الذكاء الاصطناعي في عام 2026 وتأثيرها على المستقبل"
        ),
        "desc": "فيديو سريع يستعرض أهم التطورات التكنولوجية الحديثة.",
    },
    {
        "title": "كيف تبني مشروعك البرمجي الخاص وتصل للأرباح بخطوات بسيطة",
        "desc": "دليلك السريع لبدء ريادة الأعمال البرمجية.",
    },
]


def create_video_file(output_filename="static/generated_video.mp4"):
  print("--- بدأ توليد الفيديو أوتوماتيكياً ---")
  selected = random.choice(TOPICS)

  # 1. توليد الصوت
  tts = gTTS(text=selected["title"], lang="ar")
  audio_path = "temp_audio.mp3"
  tts.save(audio_path)

  # 2. إنشاء خلفية فيديو بسيطة
  video = ColorClip(size=(720, 1280), color=(15, 23, 42), duration=5)

  os.makedirs("static", exist_ok=True)
  video.write_videofile(
      output_filename, fps=24, codec="libx264", audio_codec="aac"
  )

  if os.path.exists(audio_path):
    os.remove(audio_path)

  print("--- تم الانتهاء من رندر الفيديو بنجاح ---")
  return selected["title"], selected["desc"], output_filename


if __name__ == "__main__":
  with app.app_context():
    title, desc, v_path = create_video_file()
    new_video = Video(
        title=title, description=desc, video_url=f"/{v_path}", views=0, likes=0
    )
    db.session.add(new_video)
    db.session.commit()
    print("--- تم حفظ الفيديو بنجاح في قاعدة بيانات الموقع! ---")
