from flask import current_app as app #alias for current running app
from flask import render_template,url_for,redirect,request
from application.models import *
from datetime import datetime,date
import decimal
#stats
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

logged_admin=None
logged_inf=None
logged_spon=None



#ADMIN

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
    if s.flagged==1:
        for i in s.spon_camp:
            i.flagged= 1
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
    adreq=Adrequest.query.all()
    return render_template("adreq_status.html",adreq=adreq)

@app.route("/campaign/<int:camp_id>",methods=["GET","POST"])
def camp_details(camp_id):
    camp=Campaign.query.get(camp_id)
    if request.method=="GET":
        return render_template("camp_details.html",camp=camp)
    if request.method=="POST":
        return url_for('/camp_flag',camp=camp)
    
@app.route("/adrequest/<int:adreq_id>",methods=["GET","POST"])
def ad_details(adreq_id):
    adreq=Adrequest.query.get(adreq_id)
    if request.method=="GET":
        return render_template("ad_details.html",adreq=adreq)
    
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

@app.route("/find_details/<search_type>",methods=["GET","POST"])
def adminsearch(search_type):
    global logged_admin
    if not logged_admin:
        return redirect(url_for("admin_login"))
    if request.method=="GET":
        if search_type=="common":
            return render_template("asearch_common.html")
        if search_type=="spon_name":
            return render_template("asearch_spon.html")
        if search_type=="inf_name":            
            return render_template("asearch_inf.html")
        if search_type=="camp_name":            
            return render_template("asearch_camp.html")
    if request.method=="POST":
        if search_type=="spon_name":
            spon_name=request.form.get("spon_name").strip()
            result=Sponsor.query.filter(Sponsor.spon_name.ilike(f"%{spon_name}%")).all()
            return render_template("aresult_spon.html",result=result)
        if search_type=="inf_name":
            inf_name=request.form.get("inf_name").strip()
            result=Influencer.query.filter(Influencer.inf_name.ilike(f"%{inf_name}%")).all()
            return render_template("aresult_inf.html",result=result)
        if search_type=="camp_name":
            camp_name=request.form.get("camp_name").strip()
            result=Campaign.query.filter(Campaign.camp_name.ilike(f"%{camp_name}%")).all()
            return render_template("aresult_camp.html",result=result)

@app.route("/admin_summary",methods=["GET"])
def admin_summary():
    global logged_admin
    if not logged_admin:
        return redirect(url_for('admin_login'))
    camps=Campaign.query.all()
    ads=Adrequest.query.all()
    spons=Sponsor.query.all()
    infs=Influencer.query.all()
    adacpt,adrej,adpend=0,0,0
    for i in ads:
        if i.status=="accepted":
            adacpt+=1
        if i.status=="rejected":
            adrej+=1
        if i.status=="pending":
            adpend+=1
    plt.title('Ad request status')
    y = np.array([adacpt,adrej,adpend])
    colors = ['#4CAF50', '#F44336', '#FFEB3B']
    mylabels1= ["Accepted", "Rejected", "Pending"]
    plt.pie(y, labels = mylabels1,autopct='%1.1f%%',colors=colors)
    plt.savefig('MAD1project code/static/ad_status.png')
    plt.close()

    unsp,fsp,uninf,finf=0,0,0,0
    for i in spons:
        if i.flagged==0:
            unsp+=1
        else:
            fsp+=1  
    for i in infs:
        if i.flagged==0:
            uninf+=1
        else:
            finf+=1
    plt.title("Flagged/unflagged Users")
    y = np.array([unsp,fsp,uninf,finf])
    mylabels2= ["unflagged sponsors","flagged sponsors","unflagged influencers","flagged influencers"]
    plt.pie(y, labels = mylabels2,autopct='%1.1f%%')
    plt.savefig('MAD1project code/static/users_flagged.png')
    plt.close()

    cname,cprog=[],[]
    for camp in camps:
        cname.append(camp.camp_name)
        cprog.append(camp.progress)
    x_labels = cname
    y_values = cprog
    plt.title('Campaign Progress')
    plt.bar(x_labels, y_values, color='green', width=0.5)
    plt.xlabel('Campaigns')
    plt.ylabel('Progress')
    # Add space between x-values
    plt.xticks(range(len(x_labels)), x_labels, rotation=40, ha='right', fontsize=10)  # Adjust rotation, alignment, and font size
    plt.tight_layout() 
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for i in range(len(x_labels)):
        plt.text(i, y_values[i] + 1, f'{y_values[i]}%', ha='center', va='bottom')#percent
    plt.savefig('MAD1project code/static/campaign_progress.png')
    plt.close()

    priv,pub=0,0
    for i in camps:
        if i.visibility=="private":
            priv+=1
        elif i.visibility=="public":
            pub+=1   
    plt.title('Campaign visibility')
    y = np.array([priv,pub])
    mylabels2= ["Private","Public"]
    plt.pie(y, labels = mylabels2,autopct='%1.1f%%')
    plt.savefig('MAD1project code/static/camp_visibility.png')
    plt.close()
    return render_template("admin_summary.html",spons=spons,infs=infs,camps=camps,ads=ads)




