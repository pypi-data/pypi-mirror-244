

* #### 这是一个粗糙集的计算包，其中包含了知识约简的功能。
* This is a rough set computation package that includes knowledge reduction.
* #### 知识约简也相当简单，只要调用RoughSets.cores就可以看到哪些类别是可以约简的。
* Knowledge approximation is also fairly simple, just call RoughSets.cores to see which categories are approximable.
* #### RoughSets.KnowledgeReduction()函数输入相应参数就可以查看多个类别是否可以同时约简。其中将要检查的非核类别用list或者np.array包裹起来放入Cn参数即可同时该函数也支持单独一个类别是否可以约简的检查，返回True就是可以约简，返回False就是不能约简。
* The RoughSets.KnowledgeReduction() function can be used to see if multiple categories can be reduced at the same time by entering the appropriate parameters. Which will check the non-core categories with list or np.array wrapped up into the Cn parameter can be at the same time the function also supports a separate category can be simplified check, return True is can be simplified, return False is can not be simplified.
* #### 以下是代码示例

项目的CSDN ：https://blog.csdn.net/weixin_43069769/article/details/133958276

```python
import pandas as pd
from RoughSets import RoughSets
import numpy as np

table = pd.DataFrame(
    data = np.matrix(
        [
            [1,"晴",	"热","高","无风","N"],
            [2, '晴', '热', '高', '有风', 'N'],
            [3, '多云', '热', '高', '无风', 'P'],
            [4, '雨', '适中', '高', '无风', 'P'],
            [5, '雨', '冷', '正常', '无风', 'P'],
            [6, '雨', '冷', '正常', '有风', 'N'],
            [7, '多云', '冷', '正常', '有风', 'P'],
            [8, '晴', '适中', '高', '无风', 'N'],
            [9, '晴', '冷', '正常', '无风', 'P'],
            [10, '雨', '适中', '正常', '无风', 'P'],
            [11, '晴', '适中', '正常', '有风', 'P'],
            [12, '多云', '适中', '高', '有风', 'P'],
            [13, '多云', '热', '正常', '无风', 'P'],
            [14, '雨', '适中', '高', '有风', 'N']
      
        ]
    )
    ,columns = ["No.","天气","气温","湿度","风","类别"]
)

RS = RoughSets(table)
print(RS.Uij)

print(RS.VaRange(RS.U,RS.R))

print("U:",RS.U)
print(RS.f(a=['天气','气温'],x=["1","2"],R=RS.R,U=RS.U))

print(RS.IND(A=['气温','天气'],R=RS.R,U=RS.U,out_dataframe=True))

print(RS.IND(A=["湿度"],R=RS.R,U=RS.U,out_dataframe=True))

print(RS.isIND(A=["天气","气温"],X=["1","2"],R=RS.R,U=RS.U,out_dataframe=True))

X_case = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12','13','14']
print(f"X:\n{X_case}")
A=["天气","气温"]
print(f"A:\n{A}")
print(RS.lower_approximation(U=RS.U,X=X_case,R=RS.R,A=A,out_dataframe=True))

X_case =  ["1","2","3","4"]
print(f"X:\n{X_case}")
A=["天气","气温"]
print(f"A:\n{A}")
print(RS.upper_approximation(U=RS.U,X=X_case,R=RS.R,A=A,out_dataframe=True))

X_case =  np.ravel(RS.U[:,:1])
print(f"X:\n{X_case}")
A=["天气","气温","湿度"]
print(f"A:\n{A}")
print(RS.Pos_A(U=RS.U,X=X_case,R=RS.R,A=A,out_dataframe=True))

X_case =  ["1","2","3","4"]
print(f"X:\n{X_case}")
A=["天气","气温"]
print(f"A:\n{A}")
print(RS.NEG_A(U=RS.U,X=X_case,R=RS.R,A=A,out_dataframe=True))


X_case =  ["1","2","3","4"]
print(f"X:\n{X_case}")
A=["天气","气温"]
print(f"A:\n{A}")
print(RS.BND_A(U=RS.U,X=X_case,R=RS.R,A=A,out_dataframe=True))


X_case =  ['4', '10', '14']
print(f"X:\n{X_case}")
A=["天气","气温"]
print(f"A:\n{A}") 
print(f"isRoughSet 返回 是否是粗糙集 ：{RS.isRoughSet(U=RS.U,X=X_case,R=RS.R,A=A,out_dataframe=bool)}")
print(f"isRoughSet 返回 字典数据 ：{RS.isRoughSet(U=RS.U,X=X_case,R=RS.R,A=A,out_dataframe=False)}")
print(RS.isRoughSet(U=RS.U,X=X_case,R=RS.R,A=A,out_dataframe=True))
  

X_case =  ["1","2","3","4"]
print(f"X:\n{X_case}")
A=["天气","气温"]
print(f"A:\n{A}")
print(RS.Score(U=RS.U,X=X_case,R=RS.R,A=A,out_dataframe=True))
  
  
A = ["天气"]
B = ["天气"]
print(RS.isRed(U=RS.U,R=RS.R,B=B,A=A))

D = ["类别"]  
print(RS.Pos_C(U=RS.U,R=RS.R,D=D,C=RS.C))

D = ["类别"]  
print(RS.Core(U=RS.U,R=RS.R,C=RS.C,D=D,out_dataframe=True))

D = ["类别"]   
Cn = ["气温","湿度"]
print(f"是否可以同时删除{Cn}:{RS.KnowledgeReduction(U=RS.U,R=RS.R,C=RS.C,D=D,Cn=Cn)}")

print(RS.cores)

Cn = ["天气","湿度"]#np.array(RS.cores['属性名'])[np.array(RS.cores['是否可省略'])]
D=[RS.R[-1]]
print(RS.KnowledgeReduction(D=D,Cn=Cn,U=RS.U,R=RS.R,C=RS.C))
```
