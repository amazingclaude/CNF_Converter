#-------------------------------------------------------------------------------
# Name:        CNF_converter
# Purpose:     To convert propositional formula onto its equivalent CNF form
#
# Author:      Wenjun Liao
# Python:      Version 2.7
# Created:     15/10/2017
# Tutor:       Professor Wamberto Vasconcelos
# Reference:   Vivek, "Github," 5 May 2015 . [Online].
#              Available: https://github.com/Vivek-100/CNF_Converter.
#              [Accessed 12 10 2017].
# Note:        Code or function refered will be labeled as <Taken from Reference>
#-------------------------------------------------------------------------------

import sys
import copy

def convert_to_cnf(exp):
    print "The chosen test is: ",exp
    exp = eval(exp)
    exp = exclusive_removal(exp)
    exp = ifte_removal(exp)
    exp = biconditional_removal(exp)
    exp = implication_removal(exp)
    exp = push_negation_downwards(exp)
    exp = remove_brackets(exp)
    exp = distribution_or_over_and(exp)
    exp = remove_duplicate_symbol_recursively(exp)
    final_cnf = duplicate_op_removal(exp)

#The following code is <Taken from Reference>
#-------------------------------------------------------------------------------
    flag=1
    while(final_cnf[0]=="or"   and flag==1):
        if (len(final_cnf[2])>1  and final_cnf[2][0]=="and"):
            final_cnf = distributiviton_or_over_and(final_cnf)
            flag=1
        elif (len(final_cnf[1])>1  and final_cnf[1][0]=="and"):
            final_cnf = distributiviton_or_over_and(final_cnf)
            flag=1
        else:
            flag=0

    final_cnf=remove_duplicate_symbol_recursively(exp)
    final_cnf = duplicate_op_removal(exp)
    return final_cnf
#-------------------------------------------------------------------------------

#Function to add translate the exclusive function.
'''
    The operator defined for the exclusive or function is "xor"
    For example:
    ["xor","A","B"] should be transformed to
    ["and",["or","A","B"],["not",["and","A","B"]]]
'''

def exclusive_removal(exp):
    if (exp[0]=="xor"):
        list_1=exp[1]
        list_2=exp[2]
        exp[0]="and"
        exp[1]=["or",list_1,list_2]
        exp[2]=["not",["and",list_1,list_2]]
    for item in exp:
        if((len(item)>1) or isinstance(item, list)):
            exclusive_removal(item)
    return exp

#Function to add ifte (if then else) function
'''
    The operator defined for the ifte function is "ifte"
    For exmaple:
    ["ifte","A","B","C"] should be transfored to
    ["or",["implies","A","B"],["implies",["not","A"],"C"]]
'''
def ifte_removal(exp):
    if (exp[0]=="ifte"):
        list_1=exp[1]
        list_2=exp[2]
        list_3=exp[3]
        exp[0]="or"
        exp[1]=["implies",list_1,list_2]
        exp[2]=["implies",["not",list_1],list_3]
    for item in exp:
        if((len(item)>1) or isinstance(item, list)):
            ifte_removal(item)
    return exp

#The following function is <Taken from Reference>
#Function to remove bidirectional implications
def biconditional_removal(exp):
    if(exp[0]=="iff"):
        list_1=exp[1]
        list_2=exp[2]
        exp[0]="and"
        exp[1]=["implies",list_1,list_2]
        exp[2]=["implies",list_2,list_1]
    for item in exp:
        if((len(item)>1) or isinstance(item, list)):
            biconditional_removal(item)

    return exp

#The following function is <Taken from Reference>
#Function to remove implication
def implication_removal(exp):
    if(exp[0]=="implies"):
        list_1=exp[1]
        exp[0]="or"
        exp[1]=["not",list_1]

    for item in exp:
        if((len(item)>1) or isinstance(item, list)):
            implication_removal(item)
    return exp

#Function to remove double negations and De-Morgan's law
def push_negation_downwards(exp):
    if(exp[0]=="not"):
        rest=copy.deepcopy(exp[1])
        if(rest[0]=="not"):
            del exp[:]
            for rest_ele in rest[1]:
                exp.append(rest_ele)  # Here the rest[i] for loop method is not working as double brackets like[["or","A","B"]] might happen and cause error.

#The following code is <Taken from Reference>
#--------------------------------------------------------------------------
        elif(rest[0]=="or"):
            del exp[:]
            exp.append("and")
            for rest_ele in rest:
                if rest_ele== "or":
                    continue #skip "or"
                else:
                    exp.append(["not",rest_ele])

        elif(rest[0]=="and"):
            del exp[:]
            exp.append("or")
            for rest_ele in rest:
                if rest_ele== "and":
                    continue #skip "and"
                else:
                    exp.append(["not",rest_ele])

    for rest in exp:
        if(len(rest)>1 ):
            push_negation_downwards(rest)

    return exp
#------------------------------------------------------------------------------

