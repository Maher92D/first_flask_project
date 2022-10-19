
from flask import Flask, render_template, request,redirect
from database import database


app = Flask(__name__)
app.app_context()
db = database("db")
tablename="mytable"
@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "GET":
        result = db.sqlquery(f'''SELECT * FROM {tablename} ''')
        print(result)
        return render_template("index.html",tasks=result,title=tablename)
    else:
        try:
            first = request.form["first"]
            second = request.form["second"]
            db.sql_insert(tablename, [first,second])
            return redirect("/")

        except:
            return "there has been a problem inserting"


@app.route("/delete/<int:id>" )
def deleteitem(id):
    try:
        db.sql_delete_by_id(tablename,id)
        return redirect("/")
    except:
        return "there has been a problem deleting"


@app.route("/update/<int:id>",methods=["POST", "GET"])
def updateid(id):
    if request.method == "POST":
        first = request.form["first"]
        second = request.form["second"]
        db.sql_update_by_id(tablename, [first, second],id)
        return redirect("/")
    else:
        values = db.sql_select_by_id(tablename,id)
        return render_template("update.html",values=values[0])

@app.route("/save",methods=["POST", "GET"])
def save():
    if request.method == "GET":
        db.commit()
        result = db.sqlquery(f'''SELECT * FROM {tablename} ''')
        return render_template("index.html", tasks=result,title=tablename)

if __name__ == '__main__':
    app.run(debug=True)



