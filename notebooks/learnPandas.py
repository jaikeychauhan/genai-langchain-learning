import pandas as pd

#Creating Dataframe
#df=pd.DataFrame([2,4,3,11])
data={
    'Name':['Rahul','shiv','Veer','dimple'],
    'Age':[22,55,8,35],
    'Salary':[3000.89,23333.66,80000.55,89797.44]
}
df=pd.DataFrame(data)

#print(df.rename(columns={'Salary':'Month_Salary'},inplace=True))
#print(df.describe())

#df.to_csv(f'D:\PythonProjects\TestProj\output_file.csv',index=False)

# loadcsv=pd.read_csv('D:\PythonProjects\TestProj\output_file.csv')
# print(loadcsv)

#---------------Filter condition which return required rows-------------------
#---------------based on the condtion-----------------------------------
    #data=df[(df['Age']>22) & (df['Salary']>40000)]
    #print(data)

#=========Filter with where, it returns all data whether condition match=============
#=========or not. matched condtion shows data and not matched shows null or NaN=========
# data=df.where((df['Age']>22) & (df['Salary']>25000))
# print(data)
    #      Name   Age     Salary
    # 0     NaN   NaN        NaN
    # 1     NaN   NaN        NaN
    # 2     NaN   NaN        NaN
    # 3  dimple  35.0  897978.44

#==========Rows and Columns (Add, Update, Delete Operations)================
# 1. Add new column
df['Team']=['CEO','HR','CTO','HR']
#print(df)

# 2. Add new column based on the calculations
df['Bonus']=df['Salary'] * 2
#print(df)

# 3. Adding new row 
df.loc[len(df)]=['Mohan',40,55000,'Accountant',110000]
#print(df)

# 4. Update row value based on index name
df.loc[1,'Salary']=245000
#print(df)

# 5. Update value based on Column value
df.loc[df.Name=="Veer","Salary"]=880
print(df)
 

