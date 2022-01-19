from flask import Flask, request, render_template
# Initiating flask app
app = Flask(__name__)
# default index page of the site
@app.route('/')
def sql_database():
    from DB import sql_query #multiple connections to always get latest image of db
    status, results = sql_query(''' SELECT * FROM Products''')
    if status== 'Success':
        msg = 'SELECT * FROM Products'
    else: msg= '\nError: '+ str(results)
    print(results)
    return render_template('index.html', results=results, msg=msg)   

# for inserting data to db from html form
@app.route('/insert',methods = ['POST', 'GET']) 
def sql_datainsert():
    from DB import sql_edit_insert, sql_query
    if request.method == 'POST':
        P_name = request.form['P_name']
        # print(P_name)
        Product_id = request.form['Product_id']
        P_price = request.form['P_price']
        P_condition = request.form['P_condition']
        P_quant = request.form['P_quant']
        Description = request.form['Description']
        msg= sql_edit_insert(''' INSERT INTO Products (Product_id,P_name,P_price,P_condition,P_quant,Description) VALUES (?,?,?,?,?,?) ''', (Product_id,P_name,P_price,P_condition,P_quant,Description) )
        if msg=="Success":
            msg = 'INSERT INTO Products (Product_id,P_name,P_price,P_condition,P_quant,Description) VALUES ('+(Product_id)+','+P_name+','+P_price+','+P_condition+','+P_quant+','+Description+')'
        else: msg= "\nError: " + str(msg)
    _,results = sql_query(''' SELECT * FROM Products''')
    
    return render_template('index.html', results=results, msg=msg) 

#Deleting selected row, fetched the prod_id here to filter the search in query
@app.route('/delete',methods = ['POST', 'GET']) 
def sql_datadelete():
    from DB import sql_delete, sql_query
    if request.method == 'GET':
        delProduct_id = request.args.get('delProduct_id')
        print('delProduct_id:',delProduct_id)
        msg= sql_delete(''' DELETE FROM Products where Product_id = ? ''', (delProduct_id,) )
        if msg=="Success":
            msg= msg+ ' DELETE FROM Products WHERE Product_id = ' + delProduct_id + ''
        else: msg= "\nError: " + str(msg)
    _,results = sql_query(''' SELECT * FROM Products''')

    return render_template('index.html', results=results, msg=msg)
#method that creates csv file of the db, saves it in the root project folder.
@app.route('/export_data', methods=['POST','GET'])
def save_csv():
    from DB import tocsv, sql_query
    msg= tocsv()
    _,results = sql_query(''' SELECT * FROM Products''')
    return render_template('index.html', results=results,msg=msg)

# Step 1 of Updating process, loads the html form with selected row for update
@app.route('/query_edit',methods = ['POST', 'GET']) 
def sql_editlink():
    from DB import sql_query, sql_query2
    if request.method == 'GET':
        editProduct_id = request.args.get('editProduct_id')
        print("editProduct_id##",editProduct_id)
        status, new_results = sql_query2(''' SELECT * FROM Products where Product_id = ?''', (editProduct_id,))
        if status== "Success": 
            msg= status
        else: msg= str(new_results)
    _,results = sql_query(''' SELECT * FROM Products''')
    return render_template('index.html', new_results=new_results, results=results,msg= msg)

#Step 2 of Updating process, simple update query from the html form.
@app.route('/edit',methods = ['POST', 'GET']) 
def sql_dataedit():
    from DB import sql_edit_insert, sql_query
    if request.method == 'POST':
        P_name = request.form['P_name']
        Product_id = request.form['Product_id']
        P_price = request.form['P_price']
        P_condition = request.form['P_condition']
        P_quant = request.form['P_quant']
        Description = request.form['Description']
        msg = sql_edit_insert(''' UPDATE Products set Product_id=?,P_name=?,P_price=?,P_condition=?,P_quant=?,Description=? WHERE Product_id=? ''', (Product_id,P_name,P_price,P_condition,P_quant,Description,Product_id) )
        if msg=="Success":
            msg=msg+' UPDATE Products set  P_name = ' + P_name + ', P_price = ' + P_price + ', P_condition = ' + P_condition + ', P_quant = ' + P_quant + ', Description = ' + Description + ' WHERE Product_id = ' + Product_id
        else:
            msg= "\nError: " + str(msg)
    _,results = sql_query(''' SELECT * FROM Products''')
    return render_template('index.html', results=results, msg=msg)

if __name__ == "__main__":
    app.run(debug=True)

