import os
import csv
import subprocess

# Chạy mapper_01.py và lấy output từ stdout và stderr của process
process = subprocess.Popen(['python', 'mapper_01.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

# Decode stdout từ bytes sang string
mapper_output = stdout.decode('utf-8')

# Lấy danh sách các file trong thư mục Stocks
stock_files = os.listdir('Stocks')

# Lấy danh sách các ticker từ output của mapper_01.py
tickers = []
reader = csv.reader(mapper_output.splitlines(), delimiter='\t')  # Dùng tab delimiter để match với output của mapper
for row in reader:
    if len(row) == 3:  # Điều kiện mỗi dòng trong file csv có đúng 3 thuộc tính
        ticker, name, exchange = row
        tickers.append(ticker.strip().lower())  # Thêm ticker vào danh sách

# Tìm các file trong thư mục Stocks mà tên file (không kèm đuôi .us.txt) trùng với ticker
matching_files = [file for file in stock_files if file.replace('.us.txt', '').strip().lower() in tickers]

# Hàm kiểm tra xem giá mở phiên của file có lớn hơn giá đóng phiên không
def is_open_higher_than_close(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            return False
        first_row = rows[0]
        last_row = rows[-1]
        return float(first_row['Open']) > float(last_row['Close'])

# Kiểm tra xem giá mở phiên của các file trong matching_files có lớn hơn giá đóng phiên không
matching_tickers = []
matching_names = []
for file in matching_files:
    full_path = os.path.join('Stocks', file)  # Đường dẫn đầy đủ của file
    if is_open_higher_than_close(full_path):
        ticker = file.replace('.us.txt', '').strip().upper()
        matching_tickers.append(ticker)
        # Tìm tên của ticker trong output của mapper_01.py
        reader = csv.reader(mapper_output.splitlines(), delimiter='\t')  # Dùng tab delimiter để match với output của mapper
        for row in reader:
            if len(row) == 3 and row[0].strip().upper() == ticker:  # Điều kiện mỗi dòng có đúng 3 thuộc tính
                matching_names.append(row[1])
                break

# Lấy danh sách các ticker và tên đã sắp xếp
sorted_results = sorted(zip(matching_tickers, matching_names))

# In kết quả
for ticker, name in sorted_results:
    print("{0}: {1}".format(ticker, name))

