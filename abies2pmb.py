#!/usr/bin/python3
import os
import datetime
import subprocess
import sys
import tempfile
# -*- coding: utf-8 -*-
class abies2Pmb():
	def __init__(self):
		self.dbg=0
		
		#Dict with relations between pmb and abies
		self.pmb_abies={}
		self.pmb_abies["empr_categ"]=["TiposLector"]
		self.pmb_abies["docs_location"]=["Ubicaciones"]
		self.pmb_abies["authors"]=["Autores"]
		self.pmb_abies["exemplaires"]=["Ejemplares"]
		self.pmb_abies["notices"]=["Fondos"]
		self.pmb_abies["collections"]=["Series"]
		self.pmb_abies["notices_langues"]=["Fondos_Idiomas"]
		self.pmb_abies["publishers"]=["Editoriales"]
		self.pmb_abies["groupe"]=["Cursos"]
		self.pmb_abies["indexint"]=["CDUs"]
		self.pmb_abies["notices_tmp"]=["Fondos_all"]
		self.pmb_abies["docs_type"]=["TiposFondo"] 
		self.pmb_abies["docs_statut"]=["TiposEjemplar"] 
		self.pmb_abies["responsability"]=["Fondos_Autores"] 

		#Dict with forced column data type
		self.formatPmbColumns={}
		self.formatPmbColumns['indexint']={1:'string'}
		self.formatPmbColumns['indexint'].update({3:'string'})
		self.formatPmbColumns['responsability']={2:'string'}

		#Dict with default values to column
		self.defaultPmbValues={}
		self.defaultPmbValues['docs_location']={5:'1'}
		self.defaultPmbValues['indexint']={4:'1'}
		self.defaultPmbValues['notices']={29:'"m"'}
		self.defaultPmbValues['notices'].update({38:'1'})
		self.defaultPmbValues['exemplaires']={6:'28'}
		self.defaultPmbValues['exemplaires'].update({9:'10'})
		self.defaultPmbValues['exemplaires'].update({14:'2'})
		self.defaultPmbValues['exemplaires'].update({23:'1'})
		self.defaultPmbValues['docs_type']={2:'15'}
		self.defaultPmbValues['docs_type'].update({3:'15'})
		self.defaultPmbValues['docs_type'].update({7:'1'})
		self.defaultPmbValues['docs_statut']={6:'1'}
		self.defaultPmbValues['docs_statut'].update({7:'1'})

		#Blacklist pmb_abies tables.
		self.blacklist=['notices_tmp']

		#Dict with abies source fields for pmb
		#Numbers are the indexes of the source data table
		self.pmb_tables={}
		self.pmb_tables["docs_location"]=[0,1,'','','','','','','','','','','','','','','','','','','','','','','']
		self.pmb_tables["empr_categ"]=[0,1,'','','','']
		self.pmb_tables["authors"]=[0,1,2,'','','','','','','','','','','','']
		self.pmb_tables["publishers"]=[0,1,'','','','','','','','']
		self.pmb_tables["groupe"]=[0,1,'','','','']
		self.pmb_tables["exemplaires"]=[0,4,1,'',3,13,'',2,6,'','','','','','','','',9,'','','','','','','','','']
		self.pmb_tables["collections"]=[0,1,'','','','','','']
		self.pmb_tables["indexint"]=[0,1,'',1,'']
		self.pmb_tables["notices_tmp"]=[0,1,2,3,4,5]
		self.pmb_tables["notices"]=[0,1,14,15,16,13,'','',19,'',24,'',20,17,25,11,21,22,23,'','','','','','','',26,'','','','','','','','','','','','','',6,'','','','','','','','','','','','','']
		self.pmb_tables["notices_langues"]=[0,'',1,'']
		self.pmb_tables["docs_type"]=[0,1,'','','','','','']
		self.pmb_tables["docs_statut"]=[0,1,'','','','','','','']
		self.pmb_tables["responsability"]=[1,0,2,3,'']

