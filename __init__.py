import math
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
import os
import warnings
from eye.functions import *

app = Flask(__name__)
warnings.filterwarnings("ignore")
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '@12345678@')


# 登录
@app.route("/login")
def login():
    return render_template('login.html')


# 登出
@app.route("/login")
def logout():
    return render_template('login.html')


# 用户信息(这里是向前端提交信息使用post，没有办法直接使用网址来获取这个def的）
@app.route("/confirm_user", methods=['post'])
def use_login():
    # 获取页面信息
    user_id = request.form.get('user_id').strip()
    user_pwd = request.form.get('user_pwd').strip()

    # 管理员登录，跳转到一个新的管理页面
    if user_id == 'admin' and user_pwd == '000000':
        session['user_id'] = '管理员'
        session.permanent = True  # 长期有效，一个月的时间有效
        return redirect(url_for("admin_page"))

    # 查找用户信息
    result = get_password_by_id(user_id)
    if result == None:
        return render_template("login.html", state="用户名不存在!")
    elif user_pwd != result[1]:
        return render_template("login.html", state="用户密码错误!")
    else:
        session['user_id'] = request.form.get('user_id')
        session.permanent = True  # 长期有效，一个月的时间有效
        return redirect(url_for("index_page"))


# index页面
@app.route('/')
@app.route('/index')
def index_page():
    # 检查是否登陆
    if 'user_id' not in session.keys():
        return redirect(url_for("login"))

    # 获取个人信息
    user_name = session['user_id']
    # personal_info = get_personal_info(session['user_id']

    # 页面显示的记录数
    show_num = 5

    # 初始页面
    if len(request.args) == 0:
        # 当前页面
        curr_page = 1
        datas = get_task_list(user_name, 'all')
        item_nums = len(datas)
        all_pages = math.ceil(item_nums / show_num)
        # 显示全部数据
        session['show'] = 'all'
        # 传入前端的数据
        items = []
        for rank, item in enumerate(datas[0: curr_page * show_num]):
            temp = [(curr_page - 1) * show_num + rank + 1]
            score = 0
            for i, s_item in enumerate(item):
                if i != 2:
                    temp.append(s_item)
                else:
                    temp.append(s_item)
                    pretime = int(0.3 * int(s_item))
                    temp.append(pretime)
            # 看一下结构，通过第6项来判断是否已经阅读
            items.append(temp)
        return render_template('index.html', re_datas={
            "item_nums": item_nums,
            "all_pages": all_pages,
            "curr_page": curr_page,
            "datalist": items
        })
    else:
        # 显示标注数据
        if request.args.get('show') == 'true':
            session['show'] = 'true'
        elif request.args.get('show') == 'false':
            session['show'] = 'false'
        elif request.args.get('show') == 'all':
            session['show'] = 'all'
        # 当前页码
        curr_page = int(request.args.get('curr_page')) \
            if request.args.get('curr_page') != None else 1
        if curr_page == 0:
            curr_page = 1
        # 获取数据
        datas = get_task_list(user_name, session['show'])
        # 数据总量
        item_nums = len(datas)
        # 总页数
        all_pages = math.ceil(item_nums / show_num)
        # 当当前页超过最大页数时，重置为最大页数
        if curr_page > all_pages: curr_page = all_pages
        # 处理标注数据
        items = []
        for rank, item in enumerate(datas[(curr_page - 1) * show_num: curr_page * show_num]):
            temp = [(curr_page - 1) * show_num + rank + 1]
            score = 0
            for i, s_item in enumerate(item):
                if i != 2:
                    temp.append(s_item)
                else:
                    temp.append(s_item)
                    pretime = int(0.3 * int(s_item))
                    temp.append(pretime)
            items.append(temp)
        return render_template('index.html', re_datas={
            "item_nums": item_nums,
            "all_pages": all_pages,
            "curr_page": curr_page,
            "show": session['show'],
            "datalist": items
        })


@app.route('/admin')
def admin_page():
    # 检查是否登陆
    if 'user_id' not in session.keys():
        return redirect(url_for("login"))

    # 获取个人信息
    user_name = session['user_id']
    # personal_info = get_personal_info(session['user_id']

    # 验证管理员身份
    if user_name != "管理员":
        return redirect(url_for("login"))

    # 页面显示的记录数
    show_num = 5

    # 初始页面
    if len(request.args) == 0:
        # 当前页面
        curr_page = 1
        datas = get_task_list_admin('all')
        item_nums = len(datas)
        all_pages = math.ceil(item_nums / show_num)
        # 显示全部数据
        session['show'] = 'all'
        # 传入前端的数据
        items = []
        # enumerate函数能获取列表或数组的index和内容
        # for循环获取当前页面中需要展示的信息，并传递到前端
        # 数据格式：数据序号，
        for rank, item in enumerate(datas[0: curr_page * show_num]):
            temp = [(curr_page - 1) * show_num + rank + 1]
            for i, s_item in enumerate(item):
                temp.append(s_item)
            # 看一下结构，通过第6项来判断是否已经阅读
            items.append(temp)
        return render_template('admin.html', re_datas={
            "item_nums": item_nums,
            "all_pages": all_pages,
            "curr_page": curr_page,
            "datalist": items
        })
    else:
        # 显示标注数据
        if request.args.get('show') == 'true':
            session['show'] = 'true'
        elif request.args.get('show') == 'false':
            session['show'] = 'false'
        elif request.args.get('show') == 'all':
            session['show'] = 'all'
        # 当前页码
        curr_page = int(request.args.get('curr_page')) \
            if request.args.get('curr_page') != None else 1
        if curr_page == 0: curr_page = 1
        # 获取数据
        datas = get_task_list_admin(session['show'])
        # 数据总量
        item_nums = len(datas)
        # 总页数
        all_pages = math.ceil(item_nums / show_num)
        # 当当前页超过最大页数时，重置为最大页数
        if curr_page > all_pages: curr_page = all_pages
        # 处理标注数据
        items = []
        for rank, item in enumerate(datas[(curr_page - 1) * show_num: curr_page * show_num]):
            temp = [(curr_page - 1) * show_num + rank + 1]
            for i, s_item in enumerate(item):
                temp.append(s_item)
            items.append(temp)
        return render_template('admin.html', re_datas={
            "item_nums": item_nums,
            "all_pages": all_pages,
            "curr_page": curr_page,
            "show": session['show'],
            "datalist": items
        })


