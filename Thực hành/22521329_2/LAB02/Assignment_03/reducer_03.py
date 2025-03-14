import os
import csv
import subprocess
from datetime import datetime

# Chạy mapper_03.py và lấy output từ stdout và stderr của process
process = subprocess.Popen(['python', 'mapper_03.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

# Decode stdout từ bytes sang string
mapper_output = stdout.decode('utf-8')

# Lấy danh sách các file trong thư mục Stocks
stock_files = os.listdir('Stocks')

# Lấy danh sách các ticker từ output của mapper_03.py
tickers = []
reader = csv.reader(mapper_output.splitlines(), delimiter='\t')  # Dùng tab delimiter để match với output của mapper
for row in reader:
    if len(row) == 3:  # Điều kiện mỗi dòng trong file csv có đúng 3 thuộc tính
        ticker, name, exchange = row
        tickers.append(ticker.strip().lower())  # Thêm ticker vào danh sách

# Tìm các file trong thư mục Stocks mà tên file (không kèm đuôi .us.txt) trùng với ticker
matching_files = [file for file in stock_files if file.replace('.us.txt', '').strip().lower() in tickers]

# Hàm lấy giá mở cửa của phiên đầu tháng 7 và giá đóng cửa của phiên cuối tháng 8 năm 2007
def get_prices(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        july_open = None
        august_close = None
        for row in reader:
            date = datetime.strptime(row['Date'], '%Y-%m-%d')
            if date.year == 2007:
                if date.month == 7 and july_open is None:
                    july_open = float(row['Open'])
                if date.month == 8:
                    august_close = float(row['Close'])
        return july_open, august_close

# Khởi tạo danh sách các công ty có phiên đóng tháng 8 thấp hơn phiên mở tháng 7 năm 2007
companies_with_decrease = []

# Kiểm tra xem có công ty nào có giá phiên đóng tháng 8 thấp hơn giá phiên mở tháng 7 năm 2007 không
for file in matching_files:
    full_path = os.path.join('Stocks', file)
    july_open, august_close = get_prices(full_path)
    if july_open is not None and august_close is not None and august_close < july_open:
        ticker = file.replace('.us.txt', '').strip().upper()
        # Tìm tên của ticker trong output của mapper_03.py
        reader = csv.reader(mapper_output.splitlines(), delimiter='\t')  # Dùng tab delimiter để match với output của mapper
        for row in reader:
            if len(row) == 3 and row[0].strip().upper() == ticker:  # Điều kiện mỗi dòng có đúng 3 thuộc tính
                companies_with_decrease.append((ticker, row[1]))
                break

# Sắp xếp danh sách các công ty có giá phiên đóng tháng 8 thấp hơn giá phiên mở tháng 7 năm 2007
sorted_companies = sorted(companies_with_decrease)

# In kết quả
for ticker, name in sorted_companies:
    print("{0}: {1}".format(ticker, name))