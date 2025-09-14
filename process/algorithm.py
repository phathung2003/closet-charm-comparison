import tracemalloc
import time
from collections import defaultdict

def closet(transactions, min_count: float):
    # Start Benchmark
    total_transactions:int = len(transactions)
    time_start = time.time()
    tracemalloc.start()

    
    # Tính support cho từng item
    item_counts = defaultdict(int)
    for t in transactions:
        for item in t:
            item_counts[frozenset([item])] += 1

    # frequent single items
    freq_items = {item:count for item, count in item_counts.items() if count >= min_count}
    closed_itemsets = {}

    # candidate generation (very simple, naive)
    candidate_count = 0
    prune_count = 0
    def recursive(prefix, items):
        nonlocal closed_itemsets, candidate_count, prune_count
        n = len(items)
        for i in range(n):
            new_itemset = prefix | items[i]
            # Count support bằng scan transaction
            support = sum(1 for t in transactions if new_itemset.issubset(t))
            candidate_count += 1

            if support >= min_count:
                # Check closure
                is_closed = True
                to_remove = []
                for exist_set, exist_sup in closed_itemsets.items():
                    if exist_set.issuperset(new_itemset) and exist_sup == support:
                        is_closed = False
                        prune_count += 1
                        break
                    if new_itemset.issuperset(exist_set) and exist_sup == support:
                        to_remove.append(exist_set)
                        prune_count += 1
                for s in to_remove:
                    del closed_itemsets[s]

                if is_closed:
                    closed_itemsets[new_itemset] = support

                # Mở rộng tất cả frequent items còn lại (không lọc quá chặt)
                new_items = items[i+1:]
                if new_items:
                    recursive(new_itemset, new_items)
            else:
                prune_count += 1

    recursive(frozenset(), list(freq_items))

    # Chuyển count -> support
    closed_itemsets = {k: v / total_transactions for k, v in closed_itemsets.items()}

    
    # End Benchmark
    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Result
    result =  {
        # Dataset info
        "total_transactions": total_transactions,
        "num_unique_items": len(item_counts),
        "minsup_absolute": min_count,
        "minsup_relative": round(min_count/total_transactions, 4),

        # Kết quả thuật toán
        "closed_itemsets": closed_itemsets,
        "total_closed_itemsets": len(closed_itemsets),
        "total_candidates": candidate_count,
        "total_pruned": prune_count,
        "prune_ratio": round((prune_count/candidate_count)*100, 2) if candidate_count > 0 else 0,

        # Hiệu năng
        "runtime": round(end - time_start, 4),   # giây
        "memory": round(peak / 1024, 2)          # KB
    }
    
    statistic = ({
        # Dataset info
        "   -   Tổng số giao dịch": result["total_transactions"],
        "   -   Tổng số mục duy nhất": result["num_unique_items"],
        "   -   minsup (absolute)": result["minsup_absolute"],
        "   -   minsup (relative)": str(result["minsup_relative"]*100) + " %",
        
        # Kết quả thuật toán
        "   -   Tổng số tập mục đóng": result["total_closed_itemsets"],
        "   -   Tổng số ứng viên": result["total_candidates"],
        "   -   Tổng số bị loại": result["total_pruned"],
        "   -   Tỉ lệ loại bỏ": str(result["prune_ratio"]) + " %",
        
        # Hiệu năng
        "   -   Thời gian": str(result["runtime"]) + " giây",
        "   -   Bộ nhớ tối đa": str(result["memory"]) + " KB",
    })
    for key, value in statistic.items():
        print(f"{key}: {value}")
    
    return result
    # return closed_itemsets
    
def charm(transactions, min_count):
    # Start Benchmark
    total_transactions = len(transactions)
    time_start = time.time()
    tracemalloc.start()

    # Tidset
    item_tidset = defaultdict(set)
    for tid, transaction in enumerate(transactions):
        for item in transaction:
            item_tidset[frozenset([item])].add(tid)
    # Chuyển sang diffset (giao dịch KHÔNG chứa item)
    item_diffset = {
        item: set(range(total_transactions)) - tids
        for item, tids in item_tidset.items()
        if len(tids) >= min_count
    }

    candidate_count = 0
    prune_count = 0
    closed_itemsets = {}

    def recursive(prefix, items):
        nonlocal candidate_count, prune_count, closed_itemsets
        while items:
            item, diffset = items.pop()
            new_prefix = prefix | item
            support = total_transactions - len(diffset)

            # Bỏ qua ứng viên không đủ minsup
            if support < min_count:
                continue

            # === Ứng viên hợp lệ ===
            candidate_count += 1

            # kiểm tra closed
            is_closed = True
            for existing, sup in closed_itemsets.items():
                if existing.issuperset(new_prefix) and sup == support:
                    is_closed = False
                    prune_count += 1   # bị loại do trùng closed
                    break

            if is_closed:
                closed_itemsets[new_prefix] = support

            # mở rộng
            new_items = []
            for other_item, other_diffset in items:
                new_diffset = diffset | other_diffset
                new_support = total_transactions - len(new_diffset)
                if new_support >= min_count:
                    new_items.append((item | other_item, new_diffset))
                # nếu < minsup thì bỏ qua luôn, không tính prune

            if new_items:
                recursive(new_prefix, new_items)

    # bắt đầu đệ quy
    initial_items = list(item_diffset.items())
    recursive(frozenset(), initial_items)

    # End Benchmark
    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    result = {
        # Dataset info
        "total_transactions": total_transactions,
        "num_unique_items": len(item_tidset),
        "minsup_absolute": min_count,
        "minsup_relative": round(min_count / total_transactions, 4),

        # Kết quả thuật toán
        "closed_itemsets": closed_itemsets,
        "total_closed_itemsets": len(closed_itemsets),
        "total_candidates": candidate_count,
        "total_pruned": prune_count,
        "prune_ratio": round((prune_count / candidate_count) * 100, 2) if candidate_count > 0 else 0,

        # Hiệu năng
        "runtime": round(end - time_start, 4),
        "memory": round(peak / 1024, 2),
    }

    for k, v in {
        "   -   Tổng số giao dịch": result["total_transactions"],
        "   -   Tổng số mục duy nhất": result["num_unique_items"],
        "   -   minsup (absolute)": result["minsup_absolute"],
        "   -   minsup (relative)": str(result["minsup_relative"] * 100) + " %",
        "   -   Tổng số tập mục đóng": result["total_closed_itemsets"],
        "   -   Tổng số ứng viên": result["total_candidates"],
        "   -   Tổng số bị loại": result["total_pruned"],
        "   -   Tỉ lệ loại bỏ": str(result["prune_ratio"]) + " %",
        "   -   Thời gian": str(result["runtime"]) + " giây",
        "   -   Bộ nhớ tối đa": str(result["memory"]) + " KB",
    }.items():
        print(f"{k}: {v}")

    return result