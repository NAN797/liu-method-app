
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

st.set_page_config(page_title="Liu Method Fitting", layout="centered")
st.title("🔬 Liu 方法 拟合工具")
st.markdown("利用烧蚀直径和激光能量数据，自动拟合出光斑半径、阈值能量和通量。")

# 数据输入
default_energy = "10, 15, 22, 33, 50, 75, 110"
default_diameter = "4.1, 5.3, 6.0, 7.0, 8.1, 9.2, 10.1"

energy_input = st.text_input("输入脉冲能量 (μJ，逗号分隔)", default_energy)
diameter_input = st.text_input("输入烧蚀直径 (μm，逗号分隔)", default_diameter)

if st.button("开始拟合"):
    try:
        E_values = np.array([float(x) for x in energy_input.split(",")])
        D_values = np.array([float(x) for x in diameter_input.split(",")])

        if len(E_values) != len(D_values):
            st.error("能量和直径数量不一致！")
        else:
            D_squared = D_values**2
            ln_E = np.log(E_values)

            slope, intercept, r_value, _, _ = linregress(ln_E, D_squared)
            E_th = np.exp(-intercept / slope)
            w0 = np.sqrt(2 * slope)
            F_th = (2 * E_th) / (np.pi * w0**2)

            st.success("拟合成功 ✅")
            st.markdown(f"**阈值能量 E_th** ≈ `{E_th:.2f}` μJ")
            st.markdown(f"**光斑半径 w₀** ≈ `{w0:.2f}` μm")
            st.markdown(f"**阈值通量 F_th** ≈ `{F_th:.5f}` J/cm²")

            fig, ax = plt.subplots()
            ln_E_fit = np.linspace(ln_E.min(), ln_E.max(), 100)
            D_fit = slope * ln_E_fit + intercept
            ax.scatter(ln_E, D_squared, color='blue', label='实验数据')
            ax.plot(ln_E_fit, D_fit, color='red', label='线性拟合')
            ax.set_xlabel('ln(E)')
            ax.set_ylabel('D² (μm²)')
            ax.set_title('Liu 方法拟合图')
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

            df = pd.DataFrame({
                'Pulse Energy (μJ)': E_values,
                'ln(E)': ln_E,
                'Ablation Diameter (μm)': D_values,
                'D² (μm²)': D_squared
            })
            st.dataframe(df)

    except Exception as e:
        st.error(f"发生错误：{e}")
