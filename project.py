import sys, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   
sys.path.append(os.path.join(BASE_DIR, "process"))
from clear_data import replace_missing_with_mode, dataframe_to_transactions
from algorithm import closet,charm

# Data: Mushroom
sys.path.append(os.path.join(BASE_DIR, "data","dense", "mushroom"))
#from mushroom import mushroom_dataframe

sys.path.append(os.path.join(BASE_DIR, "data","dense", "connect-4"))
from connect_4 import connect_4_dataframe


# -----------------------------
# Xử lý dữ liệu
# -----------------------------

# 1. Đọc dữ liệu gốc
print("\nBước 1: Đọc dữ liệu")
data_frame = connect_4_dataframe()
print(data_frame.head())
print(data_frame.shape)

# 2. Xử lý dữ liệu
print("\nBước 2: Xử lý dữ liệu")
data_frame = replace_missing_with_mode(data_frame)
print(data_frame.head())
print(data_frame.shape)
data_frame.to_csv("cleaned_data.csv", index=False)

# 3. Mã hóa dữ liệu
print("\nBước 3: Mã hoá dữ liệu")
transactions = dataframe_to_transactions(data_frame)
print(f"Số transaction: {len(transactions)}")
for transaction in transactions[:5]:
    print(", ".join(transaction))

# -----------------------------
# Khai khoáng dữ liệu
# -----------------------------
n_trans:int = len(transactions)
min_support:float = 0.6
min_count:int = int(min_support * n_trans)

# -----------------------------
# CLOSET
# -----------------------------
print("\nBước 4.1: Thuật toán CLOSET")
# closed_closet = closet(transactions, min_count)
# print(f"Số closed itemsets tìm được (CLOSET): {len(closed_closet)}")
# print("5 closed itemsets đầu tiên:")
# for i, (itemset, sup) in enumerate(closed_closet.items()):
#     if i>=5: break
#     print(set(itemset), "support:", sup)

# -----------------------------
# CHARM
# -----------------------------
print("\nBước 4.2: Thuật toán CHARM")
closed_charm = charm(transactions, min_count)
# print(f"Số closed itemsets tìm được (CHARM): {len(closed_charm)}")
# print("5 closed itemsets đầu tiên:")
# for i, (itemset, sup) in enumerate(closed_charm.items()):
#     if i>=5: break
#     print(set(itemset), "support:", sup)
