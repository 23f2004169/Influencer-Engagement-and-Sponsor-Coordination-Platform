from application.database import db

class Admin(db.Model):
    __tablename__="admin"
    admin_name=db.Column(db.String,primary_key=True)
    admin_password=db.Column(db.String,nullable=False)

class Influencer(db.Model):
    __tablename__="influencer"
    inf_id=db.Column(db.String,primary_key=True,nullable=False)
    inf_name=db.Column(db.String)
    inf_password=db.Column(db.String,nullable=False)
    inf_category=db.Column(db.String,nullable=False)
    inf_niche=db.Column(db.String,nullable=False)
    inf_reach=db.Column(db.Integer,nullable=False) 
    flagged=db.Column(db.Integer, default=0)
    rating=db.Column(db.Integer)
    inf_req=db.relationship('Adrequest')

class Sponsor(db.Model):
    __tablename__="sponsor"
    spon_id=db.Column(db.String,primary_key=True,nullable=False)
    spon_name=db.Column(db.String)
    spon_password=db.Column(db.String,nullable=False)
    spon_budget=db.Column(db.Integer,nullable=False)
    spon_industry=db.Column(db.String,nullable=False)
    flagged=db.Column(db.Integer, default=0)
    spon_camp=db.relationship('Campaign')
    
class Adrequest(db.Model):
    __tablename__="adrequest"
    adreq_id=db.Column(db.Integer,primary_key=True,nullable=False)
    inf_id=db.Column(db.Integer,db.ForeignKey("influencer.inf_id"),nullable=False)
    camp_id=db.Column(db.Integer,db.ForeignKey("campaign.camp_id"),nullable=False)
    messages=db.Column(db.String)
    requirements=db.Column(db.String)
    pay_amount=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String,nullable=False)

class Campaign(db.Model):
    __tablename__="campaign"
    camp_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    spon_id=db.Column(db.Integer,db.ForeignKey("sponsor.spon_id"),nullable=False)
    camp_name=db.Column(db.String,nullable=False)
    start_date=db.Column(db.String,nullable=False)
    end_date=db.Column(db.String,nullable=False)
    budget=db.Column(db.Integer,nullable=False)
    goals=db.Column(db.String,nullable=False)
    visibility=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    flagged=db.Column(db.Integer, default=0)
    camp_ads=db.relationship("Adrequest")







