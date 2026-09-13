from datetime import datetime
from flask import Flask, abort, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///13vidio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# جدول الفيديوهات والتفاعل
class Video(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  description = db.Column(db.Text, nullable=True)
  video_url = db.Column(db.String(500), nullable=False)  # رابط الفيديو أو ملفه
  thumbnail_url = db.Column(
      db.String(500), nullable=True
  )  # صورة مصغرة للفيديو
  views = db.Column(db.Integer, default=0)
  likes = db.Column(db.Integer, default=0)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  # العلاقة مع التعليقات
  comments = db.relationship(
      "Comment", backref="video", lazy=True, cascade="all, delete-orphan"
  )


# جدول التعليقات
class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  author = db.Column(db.String(100), nullable=False, default="زائر")
  content = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  video_id = db.Column(
      db.Integer, db.ForeignKey("video.id"), nullable=False
  )


# إنشاء قاعدة البيانات تلقائياً عند الإطلاق
with app.app_context():
  db.create_all()


# الصفحة الرئيسية - عرض جميع الفيديوهات
@app.route("/")
def index():
  videos = Video.query.order_by(Video.created_at.desc()).all()
  return render_template("index.html", videos=videos)


# صفحة تشغيل الفيديو المفرد مع التعليقات والمشاهدات
@app.route("/video/<int:video_id>", methods=["GET", "POST"])
def watch_video(video_id):
  video = Video.query.get_or_404(video_id)

  # زيادة المشاهدة مع كل فتح للصفحة
  video.views += 1
  db.session.commit()

  # إضافة تعليق جديد
  if request.method == "POST":
    if "like_btn" in request.form:
      video.likes += 1
      db.session.commit()
    else:
      author = request.form.get("author", "زائر كريم")
      content = request.form.get("content")
      if content:
        new_comment = Comment(
            author=author, content=content, video_id=video.id
        )
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for("watch_video", video_id=video.id))

  return render_template("watch.html", video=video)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=7860, debug=True)
