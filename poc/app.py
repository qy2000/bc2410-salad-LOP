from flask import Flask, render_template, request, redirect, url_for
import csv
import utils.linear as linear_model
import numpy as np

app = Flask(__name__)
data1 = linear_model.data_preparation()
data_input, total, data = linear_model.create_data_input(data1)

@app.route('/', methods=['GET','POST'])
def homepage():
    min_nutrition = []
    max_nutrition = []
    dietary_req = []
    user_input = {}
    if request.method == 'POST':
        min_nutrition.append(int(request.form['min_cal']))
        max_nutrition.append(int(request.form['max_cal']))
        min_nutrition.append(int(request.form['min_carb']))
        max_nutrition.append(int(request.form['max_carb']))
        min_nutrition.append(int(request.form['min_pro']))
        max_nutrition.append(int(request.form['max_pro']))
        min_nutrition.append(int(request.form['min_fat']))
        max_nutrition.append(int(request.form['max_fat']))
        min_nutrition.append(int(request.form['min_sug']))
        max_nutrition.append(int(request.form['max_sug']))
        # min_nutrition.append(int(request.form['min_sod']))
        # max_nutrition.append(int(request.form['max_sod']))
        user_input["min_nutrition"] = min_nutrition
        user_input["max_nutrition"] = max_nutrition
        user_input['budget'] = int(request.form['Budget'])
        user_input['max_num_of_premium_toppings'] = int(request.form['Max_Premium_Toppings'])
        dietary_req = request.form.getlist('dietary_req')
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
        return render_template("saladstop.html")


if __name__ == '__main__':
    app.run


