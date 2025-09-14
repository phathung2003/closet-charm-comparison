import os
import pandas as panda
from typing import List

def parse_names_file(filename: str):
    # Get file directory
    BASE_DIRECTORY:str = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH:str = os.path.join(BASE_DIRECTORY, filename)
    
    mappings = {}
    #"r": Read - Chế độ đọc
    # "w": ghi đè (tạo mới nếu chưa có).
    # "a": ghi nối thêm.
    # "rb": đọc file nhị phân.
    # "r+": vừa đọc vừa ghi.
    with open(FILE_PATH, "r") as data:
        for line in data:
            line = line.strip()
            if not line or ":" not in line:
                continue  # bỏ qua dòng rỗng hoặc không hợp lệ

            # tách phần tên thuộc tính và giá trị
            attr, values = line.split(":", 1)
            attr = attr.strip()

            # loại bỏ số thứ tự nếu có (vd: "1. cap-shape" -> "cap-shape")
            attr = re.sub(r"^\d+\.\s*", "", attr)

            value_map = {}
            # mỗi giá trị có dạng "tên=ký hiệu"
            for v in values.split(","):
                v = v.strip()
                if "=" in v:
                    name, code = v.split("=")
                    name, code = name.strip(), code.strip()
                    value_map[code] = name

            mappings[attr] = value_map
    return mappings

# Xử lý dữ liệu thiếu (Bằng phương pháp Mode - Giá trị xuất hiện nhiều nhất trong cột)
def replace_missing_with_mode(data_frame: panda.DataFrame) -> panda.DataFrame:
    for column in data_frame.columns:
        data_frame[column] = data_frame[column].replace("?", data_frame[column].mode()[0])
    return data_frame

# Mã hoá dữ liệu
def dataframe_to_transactions(data_frame: panda.DataFrame) -> List[List[str]]:
    transactions = []
    for _, row in data_frame.iterrows():
        transactions.append([f"{column}={row[column]}" for column in data_frame.columns])
    return transactions