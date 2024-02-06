from flask import Flask, render_template, request, session

app = Flask(__name__)

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="kusuma",
  database="mpml18_2023"
)

app.secret_key = 'your secret key'

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/manager')
def manager():
    return render_template('manager.html')

@app.route('/mlogin', methods = ['POST', 'GET'])
def mlogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM manager WHERE email = %s AND password = %s', (uid, pwd))
        account = cursor.fetchone()
        cursor.close()
        if account:
            session['mid'] = request.form['uid']
            session['mname'] = account[0]
            return render_template('mhome.html', result = account[0])
        else:
            return render_template('manager.html')
        
@app.route('/mhome')
def mhome():
    return render_template('mhome.html', result = session['mname'])

@app.route('/memp')
def memp():
    return render_template('memp.html')

@app.route('/ereg', methods = ['POST', 'GET'])
def ereg():
    if request.method == 'POST':
        eid = request.form['eid']
        name = request.form['name']
        uid = request.form['uid']
        pwd = request.form['pwd']
        mob = request.form['mob']
        te = request.form['te']
        sk = request.form['sk']
        com = request.form['com']
        var = (eid, name, uid, pwd, mob, te, sk,  com)
        cursor = mydb.cursor()
        cursor.execute('insert into emp values (%s, %s, %s, %s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return render_template('memp.html')
        else:
            cursor.close()
            return render_template('memp.html')

@app.route('/mcreq')
def mcreq():
    cursor = mydb.cursor()
    cursor.execute("select * from pro where status='pending'")
    account = cursor.fetchall()
    cursor.execute("select * from pro where status='Approved'")
    account1 = cursor.fetchall()
    cursor.close()
    return render_template('mcreq.html', result = account, result1 = account1)

@app.route('/mapp/<string:id>')
def mapp(id):
    cursor = mydb.cursor()
    cursor.execute("update pro set status ='Approved' WHERE clientid='" + id +"' and  managerid = '" + session['mid'] + "'")
    mydb.commit()
    if cursor.rowcount == 1:
        cursor.execute("select * from pro where status='pending'")
        account = cursor.fetchall()
        cursor.execute("select * from pro where status='Approved'")
        account1 = cursor.fetchall()
        cursor.close()
        return render_template('mcreq.html', result = account, result1 = account1)
    else:
        cursor.execute("select * from pro where status='pending'")
        account = cursor.fetchall()
        cursor.execute("select * from pro where status='Approved'")
        account1 = cursor.fetchall()
        cursor.close()
        return render_template('mcreq.html', result = account, result1 = account1)
    
@app.route('/mcmp/<string:id>')
def mcmp(id):
    cursor = mydb.cursor()
    cursor.execute("update pro set status ='Completed' WHERE clientid='" + id +"' and  managerid = '" + session['mid'] + "'")
    mydb.commit()
    if cursor.rowcount == 1:
        cursor.execute("select * from pro where status='pending'")
        account = cursor.fetchall()
        cursor.execute("select * from pro where status='approved'")
        account1 = cursor.fetchall()
        cursor.close()
        return render_template('mcreq.html', result = account, result1 = account1)
    else:
        cursor.execute("select * from pro where status='pending'")
        account = cursor.fetchall()
        cursor.execute("select * from pro where status='approved'")
        account1 = cursor.fetchall()
        cursor.close()
        return render_template('mcreq.html', result = account, result1 = account1)

@app.route('/massign')
def massign():
    return render_template('massign.html') 

@app.route('/mtask', methods = ['POST', 'GET'])
def mtask():
    if request.method == 'POST':
        tid = request.form['tid']
        tdet = request.form['tdet']
        uid = request.form['uid']
        var = (tid, tdet, uid, 'pending', 'pending')
        cursor = mydb.cursor()
        cursor.execute('insert into etask values (%s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return render_template('massign.html')
        else:
            cursor.close()
            return render_template('massign.html')

@app.route('/mst')
def mst():
    cursor = mydb.cursor()
    cursor.execute("select * from etask")
    account = cursor.fetchall()
    return render_template('mst.html', result = account)
        
@app.route('/mticket')
def mticket():
    cursor = mydb.cursor()
    cursor.execute("select * from ticket where status='pending'")
    account = cursor.fetchall()
    cursor.execute("select * from ticket where status='assign'")
    account1 = cursor.fetchall()
    cursor.close()
    return render_template('mticket.html', result = account, result1 = account1)

@app.route('/mtas/<string:id>')
def mtas(id):
    cursor = mydb.cursor()
    cursor.execute("update ticket set status ='assign' WHERE EmpId='" + id +"'")
    mydb.commit()
    if cursor.rowcount == 1:
        cursor.execute("select * from ticket where status='pending'")
        account = cursor.fetchall()
        cursor.execute("select * from ticket where status='assign'")
        account1 = cursor.fetchall()
        cursor.close()
        return render_template('mcreq.html', result = account, result1 = account1)
    else:
        cursor.execute("select * from ticket where status='pending'")
        account = cursor.fetchall()
        cursor.execute("select * from ticket where status='assign'")
        account1 = cursor.fetchall()
        cursor.close()
        return render_template('mcreq.html', result = account, result1 = account1)
    
@app.route('/mtcmp/<string:id>')
def mtcmp(id):
    cursor = mydb.cursor()
    cursor.execute("update pro set status ='Completed' WHERE EmpId='" + id +"'")
    mydb.commit()
    if cursor.rowcount == 1:
        cursor.execute("select * from pro where status='pending'")
        account = cursor.fetchall()
        cursor.execute("select * from pro where status='assign'")
        account1 = cursor.fetchall()
        cursor.close()
        return render_template('mcreq.html', result = account, result1 = account1)
    else:
        cursor.execute("select * from pro where status='pending'")
        account = cursor.fetchall()
        cursor.execute("select * from pro where status='assign'")
        account1 = cursor.fetchall()
        cursor.close()
        return render_template('mcreq.html', result = account, result1 = account1)
        
@app.route('/emp')
def emp():
    return render_template('emp.html')

@app.route('/elogin', methods = ['POST', 'GET'])
def elogin():
    if request.method == 'POST':
        eid = request.form['eid']
        uid = request.form['uid']
        pwd = request.form['pwd']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM emp WHERE EmpId=%s and email = %s AND password = %s', (eid, uid, pwd))
        account = cursor.fetchone()
        cursor.close()
        if account:
            session['eid'] = request.form['uid']
            session['ename'] = account[0]
            return render_template('ehome.html', result = account[0])
        else:
            return render_template('emp.html')

@app.route('/ehome')
def ehome():
    return render_template('ehome.html', result = session['ename'])

@app.route('/etask')
def etask():
    cursor = mydb.cursor()
    cursor.execute("select * from etask where status = %s and EmpId = %s", ('pending', session['eid']))
    account = cursor.fetchall()
    cursor.close()
    return render_template('etask.html', result = account)

@app.route('/etk')
def etk():
    cursor = mydb.cursor()
    cursor.execute("update etask set status ='Completed' WHERE EmpId='" + session['eid'] +"'")
    mydb.commit()
    if cursor.rowcount == 1:
        cursor.execute("select * from etask where status = %s and EmpId = %s", ('pending', session['eid']))
        account = cursor.fetchall()
        cursor.close()
        return render_template('etask.html', result = account)
    else:
        cursor.execute("select * from etask where status = %s and EmpId = %s", ('pending', session['eid']))
        account = cursor.fetchall()
        cursor.close()
        return render_template('etask.html', result = account)

@app.route('/eticket')
def eticket():
    cursor = mydb.cursor()
    cursor.execute("select * from ticket where status = %s and EmpId = %s", ('assign', session['eid']))
    account = cursor.fetchall()
    cursor.close()
    return render_template('eticket.html', result = account)

@app.route('/etic')
def etic():
    cursor = mydb.cursor()
    cursor.execute("update ticket set status ='Completed' WHERE EmpId='" + session['eid'] +"'")
    mydb.commit()
    if cursor.rowcount == 1:
        cursor.execute("select * from ticket where status = %s and EmpId = %s", ('assign', session['eid']))
        account = cursor.fetchall()
        cursor.close()
        return render_template('eticket.html', result = account)
    else:
        cursor.execute("select * from ticket where status = %s and EmpId = %s", ('assign', session['eid']))
        account = cursor.fetchall()
        cursor.close()
        return render_template('eticket.html', result = account)

@app.route('/client')
def client():
    return render_template('client.html')

@app.route('/clogin', methods = ['POST', 'GET'])
def clogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM client WHERE email = %s AND password = %s', (uid, pwd))
        account = cursor.fetchone()
        cursor.close()
        if account:
            session['cid'] = request.form['uid']
            session['cname'] = account[0]
            return render_template('chome.html', result = account[0])
        else:
            return render_template('client.html')

@app.route('/chome')
def chome():
    return render_template('chome.html', result = session['cname'])

@app.route('/cmanager')
def cmanager():
    cursor = mydb.cursor()
    cursor.execute("select * from manager")
    account = cursor.fetchall()
    cursor.close()
    return render_template('cmanager.html', result = account)

@app.route('/cpro')
def cpro():
    return render_template('cpro.html')

@app.route('/cpjt', methods = ['POST', 'GET'])
def cpjt():
    if request.method == 'POST':
        cid = session['cid']
        uid = request.form['mid']
        pwd = request.form['pdet']
        mob = request.form['sk']
        loc = request.form['da']
        var = (cid, uid, pwd, mob, loc, "pending")
        cursor = mydb.cursor()
        cursor.execute('insert into pro values (%s, %s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return render_template('cpro.html')
        else:
            cursor.close()
            return render_template('cpro.html')
        
@app.route('/csta')
def csta():
    cursor = mydb.cursor()
    cursor.execute("select * from pro where clientid='"+session["cid"]+"'")
    account = cursor.fetchall()
    cursor.close()
    return render_template('csta.html', result = account)

@app.route('/cticket')
def cticket():
    cursor = mydb.cursor()
    cursor.execute("select * from ticket")
    account = cursor.fetchall()
    cursor.close()
    return render_template('cticket.html', result = account)

@app.route('/nmanger')
def nmanager():
    return render_template('nmanager.html')

@app.route('/mreg', methods = ['POST', 'GET'])
def mreg():
    if request.method == 'POST':
        name = request.form['name']
        uid = request.form['uid']
        pwd = request.form['pwd']
        mob = request.form['mob']
        com = request.form['com']
        loc = request.form['loc']
        var = (name, uid, pwd, mob, com, loc)
        cursor = mydb.cursor()
        cursor.execute('insert into manager values (%s, %s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return render_template('manager.html')
        else:
            cursor.close()
            return render_template('nmanager.html')

@app.route('/nclient')
def nclient():
    return render_template('nclient.html')

@app.route('/creg', methods = ['POST', 'GET'])
def creg():
    if request.method == 'POST':
        name = request.form['name']
        uid = request.form['uid']
        pwd = request.form['pwd']
        mob = request.form['mob']
        loc = request.form['loc']
        var = (name, uid, pwd, mob, loc)
        cursor = mydb.cursor()
        cursor.execute('insert into client values (%s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return render_template('client.html')
        else:
            cursor.close()
            return render_template('nclient.html')

@app.route('/logout')
def logout():
    session.pop('mname', None)
    session.pop('mid', None)
    session.pop('ename', None)
    session.pop('eid', None)
    session.pop('cname', None)
    session.pop('cid', None)
    return render_template('index.html')

if __name__ == '__main__':
   app.run()