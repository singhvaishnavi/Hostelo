from flask import Flask, render_template, request, session, url_for, redirect, flash
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from db import *

conn = connectDB()
cursor = conn.cursor(dictionary=True)


# execute SQL query using execute() method.
# cursor.execute("SELECT * from user")

# Fetch a single row using fetchone() method.
# data = cursor.fetchall()
# print("Database version : ",data)
# print(data[0]['status'])

# disconnect from serverc

# db.close()

global temp
temp = True

global owntemp
owntemp = False

@app.route('/myhostels')
def myhostels():
    user = session['userid']
    cursor.execute("select * from owner o, hostel h where o.userid=h.userid and h.userid=%s", (user,))
    res = cursor.fetchall()
    l = len(res)
    return render_template("myhostels.html", flag=temp, own=owntemp, l=l, row=res)

@app.route('/search')
def search():
    qu = request.args.get('search')
    q = "select * from owner o, hostel h where o.userid=h.userid and h.name like '%"+qu+"%' "
    cursor.execute(q)
    res = cursor.fetchall()
    # print(res[0])
    l = len(res)
    print('length is: ', l)
    return render_template("search.html", flag=temp, own=owntemp, l=l, row=res)
    # return render_template("login.html", flag=temp, own=owntemp)

@app.route('/addhostel', methods=['POST', 'GET'])
def addhostel():
    if request.method == 'GET':
        return render_template('addhostel.html', flag=temp, own=owntemp)
    user = request.form
    # print(user)
    userid = session['userid']
    name = user['name']
    regno = user['regno']
    regne = user['regne']
    stime= user['stime']
    sam = user['sam']
    etime = user['etime']
    eam = user['eam']
    cuisine = user['cuisine']
    diet = user['diet']
    address = user['address']
    gen= user['gen']
    cursor.execute('insert into hostel values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (userid, name, regno, regne, cuisine, diet, address, stime, etime, sam, eam, gen))
    conn.commit()

    cursor.execute('select * from hostel where regno=%s', (regno,))
    res = cursor.fetchall()
    l = len(res)
    # print(' this is -> ', res, l, res[0]['hostelid'])

    return render_template("addfacilities.html", flag=temp, own=owntemp, l=l, row=res[0]['hostelid'])

    #return redirect(url_for('index'))

@app.route('/owner', methods=['POST'])
def owner():
    user = request.form
    # print(user)
    userid = session['userid']
    firstname = user['first_name']
    lastname = user['last_name']
    gender = user['gender']
    phone = user['phone']

    cursor.execute('insert into owner values(null, %s, %s, %s, %s, %s)', (userid, firstname, lastname, gender, phone))
    conn.commit()

    return redirect(url_for('index'))

@app.route('/person', methods=['POST'])
def person():
    user = request.form
    # print(user)
    userid = session['userid']
    firstname = user['first_name']
    lastname = user['last_name']
    gender = user['gender']
    dob = user['dob']
    address = user['address']
    idd = user['id']
    phone = user['phone']
    parentphone = user['parentphone']
    inst = user['inst']
    status = user['status']
    med = user['med']

    cursor.execute('insert into person values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (userid, firstname, lastname, gender, dob, address, idd, phone, parentphone, inst, status, med))
    conn.commit()

    return redirect(url_for('index'))

@app.route('/myprofile')
def myprofile():
    if(temp == True):
        return redirect(url_for("index"))
    userid = session['userid']
    cursor.execute('select * from person where userid = %s', (userid,))
    res1 = cursor.fetchone()
    if res1 is not None:
        return render_template('persondetails.html', flag=temp, own=owntemp, person=res1)

    cursor.execute('select * from owner where userid = %s', (userid,))
    res2 = cursor.fetchone()
    if res2 is not None:
        return render_template('ownerdetails.html', flag=temp, own=owntemp, owner=res2)

    cursor.execute('select * from user where userid = %s', (userid,))
    res = cursor.fetchone()
    #print(res)
    if res is None:
        flash("invalid user name")
        return redirect(url_for('login'))
    else:
        typ = res['type']
        return render_template('addData.html', typ=typ, flag=temp, own=owntemp)


@app.route('/')
def index():
    return render_template("index.html", flag=temp, own=owntemp)

@app.route('/signup',methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        user = request.form
        if user['password'] != user['password2']:
            return redirect(url_for('signup'))
        # print(userdetails)
        pwd = user['password']
        email = user['email']
        typ = user['type']
        cursor.execute('insert into user values(null, %s, %s, %s)', (email, pwd, typ))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('signup.html', flag=temp, own=owntemp)

@app.route("/login",methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        userdetails = request.form
        userid = userdetails['email']
        passwed = userdetails['password']
        cursor.execute('select * from user where email = %s', (userid,))
        res = cursor.fetchone()
        #print(res)
        if res is None:
            flash("invalid user name")
            return redirect(url_for('login'))
        else:
            pwd= res['password']
            if passwed == pwd:
                session['logged_in']=True
                global temp
                temp= False
                #print("this is ",temp)
                session['userid']=int(res['userid'])
                if(res['type'] == 'O'):
                    global owntemp
                    owntemp = True
                # return 'You are now logged in','success'
                return redirect(url_for('index'))
            else:
                flash("invalid password")
                return redirect(url_for('login'))
    return render_template("login.html",flag=temp, own=owntemp)


@app.route("/logout")
def logout():
    global temp
    temp= True

    global owntemp
    owntemp = False

    session.clear()
    return redirect(url_for('index'))


@app.route('/addroom', methods=['POST', 'GET'])
def addroom():
    if request.method == 'GET':
        hstid = request.args.get('hostelid')
        return render_template('addroom.html', flag=temp, own=owntemp, row=hstid)
    user = request.form
    print('IN THE ADD ROOM', user)
    name = user['name']
    acavail = user['acavail']
    washroom = user['washroom']
    excup = user['excup']
    locker = user['locker']
    socket = user['socket']
    minifridge = user['minifridge']
    extra = user['extra']
    sharing = user['sharing']
    cost = user['cost']
    noofrooms = user['noofrooms']
    hostelid = user['hostelid']
    hid = user['hostelid']

    cursor.execute('insert into roomtype values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (name, acavail, washroom, excup, locker, socket, minifridge, extra, hostelid))
    conn.commit()

    cursor.execute('select * from roomtype where hostelid=%s and name=%s', (hostelid, name, ))
    res = cursor.fetchall()
    roomtypeid = res[0]['roomtypeid']
    cursor.execute('insert into roomdet values(null, %s, %s, %s, %s,%s)', (sharing, cost, noofrooms, roomtypeid,hid))
    conn.commit()
    # res = cursor.fetchall()
    # l = len(res)

    # return render_template("search.html", flag=temp, own=owntemp, l=l, row=res)
    return redirect(url_for('index'))



@app.route('/addfacilities', methods=['POST', 'GET'])
def addfacilities():
    if request.method == 'GET':
        return render_template('addfacilities.html', flag=temp, own=owntemp)
    user = request.form
    print(user)
    userid = session['userid']

    powerback = user['powerback']
    security = user['security']
    laundry = user['laundry']
    cleaning = user['cleaning']

    gym = user['gym']
    wifi = user['wifi']
    hwater = user['hwater']
    ent = user['ent']
    fridge = user['fridge']
    microwave = user['microwave']

    gas = user['gas']
    sroom = user['sroom']
    wmachine = user['wmachine']
    extra = user['extra']
    hostelid = user['hostelid']

    cursor.execute('insert into facilities values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )', (powerback, security, laundry, cleaning, gym, wifi, hwater, ent, fridge, microwave, gas, sroom, wmachine, extra, hostelid))
    conn.commit()
    # res = cursor.fetchall()
    # l = len(res)

    # return render_template("addroom.html", flag=temp, own=owntemp, row=hostelid)
    return redirect(url_for('index'))

@app.route('/viewFacilities', methods=['GET'])
def viewFacilites():
    hstid = request.args.get('hostelid')
    cursor.execute('select * from facilities where hostelid = %s', (hstid,))
    res = cursor.fetchall()
    print(res[0])
    return render_template('viewFacilities.html', flag=temp, own=owntemp, row=res[0])

@app.route('/viewRooms', methods=['GET'])
def viewRooms():
    hstid = request.args.get('hostelid')
    cursor.execute('select * from roomtype rt, roomdet rd where rt.roomtypeid=rd.roomtypeid and hostelid = %s', (hstid,))
    res = cursor.fetchall()
    l = len(res)
    # print(res[0])
    return render_template('viewRooms.html', flag=temp, own=owntemp, row=res, l=l)

@app.route('/deleteHostel', methods=['GET'])
def deleteHostel():
    hstlid=request.args.get('hostelid')
    cursor.execute('delete from hostel where hostelid=%s',(hstlid,))
    conn.commit()
    l=0
    return render_template('deleteHostel.html', flag=temp, own=owntemp, l=l)
@app.route('/Sort', methods=['GET'])
def Sort():
    return render_template('Sort.html',flag=temp, own=owntemp)




@app.route('/ascSort',methods=['GET'])
def ascSort():
    qu = request.args.get('Sort')
    q = "select min(roomdet.cost),roomdet.hid,hostel.name,hostel.gen,hostel.stime,hostel.sam,hostel.etime,hostel.eam,hostel.address from roomdet,hostel where (hostel.hostelid=roomdet.hid) group by hid order by min(roomdet.cost) asc;"
    cursor.execute(q)
    res = cursor.fetchall()
    l = len(res)
    print('length is: ', l)

    return render_template('descSort.html',flag=temp, own=owntemp, row=res, l=l)




@app.route('/descSort',methods=['GET'])
def descSort():
    qu = request.args.get('Sort')
    q = "select min(roomdet.cost),roomdet.hid,hostel.name,hostel.gen,hostel.stime,hostel.sam,hostel.etime,hostel.eam,hostel.address from roomdet,hostel where (hostel.hostelid=roomdet.hid) group by hid order by min(roomdet.cost) desc;"
    cursor.execute(q)
    res = cursor.fetchall()
    l = len(res)
    print('length is: ', l)

    return render_template('descSort.html',flag=temp, own=owntemp, row=res, l=l)

@app.route('/viewHostel', methods=['GET'])
def viewHostel():
    hstid = request.args.get('hostelid')
    q = "select * from owner o, hostel h where h.hostelid=%s",(hstid,)
    cursor.execute(q)
    res = cursor.fetchall()
    # print(res[0])
    l = len(res[0])
    print('length is: ', l)
    return render_template("viewHostel.html", flag=temp, own=owntemp, l=l, row=res[0])
# return render_template("login.html", flag=temp, own=owntemp)



@app.route('/addReview',methods=['POST','GET'])
def addReview():
    if request.method == 'GET':
        hstid = request.args.get('hostelid')
        return render_template('addReview.html', flag=temp, own=owntemp, row=hstid)
    #user = request.form
    #print( user)
    #reviewer = user['reviewer']
    #reviews = user['reviews']
    #rating = user['rating']
    #hstid=user['hid']
    #cursor.execute('insert into review values(null, %s, %s, %s, %s)', (hstid,reviews,rating,reviewer))

    #conn.commit()
    return render_template("Review.html")


@app.route('/viewReview',methods=['GET'])
def viewReview():
    hstid = request.args.get('hostelid')
    cursor.execute('select * from review r,hostel h where h.hostelid=%s',(hstid,))
    res = cursor.fetchall()
    print(res)
    l=len(res)
    return render_template('viewReview.html',flag=temp,own=owntemp, row=res,l=l)
