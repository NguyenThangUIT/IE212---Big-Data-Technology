import sys
import csv

# Định nghĩa mapper
def mapper():
    reader = csv.reader(sys.stdin)
    for row in reader:
        ticker, name, exchange = row
        if exchange == 'NYSE':
            print("{0}\t{1}\t{2}".format(ticker, name, exchange))

# Hàm main để chạy mapper với dữ liệu từ file stock_info.csv
if __name__ == "__main__": 
    with open('stock_info.csv', 'r') as f:
        sys.stdin = f
        mapper()

