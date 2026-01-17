n=5
sum1=1
def sum(n):
    global sum1
    if(n<1):
        return sum1
    sum1*=n
    sum(n-1)
    
sum(n)
print("sum is",sum1)

    