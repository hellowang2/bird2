import tkinter as tk
from tkinter import ttk
from itertools import product

#經驗之談與個人猜測
# 假設基因型是用簡單的表示方式，如 'R/R', 'R/b' 等
head_phenotype_to_genotype = {
    "紅頭": ["R/R", "R/r"],
    "橘頭": ["R/Ry", "R/r^y", "Ry/r^y"],
    "黑頭": ["b/b"],
    "鮭魚色": ["R/b", "Ry/b"]  # 假設是由藍背壓制紅頭或橘頭導致的
}

back_phenotype_to_genotype = {
    "綠背": ["G/G", "G/b", "G/Y"],
    "黃色背部": ["G/Y", "Y/Y"],
    "藍背": ["b/b"],
    "天空藍": ["b/Y"]  # 假設天空藍是由藍背加上黃色基因影響
}

chest_phenotype_to_genotype = {
    "紫胸": ["P/P", "P/w"],
    "白胸": ["w/w"]
}

# 定義基因型到表現型的映射（包括相互作用）
def interpret_head_genotype(genotype, back_phenotype):
    """
    根據頭部基因型和背部表現型確定頭部表現型
    """
    if 'R' in genotype:
        if 'Ry' in genotype or 'r^y' in genotype:
            head = "橘頭"
        else:
            head = "紅頭"
    elif 'Ry' in genotype or 'r^y' in genotype:
        head = "橘頭"
    elif genotype == 'b/b':
        head = "黑頭"
    else:
        head = "黑頭"

    # 考慮背部基因的互作
    if back_phenotype == "藍背":
        if head in ["紅頭", "橘頭"]:
            head = "鮭魚色"
    elif back_phenotype == "黃背":
        if head == "黑頭":
            head = "黃頭"

    return head

def interpret_back_genotype(genotype):
    """
    根據背部基因型確定背部表現型
    """
    if 'G' in genotype:
        if 'Y' in genotype:
            return "黃背"
        else:
            return "綠背"
    elif 'Y' in genotype:
        return "黃背"
    elif genotype == 'b/b':
        return "藍背"
    elif 'b/Y' in genotype or 'Y/b' in genotype:
        return "天空藍"
    else:
        return "綠背"

def interpret_chest_genotype(genotype):
    """
    根據胸部基因型確定胸部表現型
    """
    if 'P' in genotype:
        return "紫胸"
    elif genotype == 'w/w':
        return "白胸"
    else:
        return "未知胸部顏色" #原則上應該是個淡紫

# 根據表現型推斷可能的基因型
def get_possible_genotypes(phenotype, trait):
    if trait == 'head':
        return head_phenotype_to_genotype.get(phenotype, [])
    elif trait == 'back':
        return back_phenotype_to_genotype.get(phenotype, [])
    elif trait == 'chest':
        return chest_phenotype_to_genotype.get(phenotype, [])
    else:
        return []

# 計算所有可能的子代顏色
def calculate_offspring(parent1, parent2):
    offspring_results = []

    # 推斷父母的可能基因型
    parent1_head_genotypes = get_possible_genotypes(parent1['head'], 'head')
    parent1_back_genotypes = get_possible_genotypes(parent1['back'], 'back')
    parent1_chest_genotypes = get_possible_genotypes(parent1['chest'], 'chest')

    parent2_head_genotypes = get_possible_genotypes(parent2['head'], 'head')
    parent2_back_genotypes = get_possible_genotypes(parent2['back'], 'back')
    parent2_chest_genotypes = get_possible_genotypes(parent2['chest'], 'chest')

    # 生成所有可能的父母基因型組合
    for p1_head, p1_back, p1_chest in product(parent1_head_genotypes, parent1_back_genotypes, parent1_chest_genotypes):
        for p2_head, p2_back, p2_chest in product(parent2_head_genotypes, parent2_back_genotypes, parent2_chest_genotypes):
            # 進行基因交叉
            # 頭部基因交叉
            child_head_genotypes = []
            for allele1 in p1_head.split('/'):
                for allele2 in p2_head.split('/'):
                    child_genotype = '/'.join(sorted([allele1, allele2]))
                    child_head_genotypes.append(child_genotype)

            # 背部基因交叉
            child_back_genotypes = []
            for allele1 in p1_back.split('/'):
                for allele2 in p2_back.split('/'):
                    child_genotype = '/'.join(sorted([allele1, allele2]))
                    child_back_genotypes.append(child_genotype)

            # 胸部基因交叉
            child_chest_genotypes = []
            for allele1 in p1_chest.split('/'):
                for allele2 in p2_chest.split('/'):
                    child_genotype = '/'.join(sorted([allele1, allele2]))
                    child_chest_genotypes.append(child_genotype)

            # 確定子代表現型
            for ch_head in child_head_genotypes:
                for ch_back in child_back_genotypes:
                    for ch_chest in child_chest_genotypes:
                        # 解釋背部表現型
                        back_phenotype = interpret_back_genotype(ch_back)
                        # 解釋頭部表現型，考慮背部互作
                        head_phenotype = interpret_head_genotype(ch_head, back_phenotype)
                        # 解釋胸部表現型
                        chest_phenotype = interpret_chest_genotype(ch_chest)

                        # 添加到結果中
                        offspring_results.append({
                            'head': head_phenotype,
                            'back': back_phenotype,
                            'chest': chest_phenotype
                        })

    # 移除重複的結果
    unique_offspring = []
    seen = set()
    for bird in offspring_results:
        key = (bird['head'], bird['back'], bird['chest'])
        if key not in seen:
            seen.add(key)
            unique_offspring.append(bird)

    return unique_offspring

