#!/usr/bin/env python
# coding: utf-8

# Calculadora de probabilidades de manabase

# In[5]:

import streamlit as st
import math as math
import pandas as pd
import numpy as np

def prob_n_land(n_land, cards_mao, lands, cards_tot): #probabilidade de se ter exatamente n lands na mão, se a mão tiver c cartas e l lands no deck
    res1=1
    res2=1
    res3=1
    for i in range (0,n_land):
        res1=res1*(lands-i)
    for i in range (0,cards_mao-n_land):
        res2=res2*((cards_tot-lands)-i) 
    for i in range (0,cards_mao):
        res3=res3*(cards_tot-i) 
        
    res = math.comb(cards_mao,n_land)*res1*res2/res3
    return res

def prob_range_land(lands_min,lands_max,cards_mao, lands, cards_tot): #sem Mulligan free - prob de se obter lands_min<=n<=lands_max lands na primeira mão com l lands no deck
    res=0
    for j in range (lands_min,lands_max+1):
        res=res+prob_n_land(j,cards_mao, lands, cards_tot)
    return res



def prob_fin(lands_min,lands_max,n_mulligan,lands, cards_tot, primeiro_free): #prob de se obter lands_min<=n<=lands_max lands na primeira mão com número n de mulligans
    res=prob_range_land(lands_min,lands_max,cards_mao, lands, cards_tot)
    
    if primeiro_free == True:
        if n_mulligan == 0:
            res = res
            
        elif n_mulligan == 1:
            
            res = res + (1-res)*res
            
        else :
            res = res + (1-res)*res
            for i in range (2,n_mulligan+1):
                res = res+(1-res)*prob_range_land(lands_min,lands_max,cards_mao-(i-1), lands, cards_tot)

    else :
        for i in range (0,n_mulligan):
            res=res+(1-res)*prob_range_land(lands_min,lands_max,cards_mao-(i+1), lands, cards_tot)

    return res


import matplotlib.pyplot as plt
def mulligan_fixo(lands_min,lands_max,n_mulligan, cards_tot, primeiro_free):
    x=[]
    y=[]
    delta = []
    top_jumps_pos =[]
    for i in range (0,cards_tot+1):
        lands = i
        x.append(i) #eixo x
        y.append(prob_fin(lands_min,lands_max,n_mulligan,lands, cards_tot, primeiro_free)) #eixo y
        delta.append(y[i]-y[i-1]) # taxa de variação da probabilidade
    top_jumps_val=sorted(delta)[-20:] #valores dos 3 maiores saltos
    for j in range(0,20):
        top_jumps_pos.append(delta.index(top_jumps_val[19-j])+1) #posição dos 3 maiores saltos
    return x,y, top_jumps_pos


def plot_mulligan_fixo(lands_min,lands_max,n_mulligan, cards_tot, primeiro_free):
    xpoints,ypoints, top_jumps_pos =mulligan_fixo(lands_min,lands_max,n_mulligan, cards_tot, primeiro_free)

    plt.plot(xpoints, ypoints)
    plt.xlabel("Terrenos no Deck")
    plt.ylabel("Probabilidade de iniciar no range")
    plt.grid()
    return plt.show(), print(f'Biggest jumps in probability happen at these thresholds, in order: {top_jumps_pos}')


cards_mao = 7 #cards na sua mão - inicia como 7

st.title('Mana Base Calculator')
with st.sidebar:
    radio_box = st.radio(
        "Menu",
        ("Info", "App"),
        index=1
    )

