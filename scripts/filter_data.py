import pandas as pd


class FiltretedData:
    def __init__(self,data_no_filtreted):
        self.data_return = data_no_filtreted
        self.data_no_filtreted = data_no_filtreted
    def main(self, need_yup):
        self.rejact_to_excel_tabel(need_yup)
        return self.data_return

    def rejact_to_excel_tabel(self,need_yup):
        self.data_return = {}
        for dse, row_file in self.data_no_filtreted.items():
            for type_file, row_rc in row_file.items():
                val_row = {"dse": dse}
                for rc_pos, row in row_rc.items():
                    rc = {}

                    if type_file == 'data_2012':
                        if not need_yup:
                            if row.get('yup','') == "":
                                rc['УП']=row.get('yup','')
                                rc['Наименование']=row.get('name dse','')
                                nemend_file = row.get('file name', '')
                                if len(nemend_file)>30:
                                    nemend_file=nemend_file[-30:]
                                    nemend_file=nemend_file[nemend_file.index(" ")+1:]
                                rc['Имя изделия']=nemend_file
                                rc['РЦ (2012)']=row.get('rc','')
                            else:
                                continue
                        else:
                            rc['УП'] = row.get('yup', '')
                            rc['Наименование'] = row.get('name dse', '')
                            nemend_file = row.get('file name', '')
                            if len(nemend_file) > 30:
                                nemend_file = nemend_file[-30:]
                                nemend_file = nemend_file[nemend_file.index(" ") + 1:]
                            rc['Имя изделия'] = nemend_file
                            rc['РЦ (2012)'] = row.get('rc', '')
                    if type_file == 'data_cz':
                        rc['РЦ (СЗ)']=row.get('rc','')
                        rc['Дата из письма'] = row.get('date latter','')
                        rc['Инф из письма'] = row.get('info from latter','')
                        rc['Подписано'] = row.get('signed','')
                        rc['Комментарии'] = row.get('coment','')
                    if type_file == 'data_jp':
                        rc['№ЖП'] = row.get('numpe jp','')
                        rc['Дсе ЖП'] = row.get('dse','')
                        rc['Дата создания'] = row.get('data create','')
                        rc['Комментарий'] = row.get('coment','')
                        rc['Дата закрытия'] = row.get('data close','')
                    if type_file == 'data_tool':
                        rc['РЦ(ИНС)'] = row.get('rc','')
                        rc['ID тех.'] = row.get('id tex','')

                    val_row[rc_pos]=rc

                if len(val_row.keys()) > 1:
                    self.data_return[f"{dse}_+_{rc_pos}_+_{type_file}"] = val_row
                # print(val_row)
