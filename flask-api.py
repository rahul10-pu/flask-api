from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)
empDB=[
 {
 'id':'101',
 'name':'Saravanan S',
 'expenses':[]
 }
 ]
vendorDB=[
 {
 'id':'11',
 'name':'amazon',
  'expenses': []
 }
 ]

@app.route('/get-employee/',methods=['GET'])
def getEmp():
    if request.args.get('employee_code')==None:
        return jsonify({'message': 'employee_code not passed.'}), 400
    flag=0
    for emp in empDB:
        if (emp['id'] == request.args['employee_code']):
            flag=1
    if flag==0:
        return jsonify({'message': 'invalid employee code passed.'}), 400
    flag=0
    empId=request.args['employee_code']
    usr = [ emp for emp in empDB if (emp['id'] == empId) ] 

    return jsonify({'name': usr[0]['name'],'employee_code':  usr[0]['id']})

@app.route('/add-employee/',methods=['POST'])
def createEmp():
    if not request.json:
        return jsonify({'message': 'name not passed.'}), 400
    if request.json.get('employee_code'):
        pass
    else:
        return jsonify({'message': 'employee_code not passed.'}), 400
    for emp in empDB:
        if (emp['id'] == request.json['employee_code']):
            return jsonify({'message': 'duplicate employee_code passed.'}), 400
    dat = {
    'id':request.json['employee_code'],
    'name':request.json['name'],
    'expenses':[]
    }
    empDB.append(dat)
    # return jsonify(dat)
    return jsonify({'message': 'employee created.'}), 201

@app.route('/get-vendor/',methods=['GET'])
def getVendor():
    if request.args.get('vendor_code')==None:
        return jsonify({'message': 'vendor code not passed.'}), 400
    flag=0
    for ven in vendorDB:
        if (ven['id'] == request.args['vendor_code']):
            flag=1
    if flag==0:
        return jsonify({'message': 'invalid vendor code passed.'}), 400

    vendorId=request.args['vendor_code']
    usr = [ vendor for vendor in vendorDB if (vendor['id'] == vendorId) ] 
    return jsonify({'vendor_code':usr[0]['id'],'name':usr[0]['name']})

@app.route('/add-vendor/',methods=['POST'])
def createVendor():
    if not request.json:
        return jsonify({'message': 'name not passed.'}), 400
    if request.json.get('vendor_code'):
        pass
    else:
        return jsonify({'message': 'vendor_code not passed.'}), 400
    for ven in vendorDB:
        if (ven['id'] == request.json['vendor_code']):
            return jsonify({'message': 'duplicate vendor_code passed.'}), 400
    dat = {
    'id':request.json['vendor_code'],
    'name':request.json['name'],
    'expenses':[]
    }
    vendorDB.append(dat)
    # return jsonify(dat)
    return jsonify({'message': 'vendor created.'}), 201
@app.route('/add-expense/',methods=['POST'])
def addExpense():
  
    # print("----------------------------------------------------")
    # print(request.json)
    if not request.json:
        return jsonify({'message': 'vendor code not passed.'}), 400
    if request.json.get('employee_code')==None:
        return jsonify({'message': 'employee_code not passed.'}), 400
    if request.json.get('expense_comment')==None:
        return jsonify({'message': 'expense comment not passed.'}), 400
    if request.json.get('expense_done_on'):
        pass
    else:
        return jsonify({'message': 'expense done on not passed.'}), 400
    if request.json.get('expense_amount'):
        pass
    else:
        return jsonify({'message': 'expense amount not passed.'}), 400
    flag=0
    for ven in vendorDB:
        if (ven['id'] == request.json.get('vendor_code')):
            flag=1
    if flag==0:
        return jsonify({'message': 'vendor code invalid.'}), 400
    flag=0
    for emp in empDB:
        if (emp['id'] == request.json.get('employee_code')):
            flag=1
    if flag==0:
        return jsonify({'message': 'employee code invalid.'}), 400
    if request.json.get('expense_comment')!="":
        pass
    else:
        return jsonify({'message': 'empty expense comment provided.'}), 400
    if len(request.json.get('expense_done_on').split("-"))==3:
        pass
    else:
        return jsonify({'message': 'expense done on is not in valid format.'}), 400
    a=request.json.get('expense_amount')
    if a.isdigit() or (a.replace('.','',1).isdigit() and a.count('.') < 2):
        pass
    else:
        return jsonify({'message': 'expense amount is not in valid format.'}), 400
    if request.json.get('expense_amount').isdigit():
        pass
    else:
        return jsonify({'message': 'expense amount not an integer.'}), 400
    em = [ emp for emp in empDB if (emp['id'] == request.json['employee_code']) ]
    dat1 = {
    'vendor': request.json['vendor_code'],
    'expense_done_on': request.json['expense_done_on'], 
    'expense_comment': request.json['expense_comment'],
    'expense_amount': request.json['expense_amount']
    }
    vn = [ vnd for vnd in vendorDB if (vnd['id'] == request.json['vendor_code']) ]
    dat2 = {
    'employee': request.json['employee_code'],
    'expense_done_on': request.json['expense_done_on'], 
    'expense_comment': request.json['expense_comment'],
    'expense_amount': request.json['expense_amount']
    }
    em[0]['expenses'].append(dat1)
    vn[0]['expenses'].append(dat2)

    # return jsonify({'emp':em[0],'ven':vn[0]})

    return jsonify({'message': 'expense created.'}), 201
@app.route('/get-expense-for-employee/',methods=['GET'])
def get_expense_for_employee():
    if request.args.get('employee_code')==None:
        return jsonify({'message': 'employee_code not passed.'}), 400
    flag=0
    for emp in empDB:
        if (emp['id'] == request.args['employee_code']):
            flag=1
    if flag==0:
        return jsonify({'message': 'invalid employee code passed.'}), 400
    empId=request.args['employee_code']
    usr = [ emp for emp in empDB if (emp['id'] == empId) ]
    li=[]
    for e in usr[0]['expenses']:
        d={'vendor':e['vendor'],
           'expense_comment':e['expense_comment'],
            'expense_done_on':e['expense_done_on'],
            'expense_amount' : e['expense_amount']
        }
        li.append(d)
    return jsonify({'name':usr[0]['name'],
                    'expenses': li}), 200
@app.route('/get-expense-for-vendor/',methods=['GET'])
def get_expense_for_vendor():
    if request.args.get('vendor_code')==None:
        return jsonify({'message': 'vendor code not passed.'}), 400
    flag=0
    for ven in vendorDB:
        if (ven['id'] == request.args['vendor_code']):
            flag=1
    if flag==0:
        return jsonify({'message': 'invalid vendor code passed.'}), 400

    venId=request.args['vendor_code']
    usr = [ ven for ven in vendorDB if (ven['id'] == venId) ]
    li=[]
    for e in usr[0]['expenses']:
        d={'employee':e['employee'],
           'expense_comment':e['expense_comment'],
            'expense_done_on':e['expense_done_on'],
            'expense_amount' : e['expense_amount']
        }
        li.append(d)
    return jsonify({'name':usr[0]['name'],
                    'expenses': li}), 200
if __name__ == '__main__':
 app.run(debug=True)