#The following function is <Taken from Reference>
#Function to remove extra brackets
def remove_brackets(exp):
     i=0
     for item in exp:
        if(len(item)==1):  #to test if it is a single symbol
            temp=str(item)
            if(len(temp)>1):  #to test if the symble is in the form of ["A"]
              exp[i]=temp[2]
        elif(len(item)>1):
            remove_brackets(item)
        i=i+1

     return exp
#The following function is <Taken from Reference>
#Function to implement distributive law
def distribution_or_over_and(exp):
    if(exp[0]=="or"):
        if(len(exp[2])>1  and exp[2][0]=="and"):
            temp1=exp[1]
            temp2=exp[2]
            del exp[:]
            exp.append("and")
            for item1 in temp2:
                if item1=="and":
                    continue
                exp.append(["or",temp1,item1])
        elif(len(exp[1])>1  and exp[1][0]=="and"):
            temp1=exp[1]
            temp2=exp[2]
            del exp[:]
            exp.append("and")
            for item2 in temp1:
                if item2=="and":
                    continue
                exp.append(["or",item2,temp2])

    for item in exp:
        if(len(item)>1 ):
            distribution_or_over_and(item)

    return exp

#Function to remove duplicate symbols
'''
For example, to transform ["and","A","A"] to ["A"]
'''
def duplicates_symbol_removal(exp):

    if((exp[0]=="or") or (exp[0]=="and")):
        for i1 in range(len(exp)):
            for i2 in range(i1 + 1, len(exp)):  #i2=1,2,3,...
                if(len(exp[i2]) ==1):
                    if(exp[i2][0]==exp[i1]):#to compare a single element, eg, A ^ A, although this step is redundent
                        del exp[i2]
                        break
#THe following code is <taken from Reference>
#----------------------------------------------------------------------------------
                if(isinstance(exp[i1], list) and isinstance(exp[i2], list)): # to compare identical list
                    if(sorted(exp[i1]) == sorted(exp[i2])):
                        del exp[i2]
                        break

    for item in exp:
        if((len(item)>1) or isinstance(item, list)):
            duplicates_symbol_removal(item)
#-----------------------------------------------------------------------------------
    exp=remove_brackets(exp)
    return exp

def remove_duplicate_symbol_recursively(exp):
    t=[]
    for i in exp:
        if not i in t:
            t.append(i)
    while (t!=exp):

        exp=duplicates_symbol_removal(exp)
        t=[]
        for i in exp:
            if not i in t:
                t.append(i)
    return exp

#Function to remove duplicate operations
'''
    For example, to transform ["or","A","B",["or","C","D"],"E",["or","F","G"]]
    to ["or","A","B","C","D","E","F","G"]
'''
def duplicate_op_removal(exp):

    copy_exp=copy.deepcopy(exp)

    if(exp[0]=="or" and len(exp) > 2):
        del exp[:]
        exp.append("or")
        for i in range(1,len(copy_exp)):
            if copy_exp[i][0]=="or":
                for i2 in range (1, len(copy_exp[i])):
                    exp.append(copy_exp[i][i2])
            else:
                exp.append(copy_exp[i])

    if(exp[0]=="and" and len(exp) > 2):
        del exp[:]
        exp.append("and")
        for i in range(1,len(copy_exp)):
            if copy_exp[i][0]=="and":
                for i2 in range (1, len(copy_exp[i])):
                    exp.append(copy_exp[i][i2])
            else:
                exp.append(copy_exp[i])

#The following code is <taken from Reference>
#--------------------------------------------------------------------------------------------------------------------
    if((exp[0] == "or" or exp[0] == "and") and len(exp) == 2):# to rectify any bug if thre is [or,A] or [and, A]
        temp=exp[1]
        del exp[:]
        exp.append(temp)

    for item in exp:
        if((len(item)>1) or isinstance(item, list)):
            duplicate_op_removal(item)
#----------------------------------------------------------------------------------------------------------------------
    remove_brackets(exp)  #in case when case like ["or","A"] happens (might come from duplicate symbol removal function)
    return exp

""" TEST PROPOSITIONAL FORMULA """
#end=convert_to_cnf('["ifte","A","B","C"]')       #test for ifte function
#end=convert_to_cnf('["xor","B","C"]')            #test for xor function
#end =convert_to_cnf('["and",["or","A","A"],["or","A","A"],"A","A"]')   #test for duplicate symbol removal
#end =convert_to_cnf('["or","A","B","A","A","B","B","A","B","A","B"]')  #test for duplicate aymbol removal
#end =convert_to_cnf('["or",["and","A","B"],["and","C","D"]]')          #test for distributivity
#end =convert_to_cnf('["and","A"]')                                     #example for rectify the bug.

#end =convert_to_cnf('["implies", ["not", "A"], ["not", ["and", "B", ["not", ["or", "C", ["not", ["and", "D", "E"]]]]]]]')  #sample input 1
end=convert_to_cnf('["not", ["implies", ["implies", ["or", "P", ["not", "Q"]], "R"], ["and", "P", "R"]]]')                  #sample input 2

#end =convert_to_cnf('["or","A",["and","B","C","D"],["and","E","F","G"]]')  #example of Bug where for distributivity, only the first three parameters can be covered.

print"The convered CNF is: ", end