from flask import current_app as app #alias for current running app
from flask import render_template,url_for,redirect,request
from application.models import *
from datetime import datetime,date

logged_admin=None
logged_inf=None
logged_spon=None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin_login",methods=["GET","POST"])
def admin_login():
    if request.method=="GET":
        return render_template("admin_login.html")
    if request.method=="POST":
        admin_name=request.form.get("admin_name")
        admin_password=request.form.get("admin_password")
        try:
            admin_from_db=Admin.query.get(admin_name)
            if admin_from_db:
                password_from_db=admin_from_db.admin_password
                if password_from_db==admin_password:
                    global logged_admin
                    logged_admin=admin_name
                    return redirect(url_for("admin_dashboard"))
                
                else:
                    return render_template("admin_login.html",message="Password failed")
            else:
                return render_template("admin_login.html",message="Id failed")

        except:
            return "some error"
    return render_template("admin_login.html")

@app.route("/admin_dashboard",methods=["GET","POST"])
def admin_dashboard():
    global logged_admin
    if not logged_admin:
        return redirect(url_for("admin_login"))
    inf=Influencer.query.all() 
    spon=Sponsor.query.all()
    adreq=Adrequest.query.all()
    camp=Campaign.query.all()
    #save data in each table as a list of objects
    if request.method=="GET":
        return render_template("admin_dashboard.html",inf=inf,spon=spon,adreq=adreq,camp=camp)
    if request.method=="POST":
        current_date=date.today().strftime('%d-%m-%Y')
        return render_template("ongoing_camp.html",current_date=current_date,camp=camp)
    
@app.route("/campaigns",methods=["GET"])
def campaigns():
    camp=Campaign.query.all()
    return render_template('campaigns.html',camp=camp)

@app.route("/sponsors",methods=["GET"])
def sponsors():
    spon=Sponsor.query.all()
    return render_template('sponsors.html',spon=spon)

@app.route("/influencers",methods=["GET"])
def influencers():
    inf=Influencer.query.all()
    return render_template('influencers.html',inf=inf)

@app.route("/adrequests",methods=["GET"])
def adrequests():
    adreq=Adrequest.query.all()
    return render_template('adrequests.html',adreq=adreq)

@app.route("/ongoing_camp",methods=["GET"])
def ongoing_camp():
    camp=Campaign.query.all()
    camplist=[]
    for x in camp:
        start_date=datetime.strptime(x.start_date,'%d-%m-%Y').date()
        end_date=datetime.strptime(x.end_date,'%d-%m-%Y').date()
        current_date=datetime.now().date()
        print(start_date,end_date,current_date)
        if start_date<=current_date and  end_date>=current_date:
            camplist.append(x)
    return render_template('ongoing_camp.html',camp=camplist)

@app.route("/campaign/<int:camp_id>/flag",methods=["GET","POST"])
def camp_flag(camp_id):
    c=Campaign.query.get(camp_id)
    c.flagged= not c.flagged
    db.session.commit()
    return render_template('camp_details.html',camp=c)

@app.route("/sponsor/<spon_id>/flag",methods=["GET","POST"])
def spon_flag(spon_id):
    s=Sponsor.query.get(spon_id)
    s.flagged= not s.flagged
    db.session.commit()
    return render_template('spon_details.html',spon=s)

@app.route("/influencer/<inf_id>/flag",methods=["GET","POST"])
def inf_flag(inf_id):
    i=Influencer.query.get(inf_id)
    i.flagged= not i.flagged
    db.session.commit()
    return render_template('inf_details.html',inf=i)

@app.route("/adreq_status",methods=["GET"])
def adreq_status():
    adstatus=[]
    adreq=Adrequest.query.all()
    for i in adreq:
        if i.status=="accepted":
            adstatus.append(i)
    return render_template("adreq_status.html",adreq=adstatus)

