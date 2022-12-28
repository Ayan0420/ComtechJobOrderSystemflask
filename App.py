
# Imports
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, or_
import os

# --------------------------------------------------------------------------------------------------------
# creating the app
app = Flask(__name__)
app.secret_key = os.urandom(24)
# --------------------------------------------------------------------------------------------------------
#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ctjo_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app) #creating variable for the database which is 'db'

#Creating model table for our ctjoborder_db database to create the model "from App import db, db.create_all()"
class Data(db.Model):
    #Basic customer information
    id = db.Column(db.Integer, primary_key = True)
    job_id = db.Column(db.String(10))
    job_date = db.Column(db.String(100))
    cus_name = db.Column(db.String(100))
    cus_address = db.Column(db.String(100))
    cus_phone = db.Column(db.String(100))
    #unit information
    unit_model = db.Column(db.String(100))
    unit_specs = db.Column(db.String(100))
    unit_accessories = db.Column(db.String(100))
    work_perf = db.Column(db.String(100))
    #job payment data
    s_charge = db.Column(db.String(100))
    s_paymeth = db.Column(db.String(100))
    s_downpay = db.Column(db.String(100))
    s_bal = db.Column(db.String(100))
    s_status = db.Column(db.String(100))
    #Parts ordered data
    p_parts =db.Column(db.String(100))
    p_ord_date = db.Column(db.String(100))
    p_supp = db.Column(db.String(100))
    p_price = db.Column(db.String(100))
    p_ord_status = db.Column(db.String(100))
    p_installed = db.Column(db.String(100))
    #parts payment data
    p_downpay = db.Column(db.String(100))
    p_bal = db.Column(db.String(100))
    p_status = db.Column(db.String(100))
    p_rel_date = db.Column(db.String(100))
    # initializing all the parameters in the model
    def __init__(self, job_id, job_date, cus_name, cus_address, cus_phone, unit_model, unit_specs,
                unit_accessories, work_perf, s_charge, s_paymeth, s_downpay, s_bal, s_status, p_parts,
                p_ord_date, p_supp, p_price, p_ord_status, p_installed, p_downpay, p_bal, p_status, p_rel_date):
        
        self.job_id = job_id
        self.job_date = job_date
        self.cus_name = cus_name
        self.cus_address = cus_address
        self.cus_phone = cus_phone
        self.unit_model = unit_model
        self.unit_specs =  unit_specs
        self.unit_accessories = unit_accessories
        self.work_perf = work_perf
        self.s_charge = s_charge
        self.s_paymeth = s_paymeth
        self.s_downpay = s_downpay
        self.s_bal = s_bal
        self.s_status = s_status
        self.p_parts = p_parts
        self.p_ord_date = p_ord_date
        self.p_supp = p_supp
        self.p_price = p_price
        self.p_ord_status = p_ord_status
        self.p_installed = p_installed
        self.p_downpay = p_downpay
        self.p_bal = p_bal
        self.p_status = p_status
        self.p_rel_date = p_rel_date


db.create_all()
# --------------------------------------------------------------------------------------------------------
# Creating the login page

#admin users credentials
users = {"Admin": ("null", "password"), "user":("null", "password")}
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#login required wrapper this will authenticate the admin user
import functools

def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs): 
        if "username" in session: #if we are in session
            return func(*args, **kwargs) #we can do what ever functions in the page
        else:
            flash("Please login again to manage job orders!")
            return redirect(url_for("login")) #if not redirect to login page

    return secure_function  

def already_logged_in(func):
    @functools.wraps(func)
    def secure_function2(*args, **kwargs):
        if "username" in session:
            return redirect(url_for("dashboard"))
        return func(*args, **kwargs) 

    return secure_function2 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.route("/", methods=["GET", "POST"])
@already_logged_in
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username][1] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template("login.html", error=error)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('dashboard'))


# --------------------------------------------------------------------------------------------------------
@app.route('/dashboard')
@login_required

def dashboard():
    # page = request.args.get('page', 1, type=int)
    all_data = Data.query.order_by(desc(Data.id)).limit(10).all() 
    msg2 = "Recent Jobs:"   #retrieving data and posting it in reverse order and limited to 5 items
# paginate(per_page=6, page=page)
   
    return render_template("dashboard.html", job_order = all_data, msg2=msg2, admin_name=session["username"]) # this will be called for the data table in the page

