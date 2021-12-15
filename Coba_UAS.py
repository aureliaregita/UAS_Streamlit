'''
NAMA: AURELIA REGITA CAHYANI
NIM : 12220053
'''
##############import packages###########
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import urllib.request, urllib.parse, urllib.error
import json
import ssl
import string
from matplotlib.colors import ListedColormap
import streamlit as st
from PIL import Image

############### import file ####################
filepath = "produksi_minyak_mentah.csv"
data = pd.read_csv(filepath)

f=open('kode_negara_lengkap.json', "r")
ref=json.loads(f.read())

############### translasi #####################
kode_negara=[]
negara=[]
region=[]
sub_region=[]

for item in ref:
    kode_negara.append(item['alpha-3'])
    negara.append(item['name'])
    region.append(item['region'])
    sub_region.append(item['sub-region'])
    
trans_negara=dict(zip(kode_negara,negara))
region_negara=dict(zip(kode_negara,region))
subreg_negara=dict(zip(kode_negara,sub_region))

############### membuat daftar negara dan tahun yg ada di csv ##################
list_negara=[]
list_tahun=[]
df = pd.DataFrame(data, columns= ['kode_negara','tahun','produksi'])

for key,val in trans_negara.items():
    for i in df['kode_negara']:
        if i==key:
            neg=val
            if neg not in list_negara:
                list_negara.append(neg)

for i in df['tahun']:
    if i not in list_tahun:
        list_tahun.append(i)
############### melengkapi dataframe #############################        
#menghapus data yang bukan milik negara perseorangan
negara=[]
for i in trans_negara:
    daftar_kode=list(trans_negara.keys())
    
for i in df['kode_negara']: 
    if i in daftar_kode:
        for key,val in trans_negara.items():
            if i==key:
                name=val
    else:
        name=np.nan
    negara.append(name)

df['negara']=negara
df=df.dropna()

#menambahkan region
reg=[]
for i in df['kode_negara']: 
    for key,val in region_negara.items():
        if i==key:
            name=val
    reg.append(name)
df['region']=reg

#menambahkan sub-region
subreg=[]
for i in df['kode_negara']: 
    for key,val in subreg_negara.items():
        if i==key:
            name=val
    subreg.append(name)
df['sub-region']=subreg  
################selesai###############

################################# tampilan #############################################
############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Produksi Minyak Mentah Dunia")
st.markdown("*Haloo !! Selamat datang di laman Tugas Besar UAS Pemrograman Komputer milik* **_Aurelia Regita Cahyani (12220053)_**  :wave: :ok_woman:")
st.markdown("*Doakan semoga dapat **Indeks A** yaa!* :sunglasses: :pray:")
############### title ###############)

############### sidebar ###############
st.sidebar.title("Opsi Pilihan")
left_col, mid_col, right_col = st.columns(3)

## User inputs on the control panel
thn = st.sidebar.selectbox("Pilih Tahun", list_tahun)
neg = st.sidebar.selectbox("Pilih Negara", list_negara)
n = st.sidebar.slider('Banyak data yang ditampilkan', value= 10, min_value=0, max_value=100, step=1)
st.sidebar.write("Banyak data: ",n)
############### sidebar ###############

############### Tampilan atas tengah ###############
st.subheader("Grafik Produksi Minyak Mentah "+ neg +" Sepanjang Tahun")

#soal 1 (grafik produksi tiap tahun negara x)
#membuat dataframe baru
df1 = df
df1.set_index('negara',inplace=True)
df1=df1.loc[[neg]]

#membuat deskripsi
#memilih produksi terbesar
urutkan=df1.sort_values(['produksi'], ascending=False)
max=urutkan.iloc[0:1]

thn_max=max['tahun'].to_string(index=False,header=False)
max_prod=max['produksi'].to_string(index=False,header=False)
#memilih produksi terkecil 
urutkan=df1.sort_values(['produksi'], ascending=True)
min=urutkan.iloc[0:1]

