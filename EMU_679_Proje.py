# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 09:24:52 2023

@author: Huawei
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 16:10:16 2023

@author: Huawei
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 12:03:34 2023

@author: Huawei
"""
import gurobipy as gp
from gurobipy import GRB   
import pandas as pd
import os

# Model Sınav Programi Çizelgeleme

# Model Girdileri
directory = 'C:\\Users\\Huawei\\Masaüstü\\Hacettepe doktora\\EMÜ 679 YA ileri matematiksel yöntemler\\Proje\\Model_girdi'  
filename = 'Gozetmen_atama.csv'
file_path = os.path.join(directory, filename)
gozetmen_df = pd.read_csv(file_path)
gozetmen_df = gozetmen_df.iloc[:,0:3]
filename = 'Sınav__cakısma_maliyet.csv'
file_path = os.path.join(directory, filename)
sınav_cakısma_df = pd.read_csv(file_path)   

# Sabit veriler
sınav = list(set(sınav_cakısma_df["Sınav (i_üssü)"].tolist()))   # 15 adet dersin sınavı var
slot = list(set(gozetmen_df["Slot"].tolist()))  # 15 sınavın atanacağı 12 slot var
gozetmen = list(set(gozetmen_df["Gözetmen"].dropna().tolist()))  # 4 gözetmen var

a = {}
for i in range(len(sınav_cakısma_df)):
    row = sınav_cakısma_df.loc[i, :]
    a[row["Sınav (i)"], row["Sınav (i_üssü)"]] = row["Maliyet (a i,i_üssü)"]
    
c = {}
for i in range(len(gozetmen_df)):
    row = gozetmen_df.loc[i, :]
    c[row["Gözetmen"], row["Slot"]] = row["Maliyet (c j,k)"]

m = gp.Model("Sınav ve gözetmen atama")

x = m.addVars(sınav, slot ,vtype=GRB.BINARY, name="x")
y = m.addVars(gozetmen, slot, vtype=GRB.BINARY, name="y")

m.addConstrs(
    (x.sum(i, '*') == 1 for i in sınav), "her sınavın bir gün-derslik-zaman aralığına atanması")
m.addConstrs(
    (y.sum('*', j) == 1 for j in slot), "her gün-derslik-zaman aralığına bir gözetmen atanması")

# Bir gözetmenin aynı gün-derslik-zaman aralığında tek sınava atanma kısıtları: 
m.addConstrs(
    (y.sum(k, 1) + y.sum(k, 4) <= 1 for k in gozetmen))
m.addConstrs(
    (y.sum(k, 2) + y.sum(k, 5) <= 1 for k in gozetmen))
m.addConstrs(
   (y.sum(k, 3) + y.sum(k, 6) <= 1 for k in gozetmen))
m.addConstrs(
   (y.sum(k, 7) + y.sum(k, 10) <= 1 for k in gozetmen))
m.addConstrs(
   (y.sum(k, 8) + y.sum(k, 11) <= 1 for k in gozetmen))
m.addConstrs(
   (y.sum(k, 9) + y.sum(k, 12) <= 1 for k in gozetmen))


amac_fonk_gozetmen = gp.quicksum(c[k,j]*y[k,j] for j in slot for k in gozetmen) 
amac_fonk_sınav = gp.quicksum(a[i,i_üssü]*x[i,j]*x[i_üssü,j] for i in sınav for i_üssü in sınav for j in slot)
amac_fonk = amac_fonk_gozetmen + (amac_fonk_sınav / 2)
m.setObjective(amac_fonk, GRB.MINIMIZE)
m.optimize()

m.write("model_hand.lp")
if m.status == GRB.OPTIMAL:
    # Print optimal variable values
    for var in m.getVars():
        print(f"{var.VarName}: {var.x}")
print("Amaç fonk değeri:", m.objVal)
