# Project Tasks

## High Priority

* [~] Ensure DCF and DDM are implemented
* [~] Fix up the portfolio builder to distribute the investment amount into #shares correctly
* [] Condition data for price prediction models
* [+] Catch exceptions from price prediction models

* [~] In filter, remove items with invalid financial data

* [~] Fix up the composite score calculation to implement basic weighted sum of scores correctly
* [] Configure proper industry retrieval and handling
* [+] Increase execution speed for testing/demo - Implement Implement use_predefined_test_stock_list in stock filter
* [~] Fix up the portfolio builder to use the customer metrics somehow
* [~] Implement financial data combiner
* [~] Ingest all relevant financial data and merge

## Low-Priority

* [] Document all functions
* [] Sanitize chatbot investment amount input
* [] Apply checks for data types etc. inside all functions
* [] Bounds testing unit tests

## Long-Term Development & Improvements

- [] Build more advanced models
- [] Valuation doesn't reliably predict price response, so need to re-think score computation.
- [] Composite score formulation

### Architecture improvements

- [] Testing area ("digital playground") for formulation and validation of models
- [] Interfaces - Chatbot, Configurator to specify input parameters, Data output, Alerts & trading signals output, Optimization interface
- [] Rolling portfolio optimization workflow
- [] Live instance with up-to-date rolling validation
- [] Sensor fusion framework
- [] Data processing pipeline improvements
