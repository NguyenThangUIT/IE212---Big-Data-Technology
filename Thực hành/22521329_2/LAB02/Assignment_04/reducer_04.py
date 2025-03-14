import os
import csv
import subprocess
from datetime import datetime

# Chạy mapper_04.py và lấy output từ stdout và stderr của process
process = subprocess.Popen(['python', 'mapper_04.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

# Decode stdout từ bytes sang string
mapper_output = stdout.decode('utf-8')

# Lấy danh sách các file trong thư mục Stocks
stock_files = os.listdir('Stocks')

# Lấy danh sách các ticker từ output của mapper_04.py
tickers = []
reader = csv.reader(mapper_output.splitlines(), delimiter='\t')  # Dùng tab delimiter để match với output của mapper
for row in reader:
    if len(row) == 3:  # Điều kiện mỗi dòng trong file csv có đúng 3 thuộc tính
        ticker, name, exchange = row
        tickers.append(ticker.strip().lower())  # Thêm ticker vào danh sách

# Tìm các file trong thư mục Stocks mà tên file (không kèm đuôi .us.txt) trùng với ticker
matching_files = [file for file in stock_files if file.replace('.us.txt', '').strip().lower() in tickers]

# Hàm tính lợi nhuận từ việc mua cổ phiếu vào ngày 20/10/2005 và bán vào ngày 25/10/2005
def calculate_profit(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        open_price = None
        high_price = None
        for row in reader:
            date = datetime.strptime(row['Date'], '%Y-%m-%d')
            if date == datetime(2005, 10, 20):
                open_price = float(row['Open'])
            if date == datetime(2005, 10, 25):
                high_price = float(row['High'])
        if open_price is not None and high_price is not None:
            return high_price - open_price
    return None

# Khởi tạo danh sách các công ty có lợi nhuận
profitable_companies = []

# Kiểm tra các file trong matching_files có lợi nhuận không
for file in matching_files:
    full_path = os.path.join('Stocks', file)
    profit = calculate_profit(full_path)
    if profit is not None and profit > 0:
        ticker = file.replace('.us.txt', '').strip().upper()
        # Tìm tên của ticker trong output của mapper_04.py
        reader = csv.reader(mapper_output.splitlines(), delimiter='\t')  # Dùng tab delimiter để match với output của mapper
        for row in reader:
            if len(row) == 3 and row[0].strip().upper() == ticker:  # Điều kiện mỗi dòng có đúng 3 thuộc tính
                profitable_companies.append((row[1], profit))
                break

# Sắp xếp danh sách các công ty có lợi nhuận
sorted_companies = sorted(profitable_companies)

# In kết quả
for name, profit in sorted_companies:
    print("{0}: {1:.2f}".format(name, profit))
