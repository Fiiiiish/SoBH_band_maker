from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
# import pickle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import PIL
from PIL import Image
import os

nb_cards = 9
offset_x = [1.2 * cm, 7.4 * cm, 13.6 * cm] * 3
offset_y = [19.2 * cm, 19.2 * cm, 19.2 * cm, 10.5 * cm, 10.5 * cm, 10.5 * cm, 1.8 * cm, 1.8 * cm, 1.8 * cm]
pos_name = [0.6 * cm, 7.85 * cm]
pos_quality = [4.9 * cm, 6.9 * cm]
pos_combat = [5.02 * cm, 5.7 * cm]
pos_perso = [0.6 * cm, 4.93 * cm]
pos_cost = [4.6 * cm, 4.93 * cm]
pos_capa = [0.45 * cm, 0.47 * cm]
pos_mdl_pic = [0.4 * cm, 5 * cm]


def print_pdf_band_list(band):
    # define file name
    pdf_file = "SoBH_" + band.name + ".pdf"
    # protect against overwriting
    ind = 1
    while os.path.exists(pdf_file):
        pdf_file = "SoBH_" + band.name + "_" + str(ind) + ".pdf"
        ind += 1
    # create canvas / file
    c = canvas.Canvas(pdf_file)
    # print band list - header
    print_band_list_pdf(band, c)
    # print cards
    i = 0
    already_printed = []
    for model in band.model_list:
        model_to_print = True
        # define if model already has a card...
        for model_printed in already_printed:
            if model.name == model_printed.name and model.cost == model_printed.cost and model.quality == model_printed.quality and model.combat == model_printed.combat and model.personality == model_printed.personality:
                model_to_print = False
        # model not printed, print it!
        if model_to_print:
            already_printed.append(model)
            # print model card
            print_model_card(model, c, i)
            i += 1
            # if too many cards, add a page
            if i >= nb_cards:
                i = 0
                c.showPage()
    c.save()


def print_band_list_pdf(band, canvas):
    style = TableStyle([('VALIGN', (0, 0), (-1, -1), "TOP"),
                        ('FONT', (0, 0), (-1, 0), "Helvetica-Bold", 14),
                        ('FONT', (0, 1), (-1, 1), "Helvetica", 14),
                        ('ALIGN', (-1, 0), (-1, -1), "RIGHT"),
                        ])
    # split models in 2 columns
    col = 1
    col1 = []
    col2 = []
    for model in band.model_list:
        if col == 1:
            col1.append(create_model_table(model))
            col = 2
        else:
            col2.append(create_model_table(model))
            col = 1
    # create table with header (2 rows) and the 2 columns of models
    data = [[band.name, str(band.total_cost) + "pts"],
            [str(len(band.model_list)) + " models", "Cost of personalities: " + str(band.personalities_cost) + "pts"],
            [col1, col2]]
    table = Table(data, colWidths=9 * cm, rowHeights=[1 * cm, 1.5 * cm, 24 * cm])
    table.setStyle(style)
    # draw table
    table.wrap(18 * cm, 26 * cm)
    table.drawOn(canvas, 1.5 * cm, 2 * cm)
    # pass page
    canvas.showPage()


def create_model_table(model):
    style = [
        ('LINEABOVE', (0, 0), (-1, 0), 0.5, (0, 0, 0)),
        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (0, 1), (1, 1)),
        ('SPAN', (2, 1), (3, 1)),
        ('SPAN', (0, 2), (-1, 2)),
        ('FONT', (0, 0), (-1, 0), "Helvetica-Bold", 12),
        ('FONT', (0, 1), (-1, -1), "Helvetica", 12),
        ('ALIGN', (-1, 0), (-1, 0), "RIGHT")
    ]
    # list of capacities as paragraph
    capa_str = ""
    for capa in model.capacities_list:
        capa_str += capa.name + " ; "
    style_para = getSampleStyleSheet()['Normal']
    style_para.fontSize = 12
    capa_para = Paragraph(capa_str, style_para)
    # first line text
    if model.personality:
        model_str = model.name + " (Personality)"
    else:
        model_str = model.name
    # build table
    data = [[model_str, '', '', str(model.cost)+'pts'],
            ["Quality: " + str(model.quality) + "+", '', "Combat: " + str(model.combat), ''],
            [capa_para, '', '', '']]
    table = Table(data, colWidths=2* cm, spaceAfter=0.5* cm)
    table.setStyle(style)
    return table


def print_model_card(model, canvas, num):
    # print mdl image
    if model.picture is not None:
        pic = Image.open(model.picture)
    else:
        pic = Image.open("elfe.jpg")
    # CASE 1: image must be cut in height
    # resize image to width = 5.4cm
    wpercent = (5.4 * cm / float(pic.size[0]))
    hsize = int((float(pic.size[1]) * float(wpercent)))
    pic = pic.resize((int(5.4 * cm), hsize), PIL.Image.ANTIALIAS)
    # cut image to keep center 3cm height
    pic = pic.crop((0, int((pic.size[1] - int(3*cm))/2), int(5.4 * cm), int((pic.size[1] - int(3*cm))/2) + int(3*cm)))
    pic.save("resized_image.jpg")

    canvas.drawImage("resized_image.jpg", offset_x[num] + pos_mdl_pic[0], offset_y[num] + pos_mdl_pic[1],
                     width=5.4 * cm, height=3 * cm)
    os.remove("resized_image.jpg")
    canvas.drawImage("carte_ex.png", offset_x[num], offset_y[num], width=6.2 * cm, height=8.7 * cm,
                     mask=[250, 255, 250, 255, 250, 255])
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(offset_x[num] + pos_name[0], offset_y[num] + pos_name[1], model.name)
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawString(offset_x[num] + pos_quality[0], offset_y[num] + pos_quality[1], str(model.quality) + '+')
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawString(offset_x[num] + pos_combat[0], offset_y[num] + pos_combat[1], str(model.combat))
    if model.personality:
        canvas.setFont("Helvetica", 10)
        canvas.drawString(offset_x[num] + pos_perso[0], offset_y[num] + pos_perso[1], "Personality")
    canvas.setFont("Helvetica", 10)
    canvas.drawString(offset_x[num] + pos_cost[0], offset_y[num] + pos_cost[1], str(model.cost)+"pts")
    capa_str = ""
    for capa in model.capacities_list:
        capa_str += "<b>" + capa.name + ":</b> " + capa.help + "<br />"
    # build paragraphe & table to align texte to TOP
    styleSheet = getSampleStyleSheet()
    style = styleSheet['BodyText']
    style.fontSize = 8
    style.leading = 9
    p = Paragraph(capa_str, style)
    style.alignment = 4  # justified
    table = Table([[p]], colWidths=5.2*cm, rowHeights=4.32*cm)
    table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), "TOP")]))
    # draw table
    table.wrap(5.2 * cm, 5.9 * cm)
    table.drawOn(canvas, offset_x[num] + pos_capa[0], offset_y[num] + pos_capa[1])



# personal_record = open("data/MyBands", 'rb')
# band_list = pickle.load(personal_record)
# personal_record.close()
# print_pdf_band_list(band_list[0])

