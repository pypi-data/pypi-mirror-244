import datetime,json
from typing import Any,Callable
from localstack.utils.json import extract_jsonpath,json_safe
from localstack.utils.numbers import is_number
from localstack.utils.strings import to_str
AGG_COMPARABLE_TYPE=float|datetime.datetime
def load_data(file_ref,file_format):
	from snowflake_local.files.storage import FILE_STORAGE as D,FileRef as E;F=E.parse(file_ref);A=D.load_file(F);A=json.loads(to_str(A));G=A if isinstance(A,list)else[A];B=[]
	for C in G:
		if isinstance(C,dict):B.append({'_col1':json.dumps(C)})
		else:B.append(C)
	return B
def object_construct(*A,**E):
	B={}
	for C in range(0,len(A),2):D=A[C+1];B[A[C]]=json.loads(D)
	return json.dumps(B)
def to_json_str(obj):return json.dumps(obj)
def get_path(obj,path):
	C=obj;B=path
	if not B.startswith('.'):B=f".{B}"
	if not B.startswith('$'):B=f"${B}"
	if C is not None and not isinstance(C,(list,dict)):C=json.loads(C)
	A=extract_jsonpath(C,B)
	if A==[]:return''
	if is_number(A)and not isinstance(A,bool)and int(A)==A:A=int(A)
	A=json.dumps(A);return A
def to_variant(obj):return obj
def parse_json(obj):json.loads(obj);return obj
def to_char(obj):return str(obj)
def cancel_all_queries(session):return'canceled'
def arg_min_aggregate(_result,_input1,_input2):
	def A(val1,val2):return val1<val2
	return _arg_min_max_aggregate(_result,_input1,_input2,comparator=A)
def arg_max_aggregate(_result,_input1,_input2):
	def A(val1,val2):return val1>val2
	return _arg_min_max_aggregate(_result,_input1,_input2,comparator=A)
def _arg_min_max_aggregate(_result,_input1,_input2,comparator):
	B=_input2;A=_result
	if B is None:return A
	C=json.dumps(json_safe(_input1));D=json.dumps(json_safe(B))
	if A[1]is None:return[C,D]
	E=json.loads(A[1])
	if comparator(B,E):return[C,D]
	return A
def arg_min_max_finalize(_result):
	A=_result
	if isinstance(A[0],str):return json.loads(A[0])
	return A[0]