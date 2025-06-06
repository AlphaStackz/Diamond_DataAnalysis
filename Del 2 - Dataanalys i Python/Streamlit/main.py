import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Laddar data
data = pd.read_csv("diamonds.csv")

# Ordna kategorier
cut_order = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
color_order = ["J", "I", "H", "G", "F", "E", "D"]
clarity_order = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

data["cut"] = pd.Categorical(data["cut"], categories=cut_order, ordered=True)
data["color"] = pd.Categorical(data["color"], categories=color_order, ordered=True)
data["clarity"] = pd.Categorical(data["clarity"], categories=clarity_order, ordered=True)

# Sidtitel
st.title("💎 Diamond Price Analysis")

# Scatterplot
st.subheader("Pris vs Carat med färg = Clarity")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=data, x="carat", y="price", hue="clarity", palette="viridis", alpha=0.6, ax=ax)
ax.set_title("Pris vs Carat")
st.pyplot(fig)

# Slutsats
st.subheader("📘 Slutsats")
st.markdown("""
- **Carat (vikt)** har starkast korrelation med priset.
- **Clarity** påverkar kraftigt inom samma viktklass — särskilt synligt för `IF` och `VVS1`.
- Kombinationen av **låg carat men hög clarity** kan ge mycket högt pris.
- Scatterplotten visar tydligt dessa mönster.
""")