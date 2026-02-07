import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import re
from datetime import datetime

def clean_name_logic(name):
    if pd.isna(name):
        return "UNKNOWN"
    name = str(name).upper()
    name = re.sub(r'[^A-Z\s]', '', name)
    parts = name.split()
    if len(parts) == 0:
        return "UNKNOWN"
    return f"{parts[0]} {parts[1][0]}" if len(parts) > 1 else parts[0]

def generate_reports(master_file, monitor_file, taluk):
    df_assign = pd.read_excel(master_file)
    df_monitor = pd.read_csv(monitor_file)

    df_assign.columns = df_assign.columns.str.strip()
    df_monitor.columns = df_monitor.columns.str.strip()

    df_assign['Clean'] = df_assign.iloc[:, 0].apply(clean_name_logic)
    df_monitor['Clean'] = df_monitor.iloc[:, 0].apply(clean_name_logic)

    assigned_col = next(c for c in df_assign.columns if 'Total' in c)
    completed_col = next(c for c in df_monitor.columns if 'Total' in c)

    grp_a = df_assign.groupby('Clean')[assigned_col].sum().reset_index()
    grp_m = df_monitor.groupby('Clean')[completed_col].sum().reset_index()

    final = pd.merge(grp_a, grp_m, on='Clean', how='left').fillna(0)
    final.columns = ['Enumerator', 'Assigned', 'Completed']
    final['% Completed'] = final['Completed'] / final['Assigned'].replace(0, 1)

    # -------- EXCEL --------
    excel = io.BytesIO()
    with pd.ExcelWriter(excel, engine='xlsxwriter') as writer:
        final.to_excel(writer, index=False, sheet_name='Progress')
    excel.seek(0)

    # -------- GRAPH --------
    graph = io.BytesIO()
    plt.figure(figsize=(12, max(6, len(final) * 0.4)))
    sns.barplot(data=final, x='Completed', y='Enumerator')
    plt.title(f"{taluk} – GW Progress")
    plt.tight_layout()
    plt.savefig(graph, dpi=120)
    plt.close()
    graph.seek(0)

    # -------- CARD --------
    card = io.BytesIO()
    plt.figure(figsize=(6, 4))
    plt.axis('off')
    plt.text(0.1, 0.7, f"Taluk: {taluk}", fontsize=14)
    plt.text(0.1, 0.5, f"Assigned: {int(final['Assigned'].sum())}", fontsize=14)
    plt.text(0.1, 0.3, f"Completed: {int(final['Completed'].sum())}", fontsize=14)
    plt.text(0.1, 0.1, datetime.now().strftime("%d-%m-%Y %I:%M %p"), fontsize=10)
    plt.savefig(card, dpi=150)
    plt.close()
    card.seek(0)

    return excel, graph, card
