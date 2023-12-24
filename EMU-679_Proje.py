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
filename = 'Sınav_maliyet.csv'
file_path = os.path.join(directory, filename)
sınav_cakısma_df = pd.read_csv(file_path)   

# Sabit veriler
sınav = list(set(sınav_cakısma_df["Sınav (j)"].tolist()))   # 12 adet dersin sınavı var
slot = list(set(gozetmen_df["Slot"].tolist()))  # 12 sınavın atanacağı 12 slot var
gozetmen = list(set(gozetmen_df["Gözetmen"].tolist()))   # 4 gözetmen var

s = {}
for i in range(len(sınav_cakısma_df)):
    row = sınav_cakısma_df.loc[i, :]
    s[row["Sınav (i)"], row["Sınav (j)"]] = row["Maliyet (a i,j)"]
    
g = {}
for i in range(len(gozetmen_df)):
    row = gozetmen_df.loc[i, :]
    g[row["Gözetmen"], row["Slot"]] = row["Maliyet (c j,k)"]

m = gp.Model("Sınav ve gözetmen atama")

x = m.addVars(sınav, slot,vtype=GRB.BINARY, name="x")
y = m.addVars(slot, gozetmen, vtype=GRB.BINARY, name="y")

m.update()

m.addConstrs(
    (x.sum('*', j) == 1 for j in slot), "her bir gün-derslik-zaman aralığına bir sınav atanması")
m.addConstrs(
    (x.sum(i, '*') == 1 for i in sınav), "her sınavın bir gün-derslik-zaman aralığına atanması")
m.addConstrs(
    (y.sum('*', j) == 1 for j in slot), "her gün-derslik-zaman aralığına bir gözetmen atanması")

# Bir gözetmenin aynı gün-derslik-zaman aralığında tek sınava atanma kısıtları: 
m.addConstrs(
    (y.sum(1, k) + y.sum(4, k) == 1 for k in gozetmen))
m.addConstrs(
    (y.sum(2, k) + y.sum(5, k) == 1 for k in gozetmen))
m.addConstrs(
    (y.sum(3, k) + y.sum(6, k) == 1 for k in gozetmen))
m.addConstrs(
    (y.sum(7, k) + y.sum(10, k) == 1 for k in gozetmen))
m.addConstrs(
    (y.sum(8, k) + y.sum(11, k) == 1 for k in gozetmen))
m.addConstrs(
    (y.sum(9, k) + y.sum(12, k) == 1 for k in gozetmen))


#amac_fonk = gp.quicksum(p[i,j]*alan[i,j] for i in analiz_alani for j in recete)
m.setObjective(amac_fonk, GRB.MINIMIZE)
m.optimize()

if m.status == GRB.OPTIMAL:
    # Print optimal variable values
    for var in m.getVars():
        print(f"{var.VarName}: {var.x}")
print("Amaç fonk değeri:", m.objVal)











