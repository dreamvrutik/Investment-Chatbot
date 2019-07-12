from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from investment_bot.models import user_database
from . import forms
from investment_bot.models import Section_Details as sd,Amount_Restrictions,Section_Deduction
from investment_bot.df_library import *
from investment_bot.Reimbursement_func import *
from investment_bot.sec80E import *
from investment_bot.sec24 import *
from investment_bot.sec80U import *
from investment_bot.sec80D import *
from investment_bot.sec80DD import *
from investment_bot.sec80DDB import *
from investment_bot.Section4 import *
import datetime

employeecode="INFI4466"
data=[]
session_id="-"
amt_sec80C=0
max_amt_sec80C=0
x=Amount_Restrictions.objects.filter(section_id="80C")
x={'data':x}
for i in x['data']:
    if i.subsection_id=="all":
        max_amt_sec80C=i.Max_Amount
sec80U_subid=""

def save_data(sectionid,subsectionid,amt):
    now = datetime.datetime.now()
    now=now.year
    ss=Section_Deduction(year=str(now),employee_code=employeecode,section_id=sectionid,subsection_id=subsectionid,amount=amt)
    ss.save()


def login(request):
    # import pdb; pdb.set_trace()
    form=forms.login_form()
    if request.method=='POST':
        form=forms.login_form(request.POST)
        if form.is_valid():
            x=form.cleaned_data['employee_code']
            global employee_code
            employee_code=x
            return HttpResponse(x)
    return render(request,'investment_bot/login.html', context={'form':form})

def register(request):
    # import pdb; pdb.set_trace()
    form=forms.register_form()
    if request.method=='POST':
        form=forms.register_form(request.POST)
        if form.is_valid():
            #get data and save to database
            x=form.cleaned_data['employee_code']
            global employee_code
            employee_code=x
            print("Valid")
            form=forms.login_form()
            return render(request,'investment_bot/login.html', context={'form':form})
    return render(request,'investment_bot/register.html', context={'form':form})

