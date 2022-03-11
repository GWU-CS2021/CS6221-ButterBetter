# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

status_init = "init"
status_init_location = "location"
status_ready = "ready"
status_preference = "preference"
status_result = "result"

speech_return = "Welcome back %s! Tell me what would you like today, you could try by saying 'best asian food around' "
speech_new = "Hey, you are new here, please tell me your name to start "
speech_ready = "you could try by saying 'find asian food around' "
speech_init_complete = "Thanks %s, I will remember that, Tell me what would you like today "+speech_ready
speech_init_error_name = 'Sorry %s, Something went wrong, please tell me your name again '
speech_ask_location = 'Thanks %s, And please tell me where you are '
speech_ask_name = "Thanks, I got it. And please tell your name "
speech_sorry = 'Sorry I did not get that. '
speech_preference = 'please tell me your preference, you can try by saying "quiet restaurant within walk distance"'
speech_result = 'You can try by saying "show me some review" to hear some review, or "send to my phone" to get ' \
                'detailed information '
speech_result_ask = "You can try by saying repeat,next,show review or send to my phone "
speech_finish_search = 'After searching for %s by preference %s, '
speech_list_result = "I found %s, It is %s minutes walk away and opens until %s ,"
speech_end_of_list = "that's the end of the list "
speech_fallback_init = "Hmm, I'm not sure. "+speech_init_error_name
speech_fallback_init_re = speech_new
speech_fallback_ready = "Ok, let's start again. " + speech_ready
speech_fallback_ready_re = speech_ready
speech_review = "user %s rated %s %.1f out of 5, %s "
speech_review_notfound = "review not found "
speech_result_notfound = "no result is found "
speech_sent_to_phone = "Great choice %s, Information of %s is sent, enjoy your meal！"
speech_help = {status_ready: speech_ready,
               status_init: "please tell me your name to start ",
               status_init_location:"please tell me your location ",
               status_preference:speech_preference,
               status_result:speech_result}
speech_Introduction = "Hi, I'm I min food, a voice assistant willing to help. Just talk to me. And I can give you" \
                      " suggestion on restaurant choice. Say help if you don't know what to do"




class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        sys_object = handler_input.request_envelope.context.system
        device_id = sys_object.device.device_id
        valid, name, geo_coord, address = utils.check_user_exist(device_id)
        session_attr = handler_input.attributes_manager.session_attributes
        if valid:
            speak_output = speech_return % (name)
            session_attr["user_name"] = name
            session_attr["status"] = status_ready
        else:
            speak_output = speech_new
            session_attr["status"] = status_init
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


def get_slot_value_generic(handler_input, slot_name):
    slot = ask_utils.get_slot(handler_input=handler_input, slot_name=slot_name)
    return slot.resolutions.resolutions_per_authority[0].values[0].value.name


class NameIntentHandler(AbstractRequestHandler):
    """Handler for update/insert user location/name"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NameIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # slots = handler_input.request_envelope.request.intent.slots

        user_name = ask_utils.get_slot_value(handler_input, "user_name")

        # location = slots["location"]
        sys_object = handler_input.request_envelope.context.system
        device_id = sys_object.device.device_id
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["user_name"] = user_name
        if "location" in session_attr:
            location = session_attr["location"]
            if utils.add_user_record(device_id,user_name,location):
                session_attr["status"] = status_ready
                speech = speech_init_complete % user_name
                ask_output = speech_sorry+speech_ready
            else:
                session_attr["status"] = status_init
                speech = speech_init_error_name % user_name
                ask_output = speech_init_error_name % user_name
        else:
            speech = speech_ask_location % user_name
            ask_output = speech_sorry+speech_ask_location % user_name
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(ask_output)
                .response
        )


class LocationIntentHandler(AbstractRequestHandler):
    """Handler for update/insert user location/name"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("LocationIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # slots = handler_input.request_envelope.request.intent.slots

        # user_name = slots["user_name"]
        location = ask_utils.get_slot_value(handler_input, "location")
        sys_object = handler_input.request_envelope.context.system
        device_id = sys_object.device.device_id
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["location"] = location
        if "user_name" in session_attr:
            user_name = session_attr["user_name"]
            if utils.add_user_record(device_id, user_name, location):
                session_attr["status"] = status_ready
                speech = speech_init_complete % user_name
                ask_output = speech_sorry + speech_ready
            else:
                session_attr["status"] = status_init
                speech = speech_init_error_name % user_name
                ask_output = speech_init_error_name % user_name
        else:
            session_attr["status"] = status_init
            speech = speech_ask_name
            ask_output = speech_ask_name
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(ask_output)
                .response
        )


