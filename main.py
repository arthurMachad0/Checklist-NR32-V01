from datetime import datetime
import requests
import flet as ft
from pdf2image import convert_from_path
from fpdf import FPDF

def get_date_time():
    '''
    Função para obter data e hora atual
    '''
    try:
        response = requests.get(
            'http://worldtimeapi.org/api/timezone/America/Sao_Paulo',timeout=10
            )
        datetime_str = response.json()['datetime']
        datetime_obj = datetime.fromisoformat(datetime_str.rstrip('Z'))
    except (requests.RequestException, ValueError):
        datetime_obj = datetime.now()
    return datetime_obj.strftime('%d/%m/%Y'), datetime_obj.strftime('%H:%M:%S')


def criar_tarefa_row(tarefa, salvar_escolha):
    '''
    Função para criar linha de tarefas
    '''
    return ft.Row([
        ft.Text(tarefa, width=300, color=ft.colors.WHITE),
        ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("Sim"),
                ft.dropdown.Option("Não"),
                ft.dropdown.Option("Parcialmente"),
                ft.dropdown.Option("Não Se Aplica")
            ],
            value="Não Se Aplica",
            data=tarefa,
            on_change=salvar_escolha
        )
    ])

def gerar_pdf():
    '''
    Função para gerar o PDF
    '''
    nome_arquivo = 'Checklist_NR32.pdf'
    largura_perguntas = 162
    largura_respostas = 30

    pdf = FPDF()
    pdf.add_page()
    pdf.image('LIGA.png', x=10, y=8, w=30)
    pdf.set_xy(85, 8)
    pdf.image('SEG.png', x=175, y=8, w=20)

    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'CHECKLIST NR 32', 0, 1, 'L')

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Segurança e Saúde no Trabalho em Estabelecimentos de Saúde', 0, 1, 'C')
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'Informações Iniciais:', 0, 1)
    pdf.ln(1)

    data_str, hora_str = get_date_time()

    pdf.set_font('Arial', '', 12)
    info_hospital = (
        f"Local de Inspeção: {local_insp.value}. Gestor Responsável: {gestor.value}.\n"
        f"Data: {data_str} e Hora: {hora_str}"
    )
    pdf.multi_cell(0, 8, info_hospital)
    pdf.ln(1)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(largura_perguntas, 8, 'Assuntos Abordados', 1, 0, 'C')
    pdf.cell(largura_respostas, 8, 'Respostas', 1, 1, 'C')

    pdf.set_font('Arial', '', 10)
    for tema, tarefas in tarefas_opcoes.items():
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(largura_perguntas + largura_respostas, 8, tema, 1, 1, 'C')
        pdf.set_font('Arial', '', 10)
        for tarefa in tarefas:
            pdf.cell(largura_perguntas, 8, tarefa, 1)
            pdf.cell(largura_respostas, 8, respostas_opcoes[tarefa], 1)
            pdf.ln(8)

    pdf.ln(2)
    pdf.set_font('Arial', 'B', 12)
    pdf.multi_cell(0, 8, 'Conclusões Obtidas:')
    pdf.ln(2)

    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 8, conclusao.value)
    pdf.ln(3)
    pdf.ln(9)

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, '_______________________________', 0, 1, 'L')
    pdf.cell(0, 10, f'TST Responsável: {tst.value}', 0, 1, 'L')

    pdf.output(nome_arquivo)
    print(f"PDF gerado: {nome_arquivo}")
    return nome_arquivo


def converter_pdf_para_imagem(pdf_path):
    '''
    Função para converter PDF em imagens
    '''
    print(f"Convertendo PDF para imagem: {pdf_path}")
    images = convert_from_path(pdf_path)
    image_paths = []
    # Salva todas as pÃ¡ginas do PDF como imagens PNG
    for i, image in enumerate(images):
        image_path = f"pagina_{i+1}.png"
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
    return image_paths

def mostrar_pdf(page):
    '''
    Função para exibir o PDF como imagens
    '''
    nome_arquivo = gerar_pdf()
    image_paths = converter_pdf_para_imagem(nome_arquivo)
    
    page.clean()  # Limpa a página antes de adicionar o conteúdo do PDF

    if image_paths:
        imagens = []
        for path in image_paths:
            img = ft.Image(src=path)
            imagens.append(img)

        # Cria uma coluna para conter as imagens
        col_images = ft.Column(controls=imagens, scroll="adaptive", expand=True)

        # Ajusta o layout da pÃ¡gina
        page.add(
            ft.Column(
                controls=[
                    col_images,
                    ft.ElevatedButton("Voltar", on_click=lambda _: reset_to_main_page(page))
                ],
                expand=True
            )
        )
    else:
        page.add(
            ft.Column([
                ft.Text("Erro ao gerar o PDF.", color=ft.colors.RED),
                ft.ElevatedButton("Voltar", on_click=lambda _: reset_to_main_page(page)),
            ])
        )
    page.update()

