import streamlit as st
import pandas as pd
import umap
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)   # sklearn
warnings.filterwarnings("ignore", category=UserWarning)     # umap

# sortering (worst to best)
cut_order     = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
color_order   = ["J", "I", "H", "G", "F", "E", "D"]
clarity_order = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

st.title("Med hjälp av `UMAP` - Uniform Manifold Approximation and Projection klusteranalys kan vi gruppera diamanter efter liknande egenskaper")

st.subheader("UMAP-projekt analys 1: Diamant kluster efter `Clarity`")

@st.cache_data
def load_and_embed():
    df = pd.read_csv("diamonds.csv")
    df = df[(df["x"] > 0) & (df["y"] > 0) & (df["z"] > 0)].copy()

    df["volume"] = df["x"] * df["y"] * df["z"]
    df["cut_code"] = df["cut"].astype("category").cat.codes
    df["color_code"] = df["color"].astype("category").cat.codes
    df["clarity_code"] = df["clarity"].astype("category").cat.codes

    # Lägger in rätt kategori sortering
    df["cut"] = pd.Categorical(df["cut"], categories=cut_order, ordered=True)
    df["color"] = pd.Categorical(df["color"], categories=color_order, ordered=True)
    df["clarity"] = pd.Categorical(df["clarity"], categories=clarity_order, ordered=True)

    features = [
        "carat","cut_code","color_code","clarity_code",
        "depth","table","volume","price"
    ]
    X = StandardScaler().fit_transform(df[features])
    embedding = umap.UMAP(random_state=42).fit_transform(X)
    df["UMAP1"], df["UMAP2"] = embedding[:,0], embedding[:,1]
    return df

with st.spinner("Beräknar UMAP-embedding …"):
    data = load_and_embed()

sample_size = st.slider("Antal diamanter att visa", 1000, 50000, 10000, step=500)
plot_df = data.sample(sample_size, random_state=42)

fig, ax = plt.subplots(figsize=(10,7))
sns.scatterplot(
    data=plot_df,
    x="UMAP1", y="UMAP2",
    hue="clarity",
    palette="viridis", alpha=0.7, ax=ax
)
st.pyplot(fig)

st.subheader("UMAP-projekt analys 2: Diamant kluster efter `Color`:")
fig, ax = plt.subplots(figsize=(10,7))
sns.scatterplot(
    data=plot_df,
    x="UMAP1", y="UMAP2",
    hue="color",
    palette="viridis", alpha=0.7, ax=ax
)
st.pyplot(fig)

st.subheader("UMAP-projekt analys 3: Diamant kluster efter `Cut`:")
fig, ax = plt.subplots(figsize=(10,7))
sns.scatterplot(
    data=plot_df,
    x="UMAP1", y="UMAP2",
    hue="cut",
    palette="viridis", alpha=0.7, ax=ax
)
st.pyplot(fig)

st.subheader("UMAP-projekt analys 4: Diamant kluster efter `Price`:")
fig, ax = plt.subplots(figsize=(10,7))
sns.scatterplot(
    data=plot_df,
    x="UMAP1", y="UMAP2",
    hue="price",
    palette="viridis", alpha=0.7, ax=ax
)
st.pyplot(fig)

st.subheader("Hur kan man använda resultatet?")
st.markdown(""" 
- Med hjälp av `UMAP` kan vi reducera dimensionerna för ett mång dimensionell data 
för att se diamanterna som kluster i respektive kategori klasser.
""")

# Hämta diamant 27635
target_id = 27635
target_diamond = data.loc[target_id]

# Definiera radie för närhet i UMAP-rummet
umap_radius = 1.5

st.subheader("Filtrerat kluster: Dyraste `UMAP`-gruppen ")
st.markdown("""
Vi kan även använda `UMAP` för att markera vårt dyraste Diamant: `27635`:
""")

# Filtrera liknande diamanter inom radien
similar_cluster = data[
    ((data["UMAP1"] - target_diamond["UMAP1"])**2 + (data["UMAP2"] - target_diamond["UMAP2"])**2) ** 0.5
    <= umap_radius
].copy()

# Markera diamant 27635
ax.scatter(
    target_diamond["UMAP1"],
    target_diamond["UMAP2"],
    color="red", s=200, edgecolor="black", label="Diamant 27635", zorder=5
)
ax.legend()
st.pyplot(fig)

# Visa diamantens info
st.subheader("Diamant: 27635")
st.markdown("""
Här blir det tydligt utifrån utredningen vi gjort tidigare i priciestDiamond, vet vi att dyraste pris korrelation var en diamant med egenskaperna:
`D` i color-klassen, `Very Good` i cut-klassen och har `IF` i clarity-klassen.
""")
st.dataframe(target_diamond[["carat", "cut", "color", "clarity", "price"]].to_frame().T)

st.subheader(" Kluster nära diamant 27635 (UMAP-närhet ≤ 1.5)")
st.markdown("""
När vi fokuserar på diamant **27635** och identifierar dess närmaste grannar i UMAP-rummet
kan vi identifiera ett kluster av diamanter som delar mycket liknande egenskaper både i struktur, vikt och prisklass.
""")

fig_cluster, ax_cluster = plt.subplots(figsize=(10,7))
sns.scatterplot(
    data=similar_cluster,
    x="UMAP1", y="UMAP2",
    hue="price", palette="viridis", size="carat", sizes=(20,200), ax=ax_cluster, alpha=0.8
)
ax_cluster.set_title("Klustret kring diamant 27635")
st.pyplot(fig_cluster)

# Visa data för klustret
st.subheader("💎 **Slutlig Utredning:**")
st.markdown("""
UMAP hjälper oss att analysera **närhet i mångdimensionellt rum** vilket betyder att detta kluster representerar diamanter med liknande kombination av:
- **Hög klarhet (Clarity: IF–VVS1)**
- **Vit färg (Color: D–E)**
- **God slipning (Cut: Very Good/Premium)**
- **Liknande carat- och volymvärden**

Det aktuella klustret kring diamant `27635` visar hur **kombinationen av låg vikt men extremt hög klarhet och färg** fortfarande resulterar i höga priser. 
Denna typ av analys ger oss en djupare förståelse och svarar på frågeställningen: **Vilka attributer har starkaste korrelation med priset**.

UMAP gör det möjligt att visualisera dessa samband i två dimensioner.
""")
