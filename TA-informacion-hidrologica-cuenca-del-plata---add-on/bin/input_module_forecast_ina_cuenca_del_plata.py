
# encoding = utf-8

import os
import sys
import time
import datetime
from datetime import datetime  
from datetime import timedelta  
import requests, json

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''

def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # global_account = definition.parameters.get('global_account', None)
    # localization_method = definition.parameters.get('localization_method', None)
    # localization_method_value = definition.parameters.get('localization_method_value', None)
    
    if definition.parameters.get('opt_timestart')=="":
        raise ValueError("method value error")
        
    if definition.parameters.get('opt_timeend')=="":
        raise ValueError("method value error")
        
    if definition.parameters.get('opt_seriesid')=="":
        raise ValueError("method value error")
        
    if definition.parameters.get('opt_sitecode')=="":
        raise ValueError("method value error")
        
    if definition.parameters.get('opt_varId')=="":
        raise ValueError("method value error")
        
    pass

def collect_events(helper, ew):
    """Implement your data collection logic here

    # The following examples get the arguments of this input.
    # Note, for single instance mod input, args will be returned as a dict.
    # For multi instance mod input, args will be returned as a single value.
    opt_global_account = helper.get_arg('global_account')
    opt_localization_method = helper.get_arg('localization_method')
    opt_localization_method_value = helper.get_arg('localization_method_value')
    # In single instance mode, to get arguments of a particular input, use
    opt_global_account = helper.get_arg('global_account', stanza_name)
    opt_localization_method = helper.get_arg('localization_method', stanza_name)
    opt_localization_method_value = helper.get_arg('localization_method_value', stanza_name)

    # get input type
    helper.get_input_type()

    # The following examples get input stanzas.
    # get all detailed input stanzas
    helper.get_input_stanza()
    # get specific input stanza with stanza name
    helper.get_input_stanza(stanza_name)
    # get all stanza names
    helper.get_input_stanza_names()

    # The following examples get options from setup page configuration.
    # get the loglevel from the setup page
    loglevel = helper.get_log_level()
    # get proxy setting configuration
    proxy_settings = helper.get_proxy()
    # get account credentials as dictionary
    account = helper.get_user_credential_by_username("username")
    account = helper.get_user_credential_by_id("account id")

    # The following examples show usage of logging related helper functions.
    # write to the log for this modular input using configured global log level or INFO as default
    helper.log("log message")
    # write to the log using specified log level
    helper.log_debug("log message")
    helper.log_info("log message")
    helper.log_warning("log message")
    helper.log_error("log message")
    helper.log_critical("log message")
    # set the log level for this modular input
    # (log_level can be "debug", "info", "warning", "error" or "critical", case insensitive)
    helper.set_log_level(log_level)

    # The following examples send rest requests to some endpoint.
    response = helper.send_http_request(url, method, parameters=None, payload=None,
                                        headers=None, cookies=None, verify=True, cert=None,
                                        timeout=None, use_proxy=True)
    # get the response headers
    r_headers = response.headers
    # get the response body as text
    r_text = response.text
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = response.json()
    # get response cookies
    r_cookies = response.cookies
    # get redirect history
    historical_responses = response.history
    # get response status code
    r_status = response.status_code
    # check the response status, if the status is not sucessful, raise requests.HTTPError
    response.raise_for_status()

    # The following examples show usage of check pointing related helper functions.
    # save checkpoint
    helper.save_check_point(key, state)
    # delete checkpoint
    helper.delete_check_point(key)
    # get checkpoint
    state = helper.get_check_point(key)

    # To create a splunk event
    helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
    """

    '''
    # The following example writes a random number as an event. (Multi Instance Mode)
    # Use this code template by default.
    import random
    data = str(random.randint(0,100))
    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data)
    ew.write_event(event)
    '''

    '''
    # The following example writes a random number as an event for each input config. (Single Instance Mode)
    # For advanced users, if you want to create single instance mod input, please use this code template.
    # Also, you need to uncomment use_single_instance_mode() above.
    import random
    input_type = helper.get_input_type()
    for stanza_name in helper.get_input_stanza_names():
        data = str(random.randint(0,100))
        event = helper.new_event(source=input_type, index=helper.get_output_index(stanza_name), sourcetype=helper.get_sourcetype(stanza_name), data=data)
        ew.write_event(event)
    '''
    
    helper.log_debug("action=start, function="+collect_events.__name__)
    
    # gets results from API calls
    res = get_nivelhidrometria(helper)
    if res == None:
        helper.log_info("action=none")
        return
    
    
    # write event in JSON format 
    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=res)
    try:
        ew.write_event(event)
    except Exception as e:
        raise e
    
    helper.log_info("action=success")
    return

def get_nivelhidrometria(helper):
    
    helper.log_debug("action=start, function="+get_nivelhidrometria.__name__)
    
    # Endtime today
    today = datetime.now()
    end_time = datetime.now() + timedelta(days=15)  
    

    # input parameters
    #opt_timestart = helper.get_arg('opt_timestart')
    opt_seriesid = helper.get_arg('opt_seriesid')
    opt_siteCode = helper.get_arg('opt_sitecode')
    opt_varId = helper.get_arg('opt_varId')
    opt_callid = helper.get_arg('opt_callid')
    opt_all = helper.get_arg('opt_all')
    opt_corid = helper.get_arg('opt_corid')
    #opt_restart_checkpoint = helper.get_arg('restart_checkpoint')

    # base_url variable to store url
    base_url = "https://alerta.ina.gob.ar/pub/datos/datosProno"
        
    # checkpoint key
    key=helper.get_input_stanza_names()

    # restarts checkpoint
    #if opt_restart_checkpoint: 
    #    helper.log_debug("action=restart_checkpoint, function="+get_nivelhidrometria.__name__)
    #    helper.delete_check_point(key)
    
     # get checkpoint
    #checkpoint = helper.get_check_point(key)
    #if checkpoint is None:
    #    checkpoint=opt_timestart
    #helper.log_debug("action=get_checkpoint, checkpoint="+str(checkpoint)+", function="+get_nivelhidrometria.__name__)


    # Complete url address
    complete_url= base_url
    complete_url+= "&timeStart=" + str(today)
    complete_url+= "&timeEnd=" + str(end_time)
    complete_url+= "&seriesId=" + str(opt_seriesid)
    complete_url+= "&calId=" + str(opt_callid)
    complete_url+= "&all=" + str(opt_all)
    complete_url+= "&siteCode=" + str(opt_siteCode)
    complete_url+= "&varId=" + str(opt_varId)
    complete_url+= "&format=json"    
    
    # Return response object
    response = requests.get(complete_url)
    response_dict = json.loads(response.text)
    response_data=json.dumps(response_dict["data"])
        
    
    # Refresh Endtime
    #today = datetime.datetime.now()
    #end_time = today.strftime("%Y-%m-%d")
    
    # Set checkpoint
    #checkpoint=end_time
    #helper.save_check_point(key, checkpoint)
    #helper.log_debug("action=set_checkpoint, checkpoint="+str(checkpoint)+", function="+get_nivelhidrometria.__name__)


    helper.log_debug("action=collect, status="+str(response.raise_for_status())+", function="+get_nivelhidrometria.__name__)

    return response_data