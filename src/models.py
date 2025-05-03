from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

db = SQLAlchemy()

follows = Table(
    "follows",
    db.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True), # Añadimos un ID como clave primaria
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("followed_id", Integer, ForeignKey("users.id"))
)

class User(db.Model):

    __tablename__= "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    user_name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    posts: Mapped[list["Post"]] = relationship(backref="user")
    comments: Mapped[list["Comment"]] = relationship(backref="user")
    
    following: Mapped[list["User"]] = relationship(
        secondary="follows",
        primaryjoin=id == follows.c.user_id,
        secondaryjoin=follows.c.followed_id == id,
        backref="followers"
    )
    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "user_name": self.user_name
        }


class Post(db.Model):
    
    __tablename__="posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(String, nullable=False)

    comments: Mapped[list["Comment"]] = relationship(backref="post")
    media_items: Mapped[list["Media"]] = relationship(backref="post")

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id
        }

class Comment(db.Model):

    __tablename__= "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    text: Mapped[str] = mapped_column(String(500), nullable=False)

    user: Mapped["User"] = relationship(backref="comment")

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id

        }
    
class Media(db.Model):

    __tablename__ = "media"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    url: Mapped[str] = mapped_column(String(), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    post: Mapped["Post"]= relationship(backref="media_items")

    def serialize(self):
        return{
            "id": self.id,
            "url": self.url,
            "post_id": self.post_id

        }