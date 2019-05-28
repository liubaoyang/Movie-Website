from . import admin
from flask import render_template,request,redirect,session
from app import db
from app.admin import modles
import uuid,hashlib,json,re


@admin.route('/',methods=['POST','GET'])
def home():
    return render_template("base1.html")

# @admin.route('/search',methods=['POST','GET'])
# def search():
#     if request.method == "POST":
#         movieobj=session.get("movieobj",None)
#         print(movieobj)
#         # for i in movieobj:
#         #     print(666,i.title)
#         if movieobj!=None:
#             return render_template("search.html",search_movie=movieobj)
#         else:
#             return render_template("search.html")
#     return render_template("search.html")

@admin.route('/search_choose',methods=['POST','GET'])
def search_choose():
    if request.method == "POST":
        input_sousuo = request.form.get("name", None)
        if input_sousuo!="请输入电影名!" :
            movieobj = modles.movies.query.filter_by(title=input_sousuo).all()

            return render_template("search.html",search_movie=movieobj)
        # if input_sousuo!=None:
        #     movieobj=modles.movies.query.filter_by(title=input_sousuo).all()
        #     # for i in movieobj:
        #     #     print(666,i.title)
        #     session['movieobj']=movieobj
        # movieobj=session.get("movieobj",None)
        # print(1111)
        # if movieobj != None:
        #         print(movieobj[0].title)
        #         return render_template("search.html",search_movie=movieobj[0])
        #
        # if input_sousuo!=None:
        #     if input_sousuo == "请输入电影名!":
        #         return "no input"
        #     else:
        #         # print(77776,input_sousuo)
        #         movieobj = modles.movies.query.filter_by(title=input_sousuo).all()[0]
        #         title=movieobj.title
        #         info=movieobj.info
        #         logo=movieobj.logo
        #         a = logo.split("app/")
        #         search_data={'title':title,'info':info,'logo':a[1]}
        # if  sousuo!=None:
        #     if sousuo == "this":
        #         # print(9090,search_data)
        #         search_data = json.dumps(search_data)
        #         return search_data
    return render_template("search.html")

@admin.route('/huiyuan_usr',methods=['POST','GET'])
def huiyuan():
    if session.get("usrid",None):
        return render_template("huiyuan_usr.html")
    return redirect("/login")
@admin.route('/huiyuan_pwd',methods=['POST','GET'])
def huiyuan_pwd():
    # print("bug")
    if session.get("usrid", None):
        # print("bug234")
        return render_template("huiyuan_pwd.html")
    return redirect("/login")
@admin.route('/huiyuan_loginlog',methods=['POST','GET'])
def huiyuan_loginlog():
    return render_template("huiyuan_loginlog.html")
@admin.route('/huiyuan_moviecol',methods=['POST','GET'])
def huiyuan_moviecol():
    return render_template("huiyuan_moviecol.html")
@admin.route('/huiyuan_comment',methods=['POST','GET'])
def huiyuan_comment():
    return render_template("huiyuan_comment.html")

@admin.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        input_name=request.form.get("name",None)
        # print(hashlib.md5("123".encode("utf-8")).hexdigest())
        a = hashlib.md5()
        input_pwd=request.form.get("pwd",None)
        a.update(input_pwd.encode("utf-8"))
        input_pwd = a.hexdigest()
        m = modles.user.query.filter_by(usr=input_name).all()
        n = modles.user.query.filter_by(usr=input_name).all()[0].pwd
        if not m:
            if input_pwd != n:
                return render_template("login.html", login_inputname="输入用户名错误",login_inputpwd="输入密码错误")
            return render_template("login.html",login_inputname="输入用户名错误")
        elif input_pwd != n:
            return render_template("login.html", login_inputpwd="输入密码错误")
        else:
            userid = modles.user.query.filter_by(usr=input_name).all()[0].id
            usr_log = modles.usrlog(user_id=userid)
            db.session.add(usr_log)
            db.session.commit()
            session["usrid"]=userid
            # print(11111,session.get("usrid",None))
            return redirect("/huiyuan_usr")
    return render_template("login.html")

@admin.route('/usrinfo/',methods=['POST','GET'])
def usrinfo1():
    # formData = req.POST.get("formdata", None)
    # formObj = json.loads(formData)
    # josndata = json.dumps({"teachers": L, "id": ret.id})
    userid=session.get("usrid",None)
    if request.method=='POST':
        dearname = modles.user.query.filter_by(id=userid).all()[0].name
        email = modles.user.query.filter_by(id=userid).all()[0].email
        phone = modles.user.query.filter_by(id=userid).all()[0].phone
        intro = modles.user.query.filter_by(id=userid).all()[0].info
        data=json.dumps({'dearname':dearname,'email':email,'phone':phone,'intro':intro})
        return data


