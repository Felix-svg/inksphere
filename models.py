from config import db, bcrypt
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, SerializerMixin, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(180), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationship with Blog and Comment
    blogs = db.relationship("Blog", back_populates="user", cascade="all, delete-orphan")
    comments = db.relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.id} Email: {self.email} | Username : {self.username}>"


class Blog(db.Model, SerializerMixin):
    __tablename__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Relationship to Comment
    comments = db.relationship(
        "Comment", back_populates="blog", cascade="all, delete-orphan"
    )
    user = db.relationship("User", back_populates="blogs")

    def __repr__(self):
        return f"<Blog {self.id} - {self.title}>"


class Comment(db.Model, SerializerMixin):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    user = db.relationship("User", back_populates="comments")
    blog = db.relationship("Blog", back_populates="comments")

    def __repr__(self):
        return f"<Comment {self.id} - {self.content}>"

