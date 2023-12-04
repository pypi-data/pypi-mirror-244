import pandas as pd
import numpy as np
import time
from iothinkdb import icache
import requests
import math
from scipy.stats import pearsonr

def iothink_create_std_curve(df,p1,p2,p3,p4):
	if df.shape[1] == 1:
		model_power = df.iloc[:,0]
		hmean=max(model_power)
		amean=sum(model_power)
		d11 = 1 - p1
		d21 = hmean*(1-p2)
		d22 = hmean*(1+p2)
		d31 = amean*(1-p3)
		d32 = amean*(1+p3)
		d41 = 1-p4
		model_power = list(model_power)
		model_power = [round(i,2) for i in model_power]
		model={"power":model_power,"d11":d11,"d21":d21,"d22":d22,"d31":d31,"d32":d32,"d41":d41}
	if df.shape[1] > 1:
		corr_table = df.corr()
		corr_table_tri=corr_table.values[np.triu_indices_from(corr_table.values,1)]
		corr_table_mean = corr_table_tri.mean()
		corr_table_std = corr_table_tri.std()
		cutoff = corr_table_mean - corr_table_std
		match_ratio =  pd.DataFrame(corr_table[corr_table >= cutoff].count()/len(df.columns), columns=['match_ratio'])
		df_T = pd.DataFrame(df.values.T)
		good_sample = df_T[match_ratio['match_ratio']>=0.7]
		model_power = good_sample.mean()
		df_point=good_sample.agg([np.max,np.sum],axis=1)
		hmean = df_point['amax'].agg([np.mean,np.std])[0]
		amean = df_point['sum'].agg([np.mean,np.std])[0]
		d11 = 1 - p1
		d21 = hmean*(1-p2)
		d22 = hmean*(1+p2)
		d31 = amean*(1-p3)
		d32 = amean*(1+p3)
		d41 = 1-p4
		model_power = list(model_power)
		model_power = [round(i,2) for i in model_power]
		model={"power":model_power,"d11":d11,"d21":d21,"d22":d22,"d31":d31,"d32":d32,"d41":d41}
	return model

def iothink_confidence(x,a=0.98,benchmark_p=0.9,benchmark_n=0.82):
	if x == 1:
		return 1.
	log = math.log(x,a)
	z = 1-1/log
	output1 = benchmark_p +  (x - a)/(1-a) * (1-benchmark_p)
	output2 = benchmark_n +  (1-1/log) * (1-benchmark_n)
	return output1 if 1/log >= a else output2

def iothink_update_param(equipment_name):
	cache = icache.iCache()
	counter = cache.get(equipment_name+'_counter')
	if counter is not None:
		counter = int(counter) + 1
	else:
		counter = 1
	cache.set(equipment_name+'_counter',counter)
	return counter
	
def iothink_update_param2(equipment_name):
	cache = icache.iCache()
	counter = cache.get(equipment_name+'_counter')
	if counter is not None:
		counter = int(counter) + 1
	else:
		counter = 1
	cache.set(equipment_name+'_counter',counter)
	last_model_time = cache.get(equipment_name+"_last_model_time")
	return counter,int(last_model_time)
	
def iothink_init_param(equipment_name):
	cache = icache.iCache()
	cache.set(equipment_name+'_counter',1)
	cache.set(equipment_name+"_last_model_time",0)
	
def iothink_init_param2(equipment_name,modeltime):
	cache = icache.iCache()
	cache.set(equipment_name+'_counter',1)
	cache.set(equipment_name+"_last_model_time", int(time.mktime(modeltime.timetuple())))

def iothink_crossline(line1,line2):
	line3 = []
	for i in range(len(line1)):
		if line1[i]<=line2[i]:
			line3.append(line1[i])
		else:
			line3.append(line2[i])
	return line3
	
def iothink_check_std_curve(df,model):
	d1 = round(max(pearsonr(df,model["power"])[0],0.01),4)
	d2 = round(max(df),4)
	d3 = round(sum(df),4)
	d4 = round(sum(iothink_crossline(df,model["power"]))/sum(model["power"]),4)
	hmean = (model["d21"]+model["d22"])/2
	grate = round(max(1-abs(d2-hmean)/hmean,0.01),4)
	amean = (model["d31"]+model["d32"])/2
	arate = round(max(1-abs(d3-amean)/amean,0.01),4)
	sim = d4
	sim = max(sim,0.01)
	c = round(iothink_confidence(sim),5)
	return c,d1,d2,d3,d4,hmean,amean,sim
    
def iothink_autoupdate_model(current_model,current_modeltime,ip,modelid,init_sample_count,step_sample_count,update_sample_count,s):
	if current_model is None:
		counter = iothink_update_param("eq1")
		if counter == init_sample_count:
			url=f"http://{ip}:7600/api/v1/model?model={modelid}&s={s}&num={init_sample_count}&model_type=1"
			requests.post(url)
		return "",counter
	else:
		counter,last_model_time = iothink_update_param2("eq1")
		if counter <= init_sample_count or last_model_time == int(time.mktime(current_modeltime.timetuple())):
			if counter == init_sample_count:
				url=f"http://{ip}:7600/api/v1/model?model={modelid}&s={s}&num={init_sample_count}&model_type=1"
				requests.post(url)
			return "",counter
		else:
			if counter == step_sample_count:
				url=f"http://{ip}:7600/api/v1/model?model={modelid}&s={s}&num={step_sample_count}&model_type=1"
				requests.post(url)
			if counter%update_sample_count == 0:
				url=f"http://{ip}:7600/api/v1/model?model={modelid}&s={s}&num={step_sample_count}&model_type=2"
				requests.post(url)
			return current_model,counter