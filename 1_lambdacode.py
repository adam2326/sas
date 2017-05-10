
#################################################################################
#
# Initial function to route request to correct secondary handler
#
#################################################################################
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])



#################################################################################
#
# Secondary handlers for internal routing
#
#################################################################################

def on_launch(launch_request, session):
    # Called when the user launches the skill
    return get_welcome_response()


def on_intent(intent_request, session):
    # Called when the user specifies an 
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "InitializeIntent":
        return get_InitializeIntent_response()

    elif intent_name == "LoadTableIntent":
        return get_LoadTableIntent_response()

    elif intent_name == "ListTablesIntent":
        return get_ListTablesIntent_response()

    elif intent_name == "VariableSummaryIntent":
        return get_VariableSummaryIntent_response()

    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true"""
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


#################################################################################
#
# Functions that control the skill's behavior
#
#################################################################################

# -----------------------------------------------------------------------
# --------------- functionality for required functions ------------------
# -----------------------------------------------------------------------
def get_welcome_response():
	# when a user just "loads" the skills.
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "This is a Amazon Alexa interface to sas vieya."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with the same text.
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response():
	# when a user asks for help.
    session_attributes = {}
    card_title = "Help"
    speech_output = "Welcome to the help section for the Amazon Alexa interface to sas vieya."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))


def handle_session_end_request():
	# when the user cancels or quits.
    card_title = "Session Ended"
    speech_output = "Thank you for using the Amazon Alexa interface to sas vieya! We hope you enjoyed the experience."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



# -----------------------------------------------------------------------
# --------------- functionality for custom functions --------------------
# -----------------------------------------------------------------------

def get_InitializeIntent_response():
	# when user asks for the server to be turned on.
    session_attributes = {}
    card_title = "InitializeIntent_Info"
    speech_output = "The analytics server has been initialized."
    reprompt_text = speech_output
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))


def get_LoadTableIntent_response():
    session_attributes = {}
    card_title = "LoadTableIntent_Info"
    speech_output = "The table has been loaded"
    reprompt_text = speech_output
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))


def get_ListTablesIntent_response():
    session_attributes = {}
    card_title = "ListTablesIntent_Info"
    speech_output = "List of the current tables available in cas"
    reprompt_text = speech_output
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))


def get_ListTablesIntent_response():
    session_attributes = {}
    card_title = "VariableSummaryIntent_Info"
    speech_output = "The variable summary has been completed."
    reprompt_text = speech_output
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))

#################################################################################
#
# Helpers that build all of the responses
#
#################################################################################

# --------------- build speech response ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

# --------------- build response ----------------------
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
