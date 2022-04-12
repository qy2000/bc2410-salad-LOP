from flask import Flask, render_template, request, redirect, url_for, Response
import csv
import utils.linear as linear_model
import utils.stochastic as stochastic_model
import numpy as np
import pandas as pd
import random

app = Flask(__name__)
data1 = linear_model.data_preparation()
data_input, total, data = linear_model.create_data_input(data1)

expected_amount_of_orders_df = None

@app.route('/', methods=['GET','POST'])
def homepage():
    min_nutrition = []
    max_nutrition = []
    dietary_req = []
    user_input = {}
    if request.method == 'POST':

        value1 = request.form.getlist('Vegan') 
        value2 = request.form.getlist('Vegetarian') 
        value3 = request.form.getlist('Gluten-Free') 
        value4 = request.form.getlist('Dairy-Free') 
        value5 = request.form.getlist('Nuts-Free') 
        value6 = request.form.getlist('Spicy')

        def convert_to_0_or_1(val):
            if val == []:
                return 0
            else:
                return 1 

        min_nutrition.append(int(float(request.form['min_cal'])))
        max_nutrition.append(int(float(request.form['max_cal'])))
        min_nutrition.append(int(float(request.form['min_carb'])))
        max_nutrition.append(int(float(request.form['max_carb'])))
        min_nutrition.append(int(float(request.form['min_pro'])))
        max_nutrition.append(int(float(request.form['max_pro'])))
        min_nutrition.append(int(float(request.form['min_fat'])))
        max_nutrition.append(int(float(request.form['max_fat'])))
        min_nutrition.append(int(float(request.form['min_sug'])))
        max_nutrition.append(int(float(request.form['max_sug'])))
        # min_nutrition.append(int(request.form['min_sod']))
        # max_nutrition.append(int(request.form['max_sod']))
        user_input["min_nutrition"] = min_nutrition
        user_input["max_nutrition"] = max_nutrition
        user_input['budget'] = int(float(request.form['Budget']))
        user_input['max_num_of_premium_toppings'] = int(float(request.form['Max_Premium_Toppings']))
        # dietary_req = request.form.getlist('dietary_req')

        dietary_req = [
            convert_to_0_or_1(value1), 
            convert_to_0_or_1(value2), 
            convert_to_0_or_1(value3), 
            convert_to_0_or_1(value4), 
            convert_to_0_or_1(value5), 
            convert_to_0_or_1(value6)
        ]

        user_input["dietary_req"] = dietary_req
        response, cost, base = linear_model.generate_salad(user_input, data_input, total)

        if base == 0:
            return render_template("recommendations.html",user_input=user_input,output="Cannot make a salad... Impossible set of constraints")

        total_cost = 0
        total_cost += base
        ingredient_arr = []
        for i in range(len(response)):
            if response[i] > 0:
                index = np.where(data_input["ingredient"] == data[:,0][i])[0][0]

                ingredient_arr.append("{}, {}".format(data[:,0][i], data_input["ingredient_type"][index]))
                
                if data_input["ingredient_type"][index] == "Premium Topping":
                    total_cost += data_input["price"][index]
                
                if total[i] > 0:
                    total[i] -= 1


        return render_template("recommendations.html",user_input=user_input,output=[ingredient_arr, base, round(total_cost,2), sum(total)])
    else:
        return render_template("saladstop.html", injection={"dietary_arr": [
            {"form": "cal", "label": "Calories", "min": 0, "max": 1000, "step":1}, 
            {"form": "carb", "label": "Carbohydrates", "min": 0, "max": 250, "step":1}, 
            {"form": "pro", "label": "Proteins", "min": 0, "max": 250, "step":1}, 
            {"form": "fat", "label": "Fats", "min": 0, "max": 100, "step":1},
            {"form": "sug", "label": "Sugars", "min": 0, "max": 200, "step":1}
            ],
            "restriction_arr": [
            {"name": "Vegan"},  
            {"name": "Vegetarian"},  
            {"name": "Gluten-Free"},  
            {"name": "Dairy-Free"},   
            {"name": "Nuts-Free"},  
            {"name": "Spicy"},    
            ]
            })


@app.route('/stochastic', methods=['GET','POST'])
def stochasticpage():
    if request.method == 'POST':

        data1 = pd.read_csv(request.files['menu'])
        Demand_data = pd.read_csv(request.files['demand'])
        d = Demand_data.set_index('date').tail(21)

        Param_data = pd.DataFrame().assign(Ingredient=data1['Ingredient'], COGS=data1['COGS_per_serving'], \
                                   Ingredient_Type=data1['Ingredient_type'], Additional_Price_For_Premium_Toppings=data1['Price'], \
                                   Space = data1['Serving_size']/1000)
        Param_data['Price'] = None
        Param_data['Space'] = None

        for i in range(Param_data.shape[0]):
            if Param_data["Ingredient_Type"][i] in ["Standard Base", "Wrap", "Grain Bowl", "Standard Topping", "Dressing (Western)", "Dressing (Asian)"]:
                Param_data["Price"][i] = 0.99
            elif Param_data["Ingredient_Type"][i] in ["Premium Base"]:
                Param_data["Price"][i] = 2.99
            elif Param_data["Ingredient_Type"][i] in ["Premium Topping"]:
                Param_data["Price"][i] = Param_data["Additional_Price_For_Premium_Toppings"][i]
            Param_data["Space"][i] = round(random.uniform(0, 1), 2)
        Param_data["Min_order"] = None
        Param_data["Min_order"] = pd.Series([min(d[i]) for i in d.columns])
        Param_data = Param_data.set_index('Ingredient').T

        def formatter_for_stochastic_optimizer(p_data, data, type_, num = 1):
            if type_ == "demand":
                return np.array(p_data.values[:,0:data.shape[1]].astype(int))
            else:
                return np.array(p_data.values[num,0:data.shape[1]].astype(np.float64))

        demand = formatter_for_stochastic_optimizer(d, d, "demand")
        price = formatter_for_stochastic_optimizer(Param_data, d, "price", 4)
        cost = formatter_for_stochastic_optimizer(Param_data, d, "cost", 0)
        space = formatter_for_stochastic_optimizer(Param_data, d, "space", 3)
        min_order = formatter_for_stochastic_optimizer(Param_data, d, "Min_order", 5)

        total_space = 10000

        expected_amount_of_orders, expected_amount_of_profit = stochastic_model.generate_quantities_and_expected_profits(price, cost, demand, space, total_space, min_order)

        global expected_amount_of_orders_df

        expected_amount_of_orders_df = pd.DataFrame().assign(Ingredient=list(data1['Ingredient'])[:-1], Quantity_to_order=expected_amount_of_orders)
        expected_amount_of_orders_df = expected_amount_of_orders_df.set_index("Ingredient").T

        return render_template("analysis.html", user_input={
            "labels":list(d.columns), 
            "expected_orders":expected_amount_of_orders, 
            "expected_profit":expected_amount_of_profit
            })
    else:
        return render_template("saladstop_admin.html")


@app.route("/download")
def getPlotCSV():
    global expected_amount_of_orders_df
    temp = expected_amount_of_orders_df.to_csv()
    expected_amount_of_orders_df = None
    return Response(
        temp,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=analysis.csv"})


if __name__ == '__main__':
    app.run


