#!/usr/bin/env python3
"""
Gera o PDF final da Declaração de Recebimento + Vistoria (contraproposta)
com todas as alterações da Análise Jurídica incorporadas — versão limpa,
pronta para apresentar à locadora.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether
)
from reportlab.lib.colors import HexColor
import os

OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__),
    "docs",
    "Declaracao_Vistoria_Final_Depillagos.pdf"
)

AZUL = HexColor("#1B3A5C")
CINZA = HexColor("#555555")

def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        "DocTitle",
        parent=styles["Title"],
        fontSize=18,
        leading=22,
        textColor=AZUL,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "SubTitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        textColor=CINZA,
        alignment=TA_CENTER,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        "BodyBold",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "SectionHeader",
        parent=styles["Normal"],
        fontSize=12,
        leading=16,
        textColor=AZUL,
        fontName="Helvetica-Bold",
        spaceAfter=6,
        spaceBefore=14,
        borderWidth=0,
        borderPadding=0,
    ))
    styles.add(ParagraphStyle(
        "RoomHeader",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        fontName="Helvetica-Bold",
        spaceAfter=4,
        spaceBefore=10,
    ))
    styles.add(ParagraphStyle(
        "ItemLabel",
        parent=styles["Normal"],
        fontSize=10,
        leading=13,
        fontName="Helvetica-Bold",
        spaceAfter=2,
        spaceBefore=4,
    ))
    styles.add(ParagraphStyle(
        "ItemDesc",
        parent=styles["Normal"],
        fontSize=10,
        leading=13,
        fontName="Helvetica",
        spaceAfter=4,
        alignment=TA_JUSTIFY,
    ))
    styles.add(ParagraphStyle(
        "Clause",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        spaceBefore=4,
        fontName="Helvetica",
        leftIndent=0,
    ))
    styles.add(ParagraphStyle(
        "Ressalva",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        fontName="Helvetica-Bold",
        backColor=HexColor("#FFF8E1"),
        borderPadding=6,
    ))
    styles.add(ParagraphStyle(
        "Signature",
        parent=styles["Normal"],
        fontSize=10,
        leading=18,
        fontName="Helvetica",
        spaceBefore=30,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        textColor=CINZA,
        alignment=TA_CENTER,
    ))
    return styles


def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(CINZA)
    canvas.drawRightString(
        A4[0] - 2 * cm, A4[1] - 1.2 * cm,
        "Declaração de Recebimento e Vistoria — Contraproposta Depillagos"
    )
    canvas.drawCentredString(
        A4[0] / 2, 1.2 * cm,
        f"Página {doc.page}"
    )
    canvas.restoreState()


def item(label, desc, styles):
    """Helper: retorna lista de flowables para um item da vistoria."""
    result = []
    result.append(Paragraph(f"<b>{label}</b>", styles["ItemLabel"]))
    result.append(Paragraph(desc, styles["ItemDesc"]))
    return result


def build_document():
    styles = build_styles()
    story = []

    # ================================================================
    # PÁGINA 1 — DECLARAÇÃO
    # ================================================================
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph("DECLARAÇÃO", styles["DocTitle"]))
    story.append(Spacer(1, 0.8 * cm))

    declaracao_text = (
        "Declaro, para todos os fins, na qualidade de representante legal do "
        "<b>Centro de Estética Depillagos Ltda</b>, inscrita no CNPJ sob o nº "
        "09.223.558/0001-00, que o imóvel em que é locadora a <b>Paiva "
        "Administradora de Bens Próprios Ltda</b>, situado na Rua Coronel "
        "Francisco Alves da Silva, nº 120 — loja B, grupo 101 e 102, Centro, "
        "nesta cidade, locado pelo prazo de sessenta meses, encontra-se em "
        "boas condições de uso e ocupação, sendo certo que o atual estado de "
        "conservação decorre, em grande parte, das benfeitorias e reformas "
        "realizadas e custeadas integralmente pela LOCATÁRIA ao longo de "
        "aproximadamente 18 (dezoito) anos de ocupação contínua do imóvel, "
        "incluindo, mas não se limitando a: troca integral de piso por "
        "porcelanato, reforma completa de três banheiros, instalação de "
        "rebaixamento em gesso e iluminação, troca de portas, instalação de "
        "divisórias em MDF, nichos para ar-condicionado revestidos em mármore, "
        "e pintura completa interna e externa. Na devolução do imóvel, serão "
        "consideradas as deteriorações decorrentes do uso normal, nos termos "
        "do art. 23, III, da Lei 8.245/91, não podendo ser exigida a "
        "manutenção ou restauração de benfeitorias realizadas e custeadas "
        "exclusivamente pela LOCATÁRIA."
    )
    story.append(Paragraph(declaracao_text, styles["Body"]))
    story.append(Spacer(1, 0.3 * cm))

    # Cláusula do telhado
    telhado_text = (
        "A LOCATÁRIA declara estar ciente de que o telhado do imóvel foi "
        "reformado pela LOCADORA. A LOCADORA permanece responsável pela "
        "manutenção estrutural do telhado e pela reparação de quaisquer "
        "infiltrações dele decorrentes, nos termos do art. 22, incisos I e "
        "IV, da Lei 8.245/91. A instalação de equipamentos no telhado "
        "(incluindo condensadoras de ar-condicionado, antenas e exaustores) "
        "será permitida, mediante comunicação prévia por escrito à LOCADORA, "
        "desde que realizada por profissional qualificado. A LOCATÁRIA terá "
        "livre acesso ao telhado para fins de instalação e manutenção dos "
        "seus equipamentos, assumindo responsabilidade apenas por danos "
        "comprovadamente causados por sua conduta ou de seus prepostos ao "
        "telhado."
    )
    story.append(Paragraph(telhado_text, styles["Body"]))
    story.append(Spacer(1, 0.3 * cm))

    # Cláusula de infiltrações
    infiltracao_text = (
        "As infiltrações decorrentes de problemas no telhado, "
        "impermeabilização ou estrutura do prédio são de responsabilidade "
        "exclusiva da LOCADORA, que deverá repará-las no prazo máximo de "
        "15 (quinze) dias úteis após notificação por escrito da LOCATÁRIA. "
        "Na inércia da LOCADORA, a LOCATÁRIA poderá realizar os reparos "
        "necessários, configurando benfeitoria necessária nos termos do "
        "art. 35 da Lei 8.245/91, com direito a ressarcimento integral "
        "mediante compensação nos aluguéis vincendos."
    )
    story.append(Paragraph(infiltracao_text, styles["Body"]))
    story.append(Spacer(1, 0.3 * cm))

    # Cláusula de manutenção estrutural
    manutencao_text = (
        "A LOCADORA é responsável pela manutenção estrutural do imóvel, "
        "incluindo telhado, paredes mestras, fundações, instalações "
        "hidráulicas e elétricas principais, fachada e impermeabilização, "
        "nos termos do art. 22 da Lei 8.245/91."
    )
    story.append(Paragraph(manutencao_text, styles["Body"]))
    story.append(Spacer(1, 0.3 * cm))

    # Cláusula de benfeitorias
    benfeitorias_text = (
        "A LOCADORA reconhece que as benfeitorias existentes no imóvel, "
        "conforme descritas na vistoria anexa, foram realizadas e custeadas "
        "pela LOCATÁRIA ao longo dos anos de ocupação. As benfeitorias "
        "necessárias serão indenizáveis independentemente de autorização "
        "prévia. As benfeitorias úteis já realizadas são reconhecidas como "
        "autorizadas e igualmente indenizáveis. Na hipótese de devolução do "
        "imóvel, não será exigida a restauração ao estado anterior às "
        "benfeitorias, nos termos dos arts. 35 e 36 da Lei 8.245/91."
    )
    story.append(Paragraph(benfeitorias_text, styles["Body"]))
    story.append(Spacer(1, 0.3 * cm))

    encerramento_text = (
        "A presente declaração, firmada na presença das testemunhas do "
        "contrato, que assinam ao final da vistoria que segue, fica, para "
        "todos os efeitos de direito, fazendo parte integrante do presente "
        "contrato de locação do referido imóvel."
    )
    story.append(Paragraph(encerramento_text, styles["Body"]))

    # ================================================================
    # VISTORIA
    # ================================================================
    story.append(PageBreak())
    story.append(Paragraph("VISTORIA REALIZADA NO IMÓVEL", styles["DocTitle"]))
    story.append(Spacer(1, 0.5 * cm))

    ressalva = (
        "RESSALVA PRELIMINAR: O estado de conservação descrito nesta "
        "vistoria decorre, em sua maior parte, de benfeitorias e reformas "
        "realizadas e custeadas integralmente pela LOCATÁRIA ao longo de "
        "aproximadamente 18 (dezoito) anos de ocupação contínua. O estado "
        "original do imóvel, quando da primeira locação, era "
        "significativamente inferior ao aqui descrito. Esta vistoria não "
        "constitui reconhecimento de que o imóvel foi entregue pela LOCADORA "
        "nas condições aqui descritas, servindo apenas como registro do "
        "estado atual para fins de comparação na devolução."
    )
    story.append(Paragraph(ressalva, styles["Ressalva"]))
    story.append(Spacer(1, 0.3 * cm))

    # --- FACHADA ---
    story.append(Paragraph("FACHADA:", styles["SectionHeader"]))
    story.extend(item("FACHADA", "Revestida em cerâmica, tipo pastilhas, azul turquesa e ao redor das portas, com acabamento em granito.", styles))
    story.append(Spacer(1, 0.2 * cm))

    story.extend(item("MARQUISE", "Pintada em branco, com calha simples enferrujada, com uma lâmpada fluorescente de 40Wts.", styles))
    story.append(Paragraph(
        "<i>Nota: A calha enferrujada constitui defeito preexistente de responsabilidade da LOCADORA, devendo ser substituída no prazo de 30 dias.</i>",
        styles["ItemDesc"]
    ))
    story.append(Spacer(1, 0.2 * cm))

    story.extend(item("TETO", "Revestido em PVC, com luminária.", styles))

    # --- LOJA/Frente ---
    story.append(Paragraph("LOJA/Frente:", styles["RoomHeader"]))
    story.extend(item("PORTA", "Acesso loja — 2 de aço, pintadas em tinta esmalte platina, com 2 fechaduras de tambor no piso, com chaves e puxador de ferro; Na parte superior interna moldura em fórmica para embutir as portas; Soleiras em granito rajado.", styles))
    story.extend(item("PAREDES", "Emassadas e pintadas em tinta acrílica fosca branca, sem furos. Lateral esquerda texturizada e pintada com tinta acrílica branca.", styles))
    story.extend(item("TETO", "Emassado e pintado em tinta acrílica fosca branca, com rebaixamento em gesso, fazendo formato oval na lateral esquerda, com sancas com detalhes pintados em tinta acrílica branca. Com 15 \"Spots\" redondos embutidos e niquelados brancos, todos com globos de vidro opaco e lâmpadas econômicas; Três ventiladores de teto niquelados de branco, com dois globos de vidro opaco, em perfeito estado e funcionamento.", styles))
    story.extend(item("PISO", "Em cerâmica vitrificada em bom estado de conservação, com rodapé pintado em tinta na cor branca.", styles))
    story.extend(item("CAIXA DE DISJUNTORES", "Dupla com tampa plástica: 1 de \"30A\", 3 de \"10A\" e 6 de \"20A\".", styles))
    story.extend(item("INTERRUPTORES", "3 triplos com espelho plástico. 3 seccionados para ventiladores.", styles))
    story.extend(item("TOMADAS", "16 simples com espelho plástico branco, 2 para computador simples com espelho plástico branco, 1 para ar condicionado; 1 com fiação e terminal para antena; 1 com tampa cega.", styles))

    # --- LOJA/fundos ---
    story.append(Paragraph("LOJA/fundos:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Emassadas e pintadas em tinta acrílica branca, sem furos.", styles))
    story.extend(item("TETO", "Forrado em PVC branco, em perfeito estado, com 5 calhas duplas brancas, com tampas acrílicas transparentes e 4 lâmpadas fluorescentes de \"20A\" e 6 lâmpadas fluorescentes de \"40A\" cada, em funcionamento.", styles))
    story.extend(item("PISO", "Em cerâmica gelo em perfeito estado, com rodapé pintado.", styles))
    story.extend(item("BASCULANTES", "2 em ferro pintado em esmalte branco, com vidros canelados perfeitos e grade de ferro externa.", styles))
    story.extend(item("CAIXA DE DISJUNTORES", "Com tampa plástica: 3 de \"15A\"; 1 de \"20A\" e 1 de \"40A\".", styles))
    story.extend(item("INTERRUPTOR", "1 triplo com espelho simples.", styles))
    story.extend(item("TOMADAS", "8 simples com espelho e 1 tampa cega.", styles))

    # --- ÁREA PARA CAFÉ ---
    story.append(Paragraph("ÁREA PARA CAFÉ:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Até a metade em cerâmica branca, sem furos; acima da cerâmica pintada em tinta acrílica fosca branca, sem furos. Tijolos cobogós para ventilação. Plafonier em alumínio com lâmpada fluorescente.", styles))
    story.extend(item("TETO", "Pintado em tinta acrílica branca.", styles))
    story.extend(item("PISO", "Em cerâmica branca perfeita, com ralo plástico pequeno.", styles))
    story.extend(item("PORTA", "Sanfonada em regular estado.", styles))
    story.extend(item("BANCADA/PIA", "Em granito cinza, com cuba em inox, com torneira plástica em perfeito estado e sifão plástico com copo.", styles))
    story.extend(item("CORTINEIROS", "2, em granito cinza.", styles))
    story.append(Paragraph("Porta-sabão cromado. INTERRUPTOR com tomada acoplada, com espelho simples.", styles["ItemDesc"]))

    # --- BANHEIRO (térreo) ---
    story.append(Paragraph("BANHEIRO:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Até a metade em cerâmica branca e barra decorada; acima da cerâmica pintada em tinta acrílica fosca branca, sem furos. Plafonier de alumínio, com bocal e lâmpada econômica.", styles))
    story.extend(item("TETO", "Pintado em tinta acrílica branca.", styles))
    story.extend(item("PISO", "Em cerâmica branca em perfeito estado, com ralo plástico pequeno.", styles))
    story.extend(item("PORTA", "Sanfonada em PVC na cor areia, com trinco, em perfeito estado.", styles))
    story.extend(item("VASO SANITÁRIO", "Em louça branca, descarga em caixa externa em perfeito funcionamento.", styles))
    story.extend(item("LAVATÓRIO", "Em louça branca pequeno com torneira cromada.", styles))
    story.append(Paragraph("Chuveiro plástico simples; Instalação elétrica para chuveiro com espelho branco. Suporte plástico para toalhas em perfeito estado. Porta-sabão — 2 em inox. Porta-toalha — 1 de gancho pequeno, em inox. Porta-papel — em louça branca, com suporte. Porta sanfonada gelo com trinco interno plástico. INTERRUPTOR — 1 com tomada acoplada com espelho plástico. 1 tampa cega.", styles["ItemDesc"]))

    # --- SALA ---
    story.append(Paragraph("SALA:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Pintadas em tinta acrílica branca, sem furos.", styles))
    story.extend(item("DIVISÓRIA", "Em MDF marfim, em perfeito estado, com porta sanfonada PVC marfim em perfeito estado e funcionamento.", styles))
    story.extend(item("TETO", "Forrado em PVC branco, com calha dupla branca, com duas lâmpadas fluorescentes de 40Wts, em funcionamento.", styles))
    story.append(Paragraph("Acima do forro, grade de segurança em ferro e caixa d'água instalada, que serve ao prédio onde está localizado o imóvel.", styles["ItemDesc"]))
    story.append(Paragraph(
        "<i>Nota: A caixa d'água que serve ao prédio está localizada acima do forro deste cômodo. Eventuais vazamentos ou necessidade de manutenção da caixa d'água são de responsabilidade exclusiva da LOCADORA.</i>",
        styles["ItemDesc"]
    ))
    story.extend(item("PISO", "Em cerâmica gelo em perfeito estado.", styles))
    story.extend(item("TOMADAS", "4 simples com espelho; 1 dupla externa.", styles))

    # ================================================================
    # GRUPO 101
    # ================================================================
    story.append(Paragraph("GRUPO 101:", styles["SectionHeader"]))

    story.append(Paragraph("ESCADA COMUM DE ACESSO AO SOBRADO:", styles["RoomHeader"]))
    story.extend(item("PORTAS", "Acesso sobrado — de metal, varada, pintada em esmalte branco acetinado, com maçaneta cromada e fechadura de tambor; a calçada externa — de aço sem pintura recente, em funcionamento e bom estado, com fechadura de tambor e chave.", styles))
    story.extend(item("PAREDES", "Com textura, pintadas em tinta acrílica de computador rosa e lilás, com acabamento em madeira pintada na mesma cor, cortinadas em madeira e base quadrangular em \"L\" de ferro, sendo a outra metade de parede pintada em tinta acrílica branca neve.", styles))

    story.append(Paragraph("SALA DE ESPERA:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Emassadas, em frente com textura, demais pintadas com tinta acrílica branco neve, e um paitoril em mármore.", styles))
    story.extend(item("TETO", "Pintado em tinta acrílica branco neve, com quatro pontos de luz com bocais, plafoniers, globos plásticos e lâmpadas, uma tampa cega; ventilador de teto com três pás em funcionamento.", styles))
    story.extend(item("PISO E RODAPÉS", "Em cerâmica vitrificada branca rajada e rejunte cinza, com soleira em mármore.", styles))
    story.extend(item("TOMADAS", "4 simples com espelho.", styles))
    story.append(Paragraph("2 saída para antenas. 3 tampas cegas (2 com espelhos simples e 1 texturizada). INTERRUPTORES — 3 simples com espelhos.", styles["ItemDesc"]))

    story.append(Paragraph("RECEPÇÃO:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Pintadas em tinta acrílica azul (com registro e bojo na lateral direita).", styles))
    story.extend(item("TETO", "Pintado em tinta acrílica azul, com bocal, plafonier, globo plástico e lâmpada.", styles))
    story.extend(item("PISO E RODAPÉS", "Em cerâmica vitrificada branca rajada e rejunte cinza, com soleira em mármore.", styles))
    story.extend(item("PORTA", "Em madeira lisa, pintada em tinta esmalte fosco platina, com 1 chave.", styles))
    story.extend(item("BANCADAS", "Duas em mármore (sendo que se fechada a parede na entrega do imóvel casa seja solicitada pelo locador).", styles))
    story.extend(item("BASCULANTE", "Duplo de ferro com articulação e 19 vidros martelados perfeitos.", styles))
    story.append(Paragraph("INTERRUPTOR — 1 simples com espelho. TOMADAS — 3 simples com espelho; 1 saída para interfone com espelho; 1 entrada e 1 saída hidráulica; 1 saída para esgoto (para de máquina de lavar).", styles["ItemDesc"]))

    story.append(Paragraph("BANHEIRO:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Metade em ardósia cinza rajada e rejunte cinza, outra metade pintada em tinta acrílica branca neve.", styles))
    story.extend(item("TETO", "Pintado em tinta acrílica branco neve, com bocal, plafonier — exaustor cromado acoplado.", styles))
    story.extend(item("PISO E RODAPÉS", "Em cerâmica vitrificada branca rajada e rejunte cinza, com soleira em mármore.", styles))
    story.extend(item("PORTA", "Em madeira com moldura, pintada em tinta esmalte fosco platina, com maçaneta cromada e fechadura de trinco.", styles))
    story.extend(item("LAVATÓRIO", "Em louça cinza, com torneira cromada e sifão plástico em perfeito funcionamento.", styles))
    story.extend(item("VASO", "Em louça cinza, com caixa de descarga acoplada em perfeito funcionamento. Dois registros cromados, dois ralos plásticos grandes.", styles))
    story.append(Paragraph("INTERRUPTOR — 1 simples com espelho. TOMADAS — 3 tampas cegas.", styles["ItemDesc"]))

    # Salas I, II, III, IV
    story.append(Paragraph("SALA I/frente:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Emassadas e pintadas com tinta acrílica branco neve.", styles))
    story.extend(item("TETO", "Pintado em tinta acrílica branco neve, com fios expostos.", styles))
    story.extend(item("PISO", "Em cerâmica vitrificada branca rajada e rejunte cinza, com soleira em mármore; instalação hidráulica e elétrica próxima à parede da janela.", styles))
    story.extend(item("PORTA", "Em madeira com moldura, pintada em tinta esmalte platina, com maçaneta cromada, espelho e duas chaves.", styles))
    story.extend(item("JANELA", "Em esquadria de alumínio com duas basculantes fixas e duas móveis, com max-ar superior, batistados: sete vidros lisos perfeitos.", styles))
    story.append(Paragraph("NICHO para ar condicionado revestido em mármore, com instalação elétrica. INTERRUPTOR — 1 simples com espelho. TOMADAS — 3 simples com espelhos e 1 para ar condicionado.", styles["ItemDesc"]))

    story.append(Paragraph("SALA II/frente:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Emassadas e pintadas com tinta acrílica branco neve.", styles))
    story.extend(item("TETO", "Pintado em tinta plástica branco neve, com bocal, plafonier, globo plástico e lâmpada.", styles))
    story.extend(item("PISO", "Em cerâmica vitrificada branca rajada e rejunte cinza.", styles))
    story.extend(item("JANELA", "Em esquadria de alumínio com duas basculantes fixas e duas móveis, com max-ar superior, batistados: sete vidros lisos perfeitos.", styles))
    story.append(Paragraph("NICHO para ar condicionado revestido em mármore, com instalação elétrica. INTERRUPTOR — 1 acoplado com tomada, e espelho. TOMADAS — 4 simples com espelhos e 1 para ar condicionado. Uma entrada e uma saída hidráulica — uma com registro plástico e outra sem bojo.", styles["ItemDesc"]))

    story.append(Paragraph("SALA III/frente:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Emassadas e pintadas com tinta acrílica branco neve, saída uma pintada em tinta acrílica azul.", styles))
    story.extend(item("TETO", "Pintado em tinta acrílica branco neve, com faixas expostas.", styles))
    story.extend(item("PISO", "Em cerâmica vitrificada branca rajada e rejunte cinza, com soleira em mármore; com instalação hidráulica e elétrica próxima à janela.", styles))
    story.extend(item("PORTA", "Em madeira com moldura, pintada em tinta esmalte fosco platina, com maçaneta cromada, espelho e 1 chave.", styles))
    story.extend(item("JANELA", "Em esquadria de alumínio com duas basculantes fixas e duas móveis, com max-ar superior, batistados: sete vidros lisos perfeitos.", styles))
    story.append(Paragraph("NICHO para ar condicionado revestido em mármore, com instalação elétrica. INTERRUPTOR — 1 simples com espelho. TOMADAS — 6 simples com espelhos, uma tampa cega.", styles["ItemDesc"]))

    story.append(Paragraph("CIRCULAÇÃO/DEPÓSITO:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Emassadas e pintadas com tinta acrílica branco neve.", styles))
    story.extend(item("TETO", "Pintado em tinta plástica branco neve, com faixo para iluminação.", styles))
    story.extend(item("PISO E RODAPÉS", "Cerâmica em diagonal vitrificada branca com rajada e rejunte cinza, com soleira fina em mármore.", styles))
    story.append(Paragraph("TOMADAS — 3 simples com espelhos; 1 tampa cega. Uma entrada e uma saída hidráulica. Bancada em mármore branco.", styles["ItemDesc"]))

    story.append(Paragraph("SALA IV/fundos:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Emassadas e pintadas com tinta acrílica branco neve (rejunte barra de 2,0 x 0,60 em cerâmica branca rajada e rejunte cinza, tendo uma pintada em tinta acrílica amarelo cástico).", styles))
    story.extend(item("TETO", "Pintado em tinta plástica branco neve, com fiação exposta.", styles))
    story.extend(item("PISO", "Em cerâmica vitrificada branca rajada e rejunte cinza, com ralo plástico 15 x 15 com sifão, com soleira em mármore; instalação hidráulica e elétrica próxima a parede esquerda.", styles))
    story.extend(item("PORTA", "Em madeira com moldura, pintada em tinta esmalte fosco platina, com maçaneta cromada e espelho.", styles))
    story.extend(item("JANELA", "Em esquadria de alumínio com duas folhas móveis e 2 vidros lisos perfeitos.", styles))
    story.append(Paragraph("NICHO para ar condicionado revestido em mármore, com instalação elétrica. INTERRUPTOR — 2 simples com espelhos. TOMADAS — 9 simples com espelhos, sendo 1 para ar condicionado; 1 tampa variada para saída de som e 2 com fiação exposta. Caixa de distribuição de luz com duas tampas plásticas e 4 disjuntores de \"15\", 5 disjuntores de \"20\", 1 disjuntor de \"40\" e 1 disjuntor de \"50\".", styles["ItemDesc"]))

    # ================================================================
    # GRUPO 102
    # ================================================================
    story.append(Paragraph("GRUPO 102:", styles["SectionHeader"]))

    story.append(Paragraph("SALA/Depósito:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Emassadas e pintadas com tinta acrílica gelo — à esquerda — basculante em alumínio pequeno, tendo 3 vidros martelados e articulação perfeita; à direita — basculante de ferro grande pintado em tinta esmalte branco fosco, com 19 vidros martelados perfeitos.", styles))
    story.extend(item("TETO", "Pintado em tinta branco neve, com bocal, plafonier, globo plástico e lâmpada.", styles))
    story.extend(item("PISO", "Em cerâmica vitrificada branca rajada e rejunte cinza, tendo um ralo com tampa cega e soleira em mármore.", styles))
    story.extend(item("PORTA", "Em madeira lisa pintada em tinta esmalte platina.", styles))
    story.append(Paragraph("INTERRUPTOR — 1 simples com espelho. TOMADAS — 2 simples com espelho, 1 tampa cega. 1 entrada e 1 saída hidráulica; 1 saída para esgoto (com instalação para máquina de lavar); registro com canopla plástica. 2 saídas elétricas com tampas cegas de plástico branco.", styles["ItemDesc"]))

    story.append(Paragraph("SALA 1 (com frente à porta):", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Emassadas e pintadas com tinta acrílica gelo — à esquerda — basculante de ferro grande pintado em tinta esmalte branco fosco, com 11 vidros martelados e articulação perfeita.", styles))
    story.extend(item("TETO", "Pintado em tinta branco neve, com calha fluorescente de 40 wats em funcionamento.", styles))
    story.extend(item("PISO", "Em cerâmica gelo, com soleira em mármore; pequeno ferro fechado com cimento branco.", styles))
    story.extend(item("PORTA", "Em madeira lisa pintada em tinta esmalte platina, com maçaneta cromada simples e chave.", styles))
    story.append(Paragraph("NICHO para ar condicionado revestido em mármore, com instalação elétrica. INTERRUPTOR — 1 simples com espelho. TOMADAS — 2 simples. 1 entrada e 1 saída hidráulica. Fiação para telefone com terminal, sofra.", styles["ItemDesc"]))

    story.append(Paragraph("SALA II (COM BANCADA E PIA):", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Pintadas em tinta acrílica gelo, sendo a da pia até a metade em ardósia brancas com rejunte cinza.", styles))
    story.extend(item("TETO", "Pintado em tinta acrílica branco neve, com bocal, plafonier, globo plástico e lâmpada.", styles))
    story.extend(item("PISO", "Em cerâmica vitrificada branca rajada e rejunte cinza, tendo caixa de gordura em PVC \"Tigre\" com 250ml de capacidade e tampo.", styles))
    story.extend(item("BASCULANTE", "Em alumínio, com 4 vidros martelados e articulação perfeita.", styles))
    story.extend(item("PIA", "Em granito cinza, com cuba e ralo em inox, sifão plástico.", styles))
    story.append(Paragraph("1 bico para registro. 1 saída hidráulica com bojo pequeno para fibra. TOMADAS — 5 simples com espelho. Quadro de distribuição de luz com 4 disjuntores de \"15\" e 6 disjuntores de \"20\".", styles["ItemDesc"]))

    story.append(Paragraph("BANHEIRO:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Metade em cerâmica branca com rejunte cinza e outra metade pintada em tinta acrílica branco neve.", styles))
    story.extend(item("TETO", "Pintado em tinta acrílica branco neve, com bocal e plafonier.", styles))
    story.extend(item("PISO", "Em cerâmica vitrificada branca rajada e rejunte cinza, com soleira em mármore e ralo plástico grande.", styles))
    story.extend(item("BASCULANTE", "Em alumínio, com 4 vidros crespos e articulação perfeita.", styles))
    story.extend(item("PORTA", "Em madeira lisa pintada em tinta esmalte platina.", styles))
    story.extend(item("LAVATÓRIO", "Em louça cinza — acima de lavatório, ponto de luz com bocal e globo plástico.", styles))
    story.extend(item("VASO", "Em louça cinza em excelente estado, com tampo sifão.", styles))
    story.append(Paragraph("BOXE — com soleira em mármore. Ralo plástico pequeno. Saída hidráulica e elétrica para colocação de chuveiro. Registro cromado (torneira). INTERRUPTOR — 1 simples com espelho, 1 com tomada acoplada e espelho.", styles["ItemDesc"]))

    story.append(Paragraph("SALA III:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Emassadas e pintadas com tinta acrílica gelo.", styles))
    story.extend(item("TETO", "Pintado em tinta plástica branco neve, com bocal e plafonier.", styles))
    story.extend(item("PISO", "Em cerâmica vitrificada branca rajada e rejunte cinza, com soleira em mármore.", styles))
    story.extend(item("PORTA", "Em madeira lisa, pintada em tinta esmalte platina, com maçaneta cromada, espelho.", styles))
    story.extend(item("JANELA", "Em duas folhas de alumínio com cremona e articulação perfeito(s), com 7 vidros perfeitos.", styles))
    story.append(Paragraph("NICHO para ar condicionado revestido em mármore, com placa de proteção e instalação elétrica. INTERRUPTOR — 1 simples com espelho. TOMADAS — 3 simples com espelhos. Uma saída para fio de antena. Duas saídas hidráulicas.", styles["ItemDesc"]))

    story.append(Paragraph("CORREDOR DE ACESSO:", styles["RoomHeader"]))
    story.extend(item("PAREDES", "Emassadas e pintadas com tinta acrílica gelo.", styles))
    story.extend(item("TETO", "Pintado em tinta branco neve, com bocal, plafonier, globo plástico e lâmpada, tendo uma pequena porta em madeira também pintada em branco e com trinco de segurança, de acesso ao telhado do imóvel.", styles))
    story.extend(item("PISO", "Em cerâmica vitrificada branca rajada e rejunte cinza, com soleira em mármore.", styles))
    story.append(Paragraph("INTERRUPTOR — 1 simples com espelho. TOMADAS — 1 simples. 1 tampa cega.", styles["ItemDesc"]))

    # --- Tintas ---
    story.append(Paragraph("Tintas utilizadas para a pintura da loja (térreo):", styles["RoomHeader"]))
    story.append(Paragraph("Paredes — Tinta Coral Acrílico Premium na cor branca. Portas — esmalte Coral na cor platina.", styles["ItemDesc"]))

    story.append(Paragraph("Tintas utilizadas para a pintura do sobrado:", styles["RoomHeader"]))
    story.append(Paragraph("Paredes — Tinta acrílica Coralar Econômica na cor gelo. Tetos — Tinta acrílica Coralar Econômica na cor branca. Portas e portas — esmalte semibrilho Coralar na cor platina.", styles["ItemDesc"]))

    # --- Chaves ---
    story.append(Paragraph("Chaves Entregues:", styles["RoomHeader"]))
    story.append(Paragraph("Escritório — 2 chaves da porta da direita e 2 chaves da porta da esquerda.", styles["ItemDesc"]))
    story.append(Paragraph("Sobrado — 1 da porta de aço; 1 da porta de metal de acesso ao prédio; 1 da porta de entrada do imóvel.", styles["ItemDesc"]))

    # --- Fachada (alterada) ---
    story.append(Spacer(1, 0.5 * cm))
    fachada_text = (
        "OBS: A FACHADA DO PRÉDIO ONDE SE LOCALIZA O IMÓVEL, ASSIM COMO A "
        "ÁREA COMUM DE ACESSO AO SOBRADO FORAM PINTADAS PELA LOCATÁRIA COM "
        "AUTORIZAÇÃO DO PROPRIETÁRIO. Eventuais modificações na fachada "
        "(incluindo sinalização comercial, manutenção e reparos) poderão ser "
        "realizadas pela LOCATÁRIA mediante comunicação prévia por escrito à "
        "LOCADORA, mantendo-se o padrão estético do prédio. A manutenção "
        "periódica da fachada (pintura, reparos por desgaste natural) é de "
        "responsabilidade da LOCADORA, conforme art. 22 da Lei 8.245/91."
    )
    story.append(Paragraph(fachada_text, styles["BodyBold"]))

    # --- Amianto ---
    story.append(Spacer(1, 0.3 * cm))
    amianto_text = (
        "A LOCADORA declara estar ciente da existência de telhas de amianto "
        "nas áreas adjacentes ao imóvel locado e compromete-se a providenciar "
        "sua substituição por material permitido por lei, em conformidade com "
        "a Lei Estadual RJ nº 3.579/2001 e a decisão do STF na ADI 3937, no "
        "prazo de 180 (cento e oitenta) dias."
    )
    story.append(Paragraph(amianto_text, styles["Body"]))

    # --- Assinaturas ---
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph("Araruama-RJ, _____ de ______________ de 2025.", styles["Body"]))
    story.append(Spacer(1, 1.5 * cm))

    story.append(Paragraph("_______________________________________", styles["Signature"]))
    story.append(Paragraph("LOCATÁRIA", styles["Body"]))
    story.append(Spacer(1, 1 * cm))

    story.append(Paragraph("_______________________________________", styles["Signature"]))
    story.append(Paragraph("LOCADORA", styles["Body"]))
    story.append(Spacer(1, 1 * cm))

    story.append(Paragraph("_______________________________________", styles["Signature"]))
    story.append(Paragraph("TESTEMUNHA 1", styles["Body"]))
    story.append(Spacer(1, 0.8 * cm))

    story.append(Paragraph("_______________________________________", styles["Signature"]))
    story.append(Paragraph("TESTEMUNHA 2", styles["Body"]))

    # Build PDF
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Declaração de Recebimento e Vistoria — Contraproposta Depillagos",
        author="Centro de Estética Depillagos Ltda",
    )
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"PDF gerado com sucesso: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_document()
