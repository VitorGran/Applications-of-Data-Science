import gradio as gr
import pandas as pd
import os
from datetime import datetime

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["timestamp", "nome", "data nascimento", "idade", "e-mail", "convenio", "prioridade", "motivo"]

def cadastrar_paciente(nome, data_nasc, idade, email, convenio, prioridade, motivo):
    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome,
        "data nascimento": data_nasc,
        "idade": idade,
        "e-mail": email,
        "convenio": convenio,
        "prioridade": prioridade,
        "motivo": motivo
    }
    novo = pd.DataFrame([linha])
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)
    return "Paciente cadastrado com sucesso!", pd.read_csv(ARQUIVO_CSV).tail(5)

with gr.Blocks() as demo:
    gr.Markdown("## Cadastro de Pacientes")
    
    with gr.Row():
        nome = gr.Textbox(label="Nome do paciente")
        data_nasc = gr.Textbox(label="Data de Nascimento", placeholder="AAAA-MM-DD")
    
    with gr.Row():
        idade = gr.Number(label="Idade")
        email = gr.Textbox(label="E-mail")
    
    convenio = gr.Dropdown(
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
        label="Convênio"
    )
    prioridade = gr.Slider(1, 5, step=1, label="Prioridade do atendimento")
    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)
    botao = gr.Button("Cadastrar")
    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos pacientes cadastrados")
    botao.click(
        cadastrar_paciente,
        [nome, data_nasc, idade, email, convenio, prioridade, motivo],
        [saida_msg, tabela]
    )

demo.launch(share=True)