# GUI
def create_gui():
    def calculate():
        parent1 = {
            'head': male_head_var.get(),
            'back': male_back_var.get(),
            'chest': male_chest_var.get()
        }
        parent2 = {
            'head': female_head_var.get(),
            'back': female_back_var.get(),
            'chest': female_chest_var.get()
        }

        offspring = calculate_offspring(parent1, parent2)

        result_text.delete(1.0, tk.END)
        for bird in offspring:
            result_text.insert(tk.END, f"子代顏色：頭部 - {bird['head']}，背部 - {bird['back']}，胸部 - {bird['chest']}\n")

    # 建立主視窗
    root = tk.Tk()
    root.title("胡錦鳥基因計算器")

    # 父鳥選項
    ttk.Label(root, text="父鳥外觀特徵：").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    male_frame = ttk.LabelFrame(root, text="父鳥 (雄性)")
    male_frame.grid(row=0, column=1, padx=10, pady=5)

    # 父鳥頭部顏色
    ttk.Label(male_frame, text="頭部顏色:").grid(row=0, column=0, sticky='w')
    male_head_var = tk.StringVar()
    male_head_combo = ttk.Combobox(male_frame, textvariable=male_head_var, values=[
        "紅頭", "橘頭", "黑頭", "鮭魚色"
    ], state="readonly")
    male_head_combo.grid(row=0, column=1, padx=5, pady=2)
    male_head_combo.current(0)

    # 父鳥背部顏色
    ttk.Label(male_frame, text="背部顏色:").grid(row=1, column=0, sticky='w')
    male_back_var = tk.StringVar()
    male_back_combo = ttk.Combobox(male_frame, textvariable=male_back_var, values=[
        "綠背", "黃背", "藍背", "天空藍"
    ], state="readonly")
    male_back_combo.grid(row=1, column=1, padx=5, pady=2)
    male_back_combo.current(0)

    # 父鳥胸部顏色
    ttk.Label(male_frame, text="胸部顏色:").grid(row=2, column=0, sticky='w')
    male_chest_var = tk.StringVar()
    male_chest_combo = ttk.Combobox(male_frame, textvariable=male_chest_var, values=[
        "紫胸", "白胸"
    ], state="readonly")
    male_chest_combo.grid(row=2, column=1, padx=5, pady=2)
    male_chest_combo.current(0)

    # 母鳥選項
    ttk.Label(root, text="母鳥外觀特徵：").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    female_frame = ttk.LabelFrame(root, text="母鳥 (雌性)")
    female_frame.grid(row=1, column=1, padx=10, pady=5)

    # 母鳥頭部顏色
    ttk.Label(female_frame, text="頭部顏色:").grid(row=0, column=0, sticky='w')
    female_head_var = tk.StringVar()
    female_head_combo = ttk.Combobox(female_frame, textvariable=female_head_var, values=[
        "紅頭", "橘頭", "黑頭", "鮭魚色"
    ], state="readonly")
    female_head_combo.grid(row=0, column=1, padx=5, pady=2)
    female_head_combo.current(0)

    # 母鳥背部顏色
    ttk.Label(female_frame, text="背部顏色:").grid(row=1, column=0, sticky='w')
    female_back_var = tk.StringVar()
    female_back_combo = ttk.Combobox(female_frame, textvariable=female_back_var, values=[
        "綠背", "黃背", "藍背", "天空藍"
    ], state="readonly")
    female_back_combo.grid(row=1, column=1, padx=5, pady=2)
    female_back_combo.current(0)

    # 母鳥胸部顏色
    ttk.Label(female_frame, text="胸部顏色:").grid(row=2, column=0, sticky='w')
    female_chest_var = tk.StringVar()
    female_chest_combo = ttk.Combobox(female_frame, textvariable=female_chest_var, values=[
        "紫胸", "白胸"
    ], state="readonly")
    female_chest_combo.grid(row=2, column=1, padx=5, pady=2)
    female_chest_combo.current(0)

    # 計算按鈕
    calculate_button = ttk.Button(root, text="計算子代顏色", command=calculate)
    calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    # 顯示結果的文字框
    result_text = tk.Text(root, height=20, width=80)
    result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

# 啟動 GUI
create_gui()

