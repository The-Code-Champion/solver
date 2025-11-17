import numpy as np
from numpy import linspace,append
import sympy as sp
from sympy import Eq, symbols, simplify
from sympy.solvers import solve
import flask
from flask import Flask, request, render_template, app

Flask_app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def equation_solver():

    Var = request.form.get('Var_num','').split(',')
    Eq = request.form.get('Eq_num','').split(';')
    Constant = request.form.get('Constant_num','').split(',')

    Eq_length = len(Eq)
    Var_length = len(Var)
    Constant_length = len(Constant)

    Eq_range = range(Eq_length)
    Var_range = range(Var_length)
    Constant_range = range(Constant_length)

    Eqs = []
    Variables = []
    Consts = []
    Consts_Vals = []

    

    if Var_length <= Eq_length:
        for number in Var_range:
            Variables.append(Var.split(',')[number].strip())
        for number in Eq_range:
            Eq_Split = []
            Eq_Split = [Eq,0]
            eq = Eq(Eq_Split[0],Eq_Split[1])
            Eqs.append(eq)

        for num in Constant_range:
            Const = Constant[num].split(':')
            Consts.append(Const[num][0].strip())
            Consts_Vals.append(Const[num][1].strip())

        substitution_map = {}
        Variables2 = symbols(Variables)

        for num in Constant_range:
            substituted_vals = {Consts[num]: Consts_Vals[num]}
            substitution_map.update(substituted_vals)
    
        substituted_eqs = [eq.subs(substitution_map) for eq in Eqs]

        output = solve(substituted_eqs,Variables2,dict=True)

        outputValues = {}

        for number in Eq_range:
            outVal = {Variables[number]: float(output[0][Variables2[number].evalf()])}
            outputValues.update(outVal)

        print(outputValues)
    elif Var_length > Eq_length:
        print('Too many unknowns for the number of equations.')
    else:
        print('You broke the code')

'''
Ax
Dx
Ay
AB
AC
BC
BD
BE
CE
DE
Ax+Dx-F
Ay+2*G
-G*d1+F*d2-Dx*(d2+d3)
Ax+AC*(d1/sqrt(d1^2+d2^2))
Ay-AB-AC*(d2/sqrt(d1^2+d2^2))
-F-BC-AC*(d1/sqrt(d1^2+d2^2))
-CE+AC*(d2/sqrt(d1^2+d2^2))
Dx+DE
G+BD
BC+BE*(d1/sqrt(d1^2+d3^2))
d1:4.49
d2:5.26
d3:5.81
F:73.4
G:65.8

#########################################

Ax,Dx,Ay,AB,AC,BC,BD,BE,CE,DE
Ax+Dx-F;Ay+2*G;-G*d1+F*d2-Dx*(d2+d3);Ax+AC*(d1/sqrt(d1^2+d2^2));Ay-AB-AC*(d2/sqrt(d1^2+d2^2));-F-BC-AC*(d1/sqrt(d1^2+d2^2));-CE+AC*(d2/sqrt(d1^2+d2^2));Dx+DE;G+BD;BC+BE*(d1/sqrt(d1^2+d3^2))
d1:4.49,d2:5.26,d3:5.81,F:73.4,G:65.8
'''