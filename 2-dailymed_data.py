import re
import time
import pandas as pd
import requests
import os
from lxml import etree
from datetime import datetime
from orderedset import OrderedSet
import argparse

parser = argparse.ArgumentParser(description='Download data')

parser.add_argument('--SPL-path', '-s', required=True, type=str,
    help='SPL data path.')
parser.add_argument('--URL', '-u', required=True, type=str,
    help='DailyMed URL.')

args = parser.parse_args()

DAILYMED_SPL = args.SPL_path
DAILYMED_SPL_URL = args.URL
DAILYMED_ORIGIN = 'dm_spl_zip_files_meta_data.txt'
DAILYMED_RAW = 'dailymed_raw.csv'
DAILYMED_ERROR = 'dailymed_error.csv'
DAILYMED_SPL_ERROR = 'dailymed_spl_error.csv'
DAILYMED_REMAP = 'dailymed_remap.csv'

namespaces = {"v": "urn:hl7-org:v3"}


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def printbold(string):
    print(''.join(style.BOLD + '\n' + string + style.END))


class SPL:
    def __init__(self, xmlString):
        p = etree.XMLParser(huge_tree=True)
        self.xml = etree.fromstring(xmlString, p)

    @property
    def Drug_Name(self):
        try:
            name = self.xml.xpath("//v:manufacturedProduct/v:manufacturedProduct/v:name"
                                  "| //v:manufacturedProduct/v:manufacturedMedicine/v:name", namespaces=namespaces)

            return name[0].text.replace("\t", "").replace("\n", "")
        except:
            return ""

    @property
    def NDCs(self):
        try:
            ndcs = self.xml.xpath("//v:manufacturedProduct/v:manufacturedProduct/v:code/@code"
                                  "| //v:manufacturedProduct/v:manufacturedMedicine/v:code/@code",
                                  namespaces=namespaces)
            return ndcs
        except:
            return ""

    @property
    def Effective_Date(self):
        try:
            date = self.xml.xpath("//v:effectiveTime/@value", namespaces=namespaces)
            date[0] = date[0][0:8]
            date = datetime.strptime(date[0], '%Y%m%d')
            return date
        except:
            return ""

    @property
    def Box_Warning(self):  # "ENTRESTO":box_warning repeated!!!
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34066-1']/..//v:title"
                                                      "| //v:code[@code='34066-1']/..//v:paragraph"
                                                      "| //v:code[@code='34066-1']/..//v:item",
                                                      namespaces=namespaces))
            excerpt_section_paragraphs = (self.xml.xpath("//v:code[@code='34066-1']/..//v:excerpt//v:title"
                                                         " | //v:code[@code='34066-1']/..//v:excerpt//v:paragraph"
                                                         " | //v:code[@code='34066-1']/..//v:excerpt//v:item",
                                                         namespaces=namespaces))
            note_section_paragraphs = filter(lambda x: x not in excerpt_section_paragraphs, note_section_paragraphs)
            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""


    # 	INDICATIONS & USAGE SECTION - 34067-9

    @property
    def Indication(self):  # TODO: much to do for short summary
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34067-9']/..//v:title" 
                                                      " | //v:code[@code='34067-9']""/..//v:paragraph"
                                                      " | //v:code[@code='34067-9']/..//v:item",
                                                      namespaces=namespaces))
            excerpt_section_paragraphs = (self.xml.xpath("//v:code[@code='34067-9']/..//v:excerpt//v:title" 
                                                         " | //v:code[@code='34067-9']/..//v:excerpt//v:paragraph"
                                                         " | //v:code[@code='34067-9']/..//v:excerpt//v:item",
                                                         namespaces=namespaces))
            note_section_paragraphs = filter(lambda x: x not in excerpt_section_paragraphs, note_section_paragraphs)

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # INFORMATION FOR PATIENTS SECTION - 34076-0
    @property
    def Information_for_Patients(self):  # why 'Route of Administration'?
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34076-0']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            """ for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))
            """

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # Dosage and Administration with Dosing Regimen
    ## DOSAGE & ADMINISTRATION SECTION

    @property
    def Dosage_Administration(self):  # TODO: subtitles in BOLD

        """
        note_section_paragraphs = (self.xml.xpath("//v:code[@code='34068-7']" "/following-sibling::v:paragraph[1]",
            namespaces=namespaces))
        """
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34068-7']/..//v:title"
                                                      "| //v:code[@code='34068-7']/..//v:paragraph"
                                                      "| //v:code[@code='34068-7']/..//v:item",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # MECHANISM OF ACTION SECTION  - 43679-0
    @property
    def Mechanism_of_Action(self):
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='43679-0']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # PHARMACODYNAMICS SECTION - 43681-6
    @property
    def Pharmacodynamics(self):
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='43681-6']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # DRUG PRODUCT & SAFETY INFORMATION
    # PREGNANCY SECTION - 42228-7

    @property
    def Pregnancy(self):  # It's called "Pregnancy"
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='42228-7']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    @property
    def Teratogenic_Effects(self):  # NEED "Animal Findings"?
        try:
            note_section_paragraphs = (
                self.xml.xpath("//v:code[@code='34077-8']/..//v:paragraph | //v:code[@code='34077-8']/..//v:item",
                               namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    @property
    def Nonteratogenic_Effects(self):
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34078-6']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    @property
    def Lactation(self):
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='77290-5']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # How about LACTATION SECTION (77290-5)?
    @property
    def Nursing_Mothers(self):  # NURSING MOTHERS SECTION
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34080-2']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            # OrderedSet library is used to remove any duplicate selected text while maintaining text order.
            # This may be able to be replaced by just using a standard dict. With something like
            # ' '.join(list(dict.fromkeys(text)))
            # but this has not been tested.

            return ' '.join(OrderedSet(text))
        except:
            return ""

    # FEMALES & MALES OF REPRODUCTIVE POTENTIAL SECTION 77291 - 3
    @property
    def Females_Males_of_Reproductive_Potential(self):
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='77291-3']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # PHARMACOKINETICS SECTION - 43682-4
    @property
    def Pharmacokinetics(self):  # TODO: how to assign each paragraph?
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='43682-4']/..//v:title"
                                                      "| //v:code[@code='43682-4']/..//v:paragraph"
                                                      "| //v:code[@code='43682-4']/..//v:item",
                                                      namespaces=namespaces))

            table_section_paragraphs = (self.xml.xpath("//v:code[@code='43682-4']/..//v:table//v:title"
                                                       "| //v:code[@code='43682-4']/..//v:table//v:paragraph"
                                                       "| //v:code[@code='43682-4']/..//v:table//v:item",
                                                       namespaces=namespaces))
            note_section_paragraphs = filter(lambda x: x not in table_section_paragraphs, note_section_paragraphs)

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    @property
    def Pharmacokinetics_Table(self):
        try:
            table_section_paragraphs = (self.xml.xpath("//v:code[@code='43682-4']/..//v:table",
                                                       namespaces=namespaces))

            text = list()
            for paragraph in table_section_paragraphs:
                table_string = ''.join(paragraph.xpath(".//v:caption/text()", namespaces=namespaces)).strip()
                table_string += '<table>'
                for row in paragraph.xpath(".//v:tr", namespaces=namespaces):
                    table_string += '<tr>'
                    for col in row.xpath(".//v:th", namespaces=namespaces):
                        table_string += '<td><b>{}</b></td>'.format(' '.join(col.xpath('.//text()')).strip())
                    for col in row.xpath(".//v:td", namespaces=namespaces):
                        colspan = col.get('colspan')
                        rowspan = col.get('rowspan')
                        if colspan or rowspan:
                            table_string += '<td colspan={} rowspan={}>{}</td>'.format(colspan, rowspan, ' '.join(col.xpath('.//text()')).strip())
                        else:
                            table_string += '<td>{}</td>'.format(' '.join(col.xpath('.//text()')))
                    table_string += '</tr>'
                table_string += '</table>'
                text.append(table_string)

            return '\n\n'.join(text)
        except:
            return ""

    # CARCINOGENESIS & MUTAGENESIS & IMPAIRMENT OF FERTILITY SECTION - 34083-6
    @property
    def Carcinogenesis(self):
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34083-6']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""


    # HOW SUPPLIED SECTION - 34069 - 5
    @property
    def How_Supplied(self):
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34069-5']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    @property
    def Appl_No(self):
        try:
            Appl_no = list(set(self.xml.xpath("//v:approval/v:id/@extension", namespaces=namespaces)))
            return ' '.join(OrderedSet(Appl_no))
        except:
            return ""

def data_collection():
    dm_metadata_df = pd.read_csv(DAILYMED_ORIGIN, delimiter='|', dtype=str)
    raw_df = pd.DataFrame(columns=['SETID', 'SPL'])
    error_df = pd.DataFrame(columns=['SETID'])
    for index, row in dm_metadata_df.iterrows():
        try:
            r = requests.get(url=DAILYMED_SPL_URL + row.SETID + '.xml')
            raw_df = raw_df.append({
                'SETID': row.SETID,
                'SPL': r.content
            }, ignore_index=True)
        except:
            print("cannot get SPL for SETID %s." % row.SETID)
            error_df = error_df.append({'SETID': row.SETID}, ignore_index=True)
            continue

        if (index + 1) % 100 == 0:
            raw_df.to_csv(DAILYMED_RAW, index=False)
            error_df.to_csv(DAILYMED_ERROR, index=False)
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S."),
                  '{} completed: {} success, {} failed. (Total progress: {:.4f})'.format(str(index + 1),
                         str(len(raw_df)), str(len(error_df)),(index + 1)/len(dm_metadata_df)))



    print('Total {} completed: {} success, {} failed.'.format(str(len(dm_metadata_df)), str(len(raw_df)),
                                                             str(len(error_df))))
    return raw_df, error_df


def spl_parse(raw_df):
    df = pd.DataFrame(columns=['Appl_No', 'SETID', 'Drug_Name', 'Effective_Date', 'Pharmacokinetics',
        'Pharmacokinetics_Table', 'Box_Warning', 'NDCs', 'Indication', 'Information_for_Patients',
        'Dosage_Administration', 'Mechanism_of_Action', 'Pregnancy', 'Teratogenic_Effects',
        'Nonteratogenic_Effects', 'Lactation', 'Nursing_Mothers', 'Females_Males_of_Reproductive_Potential',
        'Carcinogenesis', 'How_Supplied'])
    error_df = pd.DataFrame(columns=['SETID'])
    for i, row in raw_df.iterrows():
        if re.search(r'<document.+</document>', row.SPL):
            try:
                spl_string = re.search(r'<document.+</document>', row.SPL).group()
                spl_string = re.sub('\\\\n', '', spl_string)
                spl = SPL(spl_string)
                df = df.append({
                    'Appl_No': spl.Appl_No,
                    'SETID': row.SETID,
                    'Drug_Name': spl.Drug_Name,
                    'Effective_Date': str(spl.Effective_Date),
                    'Pharmacokinetics': spl.Pharmacokinetics,
                    'Pharmacokinetics_Table': spl.Pharmacokinetics_Table,
                    'Box_Warning': spl.Box_Warning,
                    'NDCs': spl.NDCs,
                    'Indication': spl.Indication,
                    'Information_for_Patients': spl.Information_for_Patients,
                    'Dosage_Administration': spl.Dosage_Administration,
                    'Mechanism_of_Action': spl.Mechanism_of_Action,
                    'Pregnancy': spl.Pregnancy,
                    'Teratogenic_Effects': spl.Teratogenic_Effects,
                    'Nonteratogenic_Effects': spl.Nonteratogenic_Effects,
                    'Lactation': spl.Lactation,
                    'Nursing_Mothers': spl.Nursing_Mothers,
                    'Females_Males_of_Reproductive_Potential': spl.Females_Males_of_Reproductive_Potential,
                    'Carcinogenesis': spl.Carcinogenesis,
                    'How_Supplied': spl.How_Supplied,
                }, ignore_index=True)
            except:
                error_df = error_df.append({'SETID': row.SETID}, ignore_index=True)
                continue
        else:
            error_df = error_df.append({'SETID': row.SETID}, ignore_index=True)
        if (i + 1) % 5000 == 0:
            print('{} completed: {} success, {} failed'.format(str(i + 1), str(len(df)), str(len(error_df))))

    print('Total {} completed: {} success, {} failed'.format(str(len(raw_df)), str(len(df)), str(len(error_df))))
    return df, error_df


def identifier_remap(raw_df):
    new_row_count = 0
    new_row_df = pd.DataFrame()
    raw_df['Effective_Date'] = pd.to_datetime(raw_df['Effective_Date']).dt.date
    remap_df = raw_df.copy()
    for index, row in remap_df.iterrows():
        if not pd.isna(row.FDA_Application_Number):
            fda_appl_no_list = row['FDA_Application_Number'].split(' ')
            if len(fda_appl_no_list) > 1:
                new_row_count += len(fda_appl_no_list) - 1
                remap_df.at[index, 'FDA_Application_Number'] = fda_appl_no_list[0]
                for i in range(1, len(fda_appl_no_list)):
                    new_row = row
                    new_row['FDA_Application_Number'] = fda_appl_no_list[i]
                    new_row_df = new_row_df.append(new_row)
    remap_df = remap_df.append(new_row_df)
    return remap_df


def remove_duplicate(remap_df):
    no_appl_num_df = remap_df[pd.isna(remap_df['FDA_Application_Number'])].copy()
    remap_df = remap_df[~pd.isna(remap_df['FDA_Application_Number'])]

    nda_pattern = r'^ANDA|^NDA'
    nda_filter = remap_df['FDA_Application_Number'].str.match(nda_pattern)

    nda_df = remap_df[nda_filter].copy()
    nda_df = nda_df \
        .sort_values(['FDA_Application_Number', 'Effective_Date'], ascending=(True, False)) \
        .reset_index(drop=True)
    nda_df = nda_df \
        .drop_duplicates(subset=['FDA_Application_Number'], keep='first') \
        .reset_index(drop=True)

    non_nda_df = remap_df[~nda_filter].copy()
    non_nda_df = non_nda_df \
        .sort_values(['FDA_Application_Number', 'Effective_Date'], ascending=(True, False)) \
        .reset_index(drop=True)
    non_nda_df = non_nda_df \
        .drop_duplicates(subset=['FDA_Application_Number'], keep='first') \
        .reset_index(drop=True)
    non_nda_df = non_nda_df.append(no_appl_num_df)

    return nda_df, non_nda_df

start_time = time.time()
print('Step 1 of 4: Data collection (take 7-12 hours depending on computer and internet connections)')
dailymed_raw_df, dailymed_error_df = data_collection()
dailymed_error_df.to_csv(DAILYMED_ERROR, index=False)
dailymed_raw_df.to_csv(DAILYMED_RAW, index=False)
step1_time = time.time()
hours, rem = divmod(step1_time - start_time, 3600)
minutes, seconds = divmod(rem, 60)
print("Step 1 used {:0>2}:{:0>2}:{:05.2f}\n".format(int(hours), int(minutes), seconds))

dailymed_raw_df = pd.read_csv(DAILYMED_RAW, dtype=str)
print('Step 2 of 4: Parse SPL')
dailymed_spl_df, dailymed_error_spl_df = spl_parse(dailymed_raw_df)
dailymed_spl_df.to_csv(DAILYMED_SPL, index=False)
dailymed_error_spl_df.to_csv(DAILYMED_SPL_ERROR, index=False)
step2_time = time.time()
hours, rem = divmod(step2_time - step1_time, 3600)
minutes, seconds = divmod(rem, 60)
print("Step 2 used {:0>2}:{:0>2}:{:05.2f}\n".format(int(hours), int(minutes), seconds))

dailymed_spl_df = pd.read_csv(DAILYMED_SPL, dtype=str)
print('Step 3 of 4: Unify identifier')
dailymed_remap_df = identifier_remap(dailymed_spl_df)
dailymed_remap_df.to_csv(DAILYMED_REMAP, index=False)
print('Unify identifier: {} records'.format(str(len(dailymed_remap_df))))
step3_time = time.time()
hours, rem = divmod(step3_time - step2_time, 3600)
minutes, seconds = divmod(rem, 60)
print("Step 3 used {:0>2}:{:0>2}:{:05.2f}\n".format(int(hours), int(minutes), seconds))

step3_time = time.time()
dailymed_remap_df = pd.read_csv(DAILYMED_REMAP, dtype=str)
print('Step 4 of 4: Filter NDA/ANDA Drug')
dailymed_nda_df, dailymed_non_nda_df = remove_duplicate(dailymed_remap_df)
print('NDA/ANDA Drug: {} records'.format(str(len(dailymed_nda_df))))
step4_time = time.time()
hours, rem = divmod(step4_time - step3_time, 3600)
minutes, seconds = divmod(rem, 60)
print("Step 4 used {:0>2}:{:0>2}:{:05.2f}\n".format(int(hours), int(minutes), seconds))
dailymed_nda_df.to_csv('dailymed_nda_df.csv', index=False)