#INFLUENCER


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
        try:
            exist=Influencer.query.filter_by(inf_id=inf_id).first()
            if exist:
                return render_template("inf_reg.html",message="Influencer username already exists")
            else:
                new_inf=Influencer(inf_id=inf_id,inf_name=inf_name,inf_password=inf_password, inf_category= inf_category,inf_niche=inf_niche,inf_reach=inf_reach)
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
    camplist=[]
    camp=Campaign.query.all()
    inf=Influencer.query.get(inf_id)
    for x in camp:
        start_date=datetime.strptime(x.start_date,'%d-%m-%Y').date()
        end_date=datetime.strptime(x.end_date,'%d-%m-%Y').date()
        current_date=datetime.now().date()
        if start_date<=current_date and  end_date>=current_date:
            camplist.append(x)
    print(camplist)
    for x in inf.inf_req:
        if x.status=="pending" and inf.flagged==0:
            newlist.append(x)
    print(newlist)
    last=[]
    for camp in camplist:
        for i in camp.camp_ads:
            print(i)
            for a in newlist:
                if a==i:
                    last.append(a)
            print(last)
    print(newlist)
    print(last)
    return render_template('new_adreq.html',adreq=last,inf=inf,camp=camplist)

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

@app.route('/influencer/<inf_id>/<adreq_id>/negotiate',methods=["GET","POST"])
def negotiate(inf_id,adreq_id):
    inf=Influencer.query.get(inf_id)
    ad=Adrequest.query.get(adreq_id)
    if request.method=="GET":
        return render_template("inf_negotiate.html",inf=inf,adreq=ad)
    if request.method=="POST":
        infid=request.form.get("inf_id")
        inf_msg=request.form.get("messages")
        if inf_id==infid:
            ad.messages+=infid +"(Influencer)"+':'+ inf_msg+"//"
            ad.messages = ad.messages.replace('//', '\n')
        db.session.commit()
        return render_template("inf_dashboard.html",inf=inf)
    
@app.route('/influencer/<inf_id>/<camp_id>/request',methods=["GET","POST"])
def inf_request(inf_id,camp_id):
    inf=Influencer.query.get(inf_id)
    camp=Campaign.query.get(camp_id)
    if request.method=="GET":
        return render_template("inf_request.html",inf=inf,camp=camp)
    if request.method=="POST":
        infid=request.form.get("inf_id")
        inf_msg=request.form.get("messages")
        if inf_id==infid:
            camp.request+=infid +"(Influencer)"+':'+ inf_msg+"//"
            camp.request = camp.request.replace('//', '\n')
        db.session.commit()
        return render_template("inf_camp_details.html",inf=inf,camp=camp)

@app.route('/influencer/<inf_id>/earnings',methods=["GET"])
def earnings(inf_id):
    earned=0
    ads=Adrequest.query.all()
    inf=Influencer.query.get(inf_id)
    for x in inf.inf_req:
        if x.status=="accepted":            
            earned+=x.pay_amount
        #print(earned)
    return render_template("inf_dashboard.html",inf=inf,adreq=ads,earned=earned)