# =========================================================================================================
# Search
@app.route("/search", methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_input']
        search = "%{0}%".format(search_value)
        msg = "  Note: If no result found in the table, the data does not exist. -Ayan"
        print_search = "Search results for: " + str('"') + search_value + str('"')
        results = Data.query.filter(or_(Data.job_id.like(search), 
                                        Data.job_date.like(search),
                                        Data.cus_name.like(search),
                                        Data.cus_address.like(search),
                                        Data.cus_phone.like(search),
                                        Data.unit_model.like(search),
                                        Data.unit_specs.like(search),
                                        Data.unit_accessories.like(search),
                                        Data.work_perf.like(search),
                                        Data.s_status.like(search),
                                        Data.p_parts.like(search),
                                        Data.p_ord_date.like(search),
                                        Data.p_ord_status.like(search),
                                        Data.p_status.like(search),
                                        )).all()
        return render_template('dashboard.html', job_order= results, search_input= print_search, msg=msg)
         

    else:
        return redirect(url_for('dashboard'))
 
# =========================================================================================================
#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        job_id = request.form['job_id']
        job_date = request.form['job_date']
        cus_name = request.form['cus_name']
        cus_address = request.form['cus_address']
        cus_phone = request.form['cus_phone']

        unit_model = request.form['unit_model']
        unit_specs = request.form['unit_specs']
        unit_accessories = request.form['unit_accessories']
        work_perf = request.form['work_perf']

        s_charge = request.form['s_charge']
        s_paymeth = request.form['s_paymeth']
        s_downpay = request.form['s_downpay']
        s_bal = request.form['s_bal']
        s_status = request.form['s_status']

        p_parts = request.form['p_parts']
        p_ord_date = request.form['p_ord_date']
        p_supp = request.form['p_supp']
        p_price = request.form['p_price']
        p_ord_status = request.form['p_ord_status']
        p_installed = request.form['p_installed']

        p_downpay = request.form['p_downpay']
        p_bal = request.form['p_bal']
        p_status = request.form['p_status']
        p_rel_date = request.form['p_rel_date']

        
        my_data = Data(job_id, job_date, cus_name, cus_address, cus_phone, unit_model, unit_specs,
                unit_accessories, work_perf, s_charge, s_paymeth, s_downpay, s_bal, s_status, p_parts,
                p_ord_date, p_supp, p_price, p_ord_status, p_installed, p_downpay, p_bal, p_status, p_rel_date)
        
        db.session.add(my_data)
        db.session.commit()

        flash("Job Order Added Successfuly!")

        return redirect(url_for('dashboard'))

# =========================================================================================================
#this is our update route where we are going to update our job order
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.job_id = request.form['job_id']
        my_data.job_date = request.form['job_date']
        my_data.cus_name = request.form['cus_name']
        my_data.cus_address = request.form['cus_address']
        my_data.cus_phone = request.form['cus_phone']

        my_data.unit_model = request.form['unit_model']
        my_data.unit_specs = request.form['unit_specs']
        my_data.unit_accessories = request.form['unit_accessories']
        my_data.work_perf = request.form['work_perf']

        my_data.s_charge = request.form['s_charge']
        my_data.s_paymeth = request.form['s_paymeth']
        my_data.s_downpay = request.form['s_downpay']
        my_data.s_bal = request.form['s_bal']
        my_data.s_status = request.form['s_status']

        my_data.p_parts = request.form['p_parts']
        my_data.p_ord_date = request.form['p_ord_date']
        my_data.p_supp = request.form['p_supp']
        my_data.p_price = request.form['p_price']
        my_data.p_ord_status = request.form['p_ord_status']
        my_data.p_installed = request.form['p_installed']
        
        my_data.p_downpay = request.form['p_downpay']
        my_data.p_bal = request.form['p_bal']
        my_data.p_status = request.form['p_status']
        my_data.p_rel_date = request.form['p_rel_date']

        db.session.commit()
        flash("Job Updated Successfully!")

        return redirect(url_for('dashboard'))

# =========================================================================================================
#This route is for deleting our job order
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Job Deleted Successfully!")

    return redirect(url_for('dashboard'))

# =========================================================================================================

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=1234, threaded=True)
