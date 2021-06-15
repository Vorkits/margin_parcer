import xlsxwriter


class Xlsx_write:
    table_colums=['Имя','Оптовая цена','Каспи id','kaspi name','Маржа 1','Маржа 2','Маржа 3','Маржа 4','Маржа 5']
    def write_table(self,table_name,table_data):
        """[summary]

        Args:
            table_name ([type]): [description]
            table_data {'product_name':{product_data}}
        """
        workbook = xlsxwriter.Workbook(f'{table_name}.xlsx')
        worksheet = workbook.add_worksheet()
        for i,col in enumerate(self.table_colums):
            worksheet.write(0,i,col)
        row = 1
        for product_name in table_data:
            product_data=table_data[product_name]
            
            print(product_data['name'],product_data['price'],product_data['id'],product_data['margin'])
            worksheet.write(row,0,product_data['name'])
            worksheet.write(row,1,product_data['price'])
            worksheet.write(row,2,product_data['id'])
            worksheet.write(row,3,product_data['kaspi_name'])
            for i,margin in enumerate(product_data['margin']):
                worksheet.write(row,i+4,margin)
            row+=1
        workbook.close()