@app.route("/find_details",methods=["GET","POST"])
def find_details():
    if request.method=="GET":
        return render_template("find_details.html")
    if request.method=="POST":
        find_id=request.form.get("find_details")
        try:
            c=Campaign.query.get(find_id)
            i=Influencer.query.get(find_id)
            s=Sponsor.query.get(find_id)
            if c:
                return render_template("camp_details.html",camp=c)
            if s:
                return render_template("spon_details.html",spon=s)
            if i:
                return render_template("inf_details.html",inf=i)
                
            else:
                return render_template("find_details.html",message="Id incorrect")
        except:
            return render_template("find_details.html",message="Id failed")

@app.route("/campaign/<int:camp_id>",methods=["GET","POST"])
def camp_details(camp_id):
    camp=Campaign.query.get(camp_id)
    if request.method=="GET":
        return render_template("camp_details.html",camp=camp)
    if request.method=="POST":
        return url_for('/camp_flag',camp=camp)
    
@app.route("/influencer/<inf_id>",methods=["GET"])
def inf_details(inf_id):
    inf=Influencer.query.get(inf_id)
    return render_template("inf_details.html",inf=inf)

@app.route("/sponsor/<spon_id>",methods=["GET"])
def spon_details(spon_id):
    spon=Sponsor.query.get(spon_id)
    return render_template("spon_details.html",spon=spon)

@app.route('/campaign/<int:camp_id>/delete',methods=['GET'])
def del_camp(camp_id):
    del_camp=Campaign.query.get(camp_id)
    db.session.delete(del_camp)
    db.session.commit()
    return redirect("/admin_dashboard")

@app.route('/sponsor/<spon_id>/delete',methods=['GET'])
def del_spon(spon_id):
    del_spon=Sponsor.query.get(spon_id)
    db.session.delete(del_spon)
    db.session.commit()
    return redirect("/admin_dashboard")

@app.route('/influencer/<inf_id>/delete',methods=['GET'])
def del_inf(inf_id):
    del_inf=Influencer.query.get(inf_id)
    db.session.delete(del_inf)
    db.session.commit()
    return redirect("/admin_dashboard")

@app.route('/inf_reg', methods=['GET','POST'])
def inf_reg():
    if request.method=="GET":
        return render_template("inf_reg.html")
    if request.method=="POST":
        inf_id =request.form.get("inf_id")
        inf_name=request.form.get("inf_name")
        inf_password=request.form.get("inf_password")
        inf_category=request.form.get("inf_category")
        inf_niche=request.form.get("inf_niche")
        inf_reach=request.form.get("inf_reach")
        rating=request.form.get("rating")
        try:
            exist=Influencer.query.filter_by(inf_id=inf_id).first()
            if exist:
                return render_template("inf_reg.html",message="Influencer username already exists")
            else:
                new_inf=Influencer(inf_id=inf_id,inf_name=inf_name,inf_password=inf_password, inf_category= inf_category,inf_niche=inf_niche,inf_reach=inf_reach,rating=rating)
                db.session.add(new_inf)
                db.session.commit()
                global logged_inf
                logged_inf=inf_id
                return redirect(url_for("inf_dashboard",inf_id=inf_id))
        except:
            return "some error"
    return render_template("inf_reg.html")
    
@app.route("/inf_login",methods=["GET","POST"])
def inf_login():
    if request.method=="GET":
        return render_template("inf_login.html")
    if request.method=="POST":
        inf_id=request.form.get("inf_id")
        inf_password=request.form.get("inf_password")
        try:
            inf_from_db=Influencer.query.get(inf_id)
            if inf_from_db:
                password_from_db=inf_from_db.inf_password
                if password_from_db==inf_password:
                    global logged_inf
                    logged_inf=inf_id
                    return redirect(url_for("inf_dashboard",inf_id=inf_id))
                else:
                    return render_template("inf_login.html",message="Password failed")
            else:
                return render_template("inf_login.html",message="Id failed")

        except:
            return "some error"
    return render_template("inf_login.html")

