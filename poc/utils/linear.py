from rsome import ro
from rsome import grb_solver as grb
import pandas as pd
import numpy as np
import traceback


def data_preparation():
    data1 = pd.read_csv('../data/menu.csv')
    ORIGINAL_QTY = 5
    data1['Total'] = ORIGINAL_QTY
    return data1


def create_data_input(data1):
    data = data1.values

    ingredient, ingredient_type, price, cost, calories, carbs, protein, fat, sugar =\
    data[:,0], data[:,1], data[:,2], data[:,6], data[:,8], data[:,9], data[:,10], data[:,11], data[:,12]

    vegan, vegetarian, gluten, dairy, nuts, spicy =\
    data[:,-9], data[:,-8], data[:,-7], data[:,-6], data[:,-5], data[:,-4]

    data_input = {
        "ingredient": ingredient,
        "ingredient_type": ingredient_type,
        "price": price,
        "cost": cost,
        "calories": calories,
        "carbs": carbs,
        "protein": protein,
        "fat": fat,
        "sugar": sugar,
        "vegan": vegan,
        "vegetarian": vegetarian,
        "gluten": gluten,
        "dairy": dairy,
        "nuts": nuts,
        "spicy": spicy,
    }

    total = data[:,-1]
    total[-1] = 0

    return data_input, total, data


def generate_salad(user_input, data_input, ingredient_qty):
    
    try:
    
        '''
        Construct Optimizer.
        '''
        model = ro.Model('Salad selector model')

        '''
        Other variables to be used later:
        n refers to the total number of ingredients offered by salad stop
        '''
        n = len(data_input["ingredient"])

        '''
        Initialize Decision Variables
        x is the selection of an ingredient in the salad (binary variables)
        s is the standard base selection (binary variable)
        t is the premium base selection (binary variable)
        '''
        x = model.dvar(n, vtype='B')
        s = model.dvar((1,), vtype='B')
        t = model.dvar((1,), vtype='B')

        '''
        Create Objective Function: To minimize cost paid by the customer while meeting user input constraints.
        
        This objective function is preferred because the problem stems from the customer side rather than the business side.
        Whereby customers are confused at what to order due to the presence of too many choices. If we are optimizing the choices
        customers should make, then we should minimize the cost of the salad paid by the customer as the customer would want to
        pay as little as possible for their salad.
        '''
        model.min((9.9*s + 11.9*t + sum(x[i]*data_input["price"][i] for i in range(n) if data_input["ingredient_type"][i] in ['Premium Topping'])))

        '''
        Alternative Objective Function: To maximize profit earned by the business while meeting user input constraints.
        '''
        # model.max((9.9*s + 11.9*t + sum(x[i]*data_input["price"][i] for i in range(n) if data_input["ingredient_type"][i] in ['Premium Topping'])) - (sum(x[i]*data_input["cost"][i] for i in range(n))))
        
        '''
        Constraints 1: Optimizer will not select ingredient with 0 quantity left 
        '''
        model.st(sum(x[i] for i in range(n) if ingredient_qty[i] == 0) == 0)

        '''
        Constraints 2: Depending on the base selected, ingredients should be of the same category as the type of base selected
        '''
        model.st(sum(x[i] for i in range(n) if data_input["ingredient_type"][i] in ['Standard Base', 'Wrap', 'Grain Bowl']) == s)
        model.st(sum(x[i] for i in range(n) if data_input["ingredient_type"][i] in ['Premium Base']) == t)

        '''
        Constraints 3: Ensure that either standard base is selected or premium base selected. Cannot be neither selected or both selected
        '''
        model.st(0 <= s <= 1)
        model.st(0 <= t <= 1)
        model.st(s + t == 1)

        '''
        Constraints 4: Ensure that only exactly 7 toppings unless the user wants more will be chosen
        '''
        model.st(sum(x[i] for i in range(n) if data_input["ingredient_type"][i] in ['Standard Topping']) == 7)

        '''
        Constraints 5: Ensure that only exactly 2 dressings unless the user wants more will be chosen
        '''
        model.st(sum(x[i] for i in range(n) if data_input["ingredient_type"][i] in ['Dressing (Asian)', 'Dressing (Western)']) == 2)

        '''
        Constraints 6: Ensure that the selection of ingredients meets nutrition requirements of user
        '''
        nutrition_list = [data_input["calories"], data_input["carbs"], data_input["protein"], data_input["fat"], data_input["sugar"]]
        for j in range(len(nutrition_list)):
            nutri =  nutrition_list[j]
            model.st(user_input["min_nutrition"][j] <= sum(x[i]*nutri[i] for i in range(n)))
            model.st(sum(x[i]*nutri[i] for i in range(n)) <= user_input["max_nutrition"][j])

        '''
        Constraints 7: Ensure that the dietary needs of user is met
        '''
        reqs = [data_input["vegan"], data_input["vegetarian"], data_input["gluten"], data_input["dairy"], data_input["nuts"], data_input["spicy"]]
        for k in range(len(user_input["dietary_req"])):
            req_type = reqs[k]
            if user_input["dietary_req"][k] == 0:
                model.st(sum(x[i] for i in range(n) if req_type[i] == 1) == 0 )

        '''
        Constraints 8: Ensure that the number of premium toppings meet user requirements
        '''
        model.st(sum(x[i] for i in range(n) if data_input["ingredient_type"][i] in ['Premium Topping']) >= user_input["max_num_of_premium_toppings"])

        '''
        Constraints 9: Ensure that the total cost of the salad is within the user's budget
        '''
        model.st((9.9*s + 11.9*t + sum(x[i]*data_input["price"][i] for i in range(n) if data_input["ingredient_type"][i] in ['Premium Topping'])) <= user_input["budget"])

        '''
        Constraints 10: Ensure that the total cost of the salad is within the user's budget
        '''
        model.st(x >= 0)
        
        '''
        Solve Model and generate results
        '''
        model.solve(grb)
        
        if int(s.get()[0]) == 1:
            base = 9.9
        else:
            base = 11.9

        return x.get(), model.get(), base
    
    except:

        traceback.print_exc()

        return [], 0, 0