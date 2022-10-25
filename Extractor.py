
from operator import mod


rockyou =  open('Big_Dictionary.txt', 'r')
temp_write = open('temp.txt', 'w')


temp_line = "DEFAULT"

while temp_line:
    temp_line = rockyou.readline().strip()
    if len(temp_line) < 8 or len(temp_line) > 16:
        continue
    
    if  any(c.isalpha() for c in temp_line) :
    ##and any(c.isnumeric() for c in temp_line)  
    ##and (not any(c.isalnum() for c in temp_line))
        
        print(1)
        if any(c.isupper() for c in temp_line) and any(c.islower() for c in temp_line):
            temp_write.writelines(temp_line + '\n')
            
            

temp_write.close()
rockyou.close()

        
