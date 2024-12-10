import streamlit as st
import pandas as pd

letters = st.text_input(
    label="Letras:",
    help="Letras disponível para pesquisa.",
    value="athlrim",
)
center = st.text_input(
    label="Central",
    max_chars=1,
    help="A letra obrigatória!",
    value="l",
)
min_length = st.number_input(
    label="Mínimo de letras:",
    min_value=4,
    max_value=46,
    help="Mínimo de letras permitidos",
)
max_length = st.number_input(
    label="Máximo de letras:",
    min_value=3,
    max_value=46,
    value=25,
    help="Máximo de letras permitido",
)

if st.button("Sugestões"):
    df = pd.read_csv("./words.txt", names=["Palavra"])
    df["Tamanho"] = df["Palavra"].str.len()
    domain = letters + center
    condition = (
        (df["Tamanho"] >= min_length)
        & (df["Tamanho"] <= max_length)
        & (df["Palavra"].str.contains(center))
        & (df["Palavra"].apply(lambda word: all(c in domain for c in word)))
    )

    df = df.loc[condition].sort_values(by="Tamanho", ascending=True)
    grouped_df = df.groupby(by="Tamanho")
    for key, _ in grouped_df:
        values = grouped_df.get_group(key).sort_values(by="Palavra", ascending=True)
        candidates = ";".join(values["Palavra"].tolist())
        st.write(f"{key} letras")
        st.write(candidates)
