from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from investment_bot.models import user_database
from . import forms
from investment_bot.models import Section_Details as sd
from investment_bot.df_library import *

def sec80DDB(session_id):
    s="Please select your age criteria from the suggestion chip below."
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(["0-60","60-80","80 or more","None"])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    x=session_id
    outputcontext=[['a1','1',{'parameter_name':1}],['a2','1',{'parameter_name':1}],['a3','1',{'parameter_name':1}],['80DDB-followup','1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec80DDB_fallback(session_id):
    s="Please select your age criteria from the suggestion chip below."
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(["0-60","60-80","80 or more","None"])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    x=session_id
    outputcontext=[['a1','1',{'parameter_name':1}],['a2','1',{'parameter_name':1}],['a3','1',{'parameter_name':1}],['80DDB-followup','1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec80DDB_cancel(session_id):
    s="Ok cancelled\n"
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

def sec80DDB_getAMT(session_id,subid):
    x=sd.objects.filter(section_id="80DDB")
    x={'data':x}
    s=""
    for i in x['data']:
        if i.subsection_id==subid:
            s=i.subsection_id+" "+i.query
            break
    s+="\n Please enter the amount for sec80DDB subsestion-"+subid
    fulfillmentText = s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr])
    if subid=="1":
        s1="a1"
    elif subid=="2":
        s1="a2"
    else:
        s1="a3"
    outputcontext=[[s1,'1',{'parameter_name':1}],['80DDB-followup','1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec80DDB_amt_fallback(session_id,param,param2):
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
    outputcontext=[[param,'1',{'parameter_name':1}],[param2,'1',{'parameter_name':1}],["80DDB-followup",'1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec80DDB_amt_confirm(amt,session_id,param1,param2):
    s="Amount Rs."+str(amt)+" is recorded for section 80DDB.\n"
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
    outputcontext=[['welcome','0',{'parameter_name':0}],['80DDB-followup','0',{'parameter_name':0}],[param1,'0',{'parameter_name':0}],[param2,'0',{'parameter_name':0}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply



def sec80DDB_amt_exceed(max_amt,session_id,param1,param2):
    s="Sorry The amount you entered exceeds the Max-Limit of This Section. Please enter the amount in appropriate bounds. The max limit is "+str(max_amt)
    fulfillmentText = s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr])
    outputcontext=[['80DDB-followup','1',{'parameter_name':1}],[param1,'1',{'parameter_name':1}],[param2,'1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply
