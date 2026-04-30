
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

                    if type_file == 'data_2012':
                        val_row['Уп']=row.get('yup','')
                        val_row['Наименование']=row.get('name dse','')
                        nemend_file =  row.get('file name','')[-30:]
                        nemend_file=nemend_file[nemend_file.index(" ")+1:]
                        val_row['Имя изделия']=nemend_file
                        val_row['Рц']=row.get('rc','')
                    if type_file == 'data_cz':
                        val_row['Рц из Сз']=row.get('rc','')
                        val_row['Дата из письма'] = row.get('date latter','')
                        val_row['Инф из письма'] = row.get('info from latter','')
                        val_row['Подписано'] = row.get('signed','')
                    if type_file == 'data_jp':
                        val_row['№Жп'] = row.get('numpe jp','')
                        val_row['Дсе ЖП'] = row.get('dse','')
                        val_row['Дата создания'] = row.get('data create','')
                        val_row['data close'] = row.get('Датат закрытия','')

                self.data_return[f"{dse}_+_{rc_pos}_+_{type_file}"] = val_row