@admin.route('/huiyuan_xiugaiinfo',methods=['POST','GET'])
def xiugaishuju():
    if request.method == "POST":
        usrid=session.get("usrid",None)
        input_name = request.form.get("name", None)
        input_eamil = request.form.get("email", None)
        input_phone = request.form.get("phone", None)
        input_intro = request.form.get("intro", None)
        # print(666,input_name,input_eamil,input_phone,input_intro)
        usrinfo = modles.user.query.filter_by(id=usrid).all()[0]
        usrinfo.name=input_name
        usrinfo.email = input_eamil
        usrinfo.phone = input_phone
        usrinfo.info = input_intro
        db.session.commit()
        return redirect('/huiyuan_usr')
    return redirect('/login')

@admin.route('/huiyuan_xiugaipwd',methods=['POST','GET'])
def xiugaipwd():
    if request.method == "POST":
        usrid=session.get("usrid",None)
        a=hashlib.md5()
        input_pwd = request.form.get("oldpwd", None)
        a.update(input_pwd.encode("utf-8"))
        input_pwd = a.hexdigest()
        n = modles.user.query.filter_by(id=usrid).all()[0].pwd
        if input_pwd != n:
            return render_template("huiyuan_pwd.html",oldpwd="旧密码输入错误")
        input_pwd = request.form.get("newpwd", None)
        a = hashlib.md5()
        a.update(input_pwd.encode("utf-8"))
        newpwd = a.hexdigest()
        usrpwd = modles.user.query.filter_by(id=usrid).all()[0]
        usrpwd.pwd=newpwd
        db.session.commit()
        return redirect('/huiyuan_pwd')
    return redirect('/login')


@admin.route('/register',methods=['POST','GET'])
def register():
    if request.method=="POST":
        name = request.form.get('usrname', None)
        a = hashlib.md5()
        password = request.form.get('pwd', None)
        a.update(password.encode("utf-8"))
        password = a.hexdigest()
        password2 = request.form.get('pwd2', None)
        a.update(password2.encode("utf-8"))
        dearname = request.form.get('dearname', None)
        email = request.form.get('email', None)
        tel = request.form.get('tel', None)
        # request.files['usrimg'].save('\home\1.')
        # usrimg=
        intro = request.form.get('intro', None)
        unique=str(uuid.uuid4())
        usrinfo=modles.user(usr=name,pwd=password,name=dearname,uuid=unique,email=email,phone=tel,info=intro)
        db.session.add(usrinfo)
        db.session.commit()
        return "OK!"
    return render_template("register.html")


@admin.route('/movie',methods=['POST','GET'])
def movie():
    return render_template("movie.html")

@admin.route('/play_choose',methods=['POST','GET'])
def play_choose():
    formData = request.form.get("flag", None)
    if formData== '1':
        session['flag']=1
    if formData == '2':
        session['flag'] =2
    # print(6666666666)
    # print(666,session.get('flag', None))
    return "1111111111"


@admin.route('/movie_ajax',methods=['POST','GET'])
def movie_ajax():
    if request.method=="POST":
        # userid = session.get("usrid", None)
        # Data = request.form.get("flag", None)
        # if Data == 1:
        #     session['flag'] = 1
        # if Data == 2:
        #     session['flag'] = 2
        formData = request.form.get("a", None)
        if formData == "imgfile":
            img_url1 = modles.movies.query.filter_by().all()[0].logo
            # a = img_url1.split("app/")
            # print(img_url1)
            title1 = modles.movies.query.filter_by().all()[0].title

            img_url2 = modles.movies.query.filter_by().all()[1].logo
            # a2 = img_url2.split("app/")
            # print(img_url2)
            title2 = modles.movies.query.filter_by().all()[1].title
            data = json.dumps({'img_url1': img_url1, 'title1': title1, 'img_url2': img_url2, 'title2': title2, })
            return data
        if formData == "moviefile":
            # print(777,session.get("flag", None))
            if session.get("flag", None) == 1:
                # print(777777777777)
                movie_url = modles.movies.query.filter_by().all()[0].url
                # a = movie_url.split("app/")
                title = modles.movies.query.filter_by().all()[0].title
                # print(666, a,title)
                data = json.dumps({'movie_url': movie_url, 'title': title, })
                return data
            if session.get("flag", None) == 2:
                movie_url = modles.movies.query.filter_by().all()[1].url
                # a = movie_url.split("app/")
                title = modles.movies.query.filter_by().all()[1].title
                data = json.dumps({'movie_url': movie_url, 'title': title, })
                return data
        return "!111111111111"


@admin.route('/play',methods=['POST','GET'])
def play():
    if session.get("flag", None) == 1:
        movieid = modles.movies.query.filter_by().all()[0].id
    if session.get("flag", None) == 2:
        movieid = modles.movies.query.filter_by().all()[1].id
    if request.method=="POST":
        usrid=session.get("usrid",None)
        formData = request.form.get("input_comment", None)
        print(formData)
        data=re.findall(r"^<p>(.*)</p>$",formData)
        usrinfo = modles.comment(content=data,movies_id=movieid,user_id=usrid)
        db.session.add(usrinfo)
        db.session.commit()
        commentobj=modles.comment.query.filter_by(movies_id=movieid).all()
        return render_template("play.html",movies=commentobj)
    commentobj = modles.comment.query.filter_by(movies_id=movieid).all()
    return render_template("play.html",movies=commentobj)