if radio_box == "Info":
    st.header("Welcome to the Magic Mana Base Calculator!")
    st.subheader("-by Rafael J. Hauy")
    st.caption("                  -- 3.0.0 - Beauty in presentation")
    st.markdown("This is the web version of the mana base calculator. It gives you the probabilities of begining the game with a set number of lands in your hand.")
    st.markdown("The current version has a problem, that for probabilities near 1, some values get round up to 0, so that they don't drop as they should afterwards. This has to be corrected by increasing the precision of the calculations.")

    st.header("How the probabilities are beeing computed")
    st.markdown("The first thing to do is to compute the probability of having exactly $n\_land$ lands in your hand, $cards\_mao$ cards in your hand and $lands$ lands in your deck of $cards\_tot$ total cards. This is given by the probability of a specific combination of $n\_land$ lands, times the number of configurations with $n\_land$. This means")
    st.latex(r'''P(x=n\_lands)= \binom{cards\_mao}{n\_lands}\frac{\displaystyle\prod_{i=0}^{n\_lands-1}(lands-i)\displaystyle\prod_{j=0}^{cards\_mao-n\_lands-1}(cards\_tot-lands-j)}{\displaystyle\prod_{k=0}^{cards\_mao-1}(cards\_tot-k)}''')
    st.markdown("To compute this I used the function")
    st.code('''def prob_n_land(n_land, cards_mao, lands, cards_tot):
    res1=1
    res2=1
    res3=1
    for i in range (0,n_land):
        res1=res1*(lands-i)
    for i in range (0,cards_mao-n_land):
        res2=res2*((cards_tot-lands)-i) 
    for i in range (0,cards_mao):
        res3=res3*(cards_tot-i) 
        
    res = math.comb(cards_mao,n_land)*res1*res2/res3
    return res''')
    st.markdown("We then compute the probability of having between $lands\_min$ and $lands\_max$ lands in a hand of size $cards\_mao$. This would simply be")
    st.latex("P(lands\_min\leq x\leq lands\_max)=\displaystyle\sum_{n\_lands=lands\_min}^{lands\_max}P(x=n\_lands)")
    st.code('''def prob_range_land(lands_min,lands_max,cards_mao, lands, cards_tot): 
    res=0
    for j in range (lands_min,lands_max+1):
        res=res+prob_n_land(j,cards_mao, lands, cards_tot)
    return res''')
    st.markdown("Now we have to consider the chances o getting in the desired range with $n\_mulligan$ draws and also considering the cases where the first Mulligan is free and the first Mulligan not beeing free. If the first Mulligan is not free, the probability of beeing in range is (with the notation $lands\_min\leq x\leq lands\_max=range$):" )
    st.latex("P(range|n\_mulligan)=P(range)")
    st.latex("+\displaystyle\sum_{i=1}^{n\_mulligan}\displaystyle\prod_{j=0}^{i-1}(1-P(range|cards\_mao-i+j+1))\cdot P(range|cards\_mao-i)")
    st.markdown("and if the firs Mulligan is free:")
    st.latex("P(lands\_min\leq x\leq lands\_max|n\_mulligan)=P(lands\_min\leq x\leq lands\_max)+(1-P(lands\_min\leq x\leq lands\_max))P(lands\_min\leq x\leq lands\_max)")
    st.latex("+\displaystyle\sum_{i=2}^{n\_mulligan}(1-P(lands\_min\leq x\leq lands\_max|cards\_mao-i+2))\cdot P(lands\_min\leq x\leq lands\_max|cards\_mao-i+1)")




if radio_box == "App":
    cards_tot = st.number_input(label = 'Total cards in your deck, excluding the commander', value = 99, min_value = 20, max_value = 1000000000)
    n_mulligan = st.number_input(label = 'Number of mulligans you are willing to make', value = 2, min_value = 0, max_value = 6)
    primeiro_free = st.checkbox(label = 'First Mulligan free', value=True,)
    [lands_min,lands_max]=values = st.slider(
     'Select the range of lands desired in the opening hand',
     0, 7, (3, 4))
    dados = pd.DataFrame({
    'a': mulligan_fixo(lands_min,lands_max,n_mulligan, cards_tot, primeiro_free)[1]
    })
    st.line_chart(dados)