@app.route('/influencer/<inf_id>/progress',methods=["GET","POST"])
def progress(inf_id):
    inf=Influencer.query.get(inf_id)
    campid=[]
    for i in inf.inf_req:
        if i.status=="accepted":
            campid.append(i.camp_id)
    uniquecamps=set(campid)
    lcamp=list(uniquecamps)
    camps=[]
    for i in lcamp:
        c=Campaign.query.get(i)
        camps.append(c)
    if request.method=="GET":
        return render_template("inf_progress.html",inf=inf,camps=camps)
    if request.method=="POST":
        progress=request.form.get("progress")
        camp_id=request.form.get("camp_id")
        update_camp=Campaign.query.get(camp_id)
        update_camp.progress= progress
        db.session.commit()
        return render_template("inf_progress.html",camps=camps,inf=inf)
   
@app.route("/update_inf/<inf_id>",methods=["GET", "POST"])
def update_inf(inf_id):
    global logged_inf
    if not logged_inf:
        return redirect(url_for("inf_login"))
    if request.method=="GET":
        inf=Influencer.query.get(inf_id)
        return render_template("update_inf.html",inf=inf)
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

@app.route("/infsearch/<search_type>/<inf_id>", methods=["GET", "POST"])
def infsearch(search_type,inf_id):
    global logged_inf
    if not logged_inf:
        return redirect(url_for("inf_login"))
    inf=Influencer.query.get(inf_id)
    if request.method=="GET":
        if search_type=="common":
            if inf.flagged==1:
                return render_template("isearch_common.html",inf=inf,message="You do not have permission to perform this action. Please contact the admin for assistance.")
            return render_template("isearch_common.html",inf=inf)
        if search_type=="niche":            
            return render_template("isearch_niche.html",inf=inf)
        if search_type=="camp_name":            
            return render_template("isearch_camp.html",inf=inf)
    if request.method=="POST":
        if search_type=="niche":
            niche=request.form.get("niche").strip()
            sresult=Campaign.query.filter(Campaign.niche.ilike(f"%{niche}%")).all()
            return render_template("iresult_camp.html",sresult=sresult,inf=inf)
        if search_type=="camp_name":
            camp_name=request.form.get("camp_name").strip()
            sresult=Campaign.query.filter(Campaign.camp_name.ilike(f"%{camp_name}%")).all()
            return render_template("iresult_camp.html",sresult=sresult,inf=inf)
        
@app.route("/inf_summary/<inf_id>",methods=["GET"])
def inf_summary(inf_id):
    global logged_inf
    if not logged_inf:
        return redirect(url_for('inf_login'))
    camps=Campaign.query.all()
    ads=Adrequest.query.all()
    spons=Sponsor.query.all()
    infs=Influencer.query.all()
    inf=Influencer.query.get(inf_id)
    adacpt,adrej,adpend=0,0,0
    for i in inf.inf_req:
        if i.status=="accepted":
            adacpt+=1
        if i.status=="rejected":
            adrej+=1
        if i.status=="pending":
            adpend+=1
    if adpend!=0 or adacpt!=0 or adrej!=0:
        y = np.array([adacpt,adrej,adpend])
        y = np.nan_to_num(y, nan=0)  # Replace NaN values with 0
        mylabels1= ["Accepted", "Rejected", "Pending"]
        colors = ['#4CAF50', '#F44336', '#FFEB3B']
        plt.title('Ad request status')
        total = sum(y)
        autopct = lambda pct: f'{int(round(pct * total / 100.0))}'
        plt.pie(y, labels=mylabels1, autopct=autopct, colors=colors)
        #plt.pie(y, labels = mylabels1,autopct='%1.1f%%',colors=colors)
        plt.savefig('MAD1project code/static/i_ad_status.png')
        plt.close()

    camps=[]
    for i in inf.inf_req:
        if i.status=="accepted":
            camps.append(i.camp_id)
    uniquecamps=set(camps)
    lcamp=list(uniquecamps)
    cname,cprog=[],[]
    for i in lcamp:
        c=Campaign.query.get(i)
        cname.append(c.camp_name)
        cprog.append(c.progress)
    x_labels = cname
    y_values = cprog
    if cname!=[] and cprog!=[]:
        plt.bar(x_labels, y_values, color='blue', width=0.5)
        plt.xticks(range(len(x_labels)), x_labels, rotation=40, ha='right', fontsize=10)  # Adjust rotation, alignment, and font size
        plt.title('Campaign Progress')
        plt.xlabel('Campaigns')
        plt.ylabel('Progress')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout() 
        for i in range(len(x_labels)):
            plt.text(i, y_values[i] + 1, f'{y_values[i]}%', ha='center', va='bottom')#percent
        plt.savefig('MAD1project code/static/i_campaign_progress.png')
        plt.close()
    return render_template("inf_summary.html",inf=inf,spons=spons,infs=infs,camps=camps,ads=ads,cname=cname,cprog=cprog,adpend=adpend,adrej=adrej,adacpt=adacpt)