@app.route("/influencer/<inf_id>/inf_dashboard",methods=["GET","POST"])  
def inf_dashboard(inf_id):
    global logged_inf
    if not logged_inf:
        return redirect(url_for("inf_login"))
    inf=Influencer.query.get(inf_id)  
    adreq=Adrequest.query.all()
    camps=Campaign.query.all()
    if request.method=="GET":
        return render_template("inf_dashboard.html",inf=inf,camps=camps,adreq=adreq)
    
@app.route("/active_camp/<inf_id>",methods=["GET"])
def active_camp(inf_id):
    inf=Influencer.query.get(inf_id)
    camp=Campaign.query.all()
    camplist=[]
    for x in camp:
        start_date=datetime.strptime(x.start_date,'%d-%m-%Y').date()
        end_date=datetime.strptime(x.end_date,'%d-%m-%Y').date()
        current_date=datetime.now().date()
        print(start_date,end_date,current_date)
        if start_date<=current_date and  end_date>=current_date and x.visibility=="public":
            camplist.append(x)
        print(camplist)
    return render_template('active_camp.html',camp=camplist,inf=inf)

@app.route("/campaign/<int:camp_id>/<inf_id>/inf",methods=["GET"])
def inf_camp_details(camp_id,inf_id):
    inf=Influencer.query.get(inf_id)
    camp=Campaign.query.get(camp_id)
    if request.method=="GET":
        return render_template("inf_camp_details.html",camp=camp,inf=inf)
    
@app.route("/adrequest/<int:adreq_id>/<inf_id>/inf",methods=["GET"])
def inf_ad_details(adreq_id,inf_id):
    inf=Influencer.query.get(inf_id)
    adreq=Adrequest.query.get(adreq_id)
    if request.method=="GET":
        return render_template("inf_ad_details.html",adreq=adreq,inf=inf)

@app.route("/adrequest/<inf_id>/new_adreq",methods=["GET","POST"])
def new_adreq(inf_id):
    newlist=[]
    inf=Influencer.query.get(inf_id)
    for x in inf.inf_req:
        if x.status=="pending":
            newlist.append(x)
        #print(newlist)
    return render_template('new_adreq.html',adreq=newlist,inf=inf)

@app.route('/influencer/<adreq_id>/<inf_id>/adaccept',methods=['GET','POST'])
def inf_adaccept(adreq_id,inf_id):
    newlist=[]
    inf=Influencer.query.get(inf_id)
    ad=Adrequest.query.get(adreq_id)
    ad.status="accepted"
    db.session.commit()
    for x in inf.inf_req:
        if x.status=="pending":
            newlist.append(x)
    return render_template("new_adreq.html",inf=inf,adreq=newlist)

@app.route('/influencer/<adreq_id>/<inf_id>/adreject',methods=['GET','POST'])
def inf_adreject(adreq_id,inf_id):
    newlist=[]
    inf=Influencer.query.get(inf_id)
    ad=Adrequest.query.get(adreq_id)
    ad.status="rejected"
    db.session.commit()
    for x in inf.inf_req:
        if x.status=="pending":
            newlist.append(x)
    return render_template("new_adreq.html",inf=inf,adreq=newlist)

@app.route('/influencer/<inf_id>/earnings',methods=["GET"])
def earnings(inf_id):
    earned=0
    ads=Adrequest.query.all()
    inf=Influencer.query.get(inf_id)
    for x in inf.inf_req:
        if x.status=="accepted":            
            earned+=x.pay_amount
        print(earned)
    return render_template("inf_dashboard.html",inf=inf,adreq=ads,earned=earned)

