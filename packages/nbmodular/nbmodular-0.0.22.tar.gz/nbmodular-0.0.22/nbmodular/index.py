#|echo: false
import pandas as pd
def get_my_previous_variable():
    my_previous_variable = 100
    return my_previous_variable

def two_plus_three():
    a = 2
    b = 3
    c = a+b
    print (f'The result of adding {a}+{b} is {c}')
    return a, b, c

def add_100(my_previous_variable):
    my_previous_variable = my_previous_variable + 100
    print (f'The result of adding 100 to my_previous_variable is {my_previous_variable}')
    return my_previous_variable

def multiply_by_two(c):
    d = c*2
    print (f'Two times {c} is {d}')
    return d

def analyze(x):
    x = [1, 2, 3]
    y = [100, 200, 300]
    z = [u+v for u,v in zip(x,y)]
    product = [u*v for u, v in zip(x,y)]
    return x, y, x, y

def determine_approximate_age(name, birthday_year=2000):
    current_year = datetime.datetime.today().year
    approximate_age = current_year-birthday_year
    print (f'hello {name}, your approximate age is {approximate_age}')
    return approximate_age, current_year

def use_current_year(current_year):
    print (current_year)

def myfunc(x, y, a=1, b=3):
    print ('hello', a, b)
    c = a+b
    return c

def other_func(a, b):
    print ('hello', a, b)
    c = a+b
    return c

def my_new_function():
    my_new_local = 3
    my_other_new_local = 4

def my_second_new_function():
    my_second_variable = 100
    my_second_other_variable = 200

def bunch_data():
    x = Bunch (a=1, b=2)
    return x

def bunch_processor(x, day=1):
    a = x["a"]
    b = x["b"]
    c = 3
    a = 4
    x["a"] = a
    x["c"] = c
    x["day"] = day
    return x

def days(df, fy, x=1, y=3, n=4):
    df_group = df.groupby(['Year','Month']).agg({'Day': lambda x: len (x)})
    df_group = df.reset_index()
    print ('other args: fy', fy, 'x', x, 'y', y)
    return df_group, x

def multiples(x, n):
    result = [x*i for i in range(n)]
    return result

def say_hi():
    print ('hi')

# -----------------------------------------------------
# pipeline
# -----------------------------------------------------
def index_pipeline (test=False, load=True, save=True, result_file_name="index_pipeline"):
    """Pipeline calling each one of the functions defined in this module."""
    
    # load result
    result_file_name += '.pk'
    path_variables = Path ("index") / result_file_name
    if load and path_variables.exists():
        result = joblib.load (path_variables)
        return result

    my_previous_variable = get_my_previous_variable ()
    a, b, c = two_plus_three ()
    my_previous_variable = add_100 (my_previous_variable)
    d = multiply_by_two (c)
    x, y, x, y = analyze (x)
    approximate_age, current_year = determine_approximate_age (name)
    use_current_year (current_year)
    c = myfunc (x, y)
    c = other_func (a, b)
    my_new_function ()
    my_second_new_function ()
    x = bunch_data ()
    x = bunch_processor (x)
    df_group, x = days (df, fy)
    result = multiples (x, n)
    say_hi ()

    # save result
    result = Bunch (x=x,my_previous_variable=my_previous_variable,a=a,b=b,approximate_age=approximate_age,d=d,y=y,df_group=df_group,result=result,c=c,current_year=current_year)
    if save:    
        path_variables.parent.mkdir (parents=True, exist_ok=True)
        joblib.dump (result, path_variables)
    return result

