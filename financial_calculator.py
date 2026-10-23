def calculate_financials(freight_amount, advance_amount, diesel, toll, food, loading, unloading, other):
    """
    Computes financial breakdown for a trip memo:
    Total Expense = Diesel + Toll + Food + Loading + Unloading + Other Expenses
    Profit = Freight Amount - Total Expense
    Status = Profit (if profit >= 0) else Loss
    Net Amount = Freight Amount - Advance Amount - Total Expense
    """
    freight = float(freight_amount or 0.0)
    advance = float(advance_amount or 0.0)
    diesel_exp = float(diesel or 0.0)
    toll_exp = float(toll or 0.0)
    food_exp = float(food or 0.0)
    loading_exp = float(loading or 0.0)
    unloading_exp = float(unloading or 0.0)
    other_exp = float(other or 0.0)

    total_expense = round(diesel_exp + toll_exp + food_exp + loading_exp + unloading_exp + other_exp, 2)
    profit = round(freight - total_expense, 2)
    
    if profit < 0:
        status = "Loss"
        loss_amount = abs(profit)
        profit_amount = 0.0
    else:
        status = "Profit"
        profit_amount = profit
        loss_amount = 0.0

    net_amount = round(freight - advance - total_expense, 2)

    return {
        "freight_amount": freight,
        "advance_amount": advance,
        "total_expense": total_expense,
        "profit": profit,
        "profit_amount": profit_amount,
        "loss_amount": loss_amount,
        "net_amount": net_amount,
        "status": status,
        "breakdown": {
            "diesel": diesel_exp,
            "toll": toll_exp,
            "food": food_exp,
            "loading": loading_exp,
            "unloading": unloading_exp,
            "other": other_exp
        }
    }
