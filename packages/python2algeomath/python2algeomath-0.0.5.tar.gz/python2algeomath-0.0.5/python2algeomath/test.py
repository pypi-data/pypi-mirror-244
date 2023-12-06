# 함수따라 다각형 만들어보기

import sympy as sp
import numpy as np  # numpy는 배열관련 강력한 기능을 지원합니다.
from __init__ import AlgeoMathBlock

builder = AlgeoMathBlock()

x, y, c, t = sp.symbols("x y c t")
builder.init_variable(["x", "y", "a", "i", "t"])

# f 함수와 g함수 작성
f = x**2 + 2 * x + 1
g = 2 * x

# 일단 함수 그려보기
builder.add_function_graph("f", sp.latex(f))
builder.add_function_graph("g", sp.latex(g))
# 1부터 2까지 10개로 쪼갬
# n = 10
# x_list = np.linspace(0, 2, n)
# # (x, f(x))와 (x, g(x))를 30개 찍음
# for i, t in enumerate(x_list):
#   builder.add_dot_block(t, f.subs(x, t), f"F{i}")
#   builder.add_dot_block(t, g.subs(x, t), f"G{i}")

a, b, n = (0, 1, 20)

xstep = (b - a) / n
# a이상 b미만, n개로
# 위 방식을 블록 코딩 내의 포문으로 대체해볼까?
builder.start_control_for("t", 0, n, 1)
# function_dot 은 위에서 function을 선어
builder.add_function_dot('"F"+t', f"{a}+t*{xstep}", "f")
builder.add_function_dot('"G"+t', f"{a}+t*{xstep}", "g")
builder.end_control_for()

# 이들을 모두 이은 다각형 생성
# 순서대로 이을 목록 생성
polygon_list = []

# F0, F1, ... F29추가
for i in range(n + 1):
    polygon_list.append(f"F{i}")
# G29, G28, ... G1, G0 추가
for i in range(n + 1):
    polygon_list.append(f"G{n-i}")
# 쉼표로 구분되는 문자열로 변환
polygonStr = ",".join(polygon_list)

# 다각형 생성
builder.execute_set('"FuncPoly"', f'"Polygon({polygonStr})"')

# 점 과 그 이름 모두 감추기
builder.hide_point()


xml_string = builder.to_xml_string()
print(xml_string.decode())