def reset_to_main_page(page):
    page.clean() 
    pagina_principal(page)

def pagina_principal(page: ft.Page):
    '''
    Função da pÃ¡gina principal
    '''
    page.title = "Checklist NR32"
    page.window_icon = "LIGA.PNG" 
    container = ft.Column(scroll="adaptive", expand=True)

    global local_insp, gestor, tst, conclusao
    local_insp = ft.TextField(label="Local de Inspeção", width=300)
    gestor = ft.TextField(label="Nome do Gestor", width=300)
    tst = ft.TextField(label="Nome do Técnico de Segurança de Trabalho", width=300)
    conclusao = ft.TextField(label="Conclusões", width=300, multiline=True)

    container.controls.extend([
        ft.Text("Bem-vindo ao Checklist", size=24, weight="bold", color=ft.colors.WHITE),
        local_insp, gestor, tst
    ])

    global tarefas_opcoes, respostas_opcoes
    tarefas_opcoes = {
        "EPI'S NR 06": [
            "Todos os colaboradores estão usando EPI's?",
            "Os EPI's estão em boas condições de conservaçãoo e higiene?",
            "Colaboradores recebem instruções quanto ao uso de EPI?"
        ],
        "ADORNOS / CALÇADOS FECHADOS - NR 32": [
            "Os colaboradores estão utilizando adornos?",
            "Todos os colaboradores estão utilizando calçado fechado?"
        ],
        "RESÍDUOS - NR 32 / RDC 306": [
            "Todas as lixeiras estão sinalizadas com identificação do tipo de resíduo?",
            "Todas as lixeiras estão em boas condições e com acionamento por pedal?",
            "As caixas de perfurocortantes estão abaixo do limite de preenchimento?",
            "Os colaboradores receberam treinamento quanto ao descarte de perfurocortante?",
            "Os colaboradores foram instruídos quanto ao procedimento em caso de acidente material biológico?",
            "Os resíduos estão bem acondicionados e em local apropriado?",
            "Existe no setor instruções sobre fluxo de acidente do trabalho?"
        ],
        "EQUIPAMENTO DE COMBATE A INCÊNDIO - 32.3.7.5": [
            "Os extintores estão desobstruídos?",
            "Estão bem sinalizados?",
            "Têm funcionários treinados para agir em caso de incêndio?"
        ]
    }

    respostas_opcoes = {tarefa: "Não Se Aplica"
                        for tema in tarefas_opcoes.values() for tarefa in tema}

    def salvar_escolha(e):
        respostas_opcoes[e.control.data] = e.control.value

    def gerar_texto(e):
        texto = f"Local de Inspeção: {local_insp.value}\nGestor Responsável: {gestor.value}\nTécnico de Segurançaa do Trabalho Responsável: {tst.value}\n\nOpções Marcadas:\n"
        for tema, tarefas in tarefas_opcoes.items():
            texto += f"\n{tema}:\n"
            for tarefa in tarefas:
                texto += f"  {tarefa} {respostas_opcoes[tarefa]}\n"
        return texto

    def gerar_conclusao(e):
        texto_conclusao = f'\nConclusão: {conclusao.value}'
        return texto_conclusao

    def gerar_Texto(e):
        texto_completo = gerar_texto(e) + gerar_conclusao(e)
        resultado_text.value = texto_completo
        page.update()

    for tema, tarefas in tarefas_opcoes.items():
        container.controls.append(ft.Text(tema, size=20, weight="bold", color=ft.colors.YELLOW))
        for tarefa in tarefas:
            container.controls.append(criar_tarefa_row(tarefa, salvar_escolha))
    
    container.controls.append(ft.Text("Conclusões Obtidas",
        size=20, weight="bold", color=ft.colors.YELLOW))
    container.controls.append(conclusao)

    resultado_text = ft.Text()
    container.controls.append(resultado_text)

    container.controls.append(ft.Row([
        ft.ElevatedButton("Gerar PDF", on_click=lambda _: mostrar_pdf(page)),
        ft.ElevatedButton("Gerar Texto", on_click=gerar_Texto)
    ]))

    page.add(container)

# Configuração da aplicação Flet
def main(page: ft.Page):
    page.window_width = 1000
    page.window_height = 900
    #page.bgcolor = ft.colors.BLACK
    page.theme_mode = ft.ThemeMode.DARK
    page.route = "/"
    
    pagina_principal(page)

ft.app(target=main)