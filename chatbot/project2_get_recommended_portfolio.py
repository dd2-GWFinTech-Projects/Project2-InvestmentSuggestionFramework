### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta


### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")


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


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


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


### Intents Handlers ###
def recommend_portfolio(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    firstName = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    investmentAmount = get_slots(intent_request)["investmentAmount"]
    riskLevel = get_slots(intent_request)["riskLevel"]
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.

        ### YOUR DATA VALIDATION CODE STARTS HERE ###

        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data(age, investmentAmount)

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

        ### YOUR DATA VALIDATION CODE ENDS HERE ###

        # Fetch current session attibutes
        output_session_attributes = intent_request["sessionAttributes"]

        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the initial investment recommendation

    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE STARTS HERE ###

    initial_recommendation = get_investment_recommendation(riskLevel)

    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE ENDS HERE ###

    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """{} thank you for your information;
            based on the risk level you defined, my recommendation is to choose an investment portfolio with {}
            """.format(
                firstName, initial_recommendation
            ),
        },
    )


### Data Validation ###
def validate_data(age, investmentAmount):
    """
    Validates the data provided by the user.
    """

    # Handle default starting values - pass responsibility to the slots to retrieve values

    if age is None and investmentAmount is None:
        return build_validation_result(True, None, None)

    if age is not None:

        # Validate age

        if int(age) is None:
            return build_validation_result(
                False, "age", "Age must be a number. How old are you?"
            )

        age = int(age)

        if age <= 0:
            return build_validation_result(
                False, "age", "Age must be greater than 0. How old are you?"
            )

        if age >= 65:
            return build_validation_result(
                False, "age", "Age must be less than 65. How old are you?"
            )

    if investmentAmount is not None:

        # Validate investmentAmount

        if float(investmentAmount) is None:
            return build_validation_result(
                False,
                "investmentAmount",
                "The investment amount must be a number. How much do you want to invest?",
            )

        investmentAmount = float(investmentAmount)

        if investmentAmount < 5000:
            return build_validation_result(
                False,
                "investmentAmount",
                "The investment amount must be greater than or equal to 5000. How much do you want to invest?",
            )

    # Success!
    return build_validation_result(True, None, None)


### Data Validation ###
def validate_data_v1(age, investmentAmount):
    """
    Validates the data provided by the user.
    """

    # Validate age

    if age is None or int(age) is None:
        return build_validation_result(
            False, "age", "Age must be a number. How old are you?"
        )

    age = int(age)

    if age <= 0:
        return build_validation_result(
            False, "age", "Age must be greater than 0. How old are you?"
        )

    if age >= 65:
        return build_validation_result(
            False, "age", "Age must be less than 65. How old are you?"
        )

    # Validate investmentAmount

    if investmentAmount is None or float(investmentAmount) is None:
        return build_validation_result(
            False,
            "investmentAmount",
            "The investment amount must be a number. How much do you want to invest?",
        )

    investmentAmount = float(investmentAmount)

    if investmentAmount < 5000:
        return build_validation_result(
            False,
            "investmentAmount",
            "The investment amount must be greater than or equal to 5000. How much do you want to invest?",
        )

    # Success!
    build_validation_result(True, None, None)


def get_investment_recommendation(riskLevel):
    """
    Computes recommended investment amount.
        none: "100% bonds (AGG), 0% equities (SPY)"
        very low: "80% bonds (AGG), 20% equities (SPY)"
        low: "60% bonds (AGG), 40% equities (SPY)"
        medium: "40% bonds (AGG), 60% equities (SPY)"
        high: "20% bonds (AGG), 80% equities (SPY)"
        very high: "0% bonds (AGG), 100% equities (SPY)"
    """
    if riskLevel == "None":
        return "100% bonds (AGG), 0% equities (SPY)"
    elif riskLevel == "Low":
        return "60% bonds (AGG), 40% equities (SPY)"
    elif riskLevel == "Medium":
        return "40% bonds (AGG), 60% equities (SPY)"
    elif riskLevel == "High":
        return "20% bonds (AGG), 80% equities (SPY)"
    elif riskLevel == "Very Low":
        return "80% bonds (AGG), 20% equities (SPY)"
    elif riskLevel == "Very High":
        return "0% bonds (AGG), 100% equities (SPY)"
    else:
        return None


### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "RecommendPortfolio":
        return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
