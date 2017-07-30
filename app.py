# coding=utf-8
import authentication.account_interface as ai
import global_var as gv
import stock.stock_interface as si

if __name__ == '__main__':
    si.init()
    ai.init()
    gv.run()