thn_min=min['tahun'].to_string(index=False,header=False)
min_prod=min['produksi'].to_string(index=False,header=False)

#plot
fig=plt.figure()
plt.plot(df1['tahun'], df1['produksi'])
plt.xlabel("Tahun")
plt.ylabel("Jumlah Produksi")


col9,col10=st.columns([3,2])
col9.pyplot(fig)

with st.expander("Deskripsi"):
     st.write(f"Produksi tertinggi terjadi pada **{thn_max}** dengan jumlah produksi **{max_prod}**")
     st.write(f"Produksi terendah terjadi pada **{thn_min}** dengan jumlah produksi **{ min_prod}**")
 
############### Tampilan atas tengah ###############


############### left column ###############
col1,col2=st.columns(2)
col1.subheader(str(n)+" Besar Negara dengan Jumlah Produksi Tertinggi Tahun " + str(thn))
#soal 2 (n besar negara dengan produksi tertinggi tahun x)
#membuat dataframe baru
df2 = df
df2.set_index('tahun',inplace=True)

#menghapus data yang bukan milik negara tunggal
negara=[]
for i in trans_negara:
    daftar_kode=list(trans_negara.keys())
for i in df2['kode_negara']: 
    if i in daftar_kode:
        for key,val in trans_negara.items():
            if i==key:
                name=val
    else:
        name=np.nan
    negara.append(name)

df2['negara']=negara
df2=df2.dropna()
#memilih tahun dan n data terbesar
df2=df2.loc[[thn]]
sort_produksi=df2.sort_values(['produksi'], ascending=False)
great_n=sort_produksi.iloc[0:n] 

#plot
fig=plt.figure(figsize=(10,7))
plt.pie(great_n['produksi'],labels=great_n['produksi'])
plt.legend(great_n['negara'],title="Negara", fontsize=8.5, loc=2)
col1.pyplot(fig)
############### left column ###############


###############  right column ###############
col2.subheader(str(n)+" Besar Negara dengan Jumlah Produksi Kumulatif Tertinggi")
#soal 3 (5 besar negara dengan produksi kumulatif tertinggi)
#membuat dataframe baru
df3 = df
#menghitung kumulasi
df3['total'] = df3.groupby(['negara'])['produksi'].transform('sum')
new_df = df3.drop_duplicates(subset=['negara'])

#menghitung kumulasi
df3['total'] = df3.groupby(['negara'])['produksi'].transform('sum')
new_df = df3.drop_duplicates(subset=['negara'])

#memilih n data terbesar
sort_produksi=new_df.sort_values(['total'], ascending=False)
great=sort_produksi.iloc[0:n]

#plot
fig=plt.figure(figsize=(10,7))
plt.pie(great['total'],labels=great['total'])
plt.legend(great['negara'],title="Negara", fontsize=8.5, loc=2)
col2.pyplot(fig)
############### right column ###############


############### left column ###############
col3,col4=st.columns(2)
col3.subheader("Daftar Negara dengan Tingkat Produksi Minyak Paling Tinggi Tiap Tahun")
#soal 4.1 (daftar negara dengan produksi terbesar tiap tahun)
#membuat dataframe baru
data4 = pd.read_csv(filepath, index_col="tahun")
df4 = pd.DataFrame(data4, columns= ['kode_negara','produksi'])

#menghapus data yang bukan milik negara perseorangan
negara=[]
for i in trans_negara:
    daftar_kode=list(trans_negara.keys())
    
for i in df4['kode_negara']: 
    if i in daftar_kode:
        for key,val in trans_negara.items():
            if i==key:
                name=val
    else:
        name=np.nan
    negara.append(name)

df4['negara']=negara
df4=df4.dropna()

#menambahkan region
reg=[]
for i in df4['kode_negara']: 
    for key,val in region_negara.items():
        if i==key:
            name=val
    reg.append(name)
df4['region']=reg

#menambahkan sub-region
subreg=[]
for i in df4['kode_negara']: 
    for key,val in subreg_negara.items():
        if i==key:
            name=val
    subreg.append(name)
