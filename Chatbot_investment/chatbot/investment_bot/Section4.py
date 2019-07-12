from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from investment_bot.models import user_database
from . import forms
from investment_bot.models import Section_Details as sd
from investment_bot.df_library import *

def sec4(session_id):
    s="Previous Employer Details.\nPlease select the option from the suggestion chip below."
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(["Salary","TDS","None"])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    x=session_id
    outputcontext=[['sprev','1',{'parameter_name':1}],['tprev','1',{'parameter_name':1}],['S4-followup','1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply


def sec4_cancel(session_id):
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

def sec4_fallback(session_id):
    s="Please select from the suggestion chip below."
    fulfillmentText=s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    aog_sc = aog.suggestion_chips(["Salary","TDS","None"])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
    x=session_id
    outputcontext=[['sprev','1',{'parameter_name':1}],['tprev','1',{'parameter_name':1}],['S4-followup','1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec4_getAMT(session_id,subid):
    x=sd.objects.filter(section_id="Section-4")
    x={'data':x}
    s=""
    for i in x['data']:
        if i.subsection_id==subid:
            s=i.subsection_id+" "+i.query
            break
    s+="\n Please enter the amount for sec4 subsestion-"+subid
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
        s1="sprev"
    else:
        s1="tprev"
    outputcontext=[[s1,'1',{'parameter_name':1}],['S4-followup','1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec4_amt_fallback(session_id,param,param2):
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
    outputcontext=[[param,'1',{'parameter_name':1}],[param2,'1',{'parameter_name':1}],["S4-followup",'1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec4_amt_confirm(amt,session_id,param1,param2):
    s="Amount Rs."+str(amt)+" is recorded for section 80D.\n"
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
    outputcontext=[['welcome','0',{'parameter_name':0}],['S4-followup','0',{'parameter_name':0}],[param1,'0',{'parameter_name':0}],[param2,'0',{'parameter_name':0}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply
