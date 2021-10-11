### Required Libraries ###
from main.pricegetter.PriceGetter import PriceGetter
from main.balancesheetgetter.BalanceSheetGetter import BalanceSheetGetter
from main.stockfilter.StockFilter import StockFilter
from main.priceanalysis.PriceForecaster import PriceForecaster
from main.valuation.ValuationCalculator import ValuationCalculator
from main.portfoliobuilder.PortfolioBuilder import PortfolioBuilder
from main.datastructures.CustomerMetrics import CustomerMetrics
from main.datastructures.StockInfoContainer import StockInfoContainer


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
    investmentAmount = get_slots(intent_request)["investmentAmount"]
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

    recommended_portfolio = get_recommended_portfolio(investingDuration, investmentAmount, risk, investingExperienceLevel)

    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": "Thank you for the information. Based on the inputs you provided, my recommendation is to invest the following portfolio: {}".format(
                recommended_portfolio
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


# Option 1: Build portfolio.
# Option 2: Modify portfolio based on: Filter output; combine with pre-defined sectors; or pre-defined map.



def get_recommended_portfolio(investingDuration, investmentAmount, risk, investingExperienceLevel):

    # Construct helper objects
    price_getter = PriceGetter()
    balance_sheet_getter = BalanceSheetGetter()
    stock_filter = StockFilter()
    price_forecaster = PriceForecaster()
    valuation_calculator = ValuationCalculator()
    portfolio_builder = PortfolioBuilder()

    # Build data structures
    customer_metrics = CustomerMetrics(investingDuration, investmentAmount, risk, investingExperienceLevel)
    stock_info_container = StockInfoContainer()

    # Retrieve stock list
    stock_ticker_list = price_getter.get_tickers()
    # stock_ticker_list = ["AAPL", "BNGO", "CIIC"]
    stock_info_container.add_ticker_list(stock_ticker_list)

    # Retrieve price histories
    price_getter.get_prices(stock_info_container, trailing_n_days=100)

    # Retrieve company financial information (and metadata)
    balance_sheet_getter.load_financial_info(stock_info_container)

    # Apply filter
    stock_filter.filter(stock_info_container)

    # Call price and volatility analysis/prediction code
    price_forecaster.analyze(stock_info_container)

    # Call company valuation prediction
    valuation_calculator.analyze(stock_info_container)

    # Call portfolio builder to assemble information into coherent portfolio
    portfolio_builder.build_suggested_portfolio(customer_metrics, stock_info_container)

    # Call function to add hedge positions
    portfolio_builder.add_hedge_positions(stock_info_container)

    # Generate string portfolio representation
    suggested_portfolio = stock_info_container.get_portfolio()
    return portfolio_builder.transform_portfolio_to_str(suggested_portfolio)


# Service functions
def generate_plots():
    return None


def execute_portfolio_changeover(current_positions, new_portfolio):
    return None
