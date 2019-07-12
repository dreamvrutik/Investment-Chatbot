from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from investment_bot.models import user_database
from . import forms
from investment_bot.models import Section_Details as sd
from investment_bot.df_library import *

r1=['r1','1',{'parameter_name':1}]
r2=['r2','1',{'parameter_name':1}]
r3=['r3','1',{'parameter_name':1}]
r4=['r4','1',{'parameter_name':1}]
r5=['r5','1',{'parameter_name':1}]
r6=['r6','1',{'parameter_name':1}]
r7=['r7','1',{'parameter_name':1}]
r8=['r8','1',{'parameter_name':1}]
list_c=[r1,r2,r3,r4,r5,r6,r7,r8]

def amt_exceed(session_id,max_amt,subid):
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
    oc="rem-"+subid
    bc="Reimbursement-followup"
    cc="Reimbursement-"+subid+"-followup"
    gg="r"+subid
    outputcontext=[[oc,'1',{'parameter_name':1}],[bc,'1',{'parameter_name':1}],[cc,'5',{'parameter_name':1}],[gg,'1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def Reimbursement_fallback(session_id):
    s="Sorry.Can you say that again\n"
    x=sd.objects.filter(section_id="rem")
    x={'data':x}
    s+="Following are the fields in the form :\n"
    for i in x['data']:
        s+=i.subsection_id+" "+i.query+"\n"
    fulfillmentText = s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(["Telephone,Mobile,Internet", "Office Allowance","Vehicle Maintainance","Medical Reimbursement","Club Fees","Book/Journal","Tiifin/Meal","Cubic car capacity"])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    outputcontext=[['welcome','0',{'parameter_name':0}],['Reimbursement-followup','5',{'parameter_name':5}],]
    for i in list_c:
        outputcontext.append(i)
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def cancel_rem(session_id):
    s="Ok Cancelled\n"
    x=sd.objects.filter(section_id="rem")
    x={'data':x}
    s+="Following are the fields in the form :\n"
    for i in x['data']:
        s+=i.subsection_id+" "+i.query+"\n"
    fulfillmentText = s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(["Telephone,Mobile,Internet", "Office Allowance","Vehicle Maintainance","Medical Reimbursement","Club Fees","Book/Journal","Tiifin/Meal","Cubic car capacity"])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    outputcontext=[['welcome','0',{'parameter_name':0}],['Reimbursement-followup','5',{'parameter_name':5}],]
    for i in list_c:
        outputcontext.append(i)
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def rem_fallback(subid,session_id):
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
    oc="rem-"+subid
    bc="Reimbursement-followup"
    cc="Reimbursement-"+subid+"-followup"
    gg="r"+subid
    outputcontext=[[oc,'1',{'parameter_name':1}],[bc,'1',{'parameter_name':1}],[cc,'5',{'parameter_name':1}],[gg,'1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def Reimbursement(session_id):
    x=sd.objects.filter(section_id="rem")
    x={'data':x}
    s="Following are the fields in the form :\n"
    for i in x['data']:
        s+=i.subsection_id+" "+i.query+"\n"
    fulfillmentText = s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(["Telephone,Mobile,Internet", "Office Allowance","Vehicle Maintainance","Medical Reimbursement","Club Fees","Book/Journal","Tiifin/Meal","Cubic car capacity"])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    outputcontext=[['welcome','0',{'parameter_name':0}],['Reimbursement-followup','5',{'parameter_name':5}],]
    for i in list_c:
        outputcontext.append(i)
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def Reimbursement_amt_confirm(amt,session_id):
    s="Amount Rs"+str(amt)+" is filled in the form for the selected subsection of Reimbursement section.\n"
    x=sd.objects.filter(section_id="rem")
    x={'data':x}
    s+="Following are the fields in the form :\n"
    for i in x['data']:
        s+=i.subsection_id+" "+i.query+"\n"
    fulfillmentText = s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(["Telephone,Mobile,Internet", "Office Allowance","Vehicle Maintainance","Medical Reimbursement","Club Fees","Book/Journal","Tiffin/Meal","Cubic car capacity"])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    outputcontext=[['welcome','0',{'parameter_name':0}],['Reimbursement-followup','5',{'parameter_name':5}]]
    for i in list_c:
        outputcontext.append(i)
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply
