import xhtml2pdf.pisa as pisa
import os
import cStringIO

html_model_template = """
<tr>
    <td colspan="2"><b>{}</b></td>
    <td style="text-align: right">{} pts</td>
</tr>
<tr>
    <td>Quality: {}+</td>
    <td>Combat: {}</td>
    <td></td>
</tr>
<tr>
    <td colspan="3">{}</td>
</tr>
<tr><td colspan="3" style="border-bottom: solid 1px black;font-size:4px">&nbsp;</td></tr>
<tr><td colspan="3" style="font-size:2px">&nbsp;</td></tr>
"""

html_band_header = """
<!DOCTYPE html>

<html>
    <head>
    </head>

    <body style="font-family:'Verdana'">
    
        <table>
            <col width="20">
            <col width="400">
            <col width="280">
            <col width="20">
            <tr>
                <td></td>
                <td><b>{}</b></td>
                <td style="text-align: right"><b>{} pts</b></td>
                <td></td>
            </tr>
            <tr>
                <td></td>
                <td>{} models</td>
                <td style="text-align: right">Cost of personalities: {} pts</td>
                <td></td>
            </tr>
            <tr><td colspan="4"></td></tr>
        </table>

        <table cellspacing="20">
            <col width="300">
            <col width="40">
            <col width="300">
            <tr><td valign="top">
            <table>
                <col width="120">
                <col width="100">
                <col width="80">
"""

footer_str = """
            </table>
            </td></tr>
        </table>
    </body>
</html>
"""

col_separator = """
</table>
</td>

<td></td>

<td valign="top">
<table>
    <col width="120">
    <col width="120">
    <col width="60">
"""


def print_band_list(band):
    # header: band
    header_str = html_band_header.format(band.name, band.total_cost, len(band.model_list), band.personalities_cost)
    # models on 2 columns
    model_col1 = ""
    model_col2 = ""
    col_ind = 1
    for model in band.model_list:
        if col_ind == 1:
            model_col1 += print_model(model)
            col_ind = 2
        else:
            model_col2 += print_model(model)
            col_ind = 1
    model_str = model_col1 + col_separator + model_col2
    # assembly all html str
    html_str = header_str + model_str + footer_str
    html_file = "SoBH_" + band.name + ".html"
    pdf_file = "SoBH_" + band.name + ".pdf"
    # protect against overwriting
    ind = 1
    while os.path.exists(html_file):
        html_file = "SoBH_" + band.name + "_" + str(ind) + ".html"
        pdf_file = "SoBH_" + band.name + "_" + str(ind) + ".pdf"
        ind += 1
    # write html file
    f = open(html_file, 'w')
    f.write(html_str)
    f.close()
    # print pdf
    pdf = pisa.CreatePDF(
        cStringIO.StringIO(html_str),
        file(pdf_file, "wb"))


def print_model(mdl):
    if mdl.personality:
        name_str = mdl.name + " (P)"
    else:
        name_str = mdl.name
    capa_str = ""
    for capa in mdl.capacities_list:
        capa_str += capa.name
        capa_str += " ; "
    html_model = html_model_template.format(name_str, mdl.cost, mdl.quality, mdl.combat, capa_str)
    return html_model


