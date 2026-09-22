from pydantic import BaseModel,Field,field_validator,StrictStr,StrictInt

class User(BaseModel):
    ids:StrictInt
    names:str
    ages:int = Field(gt=0,lt=100)
    lastname:str


    @field_validator("lastname")
    def lastname_validator(cls,lname):
        if len(lname)<5:
            raise ValueError("Last name can not be 5 length")
        return lname


user=User(ids=1,names= "jaikey",ages=99,lastname="ddsss")

print(user.model_construct())

# ======= Generator example in python ==============
def createor():
    i=1
    while i<=200:
        yield i
        i+=1

x=createor()
print(next(x))
print(next(x))
#print(list(x))