import xhtml2pdf.pisa as pisa
import os
import cStringIO

html_model_template = """
    <div id="card">
        <table>
            <col width="31"><col width="325"><col width="26">
            <td colspan="3" style="font-size:20px">&nbsp;</td>
            <tr><td></td>
                <td style="font-size:24px"><b>{}</b></td>
            <td></td></tr>
        </table>
        <table>
            <col width="310"><col width="50"><col width="25">
            <td colspan="3" style="font-size:8px">&nbsp;</td>
            <tr><td></td>
                <td style="font-size:36px"><b>{}+</b></td>
            <td></td></tr>
        </table>
        <table>
            <col width="319"><col width="50"><col width="15">
            <td colspan="3" style="font-size:16px">&nbsp;</td>
            <tr><td></td>
                <td style="font-size:40px"><b>{}</b></td>
            <td></td></tr>
        </table>
        <table>
            <col width="31"><col width="250"><col width="75"><col width="26">
            <td colspan="4" style="font-size:12px">&nbsp;</td>
            <tr><td></td>
                <td style="font-size:16px"><b><i>{}</i></b></td>
                <td style="font-size:16px;text-align: right"><b><i>{} pts</i></b></td>
            <td></td><td></td></tr>
        </table>

        <table>
            <col width="36"><col width="320"><col width="16">
            <td colspan="3" style="font-size:4px">&nbsp;</td>
            <tr><td></td><td style="font-size:14px">
                {}
            </td><td></td></tr>
        </table>
    </div>
"""

html_header = """
<!DOCTYPE html>

<html>
    <head>
    </head>
    
    <style type="text/css">
    #card
    {
        width: 402px;
        height: 560px;
        background: url(carte_ex.png)
    }
    </style>
    
    <body style="font-family:'Verdana'">
"""

footer_str = """
    </body>
</html>
"""


def print_band_cards(band):
    # header: band
    header_str = html_header
    # models on 2 columns
    model_str = ""
    already_printed = []
    for model in band.model_list:
        model_to_print = True
        for model_printed in already_printed:
            if model.name == model_printed.name and model.cost == model_printed.cost and model.quality == model_printed.quality and model.combat == model_printed.combat and model.personality == model_printed.personality:
                model_to_print = False
        if model_to_print:
                # print model
                already_printed.append(model)
                model_str += print_model_card(model)

    # assembly all html str
    html_str = header_str + model_str + footer_str
    html_file = "SoBH_" + band.name + "_cards.html"
    pdf_file = "SoBH_" + band.name + "_cards.pdf"
    # protect against overwriting
    ind = 1
    while os.path.exists(html_file):
        html_file = "SoBH_" + band.name + "_" + str(ind) + "_cards.html"
        pdf_file = "SoBH_" + band.name + "_" + str(ind) + "_cards.pdf"
        ind += 1
    # write html file
    f = open(html_file, 'w')
    f.write(html_str)
    f.close()


def print_model_card(mdl):
    capa_str = ""
    for capa in mdl.capacities_list:
        capa_str += "<b>" + capa.name + ": </b>"
        capa_str += capa.help + "<br />"
    if mdl.personality:
        perso_str = "Personality"
    else:
        perso_str = ""
    html_model = html_model_template.format(mdl.name, mdl.quality, mdl.combat, perso_str, mdl.cost, capa_str)
    return html_model


