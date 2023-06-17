from flask import Flask,render_template,request
import pymongo
import random
import pickle

public_model = pickle.load(open('models/knnpickle_file', 'rb'))
doctor_model = pickle.load(open('models/clf1pickle_file', 'rb'))

app = Flask(__name__)

@app.route("/")
def html():
    return render_template('index.html')
@app.route('/publicresult',methods=['POST','GET'])
def publicresult():
    if request.method=='POST':
        result=request.form
        db = client["heartcare"]
        bp = 0;chol = 0;sugar = 0
        temp=[]
        for m,n in result.items():
            temp.append(float(n))

        # prediction
        ttemp=[]
        x1 = [[29, 77], [0, 1], [94, 200], [126, 564], [0, 1], [0, 1]]
        locall = []
        for i in range(len(temp)):
            local = (temp[i] - x1[i][0]) / (x1[i][1] - x1[i][0])
            locall.append(local)
        ttemp.append(locall)
        # print(ttemp)

        # print("ttemp", ttemp)
        result1 = public_model.predict(ttemp)
        localll=result1[0]
        # print(result1[0])

        # suggestion
        suggestion = []

        if localll==1:
            collection = db["heartdisease"]
            data = collection.find_one({"_id": "1"}, {"_id": 0})
            temp7 = []
            temp8 = []
            for i, j in data.items():
                temp7.append(j)
            for k in range(5):
                y = random.randrange(len(temp7))
                if y not in temp8:
                    temp8.append(y)
                    suggestion.append(temp7[y])
            resultt=["Heart Disease Predicted"]
            conclusion=[]
            conclusion.append("!!!! Person is suffering from Heart Disease !!!!")
            conclusion.append("Please Contact the doctor as soon as possible")
            return render_template('publicform.html', result=result, resultt=resultt, suggestions=suggestion, conclusions=conclusion)
        else:
            # blood pressure
            if temp[2]>120 and temp[0]<18:
                bp = 1
                collection = db["bloodpressure"]
                data=collection.find_one({"age": "1-18"},{"_id":0,"age":0})
                temp1=[]
                temp2=[]
                for i,j in data.items():
                    temp1.append(j)
                for k in range(4):
                    y = random.randrange(len(temp1))
                    if y not in temp2:
                        temp2.append(y)
                        suggestion.append(temp1[y])
            if temp[2] > 135 and 19 < temp[0] < 40:
                bp = 1
                collection = db["bloodpressure"]
                data = collection.find_one({"age": "19-40"}, {"_id": 0, "age": 0})
                temp1 = []
                temp2 = []
                for i, j in data.items():
                    temp1.append(j)
                for k in range(4):
                    y = random.randrange(len(temp1))
                    if y not in temp2:
                        temp2.append(y)
                        suggestion.append(temp1[y])
            if temp[2] > 135 and temp[0] > 40:
                bp = 1
                collection = db["bloodpressure"]
                data = collection.find_one({"age": "41"}, {"_id": 0, "age": 0})
                temp1 = []
                temp2 = []
                for i, j in data.items():
                    temp1.append(j)
                for k in range(4):
                    y = random.randrange(len(temp1))
                    if y not in temp2:
                        temp2.append(y)
                        suggestion.append(temp1[y])
            # cholesterol
            if 170 < temp[3] < 210 and temp[0] < 19:
                chol = 1
                collection = db["cholesterol"]
                data = collection.find_one({"age": "0-19"}, {"_id": 0, "age": 0})
                temp3 = []
                temp4 = []
                for i, j in data.items():
                    temp3.append(j)
                for k in range(4):
                    y = random.randrange(len(temp3))
                    if y not in temp4:
                        temp4.append(y)
                        suggestion.append(temp3[y])
            if temp[3] > 200 and temp[0] > 19:
                chol = 1
                collection = db["cholesterol"]
                data = collection.find_one({"age": "0-19"}, {"_id": 0, "age": 0})
                temp3 = []
                temp4 = []
                for i, j in data.items():
                    temp3.append(j)
                for k in range(4):
                    y = random.randrange(len(temp3))
                    if y not in temp4:
                        temp4.append(y)
                        suggestion.append(temp3[y])
            # fasting blood sugar
            if temp[4]==1:
                sugar = 1
                collection = db["fastingbloodsugar"]
                data = collection.find_one({"_id":"1"}, {"_id": 0})
                temp5 = []
                temp6 = []
                for i, j in data.items():
                    temp5.append(j)
                for k in range(4):
                    y = random.randrange(len(temp5))
                    if y not in temp6:
                        temp6.append(y)
                        suggestion.append(temp5[y])
            resultt = ["No heart disease"]
            conclusion=[]
            if bp == 1:
                conclusion.append("Blood Pressure is high")
            if chol == 1:
                conclusion.append("Choleterol is high")
            if sugar == 1:
                conclusion.append("Fasting blood sugar is high")
            if len(conclusion)==0:
                conclusion.append("!!!!GOOD LUCK for your future !!!!")
                conclusion.append("Person are not suffering from any of these problems : ")
                conclusion.append("1. Blood pressure")
                conclusion.append("2. Cholesterol")
                conclusion.append("3. Fasting Blood Sugar")
            return render_template('publicform.html',result=result,resultt=resultt, suggestions=suggestion,conclusions=conclusion)

@app.route('/doctorresult',methods=['POST','GET'])
def doctorresult():
    if request.method=='POST':
        result=request.form
        temp=[]
        for m,n in result.items():
            temp.append(float(n))

        # prediction
        ttemp=[]
        x1 = [[0, 1], [1, 4], [0.0, 1.0], [0.0, 1.0], [-2.6, 5.0], [3.0, 7.0]]
        locall = []
        for i in range(len(temp)):
            local = (temp[i] - x1[i][0]) / (x1[i][1] - x1[i][0])
            locall.append(local)
        ttemp.append(locall)
        # print(ttemp)

        # print("ttemp", ttemp)
        result1 = doctor_model.predict(ttemp)
        localll=result1[0]
        if localll==1:
            resultt=["Heart Disease Predicted"]
            conclusions=["Person is suffering from heart disease"]
            return render_template('doctorform.html', result=result, resultt=resultt, conclusions=conclusions)
        else:
            resultt=["No heart disease"]
            conclusions=[]
            conclusions.append("!!!! GOOD NEWS !!!!")
            conclusions.append("Person are not suffering from heart disease.")
            return render_template('doctorform.html', result=result, resultt=resultt, conclusions=conclusions)
@app.route('/doctorform')
def doctorform():
    return render_template('doctorform.html')

@app.route('/publicform')
def publicform():
    return render_template('publicform.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/back')
def result1():
       return render_template('index.html')
if __name__=="__main__":
    app.run()
    client=pymongo.MongoClient("mongodb+srv://heartcare:heartcare@cluster0.3irrwx4.mongodb.net/test")
    # print(client)
# db=client["abcd"]
# collection=db["pymongocollection"]
# dictionary={'name':'a','marks':45}
# dictionary1={'name':'a1','marks':45}
# collection.insert_one(dictionary)
# collection.insert_one(dictionary1)


app.run(debug = True)
# by using debug = True it will work as development mode. So, no need to run and complie everytime after every change.