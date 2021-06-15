from math import prod
from excel_parcer_old import Xlsx_parser
from kaspi_parser import Kaspi_parser
from calculators import Margin_calculator
from excel_writer import Xlsx_write
from multiprocessing import Process, Manager, managers
from threading import Thread

from dict_divide import linch_dict_divider

class App_view:
    """
    [summary]
    
    1.get excel table
    
    result=[]
    for product in table
        result[product]={price_margins=[]}
        prices=parce_kaspi_product(product)
        for price in prices:
            price_margins.append(calculate_margin(price,initial_price))
    
    
    3. создать новую таблицу
            
            
    
    """
    def _kaspi_processing(self,product_table,result_table,kaspi_margin):
        print('call _kaspi_processing')
        for product_name in product_table:
            try:
                print('before parsing')
                product_data=product_table[product_name]
                opt_price=product_data['opt_price']
                
                kaspi_product_data=Kaspi_parser().parce_product(False,name=product_name,price=opt_price)
                # print(kaspi_product_data)
                print('after parsing')

                margin_calculation=Margin_calculator.margin_calculate(kaspi_product_data['prices'],opt_price,kaspi_margin)
                # print(margin_calculation)
                
                kaspi_product_data['margin']=margin_calculation
                
                result_table[product_name]=kaspi_product_data
            except Exception as e:
                print(e)
        print(result_table)
        Kaspi_parser().close_driver()
    
    def _get_excel_table(self,path,name_col,opt_col ):
        Table_parcer=Xlsx_parser()
        Table_parcer.ucenka_cols={'name':int(name_col),'opt_price':int(opt_col)}
        return Table_parcer.get_ucenka_table(path)
    
    def _write_result_table(self,table_name,table_data):
        Xlsx_write().write_table(table_name,table_data)
    
    
    def start_app(self,table_path,kaspi_margin,name_col,opt_col,process_count=4):
        product_table=(self._get_excel_table(table_path,name_col,opt_col))
        # print(product_table)
        

        manager=Manager()
        result_table=manager.dict()
        product_table_list=linch_dict_divider(product_table,process_count)
       
        # self._kaspi_processing(product_table,result_table,kaspi_margin)
        process_list=[]
        for i in range(process_count):
            process=Process(target=self._kaspi_processing, args=(product_table_list[i],result_table,kaspi_margin))
            process_list.append(process)
            process.start()
        for process in process_list:
            print(process)
            process.join()
            
        self._write_result_table('margin_result',result_table)
        
    
if __name__=='__main__':
    pass
    App_view().start_app('margin.xlsx',11,0,1)