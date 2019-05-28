# import pymysql
# con=pymysql.connections.Connection(host='localhost',user='root',password='yang1996',port=3306)
# # con=pymysql.connect()
#
# cursor=con.cursor()
#
# cursor.execute("create table member(id int not null primary key,usr varchar(20) not null,pwd varchar(20) not null,name varchar(20) not null,phone varchar(20) not null,info Text default null,face varchar(20) default null,registertime datetime default ,uuid varchar(20) not null")

# from app.admin import modles
# db.create_all()
from app import db
import datetime

class user(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    usr = db.Column(db.String(100),nullable=False,unique=True)
    pwd=db.Column(db.String(120),nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    phone = db.Column(db.String(100),nullable=False,unique=True)
    info = db.Column(db.Text,nullable=True)
    face = db.Column(db.String(100),nullable=True)
    uuid = db.Column(db.String(100), nullable=False, unique=True)
    registertime = db.Column(db.DateTime, default=datetime.datetime.now())
    usrlog = db.relationship("usrlog",backref="user")
    comment=db.relationship("comment",backref="user")
    moviecollect = db.relationship("moviecollect", backref="user")

class usrlog(db.Model):
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="SET NULL"))
    login_ip=db.Column(db.String(100), nullable=True)
    login_time = db.Column(db.DateTime, default=datetime.datetime.now())


# movies_label=db.Table("movies_label",db.Model.metadata,
#     db.Column("movies_id",db.Integer,db.ForeignKey("movies.id",ondelete="SET NULL")),
#     db.Column("labels_id",db.Integer,db.ForeignKey("labels.id",ondelete="SET NULL"))
# )


class labels(db.Model):
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    addtime=db.Column(db.DateTime,default=datetime.datetime.now(),index=True)
    # movies = db.relationship("movies", secondary=movies_label, back_populates="labels")
    movie = db.relationship("movies", backref="label")

class movies(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False,unique=True)
    url = db.Column(db.String(100), nullable=False)
    info = db.Column(db.Text, nullable=True)
    logo = db.Column(db.String(100), nullable=False)
    star = db.Column(db.String(100), nullable=False)
    playnum = db.Column(db.String(100), nullable=False)
    commentnum=db.Column(db.String(100), nullable=False)
    area=db.Column(db.String(100), nullable=False)
    release_time=db.Column(db.String(50))
    length=db.Column(db.String(100), nullable=False)
    addtime = db.Column(db.DateTime, default=datetime.datetime.now(),index=True)
    # labels=db.relationship("labels",secondary=movies_label,back_populates="movies")
    labels = db.Column(db.Integer, db.ForeignKey('labels.id', ondelete="SET NULL"))
    comment = db.relationship("comment", backref="movies")
    # comment = db.Column(db.Integer, db.ForeignKey("movies.id", ondelete="SET NULL"))
    moviecollect = db.relationship("moviecollect", backref="movies")

class prevue(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    pre_movie_url=db.Column(db.String(100),nullable=False)
    logo=db.Column(db.String(100),nullable=False)
    # logooo = db.Column(db.String(20), nullable=False)
    addtime=db.Column(db.DateTime,default=datetime.datetime.now(),index=True)

class comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=True)
    # content_test = db.Column(db.Text, nullable=True)
    movies_id=db.Column(db.Integer,db.ForeignKey("movies.id",ondelete="SET NULL"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete="SET NULL"))
    addtime = db.Column(db.DateTime, default=datetime.datetime.now(),index=True)

class moviecollect(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movies_id = db.Column(db.Integer, db.ForeignKey("movies.id",ondelete="SET NULL"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete="SET NULL"))
    addtime = db.Column(db.DateTime, default=datetime.datetime.now())

class auth(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    url=db.Column(db.String(100),nullable=False)
    addtime = db.Column(db.DateTime, default=datetime.datetime.now(),index=True)
    role=db.relationship("role",backref="auth")

class role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    auths=db.Column(db.Integer,db.ForeignKey("auth.id",ondelete="SET NULL"))
    addtime = db.Column(db.DateTime, default=datetime.datetime.now(),index=True)

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    pwd = db.Column(db.String(100), nullable=False)
    is_super=db.Column(db.SmallInteger,nullable=False)
    adminlog=db.relationship("adminlog",backref="admin")
    oplog = db.relationship("oplog", backref="admin")

class adminlog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id=db.Column(db.Integer,db.ForeignKey("admin.id",ondelete="SET NULL"))
    iquitp=db.Column(db.String(100),nullable=False)
    addtime = db.Column(db.DateTime, default=datetime.datetime.now(),index=True)

class oplog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id",ondelete="SET NULL"))
    ip = db.Column(db.String(100), nullable=False)
    op=db.Column(db.String(500), nullable=False)
    addtime = db.Column(db.DateTime, default=datetime.datetime.now(),index=True)













