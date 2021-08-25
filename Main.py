import Neural
import Processing
import Lineplot
import pandas as pd 
from sklearn.metrics import accuracy_score


TRAIN_SIZE = 3
TARGET_TIME = 1
HIDDEN_RNN =500
LAG_SIZE = 1
EMB_SIZE = 1

dailyreturn = Processing.load_snp_returns()

l = int (len(dailyreturn) * 0.9)

dailyreturn = Processing.Normalize(dailyreturn)

X,Y = Processing.split_into_chunks(dailyreturn, TRAIN_SIZE, TARGET_TIME, LAG_SIZE)

X,Y = Processing.createnumpyarray(X,Y,TRAIN_SIZE)

X_train, X_test, Y_train, Y_test = Processing.create_Xt_Yt(X, Y, l)

model = Neural.initialize_network(input_neu=TRAIN_SIZE,output_neu=1)

errors = Neural.training(model,X_train,Y_train,0.09,1)

result = []
resultnum=[]
actualresult = []
actualresultnum=[]
for i,row in enumerate(X_test):
     res = Neural.predict(model,row)

     if res[0] > 0.1:
         result.append(-1)
         resultnum.append(res[0])
     else:
         result.append(1)
         resultnum.append(res[0])
     actualresultnum.append(Y_test[i][0])
     
    
Lineplot.LinePlot(data1=resultnum,data2=actualresultnum)

#print(accuracy_score(resultnum, actualresultnum))

DF_Train = pd.read_csv(r'YESBANK.csv',sep=",", parse_dates=['Date'])

DF_Train['Diffrence'] = DF_Train.Close - DF_Train.Open 

DF_Train  = DF_Train.iloc[::-1]
DF_Train = DF_Train.iloc[l:len(DF_Train)-4]


#Generate Report
stock = 100
DF_Train['result'] = result
DF_Train['resultnum'] = resultnum

#DF_Train['actualresult'] = actualresult
DF_Train['actualresultnum'] = actualresultnum

DF_Train['ActualReturn'] = DF_Train.Diffrence*DF_Train.result*stock

totalInvest = DF_Train.Diffrence.abs().sum()

total_loss = DF_Train.ActualReturn[DF_Train.ActualReturn < 0].sum()

total_profit = DF_Train.ActualReturn[DF_Train.ActualReturn > 0].sum()

actual_profit = DF_Train.ActualReturn.sum()

print('TotalInvestment',totalInvest*stock)
print('Returns:',((actual_profit/(totalInvest*stock)))*100)
print('Net Profit:',actual_profit)
print('Total Profit : ',total_profit)
print('Total Loss : ',total_loss)

pd.DataFrame(DF_Train).to_csv("file.csv")