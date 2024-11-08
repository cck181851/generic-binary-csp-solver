import sys 

n,problem,output_file=sys.argv[1:]
n=int(n)

def initialize(problem,n):
    variables=list() 
    domains=list()      
    constraints=dict()
    if problem=="P1":
        return initializeP1(variables,domains,constraints,n)
    if problem=="P2":
        return initializeP2(variables,domains,constraints,n)    

def initializeP1(variables,domains,constraints,n):
    for i in range(1,n+1):
        variables.append("Q"+str(i))
    for i in range(n):
        domains.append(set(i for i in range(n)))
    constraints="""def f(x,y,valX,valY):
        return valX!=valY and abs(x-y)!=abs(valX-valY)"""
    return [variables,domains,constraints]


def initializeP2(variables,domains,constraints,n):
    variables[:]=["Western Australia","Northern Territory","South Australia","Queensland","New South Wales","Victoria","Tasmania"]   
    for _ in range(7):
        domains.append(set(i for i in range(1,n+1)))
    constraints="""def f(s1,s2,color1,color2):
            return not (s1==0 and s2 in (1,2) or s1==1 and s2 in (0,2,3) or s1==2 and s2 in (0,1,3,4,5) or s1==3 and s2 in (1,2,4) or s1==4 and s2 in (2,3,5) or s1==5 and s2 in (2,4)) or color1!=color2"""   
    return [variables,domains,constraints]  
 

variables,domains,constraints=initialize(problem,n)
mode="binary" if problem in ["P1","P2"] else "generic"
f=open(output_file,"w+")
f.write(str(mode)+"\n")
f.write(str(variables)+"\n")
f.write(str(domains)+"\n")
f.write(str(constraints)+"\n")
f.flush()
f.close()            
