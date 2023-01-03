# Financial Dashboard
# 12/23/22
# Written by Braxton Diaz and Travis Lee

# --- Imports -----------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import base64
import io
import random


# --- Plot Show ---------------------------------------------------------------
# Converts matplotlib plt to image data string
# plt is the matplotlib pyplot or figure
# width is the width of the graph image in pixels
# dpi (dots per inch) is the resolution of the image
def plt_show(plt, width=500, dpi=100):
    bytes = io.BytesIO()
    plt.savefig(bytes, format='png', dpi=dpi)  # Save as png image
    if hasattr(plt, "close"):
        plt.close()
    bytes.seek(0)
    base64_string = "data:image/png;base64," + \
        base64.b64encode(bytes.getvalue()).decode("utf-8")
    return "<img src='" + base64_string + "' width='" + str(width) + "'>"


# --- Expenses Pie Chart ------------------------------------------------------
# Reads the users monthly expenses and creates a pie chart with the data
# returns a string representing the image for the pie chart
def createExpense(inputs):
    # users monthly expenses
    y = [inputs['rent'], inputs['transportation'],
         inputs['entertainment'],
         inputs['food'], inputs['other'], inputs['expense_savings']
         ]
    # pie chart labels
    mylabels = ["Rent", "Transportation", "Entertainment",
                "Food", "Other", "Savings"]
    # pie chart colors
    mycolors = ["#FF5255", "#378AFF", "#FF75A4", "#FFA32F",
                "#E7FFDB", "#23A889"]
    # format pie chart with .1 size space between each slice
    myexplode = [.1, .1, .1, .1, .1, .1]
    # background color
    # plt.figure().patch.set_facecolor('#add8e6')
    # plot the chart
    plt.pie(y, labels=mylabels, colors=mycolors, autopct='%1.2f%%',
            explode=myexplode, shadow=True)
    return plt_show(plt)  # returns html string


# --- Savings Goal Chart ------------------------------------------------------
# Reads the users savings goal and compares current savings rate
# with the required rate to reach savings goal on time
# returns a string representing the image of the plot
def createSavingsGoal(inputs):
    slope = inputs['contribution']
    y_intercept = inputs['starting_savings']
    x_endpoint = (inputs['savings_goal'] - y_intercept)/inputs['contribution']
    x = np.linspace(0, x_endpoint, 100)
    y = slope * x + y_intercept
    # plot colort
    # plt.figure().patch.set_facecolor('#add8e6')
    # Current Saving Line
    plt.plot(x, y, '-b', label='Current Rate')
    # Saving Goal
    y_target = ((inputs['savings_goal'] - y_intercept) /
                inputs['months']) * x + y_intercept
    plt.plot(x, y_target, '-r', label='Target Rate')
    # Savings Target Line
    y_goal = 0 * x + inputs['savings_goal']
    plt.plot(x, y_goal, '--g', label='Savings Goal')
    # Plot config
    plt.legend(loc='upper center')
    plt.xlabel("Time (months)")
    plt.ylabel("Money")
    # plot saving img
    return plt_show(plt)


# --- Exponential Growth -----------------------------------------------------
# reads the users inputs and compares growth w/ and without compound interest
# returns a string representing the image for the plot
def createExponential(inputs):
    x = np.linspace(0, inputs['years'], 100)
    inside = 1 + (inputs['interest_rate'] / 100)
    rate = inputs['interest_rate'] / 100
    y = inputs['initial_investment'] * pow(inside, x) + (inputs['interest_contribution'] * (((pow(1 + rate / 12, 12 * x)) - 1) / (rate / 12)))
    # plt.figure().patch.set_facecolor('#add8e6')
    plt.plot(x, y, '-b', label='Compounding Rate')
    # without compound growth
    y = (inputs['interest_contribution'] * 12) * x + inputs['initial_investment']
    plt.plot(x, y, '-r', label='Current Rate')
    # Plot config
    plt.legend(loc='upper center')
    # plt.title("Compound Growth")
    plt.xlabel("Time (years)")
    plt.ylabel("Money")
    return plt_show(plt)


# --- Get Random Finance Tip --------------------------------------------------
# returns a random financial tip to be displayed
def getFinancialTip():
    # store tips as strings in array
    tips = [
        "58.1% of millennials have less than $10,000 in savings",
        "On average, Americans spend 10.5% of their income on food",
        "Spend less than your earn (duh)",
        "A $100 bill lasts about 22.9 years",
        "If a machine rejects your bill you can microwave it to crisp it back up",
        "If you have a retirement account worth $10,000 that grows at a rate of 8% per year, it will be worth over $46,600 in 20 years",
        "Historically, stocks provide a 10% rate over time",
        "People spend 12-18% more when using credit cards than when paying cash",
        "61% of Americans don’t have enough savings to cover a $1,000 emergency, according to a 2018 survey"
        "Credit cards were first used in the United States in the 1920’s",
    ]
    index = random.randint(0, len(tips) - 1)
    return tips[index]


# ------------------------- Main ----------------------------------------------
def main(inputs):
    # init images
    expense_img = None
    savings_img = None
    exponential_img = None
    current_months = None
    target_rate = None
    difference = None
    normal_total = None
    total_expenses = None
    interest_total = None
    interest_difference = None
    # create images based on selected option
    for i in range(len(inputs['options'])):
        if inputs['options'][i] == 'Expenses':
            expense_img = createExpense(inputs)
            expenses = [inputs['rent'], inputs['transportation'],
                        inputs['entertainment'],
                        inputs['food'], inputs['other'], inputs['expense_savings']
                    ]
            # calculate total expenses
            total_expenses = 0
            for x in expenses:
                total_expenses += x
        elif inputs['options'][i] == 'Saving Goals':
            savings_img = createSavingsGoal(inputs)
            current_months = round((inputs['savings_goal'] - inputs['starting_savings']) / inputs['contribution'],2)
            target_rate = round(((inputs['savings_goal'] - inputs['starting_savings']) / inputs['months']), 2)
            difference = round(target_rate - inputs['contribution'], 2)
        elif inputs['options'][i] == 'Compound Interest':
            exponential_img = createExponential(inputs)
            inside = 1 + (inputs['interest_rate'] / 100)
            rate = inputs['interest_rate'] / 100
            normal_total = round((inputs['interest_contribution'] * 12) * inputs['years'] + inputs['initial_investment'], 2)
            interest_total = round(inputs['initial_investment'] * pow(inside, inputs['years']) + (inputs['interest_contribution'] * (((pow(1 + rate / 12, 12 * inputs['years'])) - 1) / (rate / 12))), 2)
            interest_difference = round(interest_total - normal_total, 2)
    # get financial tip
    financial_tip = getFinancialTip()
    # --------- Return ----------------------------
    return {
        "expense_plot": expense_img,
        "savings_plot": savings_img,
        "exponential_plot": exponential_img,
        "financial_tip": financial_tip,
        "saving_rate": inputs['contribution'],
        "current_time": current_months,
        "savings_goal": inputs['savings_goal'],
        "months": inputs['months'],
        "difference": difference,
        "total_expenses": total_expenses,
        "rate": inputs['interest_rate'],
        "years": inputs['years'],
        "normal_total": normal_total,
        "interest_total": interest_total,
        "interest_difference": interest_difference
    }
