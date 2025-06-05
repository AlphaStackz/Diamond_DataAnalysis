import streamlit as st
import pandas as pd
import umap
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)   # sklearn
warnings.filterwarnings("ignore", category=UserWarning)     # umap

st.title("UMAP-projekt: Diamanter kluster efter `Clarity`")

@st.cache_data
def load_and_embed():
    df = pd.read_csv("diamonds.csv")
    df = df[(df["x"] > 0) & (df["y"] > 0) & (df["z"] > 0)].copy()

    df["volume"] = df["x"] * df["y"] * df["z"]
    df["cut_code"] = df["cut"].astype("category").cat.codes
    df["color_code"] = df["color"].astype("category").cat.codes
    df["clarity_code"] = df["clarity"].astype("category").cat.codes

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

sample_size = st.slider("Antal punkter att visa", 1000, 10000, 3000, step=500)
plot_df = data.sample(sample_size, random_state=42)

fig, ax = plt.subplots(figsize=(10,7))
sns.scatterplot(
    data=plot_df,
    x="UMAP1", y="UMAP2",
    hue="clarity",
    palette="viridis", alpha=0.7, ax=ax
)
st.pyplot(fig)

st.title("`UMAP` - med hue = `Color`:")
fig, ax = plt.subplots(figsize=(10,7))
sns.scatterplot(
    data=plot_df,
    x="UMAP1", y="UMAP2",
    hue="color",
    palette="viridis", alpha=0.7, ax=ax
)
st.pyplot(fig)

st.subheader("`UMAP` - med hue = `Cut`:")
fig, ax = plt.subplots(figsize=(10,7))
sns.scatterplot(
    data=plot_df,
    x="UMAP1", y="UMAP2",
    hue="cut",
    palette="viridis", alpha=0.7, ax=ax
)
st.pyplot(fig)


st.title("`UMAP` - med hue = `Price`:")
fig, ax = plt.subplots(figsize=(10,7))
sns.scatterplot(
    data=plot_df,
    x="UMAP1", y="UMAP2",
    hue="price",
    palette="viridis", alpha=0.7, ax=ax
)
st.pyplot(fig)

st.subheader("Detta är enbart en testning av UMAP.")
st.markdown(""" 
- Med hjälp av `UMAP` kan vi reducera dimensionerna för att se diamanterna som kluster i respektive kategori klasser.
""")


# Hämta diamant 27635
target_id = 27635
target_diamond = data.loc[target_id]

# Definiera radie för närhet i UMAP-rummet
umap_radius = 1.5

st.title("Filtrerat kluster: Dyraste `UMAP`-gruppen ")

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
st.dataframe(target_diamond[["carat", "cut", "color", "clarity", "price"]].to_frame().T)

st.subheader(" Kluster nära diamant 27635 (UMAP-närhet ≤ 1.5)")
fig_cluster, ax_cluster = plt.subplots(figsize=(10,7))
sns.scatterplot(
    data=similar_cluster,
    x="UMAP1", y="UMAP2",
    hue="price", palette="viridis", size="carat", sizes=(20,200), ax=ax_cluster, alpha=0.8
)
ax_cluster.set_title("Klustret kring diamant 27635")
st.pyplot(fig_cluster)

# Visa data för klustret
st.markdown("### Kluster-tabell")
st.dataframe(similar_cluster[["carat", "cut", "color", "clarity", "price"]].sort_values("price", ascending=False))

st.subheader("**Slutlig Utredning:**")
st.markdown("""
Här blir det tydligt utifrån utredningen vi gjort tidigare, vet vi att dyraste korrelation var en diamant med
`D` i color-klassen, `Very Good` i cut-klassen och har `IF` i clarity-klassen.
När vi kollar igenom och jämför diamantens gruppering med hjälp av `UMAP` Scatterplotten kan vi dra slutsatsen att följande kluster innehåller den dyraste diamanten.
""")
