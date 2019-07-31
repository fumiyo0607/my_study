import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# 重回帰分析を実行
def multiple_regression_analysis(x, y):
    # 定数項を追加
    x = sm.add_constant(x)

    # 最小二乗法によるモデリング
    model = smf.OLS(y,x)
    result = model.fit()

    return result