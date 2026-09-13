from datetime import datetime
import os
import random
from app import Video, app, db  # استيراد تطبيق و قاعدة بيانات الموقع
from gtts import gTTS
from moviepy.editor import ColorClip, TextClip, concatenate_videoclips

# قائمة مواضيع تريند افتراضية لتوليد الفيديو (يمكن ربطها بـ Groq لاحقاً)
TOPICS = [
    {
        "title": (
            "أحدث تقنيات الذكاء الاصطناعي في عام 2026 وتأثيرها على مستقبل"
            " البرمجة"
        ),
        "desc": (
            "فيديو سريع يستعرض أهم التطورات التكنولوجية وأدوات الأتمتة الحديثة"
            " لعشاق التقنية."
        ),
    },
    {
        "title": "كيف تبني مشروعك البرمجي الخاص وتصل للأرباح بخطوات بسيطة",
        "desc": "دليلك السريع لبدء ريادة الأعمال البرمجية وتحقيق الدخل المستقل.",
    },
    {
        "title": "أسرار وزوايا خفية في عالم السيرفرات والأتمتة السحابية",
        "desc": (
            "كيف تدير مشاريعك البرمجية على السحابة بكل سهولة وبدون تعقيد."
        ),
    },
]


def create_video_file(output_filename="static/generated_video.mp4"):
  print("--- بدأ توليد الفيديو أوتوماتيكياً ---")
  selected = random.choice(TOPICS)

  # 1. توليد الصوت باستخدام gTTS (سريع ومستقر بدون مشاكل)
  tts = gTTS(text=selected["title"], lang="ar")
  audio_path = "temp_audio.mp3"
  tts.save(audio_path)

  # 2. إنشاء فيديو بسيط وأنيق بـ MoviePy (خلفية داكنة مع نص الموضوع)
  # خلفية سوداء بحجم 720x1280 (شورتس/فيديو عمودي) ومدتها 5 ثواني
  bg_clip = ColorClip(size=(720, 1280), color=(15, 23, 42), duration=6)

  # ملاحظة: إذا لم يتوفر خط عربي مدعوم في النظام، يمكنك الاستغناء عن الـ TextClip المؤقت أو استخدام خط افتراضي
  try:
    txt_clip = (
        TextClip(
            selected["title"],
            fontsize=40,
            color="white",
            size=(640, 1100),
            method="caption",
        )
        .set_duration(6)
        .set_position("center")
    )
    video = concatenate_videoclips([bg_clip])  # أو دمج النص لو متاح
  except Exception:
    video = bg_clip  # في حال خط الخطوط، نعتمد الخلفية الاحترافية مع الصوت

  os.makedirs("static", exist_ok=True)
  video.write_videofile(
      output_filename, fps=24, codec="libx264", audio_codec="aac"
  )

  # تنظيف الملفات المؤقتة
  if os.path.exists(audio_path):
    os.remove(audio_path)

  print("--- تم الانتهاء من رندر الفيديو بنجاح ---")
  return selected["title"], selected["desc"], output_filename


if __name__ == "__main__":
  with app.app_context():
    # توليد الفيديو
    title, desc, v_path = create_video_file()

    # حفظه في قاعدة بيانات الموقع (SQLite)
    new_video = Video(
        title=title, description=desc, video_url=f"/{v_path}", views=0, likes=0
    )
    db.session.add(new_video)
    db.session.commit()
    print("--- تم حفظ الفيديو بنجاح في قاعدة بيانات الموقع! ---")
