from flask import Flask, render_template,request,redirect
from cs50 import SQL


app = Flask(__name__)
# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///poornilogin.db")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

def apology(message,url, code=400):
    """Render message as an apology to user."""
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message),goto = url,msg=message)



@app.route("/")
def index():
    return render_template("index.html",title = "Index page")

@app.route("/update_std",methods=["GET","POST"])
def update_std():
    if request.method == "POST":
        rollno = request.form.get("rollno")
        name = request.form.get("name")
        city = request.form.get("city")
        dob = request.form.get("dob")        
        if rollno:
            print("ko")
            rows = db.execute("select * from student_details where roll_no = ?",rollno)
            print(rows)
            if len(rows) == 0:
                 msg = "No students are there in this database"
                 return apology(msg,url = "/update_std")
            else:
                if name:
                    db.execute("update  student_details set name=? where roll_no=?",name,rollno)
                if city:
                    db.execute("update  student_details set city=? where roll_no=?",city,rollno)
                if dob:
                    db.execute("update  student_details set DOB=? where roll_no=?",dob,rollno)
                return redirect("/master2")
        else:
            return redirect("/master2")
                      
    else:
        print("hi")
        rows = db.execute("select * from student_details")
        l=[]
        for i in rows:
            l.append(i["roll_no"])
        print(l)
        return render_template("update_std.html",rows=l)

@app.route("/add_std",methods=["GET","POST"])
def add_std():
    if request.method == "POST":
        print("heloadd")
        name = request.form.get("name")
        city = request.form.get("city")
        dob = request.form.get("dob")
        flag=request.form.get("flag")
       
        if flag =="False":
            print("flag add",flag)            
        elif name and city and dob:
            
            db.execute("insert into student_details(name,city,DOB) values(?,?,?)",name,city,dob)
        return redirect("/master2")
    else:
       
        return render_template("add_std.html")

@app.route("/del_std",methods=["GET","POST"])
def del_std():
    if request.method == "POST":
        name = request.form.get("name")
        rollno = request.form.get("rollno")
        # flag=request.form.get("flag")
        
        # print(flag)
        # if flag == "False":
        if not name or not rollno:
            msg = "Provide all fields"
            # print(msg)
            return apology(msg,url = "/del_std")
        #     print(flag)
        elif name and rollno:
            rows = db.execute("select * from student_details")
            flag = False
            if len(rows) != 0:
                for i in rows:
                    if i["name"] == name and i["roll_no"] == int(rollno):
                        flag = True
                        break
            else:
                flag = False
            if flag:
                db.execute("delete from student_details where name = ? and roll_no = ?;",name,rollno)
                return redirect("/master2")
            else:
                msg = "Incorrect details"
                return apology(msg,url = "/del_std")
        return redirect("/master2")

    else:
        return render_template("del_std.html")

@app.route("/master1")
def get_std_details():
    rows = db.execute("select * from student_details")
    return render_template("get_std_details.html", rows = rows)

@app.route("/master2",methods=["GET","POST"])
def modify_std_details():
    if request.method == "POST":
        # buttonid = request.form.get("add")
        # if buttonid == "add":
            return redirect("/add_std")
    else:
        rows = db.execute("select * from student_details")
        return render_template("modify_std_details.html", rows = rows)



@app.route("/Administrator2",methods=["GET","POST"])
def modify_user_details():
    if request.method == "POST":
        name = request.form.get("adminname")
        pwd = request.form.get("password")
        rows = db.execute("select * from login_details")

        # error checking
        if not name or not pwd:
            msg = "Provide all fields"
            # print(msg)
            return apology(msg,url = "/Administrator2")

        # SUCCESSFUL LOGIN
        if name == "priya" and pwd == "poorni":
            return render_template("modify_user_details.html",title = "User Details",rows = rows)
        return apology("Give valid details",url = "/Administrator1")

    else:
        return render_template("admin_login.html",title= "Admin page",admin = "/Administrator1")


@app.route("/Administrator1",methods=["GET","POST"])
def get_user_details():
    if request.method == "POST":
        name = request.form.get("adminname")
        pwd = request.form.get("password")
        rows = db.execute("select * from login_details")

        # error checking
        if not name or not pwd:
            msg = "Provide all fields"
            # print(msg)
            return apology(msg,url = "/Administrator1")
        # SUCCESSFUL LOGIN

        if name == "priya" and pwd == "poorni":
            return render_template("get_user_details.html",title = "User Details",rows = rows)

        return apology("Give valid details",url = "/Administrator1")

    else:
        return render_template("admin_login.html",title= "Admin page",admin = "/Administrator1")


@app.route("/p")
def go_to_home():
    return render_template("p.html",title = "Home Page")

@app.route("/login",methods=["GET","POST"])
def login():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        name = request.form.get("username")
        pwd = request.form.get("password")
        rows = db.execute("select username,password from login_details")

        # SUCCESSFUL LOGIN
        for user in rows:
            print(user)
            if user["username"] == name and user["password"] == pwd:
                return redirect("/p")

        return apology("Give valid details",url = "/login")

        # error checking
        if not name or not password:
            msg = "Provide all fields"
            print(msg)
            return apology(msg)
    else:
        return render_template("login.html",title = "Login Page")
