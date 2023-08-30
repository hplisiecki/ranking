import pandas as pd
import os
import PyPDF2
import os

failed_path = r'D:\data\ranking\pdfs\failed_pdf'
save_path = r'D:\data\ranking\pdfs'
links_path = r'D:\data\ranking\publication_links'
new_links = r'D:\PycharmProjects\ranking\data\publications\orcid\export_to_automated'

unis = ['SWPS_Uniwersytet_Humanistycznospołeczny_z_siedzibą_w_Warszawie.csv', 'Akademia_Ignatianum_w_Krakowie.csv', 'Instytut_Psychologii_Polskiej_Akademii_Nauk.csv',
          'Akademia_Pedagogiki_Specjalnej_Marii_Grzegorzewskiej_w_Warszawie.csv', 'Uniwersytet_Adama_Mickiewicza_w_Poznaniu.csv', 'Katolicki_Uniwersytet_Lubelski_Jana_Pawła_II_w_Lublinie.csv',
          'Uniwersytet_Gdański.csv', 'Uniwersytet_Jagielloński_w_Krakowie.csv', 'Uniwersytet_Jana_Kochanowskiego_w_Kielcach.csv', 'Uniwersytet_Kardynała_Stefana_Wyszyńskiego_w_Warszawie.csv',
          'Uniwersytet_Kazimierza_Wielkiego_w_Bydgoszczy.csv', 'Uniwersytet_Marii_Curie-Skłodowskiej_w_Lublinie.csv', 'Uniwersytet_Pedagogiczny_Komisji_Edukacji_Narodowej_w_Krakowie.csv',
          'Uniwersytet_Szczeciński.csv', 'Uniwersytet_Warszawski.csv', 'Uniwersytet_Wrocławski.csv', 'Uniwersytet_Łódzki.csv', 'Uniwersytet_Śląski_w_Katowicach.csv',
        'Wyższa_Szkoła_Ekonomii_i_Innowacji_w_Lublinie.csv', 'Wyższa_Szkoła_Bankowa_w_Toruniu.csv', 'Uniwersytet_Opolski.csv', 'Uniwersytet_Mikołaja_Kopernika_w_Toruniu.csv',
        'Akademia_Ekonomiczno-Humanistyczna_w_Warszawie.csv']

for uni in unis:
    # load links
    links = pd.read_csv(os.path.join(links_path, uni))
    new_links = pd.read_csv(os.path.join(new_links, uni))

    new_links = new_links[['link', 'title', 'id']]

    links = links.merge(new_links, on='id', how='outer')
    break

