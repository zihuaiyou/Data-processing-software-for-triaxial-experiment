import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from plot_UI_2 import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math

path = None
s_name = 'Sheet1'
path_name = '000'


class Myplot(QMainWindow, Ui_MainWindow, QDialog):
    def __init__(self):
        super(Myplot, self).__init__()
        self.setupUi(self)

    def open_file(self):
        global path
        global path_name
        file = QFileDialog.getOpenFileName(self, '打开文件', ".", '工作表(*.xlsx)')
        if file[0]:
            path = file[0]
            path_name = os.path.basename(path)[0:-5]

    def input_data(self):
        global diameter, length, confiningpressure, s_name, lengthre, lc, p1, l2

        if self.lineEdit2.text() and self.lineEdit3.text() and self.lineEdit4.text() and \
                self.lineEdit5.text() and self.lineEdit6.text() and self.lineEdit7.text() and self.lineEdit8.text():
            diameter = float(self.lineEdit2.text())
            length = float(self.lineEdit3.text())
            confiningpressure = float(self.lineEdit4.text())
            lengthre = float(self.lineEdit5.text())
            lc = float(self.lineEdit6.text())
            p1 = float(self.lineEdit7.text())
            l2 = float(self.lineEdit8.text())
        else:
            QMessageBox.warning(self, '警告', '您的数据未完整输入！',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if self.lineEdit1.text():
            s_name = self.lineEdit1.text()
        else:
            pass

    def save_file(self):
        fig_path = os.getcwd()
        path_1 = path_name + '.png'
        file_name = os.path.join(fig_path, path_1)
        if os.path.isfile(file_name):
            with open(file_name, mode='rb') as r:
                content = r.read()
            file = QFileDialog.getSaveFileName(self, '另存为', ".", '图像文件(*.png *.jpg)')
            if file[0]:
                with open(file[0], mode='wb') as f:
                    f.write(content)
        else:
            QMessageBox.warning(self, '警告', '请按提示操作',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def help(self):
        # QMessageBox.about(self, '帮助', '闪退可能是工作表标签名输错，\n或者是数据表格式有误')
        dialog = QDialog()
        dialog.setWindowTitle('帮助')
        dialog.setGeometry(400, 400, 400, 250)
        textlabel = QLabel(dialog)
        textlabel.move(20, 20)
        textlabel.setFont(QFont('黑体', 10))
        textlabel.setText('闪退可能是工作表标签名输错\n或者是数据表格式有误\n数据表标准格式请参照附表格式示范')
        dialog.exec()

    def plot(self):
        if path and self.lineEdit2.text() and self.lineEdit3.text() and self.lineEdit4.text() and \
                self.lineEdit5.text() and self.lineEdit6.text() and self.lineEdit7.text() and self.lineEdit8.text():
            # 绘图时可以显示中文
            jiao = lc / (diameter + 1)
            xishu = 3.14151926 / (math.sin(jiao) - jiao * math.cos(jiao))  # 试样前后周长变化
            # 绘图时可以显示中文
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            pd.set_option('display.unicode.ambiguous_as_wide', True)
            pd.set_option('display.unicode.east_asian_width', True)
            # 导出Excel数据最大行数
            pd.set_option('display.max_columns', 100)
            pd.set_option('display.max_rows', None)
            pd.set_option('max_colwidth', 180)
            pd.set_option('display.width', 1000)
            # 读取路径
            xlsx_path = path
            # 读取不同列数据
            df1 = pd.read_excel(xlsx_path, sheet_name='3-11-2', usecols=[2])
            df2 = pd.read_excel(xlsx_path, sheet_name='3-11-2', usecols=[4])
            df3 = pd.read_excel(xlsx_path, sheet_name='3-11-2', usecols=[5])

            # 导出数据为列表
            def excel_one_line_to_list(df):
                df_li = df.values.tolist()
                result = []
                for s_li in df_li:
                    result.append(s_li[0])
                return result


            a = excel_one_line_to_list(df1)
            b = excel_one_line_to_list(df2)
            c = excel_one_line_to_list(df3)
            # 对列表数据进行计算
            stress = [((i * 1000) / (((diameter) * (diameter) * 3.1415926) / 4)) for i in a]  # 列表内数据计算
            d = [((i / p1) * l2) for i in stress]
            h = list(map(lambda x: x[0] - x[1], zip(b, d)))  # 列表间相互计算
            # 变量列表赋值
            stran1 = [i / length for i in h]
            stran2 = [(i / ((3.1415926 / xishu) * (diameter + lengthre))) for i in c]
            e = [(i * 2) for i in stran2]
            y = stress
            x = stran1
            f = [-i for i in stran2]
            x1 = f
            g = list(map(lambda x: x[0] - x[1], zip(stran1, e)))
            x2 = g
            # 绘图
            plt.plot(x, y)
            plt.plot(x1, y)
            plt.plot(x2, y)
            # x y轴标签
            plt.xlabel(r'ε/%')
            plt.ylabel(r'σ1-σ3/MPa')
            # 调整x y轴位置
            ax = plt.gca()
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            ax.spines['bottom'].set_position(('data', 0))
            ax.spines['left'].set_position(('data', 0))
            ax.patch.set_facecolor('None')
            p = max(y)
            j = p / 2  # 求峰值抗压强度半值
            # 查询stress列表中最接近最大值半值所在位置
            k = [abs(i - j) for i in y]
            l = k.index(min(k))
            # 找到拟合直线用的点
            m = y[l - 10:l + 10]  # stress中拟合直线点
            n = x[l - 10:l + 10]  # stran1中拟合直线点
            o = x1[l - 10:l + 10]  # stran2中拟合直线点
            # 拟合求斜率
            kb1 = np.polyfit(n, m, 1)
            E1 = format(kb1[0])  # 轴向应力应变曲线的斜率
            E1 = float(E1)  # 将数据由字符串变为浮点数
            kb2 = np.polyfit(o, m, 1)
            E2 = format(kb2[0])  # 径向应力应变曲线的斜率
            E2 = float(E2)
            # 求弹性模量
            q = E1 / 1000
            # 求泊松比
            r = (-E1 / E2)
            content_1 = '弹性模量为：%.4f GPa' % q
            content_2 = '泊松比为： %.6f' % r
            content_3 = '峰值抗压强度σ1-σ3是：%.3f MPa' % p
            content_4 = '峰值抗压强度σ1是: %.3f MPa' % (p + confiningpressure)
            self.textEdit.setPlainText(content_1 + '\n' + content_2 + '\n' + content_3 + '\n' + content_4)
            plt.savefig(path_name + '.png')
            plt.show()  # 输出图像

        elif path:
            QMessageBox.warning(self, '警告', '您的数据未完整输入！',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        elif self.lineEdit2.text() and self.lineEdit3.text() and self.lineEdit4.text():
            QMessageBox.warning(self, '警告', '请确认您的数据文件路径',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        else:
            QMessageBox.warning(self, '警告', '请按提示操作',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Myplot()
    main.show()
    sys.exit(app.exec_())