#SPONSOR

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
        if start_date<=current_date and  end_date>=current_date :
            ongoingcamps.append(x)
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
        niche=request.form.get("niche")
        new_camp=Campaign(camp_name=camp_name,start_date=start_date,end_date=end_date,budget=budget,niche=niche,visibility=visibility,goals=goals,description=description,spon_id=spon_id)
        db.session.add(new_camp)
        db.session.commit()
        return redirect(url_for("spon_dashboard",spon_id=spon_id))
    
@app.route("/delete_camp/<spon_id>",methods=["GET", "POST"])
def delete_camp(spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    spon=Sponsor.query.get(spon_id)
    camps=Campaign.query.all()
    if request.method=="GET":
        camps=[]
        for x in spon.spon_camp:
            camps.append(x)
        return render_template("delete_camp.html",camps=camps,spon=spon)
    if request.method=="POST":
        camp_id=request.form.get("camp_id")
        del_camp=Campaign.query.get(camp_id)
        if del_camp:
            db.session.delete(del_camp)
            db.session.commit()
        scamp=[]
        for x in spon.spon_camp:
            scamp.append(x) 
        return render_template("delete_camp.html",camps=scamp,spon=spon)

@app.route("/update_camp/<spon_id>",methods=["GET", "POST"])
def update_camp(spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    spon=Sponsor.query.get(spon_id)
    if request.method=="GET":
        scamp=[]
        for x in spon.spon_camp:
            scamp.append(x)        
        return render_template("update_camp.html",camps=scamp,spon=spon)
    if request.method=="POST":
        camp_name=request.form.get("camp_name")
        start_date=request.form.get("start_date")
        end_date=request.form.get("end_date")
        budget=request.form.get("budget")
        visibility=request.form.get("visibility")
        goals=request.form.get("goals")
        description=request.form.get("description")
        niche=request.form.get("niche")
        progress=request.form.get("progress")
        camp_id=request.form.get("camp_id")
        update_camp=Campaign.query.get(camp_id)
        update_camp.camp_name=camp_name       
        update_camp.start_date=start_date
        update_camp.end_date=end_date
        update_camp.budget=budget
        update_camp.visibility=visibility
        update_camp.goals= goals
        update_camp.description= description
        update_camp.niche=niche
        update_camp.progress= progress
        db.session.commit()
        scamp=[]
        for x in spon.spon_camp:
            scamp.append(x) 
        return render_template("update_camp.html",camps=scamp,spon=spon)

@app.route("/create_ad/<spon_id>",methods=["GET", "POST"])
def create_ad(spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    if request.method=="GET":
        spon=Sponsor.query.get(spon_id)
        infs=Influencer.query.all()
        print(infs)
        return render_template("create_ad.html",spon=spon,infs=infs)
    if request.method=="POST":
        adreq_name=request.form.get("adreq_name")
        camp_id=request.form.get("camp_id")
        pay_amount=request.form.get("pay_amount")
        inf_id=request.form.get("inf_id")
        requirements=request.form.get("requirements")
        spon_id=spon_id
        new_ad=Adrequest(adreq_name=adreq_name,camp_id=camp_id,pay_amount=pay_amount,inf_id=inf_id,requirements=requirements)
        db.session.add(new_ad)
        db.session.commit()
        return redirect(url_for("spon_dashboard",spon_id=spon_id))
    
@app.route("/delete_ad/<spon_id>",methods=["GET", "POST"])
def delete_ad(spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    spon=Sponsor.query.get(spon_id)
    ads=Adrequest.query.all()
    if request.method=="GET":
        ads=[]
        for x in spon.spon_camp:
            for ad in x.camp_ads:
                ads.append(ad)   
        return render_template("delete_ad.html",ads=ads,spon=spon)
    if request.method=="POST":
        ad_id=request.form.get("adreq_id")
        del_ad=Adrequest.query.get(ad_id)
        if del_ad:
            db.session.delete(del_ad)
            db.session.commit()
        ads=[]
        for x in spon.spon_camp:
            for ad in x.camp_ads:
                ads.append(ad)
        return render_template("delete_ad.html",ads=ads,spon=spon)
    
@app.route("/update_ad/<spon_id>",methods=["GET", "POST"])
def update_ad(spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    spon=Sponsor.query.get(spon_id)
    ads=Adrequest.query.all()
    if request.method=="GET":
        ads=[]
        for x in spon.spon_camp:
            for ad in x.camp_ads:
                ads.append(ad)  
        return render_template("update_ad.html",ads=ads,spon=spon)
    if request.method=="POST":
        adreq_name=request.form.get("adreq_name")
        camp_id=request.form.get("camp_id")
        pay_amount=request.form.get("pay_amount")
        status=request.form.get("status")
        inf_id=request.form.get("inf_id")
        requirements=request.form.get("requirements")
        messages=request.form.get("messages")
        ad_id=request.form.get("adreq_id")
        update_ad=Adrequest.query.get(ad_id)
        update_ad.adreq_name=adreq_name
        update_ad.camp_id=camp_id     
        update_ad.pay_amount=pay_amount
        update_ad.status=status
        update_ad.inf_id=inf_id
        update_ad.requirements=requirements
        update_ad.messages=messages
        db.session.commit()
        ads=[]
        for x in spon.spon_camp:
            for ad in x.camp_ads:
                ads.append(ad)
        return render_template("update_ad.html",ads=ads,spon=spon)

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
        if spon_id==sponid:
            ad.messages+=sponid+ "(Sponsor)"+":" + spon_msg+"//"
            ad.messages = ad.messages.replace('//', '\n')
        db.session.commit()
        return render_template("spon_ad_details.html",spon=spon,adreq=ad)

@app.route('/sponsor/<spon_id>/<camp_id>/request',methods=["GET"])
def spon_request(spon_id,camp_id):
    spon=Sponsor.query.get(spon_id)
    camp=Campaign.query.get(camp_id)
    if request.method=="GET":
        return render_template("spon_request.html",spon=spon,camp=camp)
    
    
@app.route("/rate/<inf_id>/<spon_id>",methods=["GET","POST"])
def rate(inf_id,spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    if request.method=="GET":
        return render_template("rate.html",i=Influencer.query.get(inf_id),spon=Sponsor.query.get(spon_id))
    if request.method=="POST":
        inf=Influencer.query.get(inf_id)
        inf.inf_total_rating+=decimal.Decimal(request.form.get("rating"))
        inf.inf_num_rating+=1
        inf.rating=((inf.inf_total_rating)/inf.inf_num_rating)
        db.session.commit()
        return redirect(url_for("spon_dashboard",spon_id=spon_id))

@app.route('/sponsor/<inf_id>/<spon_id>/infdetails',methods=["GET"])
def spon_inf_details(spon_id,inf_id):
    spon=Sponsor.query.get(spon_id)
    inf=Influencer.query.get(inf_id)
    rate=None
    camps=[]
    for i in inf.inf_req:
        if i.status=="accepted":
            camps.append(i.camp_id)
    uniquecamps=set(camps)
    lcamp=list(uniquecamps)
    for i in lcamp:
        c=Campaign.query.get(i)
        if c.progress==100:
            rate=True
            break
    return render_template("spon_inf_details.html",spon=spon,inf=inf,rate=rate)

@app.route('/campaign/<camp_id>/<spon_id>/rembudget',methods=["GET"])
def rembudget(camp_id,spon_id):
    rem=0
    spon=Sponsor.query.get(spon_id)
    camp=Campaign.query.get(camp_id)
    rem=camp.budget
    for ad in camp.camp_ads:
        rem-=ad.pay_amount
    if request.method=="GET":
        return render_template("spon_camp_details.html",rem=rem,camp=camp,spon=spon)
    return render_template("spon_camp_details.html",rem=rem,camp=camp,spon=spon)

@app.route("/sponsearch/<search_type>/<spon_id>", methods=["GET", "POST"])
def sponsearch(search_type,spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for("spon_login"))
    spon=Sponsor.query.get(spon_id)
    if request.method=="GET":
        if search_type=="common":
            if spon.flagged==1:
                return render_template("search_common.html",spon=spon,message="You do not have permission to perform this action. Please contact the admin for assistance.")
            return render_template("search_common.html",spon=spon)
        if search_type=="inf_name":
                return render_template("search_infname.html",spon=spon)
        if search_type=="inf_niche":            
            return render_template("search_infniche.html",spon=spon)
        if search_type=="inf_reach":            
            return render_template("search_infreach.html",spon=spon)
    if request.method=="POST":
        if search_type=="inf_name":
            inf_name=request.form.get("inf_name").strip()
            sresult=Influencer.query.filter(Influencer.inf_name.ilike(f"%{inf_name}%")).all()
            print(sresult)
            return render_template("sresult_infname.html",sresult=sresult,spon=spon)
        if search_type=="inf_niche":
            inf_niche=request.form.get("inf_niche").strip()
            sresult=Influencer.query.filter(Influencer.inf_niche.ilike(f"%{inf_niche}%")).all()
            return render_template("sresult_infname.html",sresult=sresult,spon=spon)
        if search_type=="inf_reach":
            reach_min=request.form.get("inf_reach").strip()
            sresult = Influencer.query.filter(Influencer.inf_reach >= int(reach_min)).all()
            return render_template("sresult_infname.html",sresult=sresult,spon=spon)
          
@app.route("/spon_summary/<spon_id>",methods=["GET"])
def spon_summary(spon_id):
    global logged_spon
    if not logged_spon:
        return redirect(url_for('spon_login'))
    camps=Campaign.query.all()
    ads=Adrequest.query.all()
    spons=Sponsor.query.all()
    infs=Influencer.query.all()
    spon=Sponsor.query.get(spon_id)
    adacpt,adrej,adpend,pub,priv=0,0,0,0,0
    cname,cprog=[],[]
    for camp in spon.spon_camp:
        cname.append(camp.camp_name)
        cprog.append(camp.progress)
    x_labels = cname
    y_values = cprog
    '''fig, ax = plt.subplots() # to remove white bg
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)'''
    if cname!=[] and cprog!=[]:
        plt.title('Campaign Progress')
        plt.bar(x_labels, y_values, color='green', width=0.5)
        plt.xlabel('Campaigns')
        plt.ylabel('Progress')
        # Add space between x-values
        plt.xticks(range(len(x_labels)), x_labels, rotation=40, ha='right', fontsize=10)  # Adjust rotation, alignment, and font size
        plt.tight_layout() 
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        for i in range(len(x_labels)):
                plt.text(i, y_values[i] + 1, f'{y_values[i]}%', ha='center', va='bottom')#percent
        plt.savefig('MAD1project code/static/s_campaign_progress.png')
        plt.close()

    for camp in spon.spon_camp:
        for i in camp.camp_ads:
            if i.status=="accepted":
                adacpt+=1
            if i.status=="rejected":
                adrej+=1
            if i.status=="pending":
                adpend+=1
    if adpend!=0 or adacpt!=0 or adrej!=0:
        plt.title('Ad request status')
        y = np.array([adacpt,adrej,adpend])
        mylabels1= ["Accepted", "Rejected", "Pending"]
        total = sum(y)
        colors = ['#4CAF50', '#F44336', '#FFEB3B']
        autopct = lambda pct: f'{int(round(pct * total / 100.0))}'
        plt.pie(y, labels=mylabels1, autopct=autopct, colors=colors)
        #plt.pie(y, labels = mylabels1,autopct='%1.1f%%')#percent
        plt.savefig('MAD1project code/static/s_ad_status.png')
        plt.close()
    
    for camp in spon.spon_camp:
        if camp.visibility=="private":
            priv+=1
        elif camp.visibility=="public":
            pub+=1
    if pub!=0 or priv!=0:
        plt.title('Campaign visibility')
        y = np.array([priv,pub])
        mylabels2= ["Private","Public"]
        plt.pie(y, labels = mylabels2,autopct='%1.1f%%')
        plt.savefig('MAD1project code/static/s_camp_visibility.png')
        plt.close()

    return render_template("spon_summary.html",spon=spon,spons=spons,infs=infs,camps=camps,ads=ads,cname=cname,cprog=cprog,adpend=adpend,adrej=adrej,adacpt=adacpt,pub=pub,priv=priv)








    
    

    
    