@app.route('/influencer/<inf_id>/<adreq_id>/negotiate',methods=["GET","POST"])
def negotiate(inf_id,adreq_id):
    newlist=[]    
    inf=Influencer.query.get(inf_id)
    ad=Adrequest.query.get(adreq_id)
    if request.method=="GET":
        return render_template("inf_negotiate.html",inf=inf,adreq=ad)
    if request.method=="POST":
        infid=request.form.get("inf_id")
        inf_msg=request.form.get("messages")
        if inf_id==infid:
            ad.messages+="//Influencer-"+infid +':'+ inf_msg+"//"
        print(inf_msg)
        db.session.commit()
        for x in inf.inf_req:
            if x.status=="pending":
                newlist.append(x)
        return render_template("new_adreq.html",inf=inf,adreq=newlist)
@app.route("/update_inf/<inf_id>",methods=["GET", "POST"])
def update_inf(inf_id):
    global logged_inf
    if not logged_inf:
        return redirect(url_for("inf_login"))
    if request.method=="GET":
        inf=Influencer.query.get(inf_id)
        return render_template("update_inf.html",i=inf)
    if request.method=="POST":
        inf_name=request.form.get("inf_name")
        inf_passsword=request.form.get("inf_password")
        inf_category=request.form.get("inf_category")
        inf_niche=request.form.get("inf_niche")
        inf_reach=request.form.get("inf_reach")
        rating=request.form.get("rating")
        update_inf=Influencer.query.get(inf_id)
        update_inf.inf_name=inf_name       
        update_inf.inf_passsword=inf_passsword
        update_inf.inf_category=inf_category
        update_inf.inf_niche=inf_niche
        update_inf.inf_reach=inf_reach
        update_inf.rating=rating
        db.session.commit()
        return redirect(url_for("inf_dashboard",inf_id=inf_id))


@app.route('/spon_reg', methods=['GET','POST'])
def spon_reg():
    if request.method=="GET":
        return render_template("spon_reg.html")
    if request.method=="POST":
        spon_id =request.form.get("spon_id")
        spon_name=request.form.get("spon_name")
        spon_password=request.form.get("spon_password")
        spon_industry=request.form.get("spon_industry")
        spon_budget=request.form.get("spon_budget")
        try:
            exist=Sponsor.query.filter_by(spon_id=spon_id).first()
            if exist:
                return render_template("spon_reg.html",message="Sponsor username already exists")
            else:
                new_spon=Sponsor(spon_id=spon_id,spon_name=spon_name,spon_password=spon_password, spon_industry=spon_industry,spon_budget=spon_budget)
                db.session.add(new_spon)
                db.session.commit()
                global logged_spon
                logged_spon=spon_id
                return redirect(url_for("spon_dashboard",spon_id=spon_id))
        except:
            return "some error"
    return render_template("spon_reg.html")
    
@app.route("/spon_login",methods=["GET","POST"])
def spon_login():
    if request.method=="GET":
        return render_template("spon_login.html")
    if request.method=="POST":
        spon_id=request.form.get("spon_id")
        spon_password=request.form.get("spon_password")
        try:
            spon_from_db=Sponsor.query.get(spon_id)
            if spon_from_db:
                password_from_db=spon_from_db.spon_password
                if password_from_db==spon_password:
                    global logged_spon
                    logged_spon=spon_id
                    return redirect(url_for("spon_dashboard",spon_id=spon_id))
                else:
                    return render_template("spon_login.html",message="Password failed")
            else:
                return render_template("spon_login.html",message="Id failed")

        except:
            return "some error"
    return render_template("spon_login.html")

