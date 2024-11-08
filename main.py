import sys,collections,time,ast 

args=sys.argv
functions=args[1:-1]
input=args[-1] 


file=open(input,"r+")
mode=file.readline().strip()
variables=file.readline() 
domains=file.readline() 
pre_constraints=file.read() # type: ignore
variables=[n.strip() for n in ast.literal_eval(variables)] 
domains=ast.literal_eval(domains)
exec(pre_constraints)    
n=len(variables)
neighbors={i:set() for i in range(n)}
total_nodes_expanded=[0]

tmp=[i[1] for i in sorted([(i,idx) for idx,i in enumerate(variables)])]
sorted_variables={i:idx for idx,i in enumerate(tmp)}
constraint_count=collections.Counter()

def checker(assignment,a,b,aVal,bVal):
    if mode=="binary":
        return f(a,b,aVal,bVal) # type: ignore
    else:
        return f(assignment,a,b,aVal,bVal) # type: ignore


for var1 in range(n):
    for var2 in range(n):
        for dom1 in domains[var1]:
            for dom2 in domains[var2]:
                if not checker({},var1,var2,dom1,dom2):
                    constraint_count[(var1,var2)]+=1 
                    constraint_count[(var2,var1)]+=1    
                    neighbors[var1].add(var2)
                    neighbors[var2].add(var2) 

def constraint_propagation(domains,constraints):
    def revise(Xi,Xj):
        revised=False 
        removed=set()
        for domainXi in domains[Xi]:
            if not any (checker({},Xi,Xj,domainXi,domainXj) for domainXj in domains[Xj]):
                revised=True
                removed.add(domainXi)
        for domain in removed:
            domains[Xi].remove(domain)         
        return revised
    queue=set() 
    for key in neighbors.keys():
        for nei in neighbors[key]:
            queue.add((key,nei))
    while queue:
        Xi,Xj=queue.pop()
        if revise(Xi,Xj):
            if not domains[Xi]: return False 
            for nei in neighbors[Xi]:
                if nei!=Xj:
                    queue.add((Xi,nei))
    return True        

def number_of_conflicts(assignment,var,val):    
    tot=0
    for var2 in neighbors.get(var,[]):
        if var2 in assignment and not checker(assignment,var,var2,val,assignment[var2]):
            tot+=1                      
    return tot

def number_of_legal_moves(assignment,var):
    tot = 0
    for val in domains[var]:
        if number_of_conflicts(assignment,var,val)==0:
            tot += 1
    return tot   

def select_unassigned_variable(assignment):       
    MRV= list() 
    DH = list()
    AN = list()
    index_map,idx={},0
    for v in range(n):
        if v not in assignment:
            MRV.append([v,number_of_legal_moves(assignment,v)])            
            DH.append([v,-sum(constraint_count[(v,vv)] if vv not in assignment else 0 for vv in neighbors[v])])
            AN.append([v,sorted_variables[v]])              
            index_map[v]=idx 
            idx+=1         
    f1=lambda x:MRV[index_map[x]][1]    
    f2=lambda x:DH[index_map[x]][1]
    f3=lambda x:AN[index_map[x]][1]
    variables=list(index_map.keys()) 
    if "MRV" in args and "DH" in args:        
        variables.sort(key=lambda x:(f1(x),f2(x),f3(x)))
    if "MRV" in args and "DH" not in args:
        variables.sort(key=lambda x:(f1(x),f3(x)))
    if "MRV" not in args and "DH" in args:
        variables.sort(key=lambda x:(f2(x),f3(x)))
    if "MRV" not in args and "DH" not in args:
        variables.sort(key=lambda x:f3(x))
    return variables[0] 

def number_of_eliminated(assignment,var,val):
    tot=0
    for nei in neighbors[var]:
        if var not in assignment:
            for domain in domains[nei]:
                if not checker(assignment,var,nei,val,domain):
                    tot+=1
    return tot                            
   
def order_domain_values(assignment,var):   
    if "LCV" not in args : 
        return sorted(domains[var])    
    return sorted(domains[var],key=lambda val:number_of_eliminated(assignment,var,val))

def assign(assignment,var,value):
    removed=[(var,i) for i in domains[var] if i!=value]
    if "CP" in args:
        for nei in neighbors[var]:
            for domain in list(domains[nei]):
                if not checker(assignment,var,nei,value,domain):
                    domains[nei].remove(domain)
                    removed.append((nei,domain)) 
    domains[var]={value}
    return removed 

def restore(removed):
    for nei,domain in removed:
        domains[nei].add(domain) 

def backtrack(assignment):
    if len(assignment)==n:
        return assignment
    total_nodes_expanded[0]+=1
    var=select_unassigned_variable(assignment)
    for value in order_domain_values(assignment,var): 
        if number_of_conflicts(assignment,var,value)==0:
            assignment[var]=value
            removed=assign(assignment,var,value)
            result=backtrack(assignment)
            if result:
                return result            
            restore(removed)
            assignment.pop(var)      
    return None  
      
if "CP" in args:
    constraint_propagation(domains,pre_constraints)

res=backtrack({})
print(total_nodes_expanded[0])
if res:
    print(total_nodes_expanded[0],sorted({variables[i]:res[i] for i in res}.items()))
else:
    print("No Solution")

