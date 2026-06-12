import streamlit as st
import os
import urllib.parse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configuração da Página Web
st.set_page_config(
    page_title="Orçamentos - Beatriz Hirayama",
    page_icon="✨",
    layout="centered"
)

# Estilização da interface web via CSS
st.markdown("""
    <style>
    .main-title { font-size:28px; font-weight:bold; color:#1A365D; text-align:center; margin-bottom:20px; }
    .section-title { font-size:18px; font-weight:bold; color:#2B6CB0; margin-top:20px; margin-bottom:10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Painel de Orçamentos Pós-Obra</div>', unsafe_allow_html=True)

# --- FORMULÁRIO NA INTERFACE WEB ---
st.markdown('<div class="section-title">Dados do Cliente</div>', unsafe_allow_html=True)
nome = st.text_input("Nome do Cliente / Empresa:", placeholder="Ex: Joao Silva")
endereco = st.text_input("Endereço / Local da Obra:", placeholder="Ex: Rua, 123 - bairro")

# Campo: Telefone do Cliente
telefone = st.text_input("WhatsApp do Cliente (Apenas números com DDD):", placeholder="Ex: 11999998888")

st.markdown('<div class="section-title">Cronograma e Equipe</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    dias_servico = st.text_input("Dias de Serviço:", placeholder="Ex: 5 Dias")
with col2:
    dias_repasse = st.text_input("Dias de Respaldo:", placeholder="Ex: 1 Dia")
with col3:
    equipe = st.text_input("Equipe Prevista:", placeholder="Ex: 3 Pessoas")

st.markdown('<div class="section-title">Demonstrativo de Valores</div>', unsafe_allow_html=True)
col_val1, col_val2 = st.columns(2)
with col_val1:
    material = st.number_input("Custos de Insumos/Produtos (R$):", min_value=0.0, step=50.0, value=0.0)
with col_val2:
    m_obra = st.number_input("Custo de Mão de Obra (R$):", min_value=0.0, step=50.0, value=0.0)

st.markdown('<div class="section-title">Particularidades do Serviço</div>', unsafe_allow_html=True)
txt_produtos = st.text_area(
    "Produtos e Equipamentos Inclusos:",
    value="Os valores apresentados neste orçamento referem-se aos produtos profissionais que serão utilizados, tais como: removedores específicos, espátulas, buchas não abrasivas, químicos decapantes, panos de microfibra, etc. Este orçamento reflete nosso compromisso com a transparência e a qualidade."
)

txt_obs = st.text_area(
    "Observações importantes sobre este serviço:",
    value="Lembrando que a quantidade de dias estipulada e material para limpeza pós-obra leva em consideração o estado atual do piso fulget e vidros (incluindo limpeza de ventiladores e lustres)."
)

# --- FUNÇÃO QUE GERA O PDF EM MEMÓRIA ---
def gerar_pdf_bytes():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    c_primaria = colors.HexColor('#1A365D')
    c_secundaria = colors.HexColor('#2B6CB0')
    c_texto = colors.HexColor('#2D3748')
    c_fundo_tabela = colors.HexColor('#F7FAFC')

    style_empresa = ParagraphStyle('Empresa', fontName='Helvetica-Bold', fontSize=18, textColor=c_primaria)
    style_sub_empresa = ParagraphStyle('SubEmpresa', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#718096'), spaceAfter=15)
    style_titulo = ParagraphStyle('TituloDoc', fontName='Helvetica-Bold', fontSize=20, textColor=c_primaria, alignment=2, spaceAfter=15)
    style_secao = ParagraphStyle('Secao', fontName='Helvetica-Bold', fontSize=12, textColor=c_secundaria, spaceBefore=12, spaceAfter=6)
    style_corpo = ParagraphStyle('Corpo', fontName='Helvetica', fontSize=10, leading=14, textColor=c_texto)
    style_negrito = ParagraphStyle('Negrito', parent=style_corpo, fontName='Helvetica-Bold')
    style_total = ParagraphStyle('Total', fontName='Helvetica-Bold', fontSize=11, textColor=c_primaria)

    header_data = [
        [Paragraph("BEATRIZ HIRAYAMA", style_empresa), Paragraph("ORÇAMENTO PÓS-OBRA", style_titulo)],
        [Paragraph("Soluções em Limpeza Técnica Profissional", style_sub_empresa), ""]
    ]
    
    if os.path.exists("logo.png"):
        try:
            logo = Image("logo.png", width=110, height=50)
            logo.hAlign = 'LEFT'
            header_data[0][0] = logo
        except:
            pass

    tabela_header = Table(header_data, colWidths=[270, 270])
    tabela_header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ]))
    story.append(tabela_header)
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primaria, spaceBefore=0, spaceAfter=15))

    intro_text = "Apresentamos nosso planejamento técnico e orçamento detalhado para a execução dos serviços pós-obra. Atuamos com foco total em excelência, organization e cuidado minucioso com o patrimônio de nossos clientes."
    story.append(Paragraph(intro_text, style_corpo))
    story.append(Spacer(1, 10))

    story.append(Paragraph("DADOS DO ATENDIMENTO", style_secao))
    dados_cliente = [
        [Paragraph("<b>Cliente:</b>", style_corpo), Paragraph(nome if nome else "-", style_corpo), Paragraph("<b>Dias de Serviço:</b>", style_corpo), Paragraph(dias_servico if dias_servico else "-", style_corpo)],
        [Paragraph("<b>Endereço:</b>", style_corpo), Paragraph(endereco if endereco else "-", style_corpo), Paragraph("<b>Respaldo:</b>", style_corpo), Paragraph(dias_repasse if dias_repasse else "Não se aplica", style_corpo)],
        [Paragraph("<b>Contato:</b>", style_corpo), Paragraph(telefone if telefone else "-", style_corpo), Paragraph("<b>Equipe Prevista:</b>", style_corpo), Paragraph(equipe if equipe else "-", style_corpo)]
    ]
    
    tabela_cliente = Table(dados_cliente, colWidths=[65, 235, 110, 130])
    tabela_cliente.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('LINEBELOW', (2,0), (3,-1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(tabela_cliente)
    story.append(Spacer(1, 15))

    if txt_produtos:
        story.append(Paragraph("PRODUTOS E EQUIPAMENTOS ESPECÍFICOS", style_secao))
        story.append(Paragraph(txt_produtos, style_corpo))
        story.append(Spacer(1, 10))
        
    if txt_obs:
        story.append(Paragraph("PARTICULARIDADES DO PROJETO / OBSERVAÇÕES", style_secao))
        story.append(Paragraph(txt_obs, style_corpo))
        story.append(Spacer(1, 15))

    story.append(Paragraph("INVESTIMENTO", style_secao))
    total = material + m_obra
    f_material = f"R$ {material:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    f_m_obra = f"R$ {m_obra:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    f_total = f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    dados_valores = [
        [Paragraph("<b>Descrição dos Custos Integrados</b>", style_negrito), Paragraph("<b>Valor</b>", style_negrito)],
        [Paragraph("Insumos de Limpeza, EPIs e Maquinário Profissional", style_corpo), Paragraph(f_material, style_corpo)],
        [Paragraph("Mão de Obra Técnica Especializada", style_corpo), Paragraph(f_m_obra, style_corpo)],
        [Paragraph("VALOR TOTAL DO INVESTIMENTO", style_total), Paragraph(f_total, style_total)]
    ]
    
    tabela_valores = Table(dados_valores, colWidths=[390, 150])
    tabela_valores.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), c_primaria),
        ('TEXTCOLOR', (0,0), (1,0), colors.white),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,1), (-1,-2), c_fundo_tabela),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
    ]))
    dados_valores[0][0].style.textColor = colors.white
    dados_valores[0][1].style.textColor = colors.white
    
    story.append(tabela_valores)
    story.append(Spacer(1, 20))

    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceBefore=5, spaceAfter=10))
    texto_compromisso = (
        "<b>Nosso Compromisso:</b> Garantimos a aplicação técnica de produtos homologados que não agridem "
        "as superfícies, mantendo o brilho e integridade de revestimentos, vidros e metais. "
        "Sua satisfação e a entrega pontual compõem o pilar de nossa prestação de serviços. Estamos à inteira "
        "disposição para ajustes e esclarecimentos."
    )
    story.append(Paragraph(texto_compromisso, style_corpo))
    story.append(Spacer(1, 30))
    
    style_assinatura = ParagraphStyle('Assinatura', fontName='Helvetica', fontSize=10, alignment=1, textColor=c_texto)
    story.append(Paragraph("___________________________________________________", style_assinatura))
    story.append(Paragraph("<b>Beatriz Hirayama</b><br/>Gestão de Serviços Pós-Obra", style_assinatura))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --- LOGICA DOS BOTÕES DE SAÍDA ---
st.markdown("<br/>", unsafe_allow_html=True)

if nome:
    nome_limpo = "".join(c for c in nome if c.isalnum() or c in (' ', '_', '-')).rstrip()
    nome_arquivo_pdf = f"Orcamento_PosObra_{nome_limpo}.pdf"
else:
    nome_arquivo_pdf = "Orcamento_PosObra.pdf"

# Gerar o PDF
pdf_data = gerar_pdf_bytes()

# Layout com duas colunas para os botões ficarem lado a lado
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    st.download_button(
        label="📥 BAIXAR ORÇAMENTO (PDF)",
        data=pdf_data,
        file_name=nome_arquivo_pdf,
        mime="application/pdf",
        use_container_width=True
    )

with col_btn2:
    if telefone:
        # Limpa o telefone deixando apenas números
        num_tel = "".join(filter(str.isdigit, telefone))
        
        # Garante o código do país (55 para Brasil) caso o usuário não digite
        if len(num_tel) == 11 or len(num_tel) == 10:
            num_tel = "55" + num_tel
            
        # Mensagem personalizada formatada para URL do WhatsApp
        msg_texto = f"Olá {nome if nome else ''}! Segue nosso orçamento, em caso de dúvidas ficamos à disposição."
        msg_codificada = urllib.parse.quote(msg_texto)
        
        # Cria o link oficial da API do WhatsApp com o nome correto corrigido aqui:
        link_whatsapp = f"https://api.whatsapp.com/send?phone={num_tel}&text={msg_codificada}"
        
        # Exibe o botão verde do WhatsApp
        st.link_button("💬 ABRIR WHATSAPP", link_whatsapp, use_container_width=True, type="primary")
    else:
        st.button("💬 ENVIAR VIA WHATSAPP (Insira o telefone)", disabled=True, use_container_width=True)
