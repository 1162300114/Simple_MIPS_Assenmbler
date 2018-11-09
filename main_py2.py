# -*- coding:utf8 -*-
#一个简易的，用于转换汇编代码的汇编器
from optparse import OptionParser
import re
import sys


opCode={'JMP':0,'ADD':1,'SUB':2,'AND':3,'OR':4,'XOR':5,'SLT':6,'SW':9,'LW':17,'BEQ':33}
regs={}
instructionType={}

#初始化参数配置的函数，减少手工工作量
def initPara():
	global opCode
	global regs
	global instructionType
	for i in range(32):
		regs['R'+str(i)]=i
	typeI=[[getOP,26],[getReg,21],[getReg,16],[getReg,11],[getImm,0]]
	typeR=[[getOP,26],[getReg,21],[getReg,16],[getImm,0]]
	typeJ1=[[getOP,26],[getReg,21],[getReg,16],[getImm,0]]
	typeJ2=[[getOP,26],[getImm,0]]
	I=['ADD','SUB','AND','OR','XOR','SLT']
	R=['SW','LW']
	J1=['BEQ']
	J2=['JMP']
	for op in I:
		instructionType[op]=typeI
	for op in R:
		instructionType[op]=typeR
	for op in J1:
		instructionType[op]=typeJ1
	for op in J2:
		instructionType[op]=typeJ2

	#instructionType[I]=typeI
	#instructionType[R]=typeR
	#instructionType[J1]=typeJ1
	#instructionType[J2]=typeJ2
	return 0

def getOP(op):
	global opCode
	ret=opCode[op]
	if ret is None:
		print('Unexpect op code in your file')
		sys.exit(1)
	return ret

def getReg(reg):
	global regs
	ret=regs[reg]
	if ret is None:
		print('Unexpect Reg name in your file')
		sys.exit(1)
	return ret

def getImm(Imm):
	return int(Imm)

def getUserPara():
	try:
		opt=OptionParser()
		opt.add_option('-s',dest='source',type=str,help='the file contain assembly code')
		opt.add_option('-t',dest='target',default='default.mem',type=str,\
			help='the machine code finished by assembler,default is default.mem')
		(options,args)=opt.parse_args()
		isValidParas=True
		errorMessage=[]
		if options.source is None:
			errorMessage.append('You should give a source file for assembler')
			isValidParas=False
		if isValidParas:
			ret={'source':options.source,'target':options.target}
			return ret
		else:
			for error in errorMessage:
				print(error)
			opt.print_help()
			return None
	except Exception as ex:
			print("exception:{0}".format(str(ex)))
			return None

def getAssemblyCode(source):
	f=open(source,'r')
	retTmp=[]
	for line in f:
		tmp=line.split('#')
		if len(tmp):
			retTmp.append(tmp[0])
	pattern='[^a-zA-Z0-9]'
	ret=[]
	for code in retTmp:
		tmp=re.split(pattern,code)
		while '' in tmp:
			tmp.remove('')
		if len(tmp):
			ret.append(tmp)
	return ret

def getMachineCode(code):
	global opCode
	global regs
	global instructionType
	ret=0
	iType=None
	for t in instructionType:
		if code[0] in t:
			iType=instructionType[t]
			break
	if iType is None:
		print('Unexpect code type in your file')
		sys.exit(1)
	if len(code)!=len(iType):
		print('code length and type length should be equal')
		sys.exit(1)
	for i in range(len(code)):
		ret+=(iType[i][0](code[i])<<iType[i][1])
	return ret

def writeToTarget(machineCodes,target):
	f=open(target,'wb')
	f.writelines(machineCodes)


def main():
	userParas=getUserPara()
	if userParas is None:
		return 1
	if initPara():
		print('Fail to init para')
		return 1
	assemblyCode=getAssemblyCode(userParas['source'])
	print(assemblyCode)
	machineCodes=[]
	for code in assemblyCode:
		machineCode=getMachineCode(code)
		machineCodes.append(bin(machineCode)[2:]+'\r\n')
	print(machineCodes)
	writeToTarget(machineCodes,userParas['target'])


if __name__ == '__main__':
	main()

