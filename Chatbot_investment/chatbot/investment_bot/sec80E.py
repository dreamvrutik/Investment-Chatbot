from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from investment_bot.models import user_database
from . import forms
from investment_bot.models import Section_Details as sd
from investment_bot.df_library import *

def sec_80E(session_id):
    x=sd.objects.filter(section_id="80E")
    x={'data':x}
    s=""
    for i in x['data']:
        s+=i.subsection_id+" "+i.query+"\n"
    s+="\n Please enter the amount for section 80E."
    fulfillmentText = s
    aog = actions_on_google_response()
    aog_sr = aog.simple_response([
        [fulfillmentText, fulfillmentText, False]
    ])
    #create suggestion chips
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr])
    outputcontext=[['80E-followup','1',{'parameter_name':1}],['80E-followup-2','1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def sec_80E_fallback(session_id):
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
    outputcontext=[['80E-followup','1',{'parameter_name':1}],['80E-followup-2','1',{'parameter_name':1}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply

def cancel_80E(session_id):
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

def sec_80E_amt_confirm(amt,session_id):
    s="Amount Rs."+str(amt)+" is filled for section 80E.\n"
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
    outputcontext=[['80E-followup','0',{'parameter_name':0}],['80E-followup-2','0',{'parameter_name':0}]]
    oc=ff_response.output_contexts(session_id,outputcontext)
    reply = ff_response.main_response(ff_text, ff_messages,output_contexts=oc)
    return reply