#dict with needed virtual tables
		#Only load one column using a 'get', any other column must be charged with formatTables or formatFields
		self.virtual_tables={}
		self.virtual_tables["CDUs"]={}
		self.virtual_tables["CDUs"].update({'index 0':''})
		self.virtual_tables["CDUs"].update({'index 1':'get Fondos_CDUs.1'})
		self.virtual_tables['Series']={}
		self.virtual_tables['Series'].update({'index 0':''})
		self.virtual_tables['Series'].update({'index 1':'get Fondos.24'})
		self.virtual_tables['Fondos_all']={'index 0':'get Fondos.0'}
		self.virtual_tables['Fondos_all'].update({'index 1':''})
		self.virtual_tables['Fondos_all'].update({'index 2':''})
		self.virtual_tables['Fondos_all'].update({'index 3':''})
		self.virtual_tables['Fondos_all'].update({'index 4':''})
		self.virtual_tables['Fondos_all'].update({'index 5':''})
		self.virtual_tables['Fondos_Idiomas']={}
		self.virtual_tables['Fondos_Idiomas']={'index 0':'get Fondos.0'}
		self.virtual_tables['Fondos_Idiomas'].update({'index 1':''})

		#Dict whith field transformations
		self.formatFields={}
		self.formatFields['TiposLector']={'index 0':'add index 0 7'}
		self.formatFields['Autores']={'index 1':'value 100=70,value 110=71,value 120=72,value 700=70'}
		self.formatFields['Ejemplares']={'index 13':'concat 13,14,15'}
		self.formatFields['Ejemplares'].update({'index 9':'date %m/%d/%y %H:%M:%S %Y-%m-%d %H:%M:%S'})
		self.formatFields['Ejemplares'].update({'index 2':'from Fondos_all.5 on 2=3'})
		#Replace index 3 with the needed data... Recipes from the other side...
		self.formatFields['Ejemplares'].update({'index 3':'from Fondos_all.4 on 1=1'})
		self.formatFields['CDUs']={'index 0':'inc 1 1000'}
		self.formatFields['Series']={'index 0':'inc 1 1000'}
		self.formatFields['Fondos']={'index 1':'value 1="a",value 2="g",value 3="m",value4="j",value 5="k",value 6="a",value 7="l"'}
		self.formatFields['Fondos'].update({'index 13':'from Autores.2 on 13=0'})
		self.formatFields['Fondos'].update({'index 24':'from Series.0 on 24=1'})
		self.formatFields['Fondos'].update({'index 26':'from Fondos_all.2 on 0=1'})
		self.formatFields['Fondos_all']={'index 2':'from CDUs.0 on 0=1'}
		self.formatFields['Fondos_all'].update({'index 3':'from Ejemplares.2 on 1=1'})
		self.formatFields['Fondos_all'].update({'index 4':'from Fondos.1 on 1=0'})
		self.formatFields['Fondos_all'].update({'index 5':'add index 3 100'})
		self.formatFields['Fondos_Idiomas']={'index 1':'from Fondos.9 on 0=0'}
		self.formatFields['TiposFondo']={'index 0':'value 1=1,value 2=12,else=+100'}
		self.formatFields['TiposEjemplar']={'index 0':'add index 0 100'}
		self.formatFields['Fondos_Autores']={'index 2':'indexValue.3 1="205",indexValue.3 0="070"'}

		#Dict whith columns that must be transformed on loadTable
		self.formatTables={}
		self.formatTables['CDUs']={'index 1':'uniq'}
		self.formatTables['Series']={'index 1':'uniq'}
		self.formatTables['Fondos_all']={'index 1':'from Fondos_CDUs.1 on 0=0'}
		self.formatTables['Fondos_Autores']={'index 3':'value 1=0,value 0=1'}


		#Dict with errors
		self.error={}
		#self.error['status']=True

		#Array with process order (including virtual and blacklisted tables)
		self.executionOrder=['Ubicaciones','TiposLector','Autores','Editoriales','Cursos','Series','CDUs','TiposEjemplar','Fondos_all','Ejemplares','Fondos','Fondos_Idiomas','TiposFondo','Fondos_Autores']
		#Tmp variables
		self.workDir='/tmp/.abiesToPmb/'
		self.tableValuesDict={}
		self.tmpInc=0

		#Work files
		self.mdb=''
		self.sql=''
		self.sqlFiles=[]
	#def _init

	def _debug(self,msg):
		if self.dbg:
			print('Migrator: '+str(msg))
	#def _debug

	def _error(self,code,index=None):
		#Error Codes
		#10 -> Table not found
		#11 -> Error ocurred while importing mdb file
		#12 -> Error exporting mdb to csv
		#13 -> Error generating sql file
		#14 -> Error concatenating sql files
		#15 -> No source table for virtual table
		#16 -> Couldn't fetch data from table
		self.error['status']=False
		self.error['code']=code
