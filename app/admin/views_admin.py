from . import admin
from flask import render_template,request,redirect,Markup,make_response,session
from datetime import timedelta
from app import db
from app.admin import modles
import uuid,hashlib
from werkzeug import secure_filename
import os,re
from bs4 import BeautifulSoup

@admin.route('/pre_movie',methods=['POST','GET'])
def pre_movie():
    with open("app/admin/douber_pachong.html", encoding='utf-8') as f:
        soup = BeautifulSoup(f, features='lxml')
    r = soup.select("div a[class='']")  # 里面也可以逐层去找，(div a)。这是类选择器，id选择器，以及层次选择器，属性选择器
    pattern_movie = re.compile(r"<a.*href=(.*)>(.*)</a>", re.S)
    pattern_img = re.compile(r"<img.*src=(.*)/>$", re.S)
    for i in r:
        ret = pattern_movie.findall(str(i))
        img = soup.select("div a[href=" + ret[0][0] + "] img[class='']")
        img_url = pattern_img.findall(str(img[0]))[0]
        # movie_url = ret[0][0]
        movie_title = ret[0][1]
        if i.parent.next_sibling.next_sibling.a:
            movie_url = i.parent.next_sibling.next_sibling.a['href']
        else:
            movie_url = "null"
        pre_movieinfo = modles.prevue(title=movie_title,pre_movie_url=movie_url,logo=img_url)
        db.session.add(pre_movieinfo)
        db.session.commit()
    return "ok"


@admin.route('/admin_base',methods=['POST','GET'])
def admin_base():
    if session.get("usr",None)=="qing jin ru":
        return render_template("adminhtml/admin_base.html")
    # print(666,session.get("usr",None))
    return redirect("/admin_login")

@admin.route('/admin_movie_list/<int:page>',methods=['POST','GET'])
def admin_movie_list(page):
    # movies = modles.movies.query.filter_by().all()
    # for i in movies:
    #     print(i.label)
    page_data=modles.movies.query.order_by(modles.movies.addtime.asc()).paginate(page=page,per_page=5,error_out=False)
    return render_template("adminhtml/movie_list.html",movies=page_data)

@admin.route('/admin_movie_add',methods=['POST','GET'])
def admin_movie_add():
    if session.get("usr",None)=="qing jin ru":
        return render_template("adminhtml/movie_add.html")
    # print(666,session.get("usr",None))
    return redirect("/admin_login")

@admin.route('/admin_movie_add_deal',methods=['POST','GET'])
def admin_movie_add_deal():
    if session.get("usr",None)=="qing jin ru":
        moviename = request.form.get("movie_name", None)
        f=request.files['movie__']
        movie_name=secure_filename(f.filename)
        movie_path=os.path.join('/home/liu/wangzhan_test/app/static/video/',movie_name)
        movie_path_real='static/video/'+movie_name
        request.files['movie__'].save(movie_path)
        intro = request.form.get("intro", None)
        f2 = request.files['img__']
        img_name = secure_filename(f2.filename)
        img_path = os.path.join('/home/liu/wangzhan_test/app/static/', img_name)
        img_path_real="static/"+img_name
        request.files['img__'].save(img_path)
        select_star = request.form.get("select_star", None)
        select_label = request.form.get("select_label", None)
        place = request.form.get("place", None)
        movie_length = request.form.get("movie_length", None)
        movie_release_time = request.form.get("movie_release_time", None)
        # print(moviename,666,movie_path,img_path,intro,select_star,select_label,place,movie_length,movie_release_time)

        movieinfo = modles.movies(title=moviename, url=movie_path_real, info=intro, logo=img_path_real,
                              star=select_star, playnum="未统计",commentnum="未统计",area=place,release_time=movie_release_time,
                              length=movie_length,labels=select_label)
        db.session.add(movieinfo)
        db.session.commit()
        return redirect("/admin_movie_add")
    return redirect("/admin_login")



# request.files['girlimg'].save('D:\\1.jpg')
# f=request.files['girlimg']
# print('111',secure_filename(f.filename))
# os.path.join


@admin.route('/admin_login',methods=['POST','GET'])
def admin_login():
    if request.method == "POST":
        input_name = request.form.get("name", None)
        # print(hashlib.md5("123".encode("utf-8")).hexdigest())
        a = hashlib.md5()
        input_pwd = request.form.get("pwd", None)
        a.update(input_pwd.encode("utf-8"))
        input_pwd = a.hexdigest()
        m = modles.user.query.filter_by(usr=input_name).all()
        n = modles.user.query.filter_by(usr=input_name).all()[0].pwd
        if input_name== "adminhtml" or "xiaoming":
            session['usr'] = "qing jin ru"
            if not m:
                if input_pwd != n:
                    return render_template("adminhtml/admin_login.html", login_inputname="输入用户名错误", login_inputpwd="输入密码错误")
                return render_template("adminhtml/admin_login.html", login_inputname="输入用户名错误")
            elif input_pwd != n:
                return render_template("adminhtml/admin_login.html", login_inputpwd="输入密码错误")
            else:
                return redirect("/admin_base")
        # return redirect("/admin_base")
    return render_template("adminhtml/admin_login.html")


# resp = make_response(render_template('test1.html',name=Markup('<h6>xiaoming<h6>')))
#     resp.set_cookie('username', 'the username')
#     session['usrname']="xiaoming"
#     print(session.get('usrname'))
#     print(request.cookies)
#     # if not session:
#     #     return redirect('/test2/')
#     return resp