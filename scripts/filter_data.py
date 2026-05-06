
class FiltretedData:
    def __init__(self,data_no_filtreted):
        self.data_return = data_no_filtreted
        self.data_no_filtreted = data_no_filtreted
    def main(self):
        self.rejact_to_excel_tabel()
        return self.data_return

    def rejact_to_excel_tabel(self):
        self.data_return = {}
        for dse, row_file in self.data_no_filtreted.items():
            for type_file, row_rc in row_file.items():
                val_row = {"dse": dse}
                for rc_pos, row in row_rc.items():
                    rc = {}
                    if type_file == 'data_2012':
                        rc['Уп']=row.get('yup','')
                        rc['Наименование']=row.get('name dse','')
                        nemend_file =  row.get('file name','')[-30:]
                        nemend_file=nemend_file[nemend_file.index(" ")+1:]
                        rc['Имя изделия']=nemend_file
                        rc['Рц']=row.get('rc','')
                    if type_file == 'data_cz':
                        rc['Рц из Сз']=row.get('rc','')
                        rc['Дата из письма'] = row.get('date latter','')
                        rc['Инф из письма'] = row.get('info from latter','')
                        rc['Подписано'] = row.get('signed','')
                        rc['Комментарии'] = row.get('coment','')
                    if type_file == 'data_jp':
                        rc['№Жп'] = row.get('numpe jp','')
                        rc['Дсе ЖП'] = row.get('dse','')
                        rc['Дата создания'] = row.get('data create','')
                        rc['Комментарий'] = row.get('coment','')
                        rc['data close'] = row.get('Датат закрытия','')
                    val_row[rc_pos]=rc

                self.data_return[f"{dse}_+_{rc_pos}_+_{type_file}"] = val_row
