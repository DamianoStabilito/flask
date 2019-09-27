from flask import Flask, render_template, request,session,redirect,url_for,flash,jsonify
from pyduino import *
import pymongo
import time
import os

#export FLASK_APP=test3.py
#flask run
#flask run -h 192.168.x.x for run in other devices 
#to show where is connect arduino
#lsof -i :5000 to show how process are active 
#sudo kill -9 <pid> to kill process

app = Flask(__name__)
app.secret_key = os.urandom(24)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]
x = mycol.delete_many({})

mylist = [
{ "name": "Damiano", "pwd": "1234"},
{ "name": "Simone", "pwd": "1111"},
{ "name": "Carlo", "pwd": "0000"},
{ "name": "admin", "pwd": "admin"}
]

x = mycol.insert_many(mylist)

# if your arduino was running on a serial port other than '/dev/ttyACM0/'
# declare: a = Arduino(serial_port='/dev/ttyXXXX')
print 'Establishing connection to Arduino...'
a = Arduino()
time.sleep(3)
print 'established!' 
LED1 = 1
LED2 = 2
LED3 = 3
APIN=0
time.sleep(1)

@app.route('/')
def index():
    if 'user' in session:
        if session['user'] == 'admin':
            return render_template('tester.html',author='admin')
        else:
            return render_template('home.html',author=session['user'])
    else:
        #return render_template('index.html')
        return redirect(url_for('do_login'))

@app.route('/offline.html')
def offline():
    return app.send_static_file('offline.html')


@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')

@app.route('/login', methods=['GET', 'POST'])
def do_login():
    if 'user' in session:
        if session['user'] == 'admin':
            return render_template('tester.html',author='admin')
        else:
            return render_template('home.html',author=session['user'])
    else:
        error = None
        if request.method == 'POST':
            for utenti in mycol.find():
                if utenti['name'] == request.form['username'] and utenti['pwd'] == request.form['password']:
                    session['user'] = request.form['username']
                    if session ['user'] == 'admin':
                        return render_template('tester.html',author='admin')
                    else:
                        return render_template('home.html',author=utenti["name"])
            print' error credenziali'
            error = 'Invalid Credentials. Please try again.'
        return render_template('index.html', error=error)


@app.route('/home', methods=['GET', 'POST'])
def home_user():
    if 'user' in session:
        if session['user'] == 'admin':
            return render_template('tester.html',author='admin')
        else:
            if request.method == 'POST':
            # if we press the turn on button
                if request.form['submit'] == 'Turn On room1': 
                    print 'TURN ON room1'
                    # turn on LED on arduino
                    a.digital_write(LED1,1)
                if request.form['submit'] == 'Turn Off room1': 
                    print 'TURN Off room1'
                    # turn on LED on arduino
                    a.digital_write(LED1,0)
                    # if we press the turn off button
                
                if request.form['submit'] == 'Turn On room2': 
                    print 'TURN ON room2'
                    # turn on LED on arduino
                    a.digital_write(LED2,1)
                if request.form['submit'] == 'Turn Off room2': 
                    print 'TURN Off room2'
                    # turn on LED on arduino
                    a.digital_write(LED2,0)

                if request.form['submit'] == 'Turn On room3': 
                    print 'TURN ON room3'
                    # turn on LED on arduino
                    a.digital_write(LED3,1)
                if request.form['submit'] == 'Turn Off room3': 
                    print 'TURN Off room3'
                    # turn on LED on arduino
                    a.digital_write(LED3,0)

                if request.form['submit'] == 'logout': 
                    print 'logout'
                    session.pop('user',None)
                    return redirect(url_for('do_login'))
                else:
                    pass
            return render_template('home.html',author=session['user']) 
    else:
        return redirect(url_for('do_login'))

@app.route('/tester', methods=['GET', 'POST'])
def tester():
    if 'user' in session:
        if session['user'] == 'admin':
            if request.method == 'POST':
                if request.form['submit'] == 'Start': 
                    print 'start'
                    a.digital_write(LED1,0) # turn LED off 
                    a.digital_write(LED2,0) # turn LED off 
                    a.digital_write(LED3,0) # turn LED off
                    time.sleep(2)
                    
                    analog_val = a.analog_read(APIN)
                    print 'ANALOG READ =',int((analog_val/1023.)*100)
                    print analog_val
                    time.sleep(2)
                    a.digital_write(LED1,1) # turn LED off 
                    time.sleep(2)
                    analog_val2 =  a.analog_read(APIN)
                    print 'ANALOG READ =',int((analog_val2/1023.)*100)
                    print analog_val2
                    if analog_val == analog_val2:
                        print ' led 1 non funzionante '
                        var1= 'NOT WORK! '
                    else:
                        print ' led 1 funzionante '
                        var1='WORK! '
                    print
                    a.digital_write(LED1,0) # turn LED off 
                    time.sleep(2)
                    analog_val = a.analog_read(APIN)
                    print 'ANALOG READ =',int((analog_val/1023.)*100)
                    print analog_val
                    time.sleep(2)
                    a.digital_write(LED2,1) # turn LED off 
                    time.sleep(2)
                    analog_val2 =  a.analog_read(APIN)
                    print 'ANALOG READ =',int((analog_val2/1023.)*100)
                    print analog_val2
                    if analog_val == analog_val2:
                        print ' led 2 non funzionante '
                        var2='NOT WORK! '
                    else:
                        print ' led 2 funzionante '
                        var2='WORK! '
                    
                    print
                    a.digital_write(LED2,0) # turn LED off 
                    time.sleep(2)
                    analog_val = a.analog_read(APIN)
                    print 'ANALOG READ =',int((analog_val/1023.)*100)
                    print analog_val
                    time.sleep(1)
                    a.digital_write(LED3,1) # turn LED off 
                    time.sleep(2)
                    analog_val2 =  a.analog_read(APIN)
                    print 'ANALOG READ =',int((analog_val2/1023.)*100)
                    print analog_val2
                    if analog_val == analog_val2:
                        print ' led 3 non funzionante '
                        var3='NOT WORK! '
                    else:
                        print ' led 3 funzionante '
                        var3='WORK! '
                    a.digital_write(LED3,0) # turn LED off 
                    print
                    flash('LED1: '+var1+' LED2: '+var2+' LED3: '+var3)
                    return render_template('tester.html',author='admin') 

                if request.form['submit'] == 'logout': 
                    session.pop('user',None)
                    return redirect(url_for('do_login'))
        else:
            return render_template('home.html',author=session['user'])
    else:
        return redirect(url_for('do_login'))
        
   


if __name__ == "__main__":
    # lets launch our webpage!
    # do 0.0.0.0 so that we can log into this webpage
    # using another computer on the same network later
    app.run(host='0.0.0.0')
    print 'CLOSING...'
    a.close()