import os
import csv
import subprocess
from datetime import datetime

# Chạy mapper_02.py và lấy output từ stdout và stderr của process
process = subprocess.Popen(['python', 'mapper_02.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

# Decode stdout từ bytes sang string
mapper_output = stdout.decode('utf-8')

# Lấy danh sách các file trong thư mục Stocks
stock_files = os.listdir('Stocks')

# Lấy danh sách các ticker từ output của mapper_02.py
tickers = []
reader = csv.reader(mapper_output.splitlines(), delimiter='\t')  # Dùng tab delimiter để match với output của mapper
for row in reader:
    if len(row) == 3:  # Điều kiện mỗi dòng trong file csv có đúng 3 thuộc tính
        ticker, name, exchange = row
        tickers.append(ticker.strip().lower())  # Thêm ticker vào danh sách

# Tìm các file trong thư mục Stocks mà tên file (không kèm đuôi .us.txt) trùng với ticker
matching_files = [file for file in stock_files if file.replace('.us.txt', '').strip().lower() in tickers]

# Hàm kiểm tra xem có công ty nào mở cổ phiếu trong tháng 1 và tháng 2 năm 2005 không
def opened_stock_in_jan_feb_2005(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = datetime.strptime(row['Date'], '%Y-%m-%d')
            if date.year == 2005 and (date.month == 1 or date.month == 2):
                return True
    return False

# Khởi tạo danh sách các công ty mở cổ phiếu trong tháng 1 và tháng 2 năm 2005
companies_opened_in_jan_feb_2005 = []

# Kiểm tra xem có công ty nào mở cổ phiếu trong tháng 1 và tháng 2 năm 2005 không
for file in matching_files:
    full_path = os.path.join('Stocks', file)
    if opened_stock_in_jan_feb_2005(full_path):
        ticker = file.replace('.us.txt', '').strip().upper()
        # Tìm tên của ticker trong output của mapper_02.py
        reader = csv.reader(mapper_output.splitlines(), delimiter='\t')  # Dùng tab delimiter để match với output của mapper
        for row in reader:
            if len(row) == 3 and row[0].strip().upper() == ticker:  # Điều kiện mỗi dòng có đúng 3 thuộc tính
                companies_opened_in_jan_feb_2005.append((ticker, row[1]))
                break

# Sắp xếp danh sách các công ty mở cổ phiếu trong tháng 1 và tháng 2 năm 2005
sorted_companies = sorted(companies_opened_in_jan_feb_2005)

# In kết quả
for ticker, name in sorted_companies:
    print("{0}: {1}".format(ticker, name))
