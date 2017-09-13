import sys
import re
from PyQt5 import QtCore, QtWidgets
from gui import Ui_Form


Ui_MainWindow = Ui_Form


def alignment(str1, space, align = 'left'):
    length = len(str1.encode('gb2312'))
    space = space - length if space >= length else 0
    if align == 'left':
        str1 = str1 + ' ' * space
    elif align == 'right':
        str1 = ' ' * space + str1
    elif align == 'center':
        str1 = ' ' * (space // 2) + str1 + ' ' * (space - space // 2)
    return str1

class MyApp(QtWidgets.QDialog, Ui_MainWindow):
    # 这里的第一个变量是你该窗口的类型，第二个是该窗口对象。
    def __init__(self):
        # 创建主界面对象
        QtWidgets.QDialog.__init__(self)
        # 主界面对象初始化
        Ui_MainWindow.__init__(self)
        # 配置主界面对象
        self.setupUi(self)
        # 设置最小、最大化按钮
        self.setWindowFlags(QtCore.Qt.Window)
        # 文件选择并显示相应内容
        self.start_pushButton.clicked.connect(self.file_choice)
        # 提取三天预报并显示内容
        self.end_pushButton.clicked.connect(self.draw_datas)
        # 保存文件
        self.save_pushButton.clicked.connect(self.save_datas)

    def file_choice(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self,"open file dialog", '', "Txt files(*.txt)")
        self.filename_lineEdit.setText(file[0])
        with open("{}".format(file[0]), 'r') as f:
            datas = f.readlines()
            self.start_textEdit.setText(''.join(datas))

    def draw_datas(self):
        filename = self.filename_lineEdit.text()
        endData = []
        rep = re.compile("\s|、")
        with open("{}".format(filename), 'r') as f:
            for i in range(30):
                buff = f.readline().replace('\n', '')
                endData.append(buff)
                if '预报结论' in buff:
                    break

            for i in range(30):
                if '各县' in f.readline():
                    break

            for i in range(30):
                buf = f.readline()
                if '首席' in buf:
                    break
                if '----------' in buf:
                    endData.append(buf[0:100])
                else:
                    buf = rep.split(buf)
                    line = []
                    for d in buf:
                        if d:
                           line.append(alignment(d, space=20, align='center'))
                    if len(line) == 9:
                        endData.append(''.join(line[0: 5]))
                    elif len(line) == 8:
                        line.insert(1, ' '*20)
                        endData.append(''.join(line[0: 5]))
                    elif len(line) > 9:
                        endData.append(''.join(line[0: 6]))
                    elif len(line) < 8:
                        endData.append(''.join(line))
        self.end_textEdit.setText(('\n'.join(endData)))

    def save_datas(self):
        endDatas = self.end_textEdit.toPlainText()
        with open('D:\\提取结果.txt', 'wt') as f:
            f.write(endDatas)
        QtWidgets.QMessageBox.information(self, 'save in D:\\', '文件保存成功')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #创建窗体对象
    window = MyApp()
    #窗体显示
    window.show()
    sys.exit(app.exec_())
