from flask import current_app as app
from application.models import *
from flask import request

#Influencer CRUD

@app.route("/api_read_inf",methods=["GET"])
def api_read_inf():
    return{"data":[inf.to_json() for inf in Influencer.query.all()]},200

@app.route("/api_delete_inf",methods=["POST"])
def api_delete_inf():
    data=request.get_json()
    inf_id=data["inf_id"]
    del_inf=Influencer.query.get(inf_id)
    if del_inf:
        db.session.delete(del_inf)
        db.session.commit()
    return {"message":"deleted successfully "}, 200

@app.route("/api_update_inf",methods=["POST"])
def api_update_inf():
    data=request.get_json()
    inf_category=data["inf_category"]
    inf_id=data["inf_id"]
    inf_name=data["inf_name"]
    inf_reach=int(data["inf_reach"])
    inf_niche=data["inf_niche"]
    flagged=data["flagged"]
    inf_num_rating=data["inf_num_rating"]
    inf_password=data["inf_password"]
    update_inf=Influencer.query.get(inf_id)
    update_inf.inf_name=inf_name       
    update_inf.flagged=flagged
    update_inf.inf_niche=inf_niche
    update_inf.inf_reach=inf_reach
    update_inf.inf_num_rating=inf_num_rating
    update_inf.inf_password= inf_password
    update_inf.inf_category= inf_category
    db.session.commit()
    return {"message":"influencer updation successful"}, 201

@app.route("/api_create_inf",methods=["POST"])
def api_create_inf():
    data=request.get_json()
    inf_category=data["inf_category"]
    inf_id=data["inf_id"]
    inf_name=data["inf_name"]
    inf_reach=int(data["inf_reach"])
    inf_niche=data["inf_niche"]
    flagged=data["flagged"]
    inf_num_rating=data["inf_num_rating"]
    inf_password=data["inf_password"]
    new_inf=Influencer(inf_name=inf_name,inf_id=inf_id,inf_category=inf_category,inf_reach= inf_reach,inf_niche=inf_niche,flagged=flagged,inf_num_rating=inf_num_rating,inf_password=inf_password)
    db.session.add(new_inf)
    db.session.commit()
    return {"message":"influencer creation successful"}, 201

#CAMPAIGN MANAGEMENT: READ,DELETE,UPDATE AND CREATE 

@app.route("/api_read_camp",methods=["GET"])
def api_read_camp():
    return{"data":[camp.to_json() for camp in Campaign.query.all()]},200

@app.route("/api_delete_camp",methods=["POST"])
def api_delete_camp():
    data=request.get_json()
    camp_id=int(data["camp_id"])
    del_camp=Campaign.query.get(camp_id)
    if del_camp:
        db.session.delete(del_camp)
        db.session.commit()
    return {"message":"successful"}, 200

@app.route("/api_update_camp",methods=["POST"])
def api_update_camp():
    data=request.get_json()
    camp_name=data["camp_name"]
    start_date=data["start_date"]
    end_date=data["end_date"]
    budget=int(data["budget"])
    visibility=data["visibility"]
    goals=data["goals"]
    description=data["description"]
    camp_id=int(data["camp_id"])
    spon_id=data["spon_id"]
    update_camp=Campaign.query.get(camp_id)
    update_camp.camp_name=camp_name       
    update_camp.start_date=start_date
    update_camp.end_date=end_date
    update_camp.budget=budget
    update_camp.visibility=visibility
    update_camp.goals= goals
    update_camp.description= description
    update_camp.spon_id=spon_id
    db.session.commit()
    return {"message":"campaign updation successful"}, 201

@app.route("/api_create_camp",methods=["POST"])
def api_create_camp():
    data=request.get_json()
    camp_name=data["camp_name"]
    start_date=data["start_date"]
    end_date=data["end_date"]
    budget=int(data["budget"])
    visibility=data["visibility"]
    goals=data["goals"]
    description=data["description"]
    spon_id=data["spon_id"]
    new_camp=Campaign(camp_name=camp_name,spon_id=spon_id,start_date=start_date,end_date=end_date,budget=budget,visibility=visibility,goals=goals,description=description)
    db.session.add(new_camp)
    db.session.commit()
    return {"message":"campaign creation successful"}, 201



#AD MANAGEMENT: READ,DELETE,UPDATE AND CREATE 

@app.route("/api_read_ad",methods=["GET"])
def api_read_ad():
    return{"data":[ad.to_json() for ad in Adrequest.query.all()]},200

@app.route("/api_delete_ad",methods=["POST"])
def api_delete_ad():
    data=request.get_json()
    adreq_id=int(data["adreq_id"])
    del_ad=Adrequest.query.get(adreq_id)
    db.session.delete(del_ad)
    db.session.commit()
    return {"message":"successful"}, 200

@app.route("/api_update_ad",methods=["POST"])
def api_update_ad():
    data=request.get_json()
    adreq_name=data["adreq_name"]
    camp_id=data["camp_id"]
    pay_amount=data["pay_amount"]
    status=data["status"]
    inf_id=data["inf_id"]
    requirements=data["requirements"]
    messages=data["messages"]
    ad_id=data["adreq_id"]
    update_ad=Adrequest.query.get(ad_id)
    update_ad.adreq_name=adreq_name
    update_ad.camp_id=camp_id     
    update_ad.pay_amount=pay_amount
    update_ad.status=status
    update_ad.inf_id=inf_id
    update_ad.requirements=requirements
    update_ad.messages=messages
    db.session.commit()
    return {"message":"ad updation successfull"},201

@app.route("/api_create_ad",methods=["POST"])
def api_create_ad():
    data=request.get_json()
    adreq_name=data["adreq_name"]
    camp_id=data["camp_id"]
    pay_amount=data["pay_amount"]
    status=data["status"]
    inf_id=data["inf_id"]
    requirements=data["requirements"]
    messages=data["messages"]
    new_ad=Adrequest(adreq_name=adreq_name,camp_id=camp_id,pay_amount=pay_amount,status=status,inf_id=inf_id,requirements=requirements,messages=messages)
    db.session.add(new_ad)
    db.session.commit()
    return {"message":"ad creation successfull"},201



'''{ "camp_name":"",
    "start_date":"",
    "end_date":"",
    "budget":,
    "visibility":"",
    "goals":"",
    "description":"",
    "camp_id":
     "spon_id": }'''

'''{
    "adreq_name":"",
    "camp_id": ,
    "pay_amount":,
    "status":"",
    "inf_id":,
    "requirements":"",
    "messages":"",
    "adreq_id":
}'''