#		if index:
#			if index in self.error.keys():
#				self.error[index].append(e)
#			else:
#				self.error[index]=e
#		else:
#			if 'ERR' in self.error.keys():
#				self.error['ERR'].append(e)
#			else:
#				self.error['ERR']=e
	#def _error

	###
	#Process array executionOrder
	###
	def beginMigration(self,mdbFile,sqlFile):

		self.error['status']=True
		self.error['code']=""
		self.mdb=mdbFile
		self.sql=sqlFile
		if self.exportMdb():
			self.sqlFiles=[]
			for abiesTable in self.executionOrder:
				self.tmpInc=0
				self._debug("Processing "+abiesTable)
				self._loadTable(abiesTable)
				if not self.error['status']:
					break
				pmbTable=self._getTableEquivalence(abiesTable)
				if not self.error['status']:
					break
				self._generateSql(pmbTable,abiesTable)
				if not self.error['status']:
					break
			if self.error['status']:
				self._debug("Concatenating sql files in an unique file")
				self._concatFiles()
				self._debug("Files generated for tables "+str(self.executionOrder))
			else:
				self._debug("Errors ocurred")
				self._debug(self.error)
		else:
			self._error(11)

		self._debug("ErrorDict:")
		self._debug(self.error)
		return self.error
	#def beginMigration

	def exportMdb(self):
		returnValue=None
		self._debug(self.mdb)
		if os.path.exists(self.mdb):
			try:
				cmdOut=subprocess.check_output(['mdb-tables',self.mdb],universal_newlines=True)
				if cmdOut:
					self.workDir=tempfile.mkdtemp()+"/"
					tables=cmdOut.strip("\n")
					listTables=tables.split(' ')
					for table in listTables:
						if table!='':
							cmdOut=subprocess.check_output(['mdb-export','-H','-d|||',self.mdb,table],universal_newlines=True)
							if cmdOut:
								f=open (self.workDir+table+".csv",'w')
								f.writelines(cmdOut)
								f.close()
					returnValue=True
			except Exception as e:
				self._error(12)
				returnValue=False
		return returnValue
	#def exportMdb

	###
	#Generates the sql
	#Input: pmb tableName
	#Output: Array of sql sentences
	###
	def _generateSql(self,destTable,abiesTable):
		transformDict=self._checkTransformField(abiesTable)
		origData=self.tableValuesDict[abiesTable]
		sqlFile=self.workDir+destTable+".sql"
		fileName=destTable+".sql"
		try:
			if destTable not in self.blacklist:
				f=open (sqlFile,'w')
			for line in origData:
				strInsertValues=self._processRow(destTable,line,transformDict)
				if destTable not in self.blacklist:
					f.write("Insert ignore into "+destTable+" values ("+strInsertValues+");\n")
			if destTable not in self.blacklist:
				f.close()
				self.sqlFiles.append(sqlFile)
		except Exception as e:
			self._error(13)

	#def _generateSql

	###
	#Process the rows from a given table and makes the desired changes on it
	#Input: pmb tableName
	#Input: orig row
	#Input: dict with the desired transformations
	#Output: transformed row
	###
	def _processRow(self,destTable,line,transformDict):
		pmbColumn=0
		strInsertValues=''
		for index in self.pmb_tables[destTable]:
			if index!='':
				if transformDict:
					if index in transformDict.keys():
						strTransform=transformDict[index]
						self._debug("Transforming value "+str(line[index])+" index "+str(index)+" with "+strTransform)
						line[index]=eval(strTransform)
				tmp=str(line[index]).strip("\n")
				#Clean tmp field
				tmp=tmp.replace('"',' ')
				chkFormat=True
				if (destTable in self.formatPmbColumns):
					if index in self.formatPmbColumns[destTable]:
						chkFormat=False
						if self.formatPmbColumns[destTable][index]=='string':
							tmp=str(tmp)
							tmp=tmp.lstrip(' ')
							tmp=tmp.rstrip(' ')
							tmp='"'+tmp+'"'
						elif self.formatPmbColumns[destTable][index]=='int':
							tmp=int(tmp)

				if chkFormat:
					try:
						int(tmp)
					except:
						tmp=tmp.lstrip(' ')
						tmp=tmp.rstrip(' ')
						tmp='"'+tmp+'"'
						pass
			else:
				if (destTable in self.defaultPmbValues):
					if pmbColumn in self.defaultPmbValues[destTable]:
						tmp=self.defaultPmbValues[destTable][pmbColumn]
					else:
				 		tmp='""'	
				else:
					tmp='""'
				
			strInsertValues=strInsertValues+tmp+','
			pmbColumn=pmbColumn+1
		strInsertValues=strInsertValues[:-1]
		return(strInsertValues)

	###
	#Concats all the generated files
	###
	def _concatFiles(self):
		self._debug("Generating "+self.sql)
		self._debug("Files list:")
		self._debug(self.sqlFiles)
		try:
			f=open(self.sql,'w')
			f.write("DELETE from docs_location;\n")
			f.write("DELETE from indexint;\n")
			f.write("DELETE from docs_type where idtyp_doc=1 or idtyp_doc=12;\n")
			for sqlFile in self.sqlFiles:
				self._debug("Opening "+sqlFile)
				a=open(sqlFile,'r')
				aContent=a.readlines()
				a.close()
				f.writelines(aContent)
			f.close()
		except Exception as e:
			self._error(14)
			
	#def _concatFile


	###
	#Loads a table from a file or a virtual table from a bunch of tables
	#Input: Table name
	###
	def _loadTable(self,tableName):
		returnValue=False
		self._debug("Opening "+tableName)
		fileName=self.workDir+tableName+'.csv'
		data=[]
		if os.path.exists(fileName):
			try:
				f=open(fileName,'r')
				lines=f.readlines()
				f.close()
				for line in lines:
					line=line.strip('\n')
					array=line.split('|||')
					data.append(array)
				returnValue=True
			except Exception as e:
				self._error(10)
		else: #Check in virtual dict
			if tableName in self.virtual_tables.keys():
				data=self._loadVirtualTable(tableName)
				returnValue=True
			else:
				self._error(10)

		self.tableValuesDict[tableName]=data
		if tableName in self.formatTables.keys():
			self.tableValuesDict[tableName]=self._checkTransformTables(tableName)
		return (returnValue)
	#def _loadTable

	###
	#Loads a virtual table as described by virtual tables dict
	#Input: Table name
	#Output: Dataset (array of arrays with the virtual table)
	###
	def _loadVirtualTable(self,tableName):
		self._debug("Loading virtual table "+tableName)
		data=[]
		dataDict={}
		if tableName in self.virtual_tables.keys():
			proceed=False
			for key,line in self.virtual_tables[tableName].items():
