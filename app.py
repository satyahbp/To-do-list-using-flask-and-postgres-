# this is a program to create apis using psycopg2

# importing flask, render_template, request and redirect
from flask import Flask, render_template, request, redirect
#importing psycopg2
import psycopg2

# initializing
app = Flask(__name__)

#connecting to database
db = psycopg2.connect(
    user= 'postgres',
    password = 'satya@123', 
    database = 'flaskdb', 
    host = '127.0.0.1', 
    port = '5432'
)
print("Successfully Connected to database!")
#getting the cursor
cur = db.cursor()


#first page
@app.route('/', methods = ['GET', 'POST'])
def start():
    # the request coming from the html page is post request, so when it receives a post request, it will execute the following
    if request.method == 'POST':
        #title variable is given the title received from the form, and so is for desc
        title = request.form['title']
        desc = request.form['desc']
        cur.execute("insert into todo(title, description) \
            values(%s, %s)", (title,desc)
        )
        db.commit()
        print("Inserted successfully!")
    cur.execute("select * from todo")
    rows = cur.fetchall()
    print(rows)
    return render_template('index.html', alltodo = rows)

#deleting a query
@app.route('/delete/<int:sno>')
def delete(sno):
    cur.execute("delete from todo where sno = %s", ([sno]))
    db.commit()
    print('Deleted Successfully!')
    return redirect('/')

#updating a query
@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        cur.execute("update todo set title = %s, description = %s where sno = %s",(title, desc, sno))
        db.commit()
        return redirect('/')
    cur.execute("select * from todo where sno = %s",([sno]))
    rows = cur.fetchone()
    print(rows)
    return render_template('update.html', todo = rows)

#running the program with debug = true
if __name__ ==   '__main__':
    app.run(debug= True)