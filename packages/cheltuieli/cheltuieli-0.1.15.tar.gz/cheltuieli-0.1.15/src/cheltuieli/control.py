import chelt_plan
import masina
import salariu_prime
from mysqlquerys import connect, mysql_rm
from datetime import date
import time


def get_cheltuieli(ini_file, selectedStartDate, selectedEndDate):
    app = chelt_plan.CheltuieliPlanificate(ini_file)
    app.prepareTablePlan('all', selectedStartDate, selectedEndDate)
    for i in app.expenses:
        print(i)


def get_income(ini_file, selectedStartDate, selectedEndDate):
    income = chelt_plan.Income(ini_file)
    income.prepareTablePlan('all', selectedStartDate, selectedEndDate)
    # for i in income.income:
    #     print(i)
    # print(income.tableHead)
    # print('brutto', brutto)
    # print('taxes', taxes)
    # print('netto', netto)
    # print('abzuge', abzuge)
    # print('uberweisung', uberweisung)

    print(20*'#')
    # table, brutto, taxes, netto, abzuge, uberweisung = income.get_salary_income('February')
    # for i in table:
    #     print(i)
    # print('brutto', brutto)
    # print('taxes', taxes)
    # print('netto', netto)
    # print('abzuge', abzuge)
    # print('uberweisung', uberweisung)
    # print(20*'#')
    # table, brutto, taxes, netto, abzuge, uberweisung = income.get_total_monthly_income('February')
    # for i in table:
    #     print(i)
    # print('brutto', brutto)
    # print('taxes', taxes)
    # print('netto', netto)
    # print('abzuge', abzuge)
    # print('uberweisung', uberweisung)
    # print(20*'#')


def main():
    script_start_time = time.time()
    selectedStartDate = date(2023, 1, 1)
    selectedEndDate = date(2023, 1, 31)

    income_ini = r"D:\Python\MySQL\cheltuieli_db.ini"

    # get_cheltuieli(income_ini, selectedStartDate, selectedEndDate)
    get_income(income_ini, selectedStartDate, selectedEndDate)


    scrip_end_time = time.time()
    duration = scrip_end_time - script_start_time
    duration = time.strftime("%H:%M:%S", time.gmtime(duration))
    print('run time: {}'.format(duration))

if __name__ == '__main__':
    main()