def fallback():
    s="Sorry. Can you say that again?"
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(["80C","80D","Reimbursement","Section-24","80E","80U","80DD","Section-4"])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    x=session_id
    outputcontext=[['welcome','0',{'parameter_name':0}],]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def welcome():
    s="Pease enter your employee code."
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips([])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    x=session_id
    outputcontext=[['welcome','1',{'parameter_name':1}],]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def welcome1():
    t=user_database.objects.get(employee_code=employeecode)
    name=t.name
    s="Hey "+name+", Welcome to investment chat-bot. What section would you like to choose for now?"
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(["80C","80D","Reimbursement","80E","Section-24","80U","80DD","80DDB","Section-4"])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    x=session_id
    outputcontext=[['welcome','0',{'parameter_name':0}],]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def welcome2():
    s="Please enter valid employee code."
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips([])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    x=session_id
    outputcontext=[['welcome','1',{'parameter_name':1}],]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def main_menu():
    s="These are the available sections in the form.\n1 80C\n2 80D\n3 Section-24\n4 Reimbursement\n5 80E\n6 80DDB\n7 80DD\n8 80DDB\n9 Section-4"
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(["80C","80D","Reimbursement","80E","Section-24","80U","80DD","80DDB","Section-4"])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    x=session_id
    outputcontext=[['welcome','0',{'parameter_name':0}],]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec_80C():
    s="Please select the required suggestion chip.\n"
    sugg=["Accured Interest on NSC","PPF","LIC","NSC Purchases","Housing Loan Principle","ULIP","Mutual funds","Pension Scheme","Children Tuition Fee","Fixed Deposits","ELSS","Agricultural Bonds","Sukanya  Samriddhi","POD","Amount for NPS","RGESS"]
    for i in sugg:
        if i!="RGESS":
            s+=i+" , "
        else:
            s+="Rajiv Gandhi Equity Saving Scheme"+" , "
    s=s[:len(s)-2]
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(sugg)
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    outputcontext=[['welcome','0',{'parameter_name':0}],['80C-followup','5',{'parameter_name':5}],['80C-followup-2','5',{'parameter_name':5}]]
    for i in range(1,17):
        x=[]
        s="80C"+str(i)
        x.append(s)
        s="1"
        x.append(s)
        s={'parameter_name':1}
        x.append(s)
        outputcontext.append(x)
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec_80C_fallback():
    s="Sorry . Can you say that again?\nPlease select the required suggestion chip.\n"
    sugg=["Accured Interest on NSC","PPF","LIC","NSC Purchases","Housing Loan Principle","ULIP","Mutual funds","Pension Scheme","Children Tuition Fee","Fixed Deposits","ELSS","Agricultural Bonds","Sukanya  Samriddhi","POD","Amount for NPS","RGESS"]
    for i in sugg:
        if i!="RGESS":
            s+=i+" , "
        else:
            s+="Rajiv Gandhi Equity Saving Scheme"+" , "
    s=s[:len(s)-2]
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(sugg)
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    outputcontext=[['welcome','0',{'parameter_name':0}],['80C-followup','5',{'parameter_name':5}],['80C-followup-2','5',{'parameter_name':5}]]
    for i in range(1,17):
        x=[]
        s="80C"+str(i)
        x.append(s)
        s="1"
        x.append(s)
        s={'parameter_name':1}
        x.append(s)
        outputcontext.append(x)
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec_80C_sub_fallback(subid):
    s="Please enter the amount in Rupees."
    fulfillmentText = s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr])
    oc="80C-"+subid
    bc="80C-followup"
    bd=bc+"-2"
    cc="80C-"+subid+"-followup"
    gg="80C"+subid
    dd=cc+"-2"
    outputcontext=[[oc,'1',{'parameter_name':1}],[bc,'1',{'parameter_name':1}],[bd,'5',{'parameter_name':5}],[cc,'5',{'parameter_name':1}],[gg,'1',{'parameter_name':1}],[dd,'1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec_80C_Amount_Confirm(amt):
    s="Amount Rs. "+str(amt)+" is filled in the form for the selected subsection of 80C section.\n"
    s+="Please select the required suggestion chip.\n"
    sugg=["Accured Interest on NSC","PPF","LIC","NSC Purchases","Housing Loan Principle","ULIP","Mutual funds","Pension Scheme","Children Tuition Fee","Fixed Deposits","ELSS","Agricultural Bonds","Sukanya  Samriddhi","POD","Amount for NPS","RGESS"]
    for i in sugg:
        if i!="RGESS":
            s+=i+" , "
        else:
            s+="Rajiv Gandhi Equity Saving Scheme"+" , "
    s=s[:len(s)-2]
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(sugg)
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    outputcontext=[['welcome','0',{'parameter_name':0}],['80C-followup','5',{'parameter_name':5}],['80C-followup-2','5',{'parameter_name':5}]]
    for i in range(1,17):
        x=[]
        s="80C"+str(i)
        x.append(s)
        s="1"
        x.append(s)
        s={'parameter_name':1}
        x.append(s)
        outputcontext.append(x)
    print(outputcontext)
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def cancel_80C():
    s="OK Cancelled.\nPlease select the required suggestion chip. Options available are : \n"
    sugg=["Accured Interest on NSC","PPF","LIC","NSC Purchases","Housing Loan Principle","ULIP","Mutual funds","Pension Scheme","Children Tuition Fee","Fixed Deposits","ELSS","Agricultural Bonds","Sukanya  Samriddhi","POD","Amount for NPS","RGESS"]
    for i in sugg:
        if i!="RGESS":
            s+=i+" , "
        else:
            s+="Rajiv Gandhi Equity Saving Scheme"+" , "
    s=s[:len(s)-2]
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips

    aog_sc = aog.suggestion_chips(sugg)
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    outputcontext=[['welcome','0',{'parameter_name':0}],['80C-followup','5',{'parameter_name':5}],['80C-followup-2','5',{'parameter_name':5}]]
    for i in range(1,17):
        x=[]
        s="80C"+str(i)
        x.append(s)
        s="1"
        x.append(s)
        s={'parameter_name':1}
        x.append(s)
        outputcontext.append(x)
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec_80C_amt_exceed(max_amt,subid):
    s="Sorry The amount you entered exceeds the Max-Limit of This Subsection. Please enter the amount in appropriate bounds. the max limit is "+str(max_amt)
    fulfillmentText = s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr])
    oc="80C-"+subid
    bc="80C-followup"
    bd=bc+"-2"
    cc="80C-"+subid+"-followup"
    gg="80C"+subid
    dd=cc+"-2"
    outputcontext=[[oc,'1',{'parameter_name':1}],[bc,'1',{'parameter_name':1}],[bd,'5',{'parameter_name':5}],[cc,'5',{'parameter_name':1}],[gg,'1',{'parameter_name':1}],[dd,'1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec_80C_main_amt_exceed():
    s="The max Limit of Section-80C is "+str(max_amt_sec80C)+". You have exceeded that. "
    s+="These are the available sections in the form.\n1 80C\n2 80D\n3 Section-24\n4 Reimbursement\n5 80E\n6 80DDB\n7 80DD\n8 80DDB\n9 Section-4"
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(["80C","80D","Reimbursement","80E","Section-24","80U","80DD","80DDB","Section-4"])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    x=session_id
    outputcontext=[['welcome','0',{'parameter_name':0}],]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply



@csrf_exempt
def webhook(request):
# build request object
    req = json.loads(request.body)
    action = req.get('queryResult').get('action')
    print(json.dumps(req,indent=4,sort_keys=True))
    if action=='input.welcome':
        global session_id
        if session_id=="-":
            session_id=str(req['session'])
        reply=welcome()
    elif action=="fallback":
        reply=fallback()
    elif action=='Reimbursement':
        reply=Reimbursement(session_id)
    elif action=="rem_fallback":
        reply=Reimbursement_fallback(session_id)
    elif "rem-"in action:
        subid=action[4]
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=rem_fallback(subid,session_id)
            f=-1
        else:
            x=Amount_Restrictions.objects.filter(section_id="rem")
            x={'data':x}
            for i in x['data']:
                if i.subsection_id==subid:
                    max_amt=int(i.Max_Amount)
                    amt=int(amt)
                    if amt<=max_amt:
                        reply=Reimbursement_amt_confirm(amt, session_id)
                        try:
                            now = datetime.datetime.now()
                            now=now.year
                            now=str(now)
                            print(now)
                            t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="rem",subsection_id=subid)
                            t.amount=amt
                            t.save()
                            print("Updated")
                        except Exception as e:
                            save_data("rem",subid, amt)
                            print("Saved")
                        f=1
                    else:
                        reply=amt_exceed(session_id,max_amt,subid)
                        f=-1
                    break
            if f==0:
                reply=Reimbursement_amt_confirm(amt, session_id)
                try:
                    now = datetime.datetime.now()
                    now=now.year
                    now=str(now)
                    t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="rem",subsection_id=subid)
                    t.amount=amt
                    t.save()
                    print("Updated")
                except Exception as e:
                    save_data("rem",subid, amt)
                    print("saved")
        #Save data to database if f==1

    elif action=="cancel-rem":
        reply=cancel_rem(session_id)
    elif "rem_" in action:
        subid=action[4]
        reply=rem_fallback(subid,session_id)
    elif action=="main-menu":
        reply=main_menu()
    elif action=="80C":
        reply=sec_80C()
    elif action=="80C_fallback":
        reply=sec_80C_fallback()
    elif "80C_" in action:
        subid=action[4]
        reply=sec_80C_sub_fallback(subid)
    elif "80C-"in action:
        subid=action[4]
        print(action)
        if action[5]=='-':
            subid='0'+subid
        else:
            subid+=action[5]
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec_80C_sub_fallback(subid)
        else:
            x=Amount_Restrictions.objects.filter(section_id="80C")
            x={'data':x}
            for i in x['data']:
                print(subid,i.subsection_id,i.Max_Amount)
                #print(i,subid)

                if i.subsection_id==subid:
                    max_amt=int(i.Max_Amount)
                    amt=int(amt)
                    if subid=='16':
                        if(amt*0.5<=25000):
                            amt=0.5*amt
                        else:
                            amt=25000
                    if amt<=max_amt:
                        if subid!='15' and subid!='16':
                            if(amt_sec80C+amt<=max_amt_sec80C):
                                reply=sec_80C_Amount_Confirm(amt)
                                try:
                                    now = datetime.datetime.now()
                                    now=now.year
                                    now=str(now)
                                    print(now)
                                    t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="80C",subsection_id=subid)
                                    t.amount=amt
                                    t.save()
                                    print("Updated")
                                except Exception as e:
                                    save_data("80C",subid, amt)
                                    print("Saved")
                                amt_sec80C+=amt
                            else:
                                #Do this via function after data entry
                                reply=sec_80C_main_amt_exceed()
                        else:
                            reply=sec_80C_Amount_Confirm(amt)
                            try:
                                now = datetime.datetime.now()
                                now=now.year
                                now=str(now)
                                print(now)
                                t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="80C",subsection_id=subid)
                                t.amount=amt
                                t.save()
                                print("Updated")
                            except Exception as e:
                                save_data("80C",subid, amt)
                                print("Saved")
                        f=1
                    else:
                        reply=sec_80C_amt_exceed(max_amt,subid)
                        f=-1
                    break
            if f==0:
                reply=sec_80C_Amount_Confirm(amt)
                try:
                    now = datetime.datetime.now()
                    now=now.year
                    now=str(now)
                    print(now)
                    t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="80C",subsection_id=subid)
                    t.amount=amt
                    t.save()
                    print("Updated")
                except Exception as e:
                    save_data("80C",subid, amt)
                    print("Saved")
        #Save data to database

    elif action=="cancel-80C":
        reply=cancel_80C()
    elif action=="80E":
        reply=sec_80E(session_id)
    elif action=="cancel-80E":
        reply=cancel_80E(session_id)
    elif action=="80E-1":
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec_80E_fallback(session_id)
        else:
            reply=sec_80E_amt_confirm(amt,session_id)
            try:
                now = datetime.datetime.now()
                now=now.year
                now=str(now)
                print(now)
                t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="80E",subsection_id=subid)
                t.amount=amt
                t.save()
                print("Updated")
            except Exception as e:
                save_data("80E",subid, amt)
                print("Saved")
    elif action=="80E_fallback":
        reply=sec_80E_fallback(session_id)
    elif action=="Sec-24":
        reply=sec_24(session_id)
    elif action=="Sec-24_fallback":
        reply=sec_24_fallback(session_id)
    elif action=="Sec-24_amount":
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec_24_fallback(session_id)
            f=-1
        else:
            subid="1"
            sec_id="sec24"
            x=Amount_Restrictions.objects.filter(section_id=sec_id)
            x={'data':x}
            for i in x['data']:
                if i.subsection_id==subid:
                    amt=int(amt)
                    max_amt=i.Max_Amount
                    if amt<=max_amt :
                        f=1
                        reply=sec_24_amt_confirm(amt,session_id)
                        try:
                            now = datetime.datetime.now()
                            now=now.year
                            now=str(now)
                            print(now)
                            t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id=sec_id,subsection_id=subid)
                            t.amount=amt
                            t.save()
                            print("Updated")
                        except Exception as e:
                            save_data(sec_id,subid, amt)
                            print("Saved")
                    else:
                        f=-1
                        reply=sec_24_amt_exceed(max_amt,session_id)
        #if f==1 save data to database

    elif action=="cancel_sec24":
        reply=cancel_sec_24(session_id)
    elif action=="Sec80U":
        reply=sec80U(session_id)
    elif action=="80U-fallback":
        reply=sec80U_fallback(session_id)
    elif action=="cancel-80U":
        reply=sec80U_cancel(session_id)
    elif action=="80U-40":
        global sec80U_subid
        sec80U_subid="1"
        reply=sec80U_getAMT(session_id,sec80U_subid)
    elif action=="80U-80":
        sec80U_subid="2"
        reply=sec80U_getAMT(session_id,sec80U_subid)
    elif action=="80U-1-1":
        subid="1"
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec80U_amt_fallback(session_id,"a40","80U-1-followup")
            f=-1
        else:
            x=Amount_Restrictions.objects.filter(section_id="80U")
            x={'data':x}
            for i in x['data']:
                if i.subsection_id==subid:
                    amt=int(amt)
                    max_amt=i.Max_Amount
                    if amt<=max_amt:
                        f=1
                        reply=sec80U_amt_confirm(amt,session_id,"a40","80U-1-followup")
                        try:
                            now = datetime.datetime.now()
                            now=now.year
                            now=str(now)
                            print(now)
                            t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="80U",subsection_id=subid)
                            t.amount=amt
                            t.save()
                            print("Updated")
                        except Exception as e:
                            save_data("80U",subid, amt)
                            print("Saved")
                    else:
                        f=-1
                        reply=sec80U_amt_exceed(max_amt,session_id,"a40","80U-1-followup")
        #if f==1 save data to database

    elif action=="80U-1-fallback":
        reply=sec80U_amt_fallback(session_id,"a40","80U-1-followup")

    elif action=="80U-2-1":
        subid="2"
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec80U_amt_fallback(session_id,"a80","80U-2-followup")
            f=-1
        else:
            x=Amount_Restrictions.objects.filter(section_id="80U")
            x={'data':x}
            for i in x['data']:
                if i.subsection_id==subid:
                    amt=int(amt)
                    max_amt=i.Max_Amount
                    if amt<=max_amt:
                        f=1
                        reply=sec80U_amt_confirm(amt,session_id,"a80","80U-2-followup")
                        try:
                            now = datetime.datetime.now()
                            now=now.year
                            now=str(now)
                            print(now)
                            t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="80U",subsection_id=subid)
                            t.amount=amt
                            t.save()
                            print("Updated")
                        except Exception as e:
                            save_data("80U",subid, amt)
                            print("Saved")
                    else:
                        f=-1
                        reply=sec80U_amt_exceed(max_amt,session_id,"a80","80U-2-followup")
        #if f==1 save data to database

    elif action=="80U-2-fallback":
        reply=sec80U_amt_fallback(session_id,"a80","80U-2-followup")

    elif action=="Sec80D":
        reply=sec80D(session_id)
    elif action=="cancel-80D":
        reply=sec80D_cancel(session_id)
    elif action=="80D-fallback":
        reply=sec80D_fallback(session_id)
    elif action=="80D-self":
        sec80D_subid="1"
        reply=sec80D_getAMT(session_id,sec80D_subid)
    elif action=="80D-1-1":
        subid="1"
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec80D_amt_fallback(session_id,"ssc","80D-1-followup")
            f=-1
        else:
            x=Amount_Restrictions.objects.filter(section_id="80D")
            x={'data':x}
            for i in x['data']:
                if i.subsection_id==subid:
                    amt=int(amt)
                    max_amt=i.Max_Amount
                    max_amt+=i.Additional_Amount
                    if amt<=max_amt:
                        f=1
                        reply=sec80D_amt_confirm(amt,session_id,"ssc","80D-1-followup")
                        try:
                            now = datetime.datetime.now()
                            now=now.year
                            now=str(now)
                            print(now)
                            t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="80D",subsection_id=subid)
                            t.amount=amt
                            t.save()
                            print("Updated")
                        except Exception as e:
                            save_data("80D",subid, amt)
                            print("Saved")
                    else:
                        f=-1
                        reply=sec80D_amt_exceed(max_amt,session_id,"ssc","80D-1-followup")
        #if f==1 save data to database

    elif action=="80D-1-fallback":
            reply=sec80D_amt_fallback(session_id,"ssc","80D-1-followup")
    elif action=="80D-par":
        sec80D_subid="2"
        reply=sec80D_getAMT(session_id,sec80D_subid)
    elif action=="80D-2-1":
        subid="2"
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec80D_amt_fallback(session_id,"par","80D-2-followup")
            f=-1
        else:
            x=Amount_Restrictions.objects.filter(section_id="80D")
            x={'data':x}
            for i in x['data']:
                if i.subsection_id==subid:
                    amt=int(amt)
                    max_amt=i.Max_Amount
                    max_amt+=i.Additional_Amount
                    if amt<=max_amt:
                        f=1
                        reply=sec80D_amt_confirm(amt,session_id,"par","80D-2-followup")
                        try:
                            now = datetime.datetime.now()
                            now=now.year
                            now=str(now)
                            print(now)
                            t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="80D",subsection_id=subid)
                            t.amount=amt
                            t.save()
                            print("Updated")
                        except Exception as e:
                            save_data("80D",subid, amt)
                            print("Saved")
                    else:
                        f=-1
                        reply=sec80D_amt_exceed(max_amt,session_id,"par","80D-2-followup")
        #if f==1 save data to database

    elif action=="80D-2-fallback":
            reply=sec80D_amt_fallback(session_id,"par","80D-2-followup")

    elif action=="Sec80DD":
        reply=sec80DD(session_id)
    elif action=="80DD-fallback":
        reply=sec80DD_fallback(session_id)
    elif action=="cancel-80DD":
        reply=sec80DD_cancel(session_id)
    elif action=="80DD-40":
        sec80DD_subid="1"
        reply=sec80DD_getAMT(session_id,sec80DD_subid)
    elif action=="80DD-80":
        sec80DD_subid="2"
        reply=sec80DD_getAMT(session_id,sec80DD_subid)
    elif action=="80DD-1-1":
        subid="1"
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec80DD_amt_fallback(session_id,"a40","80DD-1-followup")
            f=-1
        else:
            x=Amount_Restrictions.objects.filter(section_id="80DD")
            x={'data':x}
            for i in x['data']:
                if i.subsection_id==subid:
                    amt=int(amt)
                    max_amt=i.Max_Amount
                    if amt<=max_amt:
                        f=1
                        reply=sec80DD_amt_confirm(amt,session_id,"a40","80DD-1-followup")
                        try:
                            now = datetime.datetime.now()
                            now=now.year
                            now=str(now)
                            print(now)
                            t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="80DD",subsection_id=subid)
                            t.amount=amt
                            t.save()
                            print("Updated")
                        except Exception as e:
                            save_data("80DD",subid, amt)
                            print("Saved")
                    else:
                        f=-1
                        reply=sec80DD_amt_exceed(max_amt,session_id,"a40","80DD-1-followup")
        #if f==1 save data to database

    elif action=="80DD-1-fallback":
        reply=sec80DD_amt_fallback(session_id,"a40","80DD-1-followup")

    elif action=="80DD-2-1":
        subid="2"
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec80DD_amt_fallback(session_id,"a80","80DD-2-followup")
            f=-1
        else:
            x=Amount_Restrictions.objects.filter(section_id="80DD")
            x={'data':x}
            for i in x['data']:
                if i.subsection_id==subid:
                    amt=int(amt)
                    max_amt=i.Max_Amount
                    if amt<=max_amt:
                        f=1
                        reply=sec80DD_amt_confirm(amt,session_id,"a80","80DD-2-followup")
                        try:
                            now = datetime.datetime.now()
                            now=now.year
                            now=str(now)
                            print(now)
                            t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="80DD",subsection_id=subid)
                            t.amount=amt
                            t.save()
                            print("Updated")
                        except Exception as e:
                            save_data("80DD",subid, amt)
                            print("Saved")
                    else:
                        f=-1
                        reply=sec80DD_amt_exceed(max_amt,session_id,"a80","80DD-2-followup")
        #if f==1 save data to database

    elif action=="80DD-2-fallback":
        reply=sec80DD_amt_fallback(session_id,"a80","80DD-2-followup")
    elif action=="Sec80DDB":
        reply=sec80DDB(session_id)
    elif action=="80DDB-fallback":
        reply=sec80DDB_fallback(session_id)
    elif action=="cancel-80DDB":
        reply=sec80DDB_cancel(session_id)
    elif action=="80DDB-1":
        sec80DDB_subid="1"
        reply=sec80DDB_getAMT(session_id,sec80DDB_subid)
    elif action=="80DDB-2":
        sec80DDB_subid="2"
        reply=sec80DDB_getAMT(session_id,sec80DDB_subid)
    elif action=="80DDB-3":
        sec80DDB_subid="3"
        reply=sec80DDB_getAMT(session_id,sec80DDB_subid)
    elif action=="80DDB-1-1":
        subid="1"
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec80DDB_amt_fallback(session_id,"a1","80DDB-1-followup")
            f=-1
        else:
            x=Amount_Restrictions.objects.filter(section_id="80DDB")
            x={'data':x}
            for i in x['data']:
                if i.subsection_id==subid:
                    amt=int(amt)
                    max_amt=i.Max_Amount
                    if amt<=max_amt:
                        f=1
                        reply=sec80DDB_amt_confirm(amt,session_id,"a1","80DDB-1-followup")
                        try:
                            now = datetime.datetime.now()
                            now=now.year
                            now=str(now)
                            print(now)
                            t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="80DDB",subsection_id=subid)
                            t.amount=amt
                            t.save()
                            print("Updated")
                        except Exception as e:
                            save_data("80DDB",subid, amt)
                            print("Saved")
                    else:
                        f=-1
                        reply=sec80DDB_amt_exceed(max_amt,session_id,"a1","80DDB-1-followup")
        #if f==1 save data to database

    elif action=="80DDB-1-fallback":
        reply=sec80DDB_amt_fallback(session_id,"a1","80DDB-1-followup")

    elif action=="80DDB-2-1":
        subid="2"
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec80DDB_amt_fallback(session_id,"a2","80DDB-2-followup")
            f=-1
        else:
            x=Amount_Restrictions.objects.filter(section_id="80DDB")
            x={'data':x}
            for i in x['data']:
                if i.subsection_id==subid:
                    amt=int(amt)
                    max_amt=i.Max_Amount
                    if amt<=max_amt:
                        f=1
                        reply=sec80DDB_amt_confirm(amt,session_id,"a2","80DDB-2-followup")
                        try:
                            now = datetime.datetime.now()
                            now=now.year
                            now=str(now)
                            print(now)
                            t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="80DDB",subsection_id=subid)
                            t.amount=amt
                            t.save()
                            print("Updated")
                        except Exception as e:
                            save_data("80DDB",subid, amt)
                            print("Saved")
                    else:
                        f=-1
                        reply=sec80DDB_amt_exceed(max_amt,session_id,"a80","80DDB-2-followup")
        #if f==1 save data to database

    elif action=="80DDB-2-fallback":
        reply=sec80DDB_amt_fallback(session_id,"a2","80DDB-2-followup")
    elif action=="80DDB-3-1":
        subid="3"
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec80DDB_amt_fallback(session_id,"a3","80DDB-3-followup")
            f=-1
        else:
            x=Amount_Restrictions.objects.filter(section_id="80DDB")
            x={'data':x}
            for i in x['data']:
                if i.subsection_id==subid:
                    amt=int(amt)
                    max_amt=i.Max_Amount
                    if amt<=max_amt:
                        f=1
                        reply=sec80DDB_amt_confirm(amt,session_id,"a3","80DDB-3-followup")
                        try:
                            now = datetime.datetime.now()
                            now=now.year
                            now=str(now)
                            print(now)
                            t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="80DDB",subsection_id=subid)
                            t.amount=amt
                            t.save()
                            print("Updated")
                        except Exception as e:
                            save_data("80DDB",subid, amt)
                            print("Saved")
                    else:
                        f=-1
                        reply=sec80DDB_amt_exceed(max_amt,session_id,"a3","80DDB-3-followup")
        #if f==1 save data to database

    elif action=="80DDB-3-fallback":
        reply=sec80DDB_amt_fallback(session_id,"a3","80DDB-3-followup")
    elif action=="Sec4":
            reply=sec4(session_id)
    elif action=="cancel-Sec4":
        reply=sec4_cancel(session_id)
    elif action=="Sec4-fallback":
        reply=sec4_fallback(session_id)
    elif action=="Sec4-1":
        sec4_subid="1"
        reply=sec4_getAMT(session_id,sec4_subid)
    elif action=="Sec4-1-1":
        subid="1"
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec4_amt_fallback(session_id,"sprev","S4-1-followup")
            f=-1
        else:
            f=1
            reply=sec4_amt_confirm(amt,session_id,"sprev","S4-1-followup")
            try:
                now = datetime.datetime.now()
                now=now.year
                now=str(now)
                print(now)
                t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="Section-4",subsection_id=subid)
                t.amount=amt
                t.save()
                print("Updated")
            except Exception as e:
                save_data("Section-4",subid, amt)
                print("Saved")
        #if f==1 save data to database

    elif action=="Sec4-1-fallback":
            reply=sec4_amt_fallback(session_id,"sprev","S4-1-followup")
    elif action=="Sec4-2":
        sec4_subid="2"
        reply=sec4_getAMT(session_id,sec4_subid)
    elif action=="Sec4-2-1":
        subid="2"
        amt=req['queryResult']['outputContexts'][0]['parameters']['number']
        f=0
        if amt=="":
            reply=sec4_amt_fallback(session_id,"tprev","S4-2-followup")
            f=-1
        else:
            f=1
            reply=sec4_amt_confirm(amt,session_id,"tprev","S4-2-followup")
            try:
                now = datetime.datetime.now()
                now=now.year
                now=str(now)
                print(now)
                t=Section_Deduction.objects.get(employee_code=employeecode,year=now,section_id="Section-4",subsection_id=subid)
                t.amount=amt
                t.save()
                print("Updated")
            except Exception as e:
                save_data("Section-4",subid, amt)
                print("Saved")
        #if f==1 save data to database

    elif action=="Sec4-2-fallback":
            reply=sec4_amt_fallback(session_id,"tprev","S4-2-followup")
    elif action=="ec":
        x=req['queryResult']['queryText']
        if x=="INFI4466":
            reply=welcome1()
        else :
            reply = welcome2()
    print(action,session_id)
    # return generated response
    return JsonResponse(reply, safe=False)
