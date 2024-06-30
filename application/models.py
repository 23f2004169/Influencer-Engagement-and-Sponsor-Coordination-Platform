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
    rating=db.Column(db.Numeric,default=0)
    inf_req=db.relationship('Adrequest')
    inf_num_rating=db.Column(db.Integer, default=0)
    inf_total_rating=db.Column(db.Numeric, default=0)
    def to_json(self):
        return{"inf_id":self.inf_id,"inf_name":self.inf_name,"inf_password":self.inf_password,"inf_category":self.inf_category,"inf_niche":self.inf_niche,"inf_reach":self.inf_reach,"flagged":self.flagged,"rating":self.rating,"inf_req":[ad.to_json() for ad in self.inf_req]}

class Sponsor(db.Model):
    __tablename__="sponsor"
    spon_id=db.Column(db.String,primary_key=True,nullable=False)
    spon_name=db.Column(db.String)
    spon_password=db.Column(db.String,nullable=False)
    spon_budget=db.Column(db.Integer,nullable=False)
    spon_industry=db.Column(db.String,nullable=False)
    flagged=db.Column(db.Integer, default=0)
    spon_camp=db.relationship('Campaign')
    def to_json(self):
        return{"spon_id":self.spon_id,"spon_name":self.spon_name,"spon_password":self.spon_password,"spon_budget":self.spon_budget,"spon_industry":self.spon_industry,"flagged":self.flagged,"spon_camp":[camp.to_json() for camp in self.spon_camp]}

class Adrequest(db.Model):
    __tablename__="adrequest"
    adreq_id=db.Column(db.Integer,primary_key=True,nullable=False)
    inf_id=db.Column(db.Integer,db.ForeignKey("influencer.inf_id"),nullable=False)
    camp_id=db.Column(db.Integer,db.ForeignKey("campaign.camp_id"),nullable=False)
    messages=db.Column(db.String)
    requirements=db.Column(db.String)
    pay_amount=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String,nullable=False)
    def to_json(self):
        return{"adreq_id":self.adreq_id,"inf_id":self.inf_id,"camp_id":self.camp_id,"messages":self.messages,"requirements":self.requirements,"pay_amount":self.pay_amount,"status":self.status}

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
    niche=db.Column(db.String)
    camp_ads=db.relationship("Adrequest")
    def to_json(self):
        return{"camp_id":self. camp_id,"spon_id":self.spon_id,"camp_name":self.camp_name,"start_date":self.start_date,"end_date":self.end_date,"budget":self.budget,"goals":self.goals,"visibility":self.visibility,"description":self.description,"flagged":self.flagged,"camp_ads":[ad.to_json() for ad in self.camp_ads]}






