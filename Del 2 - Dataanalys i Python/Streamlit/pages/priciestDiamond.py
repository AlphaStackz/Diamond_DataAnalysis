import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Laddar data
data = pd.read_csv("./diamonds.csv")

# Ordna kategorier
cut_order     = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
color_order   = ["J", "I", "H", "G", "F", "E", "D"]
clarity_order = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

data["cut"] = pd.Categorical(data["cut"], categories=cut_order, ordered=True)
data["color"] = pd.Categorical(data["color"], categories=color_order, ordered=True)
data["clarity"] = pd.Categorical(data["clarity"], categories=clarity_order, ordered=True)

# Sidtitel
st.title("💎 Diamond Price Analysis: 2")

# Scatterplot - färg = color
st.subheader("Pris vs Carat med färg = Color")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=data, x="carat", y="price", hue="color", palette="viridis", alpha=0.6, ax=ax)
ax.set_title("Pris vs Carat / Color")
st.pyplot(fig)

# Slutsats
st.subheader("Slutsats:")
st.markdown("""
- För att analysera vidare om vilken typ av diamant som har högsta priset.
- Använder vi oss av Scatterplotten med hue = `color`.
- Scatterplotten visar tydligt att den dyraste diamanten har `D` som färgklass (dvs vitast klassen).
""")

# Scatterplot - färg = cut
st.title("💎 Diamond Price Analysis: 3")

st.subheader("Pris vs Carat med färg = cut")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=data, x="carat", y="price", hue="cut", palette="viridis", alpha=0.6, ax=ax)
ax.set_title("Pris vs Carat / Cut")
st.pyplot(fig)

# Slutsats
st.subheader("Slutsats:")
st.markdown("""
- Nu vet vi så länge att diamanten med `IF` som `Clarity`-klass och som har `D` color-klass är dyrast.
- Vi använder Scatterplotten med hue = `cut`.
- Scatterplotten visar tydligt att den dyraste diamanten har `Very Good` i `Cut`klassen.
""")

# Hämta data
most_expensive_diamond = data.loc[data["price"].idxmax()]
filtered_df = data[(data["color"] == "D") & (data["clarity"] == "IF")]
top_filtered_diamond = filtered_df.loc[filtered_df["price"].idxmax()]

# Visa info om D + IF diamant
st.title("Diamant: 27635")
st.dataframe(top_filtered_diamond[["carat", "cut", "color", "clarity", "price"]].to_frame().T)

# Varför är det viktigt?
st.subheader("Varför är det viktigt?")
st.markdown("""
"Eftersom om vi använder oss av högsta priset i .csv filens kategorier så är de inte största korrelationen till högsta priset.\"

Vilket helt enkelt hittar det högsta priset, men helt ignorerar funktionsbaserad korrelation som:
- Betydelsen av färg/klarhet
- Karatskalningseffekt
- Inte linjär i premiumprissättning\n
`most_expensive_diamond = data.loc[data["price"].idxmax()]`, alltså hjälper inte. 
""")
st.subheader("Dyrast i dataset enligt .csv: ")
st.dataframe(most_expensive_diamond[["carat", "cut", "color", "clarity", "price"]].to_frame().T)

# Hypotesanalys
st.subheader("Hypotes Analys:")
st.markdown("""
- Diamanten med `D` (vitast färg) och `IF` (högsta klarhet) når ett mycket högt pris (**18542**) trots en relativt låg vikt (**1.04 carat**).
- Om denna diamant hade haft **samma carat** som den dyraste diamanten i datasetet (**2.29 carat**), hade priset sannolikt varit **betydligt högre** än 18823.
- Detta visar att högsta kvalitet i färg och klarhet kan **överträffa alla andra egenskaper**, förutsatt att caraten ökar.
- Kombinationen av `D + IF` + hög carat skulle kunna vara den **ultimata prishöjaren**.
""")

# Hypotetisk projicering
actual_carat = 1.04
actual_price = 18542
target_carat = 2.29
projected_price = (target_carat / actual_carat) * actual_price

st.markdown(f"""
📈 *Hypotetisk:* Om priset för `D + IF` växte linjärt med carat:
`hypotes_pris` = (`most_expensive_diamond["carat"]` / `top_filtered_diamond["carat"]`) * `top_filtered_diamond["price"]`
""")

# Create a new DataFrame row for the projected D + IF diamond
projected_table_row = pd.DataFrame([{
    "carat": target_carat,
    "cut": top_filtered_diamond["cut"],
    "color": top_filtered_diamond["color"],
    "clarity": top_filtered_diamond["clarity"],
    "price": round(projected_price)
}], index=["D + IF (hypotetiskt)"])

projected_table_row