df4['sub-region']=subreg

#daftar negara dengan produksi terbesar sepanjang tahun
terbesar=pd.DataFrame()
for i in list_tahun:
    df_new=df4.loc[[i]]
    sort_produksi=df_new.sort_values(['produksi'], ascending=False)
    great=sort_produksi.iloc[0:1]
    terbesar=terbesar.append(great,ignore_index=False)

terbesar=terbesar.sort_values(['produksi'], ascending=False)

#negara dengan produksi terbesar tahun x
max_x=terbesar.loc[[thn]]

col3.dataframe(terbesar)
############### left column ###############


############### right column ###############
col4.subheader("Daftar Negara dengan Tingkat Produksi Minyak Paling Kecil (tidak nol) Tiap Tahun")
#soal 4.2 (negara dengan produksi terkecil tiap tahun yang bukan nol)
#membuat dataframe baru
df4 = df
delete=df4[df4['produksi']==0].index
df4.drop(delete, inplace=True)
df4.set_index('tahun',inplace=True)

terkecil=pd.DataFrame()

#daftar negara dengan produksi terkecil sepanjang tahun
for i in list_tahun:
    df_new=df4.loc[[i]]
    sort_produksi=df_new.sort_values(['produksi'], ascending=True)
    small=sort_produksi.iloc[:1]
    terkecil=terkecil.append(small,ignore_index=False)

terkecil=terkecil.sort_values(['produksi'], ascending=True)

#negara dengan produksi terkecil tahun x
min_x=terkecil.loc[[thn]]

col4.dataframe(terkecil)
############### right column ###############


############### left column ###############
col5,col6=st.columns(2)
col5.subheader("Daftar Negara dengan Produksi Minyak Nol Tiap Tahun")
#soal 4.3 (nol tiap tahun)
#membuat dataframe baru
data4 = pd.read_csv(filepath, index_col="tahun")
df4 = pd.DataFrame(data4, columns= ['kode_negara','produksi'])

#menghapus data yang bukan milik negara perseorangan
negara=[]
for i in trans_negara:
    daftar_kode=list(trans_negara.keys())
    
for i in df4['kode_negara']: 
    if i in daftar_kode:
        for key,val in trans_negara.items():
            if i==key:
                name=val
    else:
        name=np.nan
    negara.append(name)

df4['negara']=negara
df4=df4.dropna()

#menambahkan region
reg=[]
for i in df4['kode_negara']: 
    for key,val in region_negara.items():
        if i==key:
            name=val
    reg.append(name)
df4['region']=reg

#menambahkan sub-region
subreg=[]
for i in df4['kode_negara']: 
    for key,val in subreg_negara.items():
        if i==key:
            name=val
    subreg.append(name)
df4['sub-region']=subreg

#daftar negara dengan dengan produksi nol sepanjang tahun
nol=df4[df4.produksi==0]

col5.dataframe(nol)

###############  left column ###############

###############  right column ###############
col6.subheader("Daftar Negara dengan Produksi Minyak Nol pada Tahun " + str(thn))
nol_x=nol.loc[[thn]]
col6.dataframe(nol_x)

############### right left column ###############


############### left column ###############
col7,col8=st.columns(2)
col7.subheader("Daftar Produksi Kumulatif Minyak")
#soal 4.1.1 (kumulatif)
#membuat dataframe baru
data5 = pd.read_csv(filepath)
df5 = pd.DataFrame(data5, columns= ['kode_negara','produksi'])

#menghapus data yang bukan milik negara perseorangan
negara=[]
for i in trans_negara:
    daftar_kode=list(trans_negara.keys())
    
for i in df5['kode_negara']: 
    if i in daftar_kode:
        for key,val in trans_negara.items():
            if i==key:
                name=val
    else:
        name=np.nan
    negara.append(name)

df5['negara']=negara
df5=df5.dropna()

#menambahkan region
reg=[]
for i in df5['kode_negara']: 
    for key,val in region_negara.items():
        if i==key:
            name=val
    reg.append(name)
