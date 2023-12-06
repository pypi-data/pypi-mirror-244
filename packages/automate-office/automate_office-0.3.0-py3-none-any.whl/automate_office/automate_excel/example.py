import pathlib
import datetime

import numpy as np
import pandas as pd

from automate_office.automate_excel.excel_funcs import *


def get_border_style(cur_row_idx, cur_col_idx,row_idx_range=(1, 100), col_idx_range=(1, 100), border_color="00FF6238"):
    left_style, right_style, top_style, bottom_style = ["dashed"] * 4
    if cur_row_idx == row_idx_range[0]:
        top_style = "thin"
    if cur_row_idx == row_idx_range[1]:
        bottom_style = "thin"
    if cur_col_idx == col_idx_range[0]:
        left_style = "thin"
    if cur_col_idx == col_idx_range[1]:
        right_style = "thin"
    return create_border_style(right_style=right_style, left_style=left_style, bottom_style=bottom_style, top_style=top_style, color=border_color)


def get_number_format(cur_row_idx, cur_col_idx):
    if cur_row_idx == 1:
        return "General"
    
    if cur_col_idx == 2:
        return "0.00%"
    elif cur_col_idx == 3:
        return "#,##0.00;[红色]-#,##0.00"
    elif cur_col_idx == 4:
        # 中文在自适应列宽的时候似乎总会短一截
        return 'yyyy"年"m"月"d"日"'
    else:
        return "General"
    

if __name__ == "__main__":  
    file_path = pathlib.Path.home().joinpath("Downloads/format.xlsx")
    sheet_name = "Format"

    df = pd.DataFrame(
        {
            "col1": list("abcdefg"),
            "col2": np.random.random(size=(7, )),
            "col3": np.random.randint(low=-1e5, high=1e5, size=(7, )),
            "col4": pd.date_range(start=datetime.datetime(2023, 12, 1).date(), end=datetime.datetime(2023, 12, 7).date())
        }
    )
    df.to_excel(file_path, index=False, sheet_name=sheet_name)
    n_rows, n_cols = df.shape[0] + 1, df.shape[1]

    # 格式化
    wb = open_excel(filename=file_path)
    ws = wb[sheet_name]

    alignment = creaete_alignment_style(horizontal="center", vertical="center")
    title_font = create_font_style(font_name="微软雅黑", font_size=16, font_color="00FFFFFF", bold=True)
    content_font = create_font_style(font_name="微软雅黑", font_size=12, font_color="00000000")
    title_fill = create_fill_style(fill_type="solid", start_color="00FF6238")

    # 遍历单元格设置格式
    for row_cells in ws.iter_rows():
        for cur_cell in row_cells:
            if cur_cell.row == 1:
                cur_cell.font = title_font
                cur_cell.fill = title_fill
            else:
                cur_cell.font = content_font

            cur_cell.alignment = alignment
            cur_cell.border = get_border_style(col_idx_range=(1, n_cols), row_idx_range=(1, n_rows), cur_col_idx=cur_cell.column, cur_row_idx=cur_cell.row)
            cur_cell.number_format = get_number_format(cur_col_idx=cur_cell.column, cur_row_idx=cur_cell.row)

    # 自适应列宽
    get_autojust_col_width(ws, n_cols)

    wb.save(file_path)
