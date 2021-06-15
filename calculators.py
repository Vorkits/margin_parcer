class Margin_calculator:
    @staticmethod
    def margin_calculate(price_array,opt_price,kaspi_margin_procent):
        result_margin=[]
        for price in price_array:
            kaspi_margin=(int(price)*kaspi_margin_procent)/100
            margin=int(price)-kaspi_margin-opt_price
            result_margin.append(margin)
        return result_margin