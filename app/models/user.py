from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

from app.extensions import db


#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Database model
class User(db.Model):
    #Class vars
    #id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(25), unique=True, nullable=False)
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, pimary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}