# 校准页面1
@app.route('/check_page', methods=['GET'])
def check_page():
    a_id = request.args.get('a_id')
    session['artical_id'] = a_id
    return render_template('check.html')


# 校准页面2
@app.route('/check2_page')
def check2_page():
    return render_template('check2.html')


#新阅读页面
#需要将该文章所有的内容一次性传给前端,并且不分是否为
@app.route('/newcollect_page')
def newcollect_page():
    # 根据session获取该篇文章的所有的句子并保存到passage中(list)
    u_id = session['user_id']
    a_id = session['artical_id']
    passage = get_sentence(a_id)
    passage_ids = get_sentence_id(a_id)
    # 获取文章的标题(string)
    # 计算总句子数
    all_s = len(passage)
    title = get_title(a_id)
    # 第一次进入时，session状态为first
    if len(request.args) == 0:
        # 更改task表中的任务信息(第一次进入时更改的是state和readtime）
        change_state(u_id, a_id)
        # 当前为第一句
        curr_s = 1
        print(u_id)
        print(passage)
        print(passage_ids)
        print(title)
        # 将整篇文章的数据传入前端
        return render_template('newcollect.html', re_datas={
            "u_id": u_id,
            "a_id": a_id,
            "all_s": all_s,
            "title": title,
            "sentence": passage,
            "sentence_id": passage_ids,
            "curr_s":curr_s
        })



# task任务重置
@app.route('/resetTask', methods=['POST'])
def reset_task():
    a_id = request.form.get("a_id")  # 文章ID
    u_id = request.form.get("u_id")  # 用户id
    a_id = a_id[1:-1]
    u_id = u_id[1:-1]
    reset_state = reset_task_info(a_id, u_id)
    if reset_state == 1:
        return jsonify({"state": "重置成功,请刷新页面！"})
    else:
        return jsonify({"state": "重置失败，请重新尝试！"})


# 保存眼动数据
@app.route('/saveData', methods=['POST'])
def save_eyedata():
    # 从前端获取信息
    sid = request.form.get("s_id")  # 句子id
    uid = request.form.get("u_id")  # 用户id
    wordid = request.form.get("wordid")  # 当前的字
    x = request.form.get("x")  # x坐标
    y = request.form.get("y")  # y坐标
    time = request.form.get("time") #眼动坐标点时间
    # 打印信息查看
    # print(sid)
    # print(uid)
    # print(wordid)
    # print(x)
    # print(y)
    #更改格式
    time = time[1:-1]
    print(time)
    # 获取当前的时间
    time2 = datetime.datetime.now()
    print(time2)
    # 保存到数据库,返回保存状态
    result = save_eyedata_info(sid, uid, wordid, x, y, time)
    # 保存成功进行前端的返回
    if result == 1:
        return jsonify({"state": "成功,请刷新页面！"})
    else:
        return jsonify({"state": "失败，请重新尝试！"})


# 验证问题页面加载，将获取的数据传递到前端
@app.route('/answer')
def answer_page():
    # 获取session中的用户id和文章id
    u_id = session['user_id']
    a_id = session['artical_id']
    # 从数据库的artical表中获取问题的答案组
    options = get_options(a_id)
    # 将options分割成数组格式(在functions中测试代码）
    options = options.split("；")
    options = options[:-1]
    # 对排列顺序进行随机化（随机交换两次任意两个元素的位置）
    print(options)
    options = exchange_options(options)
    options = exchange_options(options)
    print(options)
    # 将uid、aid和选项传入answer页面
    return render_template('answer.html', options_datas={
        "options": options,
        "u_id": u_id,
        "a_id": a_id
    })


# 保存验证问题的答案并回到任务列表
@app.route('/saveAnswer', methods=['POST'])
def save_answer():
    # 从前端获取信息（uid aid answer）
    aid = request.form.get("a_id")  # 文章id
    uid = request.form.get("u_id")  # 用户id
    answer_index = int(request.form.get("answer_index"))  # 用户的答案id
    options = request.form.get("options")  # 用户的答案
    options = options[0:-1].split(",")
    option = options[answer_index][6:-5]
    print(aid)
    print(uid)
    print(option)
    # 将以上的信息保存到数据库中
    result = save_u_answer(aid, uid, option)
    if result == 1:
        return jsonify({"state": "保存成功！"})
    else:
        return jsonify({"state": "保存失败，请勿重复提交！"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=("eye-tracking.top.pem", "eye-tracking.top.key"))