@app.route("/sponsor/<spon_id>/spon_dashboard",methods=["GET","POST"])  
def spon_dashboard(spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    spon=Sponsor.query.get(spon_id) 
    adreq=Adrequest.query.all()
    ongoingcamps=[]
    for x in spon.spon_camp:
        start_date=datetime.strptime(x.start_date,'%d-%m-%Y').date()
        end_date=datetime.strptime(x.end_date,'%d-%m-%Y').date()
        current_date=datetime.now().date()
        print(start_date,end_date,current_date)
        if start_date<=current_date and  end_date>=current_date :
            ongoingcamps.append(x)
    print(ongoingcamps)
    if request.method=="GET":
        return render_template("spon_dashboard.html",spon=spon,camps=ongoingcamps,adreq=adreq)
    return render_template("spon_dashboard.html",spon=spon,camps=ongoingcamps,adreq=adreq)



@app.route("/create_camp/<spon_id>",methods=["GET", "POST"])
def create_camp(spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    if request.method=="GET":
        spon=Sponsor.query.get(spon_id)
        return render_template("create_camp.html",spon=spon)
    if request.method=="POST":
        camp_name=request.form.get("camp_name")
        start_date=request.form.get("start_date")
        end_date=request.form.get("end_date")
        budget=request.form.get("budget")
        visibility=request.form.get("visibility")
        goals=request.form.get("goals")
        spon_id=spon_id
        description=request.form.get("description")
        new_camp=Campaign(camp_name=camp_name,start_date=start_date,end_date=end_date,budget=budget,visibility=visibility,goals=goals,description=description,spon_id=spon_id)
        db.session.add(new_camp)
        db.session.commit()
        return redirect(url_for("spon_dashboard",spon_id=spon_id))
    
@app.route("/delete_camp/<spon_id>",methods=["GET", "POST"])
def delete_camp(spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    if request.method=="GET":
        spon=Sponsor.query.get(spon_id)
        camps=Campaign.query.all()
        return render_template("delete_camp.html",camps=camps,spon=spon)
    if request.method=="POST":
        camp_id=request.form.get("camp_id")
        del_camp=Campaign.query.get(camp_id)
        if del_camp:
            db.session.delete(del_camp)
            db.session.commit()
        print(del_camp)
        return redirect(url_for("spon_dashboard",spon_id=spon_id))

@app.route("/update_camp/<spon_id>",methods=["GET", "POST"])
def update_camp(spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    if request.method=="GET":
        spon=Sponsor.query.get(spon_id)
        camps=Campaign.query.all()
        return render_template("update_camp.html",camps=camps,spon=spon)
    if request.method=="POST":
        camp_name=request.form.get("camp_name")
        start_date=request.form.get("start_date")
        end_date=request.form.get("end_date")
        budget=request.form.get("budget")
        visibility=request.form.get("visibility")
        goals=request.form.get("goals")
        description=request.form.get("description")
        camp_id=request.form.get("camp_id")
        update_camp=Campaign.query.get(camp_id)
        update_camp.camp_name=camp_name       
        update_camp.start_date=start_date
        update_camp.end_date=end_date
        update_camp.budget=budget
        update_camp.visibility=visibility
        update_camp.goals= goals
        update_camp.description= description
        db.session.commit()
        return redirect(url_for("spon_dashboard",spon_id=spon_id))

@app.route("/create_ad/<spon_id>",methods=["GET", "POST"])
def create_ad(spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    if request.method=="GET":
        spon=Sponsor.query.get(spon_id)
        return render_template("create_ad.html",spon=spon)
    if request.method=="POST":
        camp_id=request.form.get("camp_id")
        pay_amount=request.form.get("pay_amount")
        status=request.form.get("status")
        inf_id=request.form.get("inf_id")
        requirements=request.form.get("requirements")
        messages=request.form.get("messages")
        spon_id=spon_id
        new_ad=Adrequest(camp_id=camp_id,pay_amount=pay_amount,status=status,inf_id=inf_id,requirements=requirements,messages=messages)
        db.session.add(new_ad)
        db.session.commit()
        return redirect(url_for("spon_dashboard",spon_id=spon_id))
    
@app.route("/delete_ad/<spon_id>",methods=["GET", "POST"])
def delete_ad(spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    if request.method=="GET":
        spon=Sponsor.query.get(spon_id)
        ads=Adrequest.query.all()
        return render_template("delete_ad.html",ads=ads,spon=spon)
    if request.method=="POST":
        ad_id=request.form.get("adreq_id")
        del_ad=Adrequest.query.get(ad_id)
        if del_ad:
            db.session.delete(del_ad)
            db.session.commit()
        print(del_ad)
        return redirect(url_for("spon_dashboard",spon_id=spon_id))
    
@app.route("/update_ad/<spon_id>",methods=["GET", "POST"])
def update_ad(spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    if request.method=="GET":
        spon=Sponsor.query.get(spon_id)
        ads=Adrequest.query.all()
        return render_template("update_ad.html",ads=ads,spon=spon)
    if request.method=="POST":
        camp_id=request.form.get("camp_id")
        pay_amount=request.form.get("pay_amount")
        status=request.form.get("status")
        inf_id=request.form.get("inf_id")
        requirements=request.form.get("requirements")
        messages=request.form.get("messages")
        ad_id=request.form.get("adreq_id")
        update_ad=Adrequest.query.get(ad_id)
        update_ad.camp_id=camp_id     
        update_ad.pay_amount=pay_amount
        update_ad.status=status
        update_ad.inf_id=inf_id
        update_ad.requirements=requirements
        update_ad.messages=messages
        db.session.commit()
        return redirect(url_for("spon_dashboard",spon_id=spon_id))

@app.route("/campaign/<int:camp_id>/<spon_id>/spon",methods=["GET"])
def spon_camp_details(camp_id,spon_id):
    spon=Sponsor.query.get(spon_id)
    camp=Campaign.query.get(camp_id)
    if request.method=="GET":
        return render_template("spon_camp_details.html",camp=camp,spon=spon)
    
@app.route("/adrequest/<int:adreq_id>/<spon_id>/spon",methods=["GET"])
def spon_ad_details(adreq_id,spon_id):
    spon=Sponsor.query.get(spon_id)
    adreq=Adrequest.query.get(adreq_id)
    camps=Campaign.query.all()
    if request.method=="GET":
        return render_template("spon_ad_details.html",adreq=adreq,spon=spon,camp=camps)
    return render_template("spon_ad_details.html",adreq=adreq,spon=spon,camp=camps)

@app.route('/sponsor/<int:adreq_id>/<spon_id>/adaccept',methods=['GET','POST'])
def spon_adaccept(adreq_id,spon_id):
    spon=Sponsor.query.get(spon_id)
    ad=Adrequest.query.get(adreq_id)
    ad.status="accepted"
    db.session.commit()
    return render_template("spon_ad_details.html",spon=spon,adreq=ad)

@app.route('/sponsor/<int:adreq_id>/<spon_id>/adreject',methods=['GET','POST'])
def spon_adreject(adreq_id,spon_id):
    spon=Sponsor.query.get(spon_id)
    ad=Adrequest.query.get(adreq_id)
    ad.status="rejected"
    db.session.commit()
    return render_template("spon_ad_details.html",spon=spon,adreq=ad)

@app.route('/sponsor/<spon_id>/<int:adreq_id>/negotiate',methods=["GET","POST"])
def spon_negotiate(spon_id,adreq_id):
    spon=Sponsor.query.get(spon_id)
    ad=Adrequest.query.get(adreq_id)
    if request.method=="GET":
        return render_template("spon_negotiate.html",spon=spon,adreq=ad)
    if request.method=="POST":
        sponid=request.form.get("spon_id")
        spon_msg=request.form.get("messages") 
        if spon.spon_id==sponid:
            ad.messages+="//Sponsor-"+sponid+ ":" + spon_msg+"//"
        db.session.commit()
        return render_template("spon_ad_details.html",spon=spon,adreq=ad)

@app.route("/admin_summary",methods=["GET"])
def admin_summary():
    global logged_admin
    if not logged_admin:
        return redirect(url_for('admin_login'))
    camps=Campaign.query.all()
    ads=Adrequest.query.all()
    spons=Sponsor.query.all()
    infs=Influencer.query.all()
    return render_template("admin_summary.html",camps=camps,spons=spons,infs=infs,ads=ads)



    


    
    

    
    