#				print (s)ourceData)
#				for key,line in sourceData.items():
					if line.startswith('get'):
						proceed=True
						sourceIndex=key.split(' ')[1]
						getFrom=line.split(' ')[1]
						sourceIndex=getFrom.split('.')[1]
						sourceTable=getFrom.split('.')[0]
						dataDict[key]=self._funcGetValueFromTable(sourceTable,sourceIndex)
			if proceed:
				#Data is charged on the dataDict, time to populate data array
				maxLen=0
				for key in dataDict.keys():
					columnLen=len(dataDict[key])
					if columnLen>maxLen:
						maxLen=columnLen
				index=0
				while index<maxLen:
					dataLine=[]
					for key in self.virtual_tables[tableName].keys():
						arrayIndex=int(key.split(' ')[-1])
						if key in dataDict.keys():
							dataLine.insert(arrayIndex,dataDict[key][index])
						else:
							dataLine.insert(arrayIndex,'')
					data.append(dataLine)
					index=index+1
		else:
			self._error(15)
		return(data)

	###
	#Finds the pmb table related with an abies table
	#Input: Table name in abies
	#Output: pmb table name
	###
	def _getTableEquivalence(self,tableName):
		pmbTable=None
		for key in self.pmb_abies.keys():
			if tableName in self.pmb_abies[key]:
				pmbTable=key
				break
		return pmbTable
	#def _getTableEquivalence

	###
	#Check if there's any transformation to apply to the fields of a table
	#Input: Abies table name
	#Output: Dict with field indexes as keys and transformations to apply as values
	def	_checkTransformField(self,abiesTable):
		transformDict={}
		if abiesTable in self.formatFields.keys():
			transform=self.formatFields[abiesTable]
			self._debug("Transforming fields "+str(transform)+" in "+abiesTable)
			for key,line in transform.items():
				index=int(key.split(' ')[-1])
				if line.startswith('add'):
					transformDict[index]=self._transformAdd(line,index)
				elif line.startswith('value'):
					transformDict[index]=self._transformValue(line,index)
				elif line.startswith('indexValue'):
					transformDict[index]=self._transformIndexValue(line,index)
				elif line.startswith('concat'):
					transformDict[index]=self._transformConcat(line,index)
				elif line.startswith('date'):
					transformDict[index]=self._transformDate(line,index)
				elif line.startswith('inc'):
					transformDict[index]=self._transformInc(line,index)
				elif line.startswith('get'):
					transformDict[index]=self._transformGet(line,index)
				elif line.startswith('from'):
					transformDict[index]=self._transformQuery(line,index,abiesTable)

		self._debug("TransformDict: "+str(transformDict))
		return transformDict
	#def _checkTransformField

	###
	#Transform routines, self-explaining
	###
	def _transformAdd(self,line,index):
		sourceIndex=line.split(' ')[2]
		increment=line.split(' ')[-1]
		returnValue='int(line['+sourceIndex+'])+'+increment
		return(returnValue)

	def _transformValue(self,line,index):
		values=line.split(',')
		tmpStr=''
		elseValue=None
		for value in values:
			relation=value.split('=')
			destValue=relation[-1]
			if not relation[0].startswith('else'):
				sourceValue=relation[0].split(' ')[-1]
				tmpStr=tmpStr+str(destValue)+' if line['+str(index)+']=="'+str(sourceValue)+'" else '
			else:
				elseValue='str(int(line['+str(index)+']) '+str(destValue)+')'
		if not elseValue:
			elseValue=destValue
			try:
				int(destValue)
				returnValue='('+tmpStr+ '"'+str(elseValue)+'")'
			except:
				returnValue='('+tmpStr+ ''+str(elseValue)+')'
		else:
			returnValue='('+tmpStr +str(elseValue)+')'

		return(returnValue)

	def _transformIndexValue(self,line,index):
		values=line.split(',')
		tmpStr=''
		elseValue=None
		for value in values:
			relation=value.split('=')
			destValue=relation[-1]
			if not relation[0].startswith('else'):
				sourceValue=relation[0].split(' ')[-1]
				sourceIndex=relation[0].split(' ')[0].split('.')[-1]
				tmpStr=tmpStr+str(destValue)+' if str(line['+str(sourceIndex)+'])=="'+str(sourceValue)+'" else '
			else:
				elseValue='str(int(line['+str(index)+']) '+str(destValue)+')'
		if not elseValue:
			elseValue=destValue
			try:
				int(destValue)
				returnValue='('+tmpStr+ '"'+str(elseValue)+'")'
			except:
				returnValue='('+tmpStr+ ''+str(elseValue)+')'
		else:
			returnValue='('+tmpStr +str(elseValue)+')'
		return(returnValue)

	def _transformConcat(self,line,index):
		concat=line.split(' ')[-1]
		concatArray=concat.split(',')
		tmpStr=''
		for concatField in concatArray:
			tmpStr=tmpStr+'line['+str(concatField)+']+'
		returnValue=tmpStr[:-1]
		return(returnValue)

	def _transformDate(self,line,index):
		dates=line.split(' ')
		sourceFormat=dates[1]+' '+dates[2]
		destFormat=dates[3]+' '+dates[4]
		returnValue='self._funcDateTransform(line['+str(index)+'],"'+sourceFormat+'","'+destFormat+'")'
		return(returnValue)

	def _funcDateTransform(self,date,origFormat,destFormat):
		date=date.replace('"','')
		destFormat=destFormat.replace('"','')
		returnValue=(datetime.datetime.strptime(date, origFormat).strftime(destFormat))
		return(returnValue)
		
	def _transformInc(self,line,index):
		increment=line.split(' ')
		inc=increment[1]
		base=0
		if len(increment)==3:
			base=int(increment[2])
		if self.tmpInc<base:
			self.tmpInc=base
		returnValue='self._funcIncrementField('+inc+')'
		return(returnValue)
	###
	#Some values need a special transformation that requires a helper function.
	#Those helper functions are the _func... 
	###
	def _funcIncrementField(self,inc):
		self.tmpInc=self.tmpInc+int(inc)
		returnValue=self.tmpInc
		return(returnValue)

	def _transformGet(self,line,index):
		getFrom=line.split(' ')[-1]
		getFromTable=getFrom.split('.')[0]
		getFromIndex=getFrom.split('.')[-1]
		returnValue='self._funcGetValueFromTable('+getFromTable+','+getFromIndex+')'
		return(returnValue)

	def _funcGetValueFromTable(self,table,index):
		fileName=self.workDir+table+'.csv'
		data=[]
		index=int(index)
		if os.path.exists(fileName):
			try:
				f=open(fileName,'r')
				lines=f.readlines()
				f.close()
				for line in lines:
					array=line.split('|||')
					data.append(array[index])
			except Exception as e:
				self._error(16)
		else:
			self._error(16)
		return(data)

	def _transformQuery(self,line,index,tableName):
		self._debug("Join field "+line)
		transformDict=[]
		arrayLine=line.split(' ')
		sourceTableField=arrayLine[1]
		joinFromTo=arrayLine[-1]
		sourceTable=sourceTableField.split('.')[0]
		sourceField=int(sourceTableField.split('.')[1])
		joinFrom=joinFromTo.split('=')[0]
		joinTo=joinFromTo.split('=')[1]
		returnValue='self._funcGetValueFromQuery("'+tableName+'","'+sourceTable+'",line['+str(joinFrom)+'],'+str(joinTo)+','+str(sourceField)+')'
		return(returnValue)

	def _funcGetValueFromQuery(self,abiesTable,sourceTable,valueFrom,fieldTo,reqFieldIndex):
		returnValue=''
		valueFrom=valueFrom.strip("\n")
		if sourceTable not in self.tableValuesDict:
			self._loadTable(sourceTable)
		for row in self.tableValuesDict[sourceTable]:
				#			print ("Comparing "+str(valueFrom)+" with "+str(row[fieldTo]))
			if valueFrom==str(row[fieldTo]).strip("\n"):
				returnValue=row[reqFieldIndex]
				break
		return returnValue
	#Transform fields functions

	###
	#Check if there's any Transform to apply to a whole table
	#Input: abies table
	#Output: Dataset with the table
	###
	def _checkTransformTables(self,tableName):
		transformDict={}
		if tableName in self.formatTables.keys():
			transform=self.formatTables[tableName]
			for key,line in transform.items():
				index=int(key.split(' ')[-1])
				if line.startswith('uniq'):
					transformDict=self._transformTableUniq(tableName,index)
				if line.startswith('from'):
					transformDict=self._transformTableJoin(tableName,index,line)
				elif line.startswith('value'):
					transformDict=self._transformTableValue(tableName,index,line)
		return transformDict
	#def _checkTransformTamble

	###
	#Function helpers for table transformation. Self-explaining
	###
	def _transformTableUniq(self,tableName,index):
		self._debug("Uniq items from index "+str(index))
		transformDict=[]
		for item in self.tableValuesDict[tableName]:
			if item not in transformDict:
				transformDict.append(item)
		return transformDict

	def _transformTableJoin(self,tableName,index,line):
		self._debug("Join "+line)
		transformDict=[]
		arrayLine=line.split(' ')
		sourceTableField=arrayLine[1]
		joinFromTo=arrayLine[-1]
		sourceTable=sourceTableField.split('.')[0]
		sourceField=int(sourceTableField.split('.')[1])
		joinFrom=joinFromTo.split('=')[0]
		joinTo=joinFromTo.split('=')[1]
		if sourceTable not in self.tableValuesDict:
			self._loadTable(sourceTable)
		#Generate a dict with joinTo as index and required field as value
		tmpDict={}
		tmpIndex=int(joinTo)
		for row in self.tableValuesDict[sourceTable]:
			rowIndex=row[tmpIndex]
			rowValue=row[sourceField]
			tmpDict.update({rowIndex:rowValue})

		#Walk through origin table and insert values from sourceTableDict
		tmpIndex=int(joinFrom)
		for row in self.tableValuesDict[tableName]:
			rowIndex=row[tmpIndex]
			if rowIndex in tmpDict:
				row.insert(tmpIndex,tmpDict[rowIndex])
			else:
				row.insert(tmpIndex,'')
			transformDict.append(row)
		return transformDict

	def _transformTableValue(self,tableName,index,line):
		self._debug("Convert "+line+" on index "+str(index))
		transformDict=[]
		values=line.split(',')
		tmpStr=''
		elseValue=None
		for value in values:
			relation=value.split('=')
			destValue=relation[-1]
			if not relation[0].startswith('else'):
				sourceValue=relation[0].split(' ')[-1]
				tmpStr=tmpStr+str(destValue)+' if row['+str(index)+']==\''+str(sourceValue)+'\' else '
			else:
				elseValue='str(int(row['+str(index)+']) '+str(destValue)+')'
		if not elseValue:
			elseValue=destValue
			try:
				int(destValue)
				convertValue='('+tmpStr+ '"'+str(elseValue)+'")'
			except:
				convertValue='('+tmpStr+ ''+str(elseValue)+')'
		else:
			convertValue='('+tmpStr +str(elseValue)+')'
		for row in self.tableValuesDict[tableName]:
			row[index]=eval(convertValue)
			transformDict.append(row)

		return(transformDict)
	#Table transformation function helpers

### MAIN PROGRAM ###

#migration=abies2Pmb()
#result=migration.beginMigration(sys.argv[1],sys.argv[2])
#print(result)
