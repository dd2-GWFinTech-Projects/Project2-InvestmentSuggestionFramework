### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)


### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "PortfolioBuilder":
        return get_recommended_portfolio_intent_handler(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Intents Handlers ###
def get_recommended_portfolio_intent_handler(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    investingDuration = get_slots(intent_request)["investingDuration"]
    investmentAmount = get_slots(intent_request)["investingAmount"]
    risk = get_slots(intent_request)["risk"]
    investingExperienceLevel = get_slots(intent_request)["investingExperienceLevel"]
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.

        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data(investmentAmount)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.

        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )

        # Fetch current session attibutes
        output_session_attributes = intent_request["sessionAttributes"]

        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the initial investment recommendation

    recommended_portfolio = get_recommended_portfolio(
        investingDuration, investmentAmount, risk, investingExperienceLevel
    )
    recommended_portfolio_report = get_recommended_portfolio_report(
        recommended_portfolio
    )

    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": "Thank you for the information. Based on the inputs you provided, my recommendation is to invest the following portfolio: {}".format(
                recommended_portfolio_report
            ),
        },
    )


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response


### Data Validation ###
def validate_data(investmentAmount):
    """
    Validates the data provided by the user.
    """

    # Handle default starting values - pass responsibility to the slots to retrieve values

    if investmentAmount is None:
        return build_validation_result(True, None, None)

    if investmentAmount is not None:

        # Validate investmentAmount

        # TODO Remove "$"

        if float(investmentAmount) is None:
            return build_validation_result(
                False,
                "investmentAmount",
                "The investment amount must be a number. How much do you want to invest?",
            )

        investmentAmount = float(investmentAmount)

        if investmentAmount < 100:
            return build_validation_result(
                False,
                "investmentAmount",
                "The investment amount must be greater than or equal to $100. How much do you want to invest?",
            )

    # Success!
    return build_validation_result(True, None, None)


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def get_recommended_portfolio(
    investingDuration, investmentAmount, risk, investingExperienceLevel
):
    # TODO Retrieve stock list
    # TODO Retrieve price histories
    # TODO Retrieve company financial information (and metadata)
    # TODO Apply filter
    # TODO Call price and volatility analysis/prediction code
    # TODO Call company valuation prediction
    # TODO Call portfolio builder to assemble information into coherent portfolio
    # TODO Call function to add hedge positions
    return {
        "NOC": 10,
        "BA": 10,
        "XROLF": 10,
        "PYPL": 10,
        "JNJ": 10,
        "PFE": 10,
        "TSLA": 10,
        "AAPL": 10,
        "BTC": 10,
    }


def get_recommended_portfolio_report(recommended_portfolio):
    recommended_portfolio_report = "\n\n--------------------\n\n"
    for stock, quantity in recommended_portfolio.items():
        recommended_portfolio_report += f"\t{stock} - {quantity} shares\n"
    recommended_portfolio_report += "\n--------------------\n"
    return recommended_portfolio_report


# Service functions
def generate_plots():
    return None


def execute_portfolio_changeover(current_positions, new_portfolio):
    return None