class SearchIntentHandler(AbstractRequestHandler):
    """Handler for search restaurant"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SearchIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # slots = handler_input.request_envelope.request.intent.slots

        # user_name = slots["user_name"]
        type = get_slot_value_generic(handler_input, "type")
        session_attr = handler_input.attributes_manager.session_attributes
        if session_attr["status"] != status_ready:
            speech = speech_help[session_attr["status"]]
            ask_output = speech
        else:
            session_attr["type"] = type
            speech = ("%s is a great choice. " + speech_preference) % type
            ask_output = speech_sorry+speech_preference
            session_attr["status"] = status_preference

        return (
            handler_input.response_builder
                .speak(speech)
                .ask(ask_output)
                .response
        )


class PreferIntentHandler(AbstractRequestHandler):
    """Handler for search restaurant"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("PreferIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # slots = handler_input.request_envelope.request.intent.slots
        pref_a = ask_utils.get_slot_value(handler_input, "pref_a")
        pref_b = ask_utils.get_slot_value(handler_input, "pref_b")
        if pref_b is None:
            pref_b = ""
            if pref_a is None:
                pref_a = "random"
            else:
                pref_a = get_slot_value_generic(handler_input, "pref_a")
        else:
            pref_b = get_slot_value_generic(handler_input, "pref_b")
        session_attr = handler_input.attributes_manager.session_attributes
        speech = speech_help[session_attr["status"]]
        ask_output = speech
        sys_object = handler_input.request_envelope.context.system
        device_id = sys_object.device.device_id

        if session_attr["status"] == status_preference:
            # TODO inplement get real restaurant info here
            restaurants = utils.get_restaurant(utils.get_md5(device_id),pref_a,pref_b,session_attr["type"])
            if len(restaurants) == 0:
                speech = speech_result_notfound
                session_attr["status"] = status_ready
            else:
                session_attr["result"] = restaurants
                session_attr["marker"] = 0
                # result common structure
                #current = session_attr["result"][session_attr["marker"]]
                current=restaurants[0]

                speech = (speech_finish_search + speech_list_result + speech_result_ask) % \
                           (session_attr["type"],pref_a+","+pref_b, current["title"], int(current["dist"]*30),
                            utils.get_time_str(current["close"]))
                session_attr["repeat"] = speech
                ask_output = speech_sorry + speech_result_ask
                session_attr["status"] = status_result

        return (
            handler_input.response_builder
                .speak(speech)
                .ask(ask_output)
                .response
        )


class NextIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.NextIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        speech = speech_help[session_attr["status"]]
        ask_output = speech_help[session_attr["status"]]
        if session_attr["status"] == status_result:
            if session_attr["marker"]+1<len(session_attr["result"]):
                session_attr["marker"]+=1
                current = session_attr["result"][session_attr["marker"]]
                speech = (speech_list_result + speech_result_ask) % \
                         (current["title"], int(current["dist"] * 20), utils.get_time_str(current["close"]))
                session_attr["repeat"] = speech
                ask_output = speech_sorry + speech_result_ask
            else:
                speech = speech_end_of_list
        elif session_attr["status"] == status_preference:
            sys_object = handler_input.request_envelope.context.system
            device_id = sys_object.device.device_id
            # TODO inplement get real restaurant info here
            restaurants = utils.get_restaurant(utils.get_md5(device_id),"random","random",session_attr["type"])
            if len(restaurants) == 0:
                speech = speech_result_notfound
                session_attr["status"] = status_ready
            else:
                session_attr["result"] = restaurants
                session_attr["marker"] = 0
                # result common structure
                current = session_attr["result"][session_attr["marker"]]

                speech = (speech_finish_search + speech_list_result + speech_result_ask) % \
                         (session_attr["type"], "random", current["title"], int(current["dist"] * 30),
                          utils.get_time_str(current["close"]))
                session_attr["repeat"] = speech
                ask_output = speech_sorry + speech_result_ask
                session_attr["status"] = status_result
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(ask_output)
                .response
        )


class PreviousIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.PreviousIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        speech = speech_help[session_attr["status"]]
        ask_output= speech
        if session_attr["status"] == status_result:
            if session_attr["marker"]-1>=0:
                session_attr["marker"]-=1
                current = session_attr["result"][session_attr["marker"]]
                speech = (speech_list_result + speech_result_ask) % \
                               (current["title"], int(current["dist"] * 30), utils.get_time_str(current["close"]))
                session_attr["repeat"] = speech
                ask_output = speech_sorry + speech_result_ask
            else:
                speech = speech_end_of_list

        return (
            handler_input.response_builder
                .speak(speech)
                .ask(ask_output)
                .response
        )


class ReviewIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ReviewIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        speech = speech_help[session_attr["status"]]
        ask_output = speech
        if session_attr["status"] == status_result:
            # TODO search for review
            valid,name,review,user,rating=utils.get_review(session_attr["result"][session_attr["marker"]]["rest_id"])
            if valid:
                speech= speech_review % (user,name,rating,review)
            else:
                speech = speech_review_notfound
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(ask_output)
                .response
        )


class SendToPhoneIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.SendToPhoneIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        speech = speech_help[session_attr["status"]]
        ask_output = speech
        if session_attr["status"] == status_result:
            restaurant = session_attr["result"][session_attr["marker"]]
            utils.send_to_phone(session_attr["user_name"],restaurant)
            # TODO send restaurant to phone
            speech = speech_sent_to_phone % (session_attr["user_name"], restaurant["title"])
            session_attr["status"] = status_ready
        return (
            handler_input.response_builder
                .speak(speech)
                #.ask(ask_output)
                .response
        )

class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech = speech_Introduction

        return (
            handler_input.response_builder
                .speak(speech)
                .ask(speech)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        return (
            handler_input.response_builder
                .speak(speech_help[session_attr["status"]])
                .ask(speech_help[session_attr["status"]])
                .response
        )


class RepeatIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        speech = speech_help[session_attr["status"]]
        if "repeat" in session_attr and session_attr["status"] == status_result:
            speech = session_attr['repeat']
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(speech)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speech)
                .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        session_attr = handler_input.attributes_manager.session_attributes
        if session_attr["status"] == status_init or session_attr["status"] == status_init_location:
            speech = speech_fallback_init
            reprompt =  speech_fallback_init_re
        else:
            session_attr["status"] = status_ready
            speech = speech_fallback_ready
            reprompt = speech_fallback_ready_re

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speech = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speech)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speech)
                .ask(speech)
                .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(NameIntentHandler())
sb.add_request_handler(LocationIntentHandler())
sb.add_request_handler(SearchIntentHandler())
sb.add_request_handler(PreferIntentHandler())
sb.add_request_handler(NextIntentHandler())
sb.add_request_handler(PreviousIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(ReviewIntentHandler())
sb.add_request_handler(SendToPhoneIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