df5['region']=reg

#menambahkan sub-region
subreg=[]
for i in df5['kode_negara']: 
    for key,val in subreg_negara.items():
        if i==key:
            name=val
    subreg.append(name)
df5['sub-region']=subreg

#membuat kumulasi data
df5['total'] = df5.groupby(['negara'])['produksi'].transform('sum')
new_df = df5.drop_duplicates(subset=['negara'])

#display
col7.dataframe(new_df)

#memilih data produksi kumulatif terbesar 
sort_produksi1=new_df.sort_values(['total'], ascending=False)
max_kumulatif=sort_produksi1.iloc[0:1]

#memilih data produksi kumulatif terkecil tak nol 
sort_produksi2=new_df.sort_values(['total'], ascending=True)
delete=sort_produksi2[sort_produksi2['produksi']==0].index
sort_produksi2.drop(delete, inplace=True)
min_kumulatif=sort_produksi2.iloc[0:1]
############### left column ###############

############### right column ###############
col8.subheader("Daftar Negara dengan Produksi Kumulatif Minyak Nol")

#data dengan produksi kumulatif nol
nol_kumulatif=new_df[new_df.total==0]
col8.dataframe(nol_kumulatif)
#print(nol_kumulatif.to_string(index=False))
############### lower right column ###############

############### lower left column ###############
st.subheader("Summary")

#extract data dari excel dan buat summary
neg_max=max_x['negara'].to_string(index=False,header=False)
subreg_max=max_x['sub-region'].to_string(index=False,header=False)
reg_max=max_x['region'].to_string(index=False,header=False)
kode_max=max_x['kode_negara'].to_string(index=False,header=False)
prod_max=max_x['produksi'].to_string(index=False,header=False)
st.markdown(f"**Negara dengan produksi minyak terbesar pada tahun {thn} adalah **  {neg_max} ({kode_max}), Region {reg_max}, Sub-region {subreg_max}, dengan jumlah produksi {prod_max} \n")

neg_min=min_x['negara'].to_string(index=False,header=False)
subreg_min=min_x['sub-region'].to_string(index=False,header=False)
reg_min=min_x['region'].to_string(index=False,header=False)
kode_min=min_x['kode_negara'].to_string(index=False,header=False)
prod_min=min_x['produksi'].to_string(index=False,header=False)
st.markdown(f"**Negara dengan produksi minyak terkecil pada tahun {thn} adalah **  {neg_min} ({kode_min}), Region {reg_min}, Sub-region {subreg_min}, dengan jumlah produksi {prod_min} \n")

neg_max_kum=max_kumulatif['negara'].to_string(index=False,header=False)
subreg_max_kum=max_kumulatif['sub-region'].to_string(index=False,header=False)
reg_max_kum=max_kumulatif['region'].to_string(index=False,header=False)
kode_max_kum=max_kumulatif['kode_negara'].to_string(index=False,header=False)
prod_max_kum=max_kumulatif['total'].to_string(index=False,header=False)
st.markdown(f"**Negara dengan produksi kumulatif minyak terbesar adalah **  {neg_max_kum} ({kode_max_kum}), Region {reg_max_kum}, Sub-region {subreg_max_kum}, dengan jumlah produksi {prod_max_kum} \n")

neg_min_kum=min_kumulatif['negara'].to_string(index=False,header=False)
subreg_min_kum=min_kumulatif['sub-region'].to_string(index=False,header=False)
reg_min_kum=min_kumulatif['region'].to_string(index=False,header=False)
kode_min_kum=min_kumulatif['kode_negara'].to_string(index=False,header=False)
prod_min_kum=min_kumulatif['total'].to_string(index=False,header=False)
st.markdown(f"**Negara dengan produksi kumulatif minyak terkecil adalah **  {neg_min_kum} ({kode_min_kum}), Region {reg_min_kum}, Sub-region {subreg_min_kum}, dengan jumlah produksi {prod_min_kum} \n")
