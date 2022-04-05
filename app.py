from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)
min_nutrition = []
max_nutrition = []
dietary_req = []
user_input = {}

@app.route('/', methods=['GET','POST'])
def homepage():
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
        min_nutrition.append(int(request.form['min_sod']))
        max_nutrition.append(int(request.form['max_sod']))
        user_input["min_nutrition"] = min_nutrition
        user_input["max_nutrition"] = max_nutrition
        user_input['budget'] = int(request.form['Budget'])
        user_input['max_num_of_premium_toppings'] = int(request.form['Max_Premium_Toppings'])
        dietary_req = request.form.getlist('dietary_req')
        user_input["dietary_req"] = dietary_req
        return redirect(url_for('recommendations', user_input=user_input))
    else:
        return render_template("saladstop.html")


@app.route('/recommendations', methods=['GET','POST'])
def recommendations():
    return render_template("recommendations.html",user_input=user_input)



if __name__ == '__main__':
    app.run


