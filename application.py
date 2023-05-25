import sys
import string
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QBrush, QFont


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('inter.ui', self)  # Загружаем дизайн
        self.spinBox.setRange(1, 26)
        self.setWindowTitle("Автоматизированный поиск кратчайшего расстояния")
        self.pushButton.clicked.connect(self.create)#создали таблицу по числу вершин
        self.but_table.clicked.connect(self.run)#считали данные с таблицы
        self.alp = list(string.ascii_uppercase)
        self.dict = {}
        self.start = ""
        self.end = ""
        self.reset_but.clicked.connect(self.reset)
        self.task_but.clicked.connect(self.examination)#задали конечные точки и проверяем
        self.costs = {}
        self.mas = []
        self.neir = {}
        self.min_way = 0
        self.ways = []
        self.flag = False
        self.ver = ""
        self.regim_ob = False
        self.regim_go = False
        self.regim_not = False
        self.text.setVisible(False)
        self.table_otvet.setVisible(False)
        self.label_5.setVisible(False)
        self.tableWidget.cellChanged.connect(self.cell_changed)
        self.buttonGroup.buttonClicked.connect(self.regim)
        self.flu = False
        self.tableWidget.blockSignals(False)

    def cell_changed(self, row, col):
        if self.flu and row != col:
            item = self.tableWidget.item(row, col).text()
            self.tableWidget.blockSignals(True)
            self.tableWidget.setItem(col, row, QTableWidgetItem(item))
        t = self.spinBox.value()
        if row == int(t) - 1 and col == int(t) - 1:
            self.flu = True
        self.tableWidget.blockSignals(False)

    def create(self):
        self.flag = False
        t = self.spinBox.value()
        self.alp = list(string.ascii_uppercase)
        self.tableWidget.setColumnCount(t)
        self.tableWidget.setRowCount(t)
        for x in range(t):
            self.tableWidget.setColumnWidth(x, 180)
        for x in range(t):
            self.tableWidget.setRowHeight(x, 70)
        self.alp = self.alp[:t]
        self.tableWidget.setHorizontalHeaderLabels(self.alp)
        self.tableWidget.setVerticalHeaderLabels(self.alp)
        for i in range(t):
            for j in range(t):
                if j == i:
                    item2 = QTableWidgetItem()
                    self.tableWidget.setItem(i, j, item2)
                    item2.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable)
                    self.tableWidget.item(i, j).setBackground(QColor(192, 192, 192))
                    item2.setFont(QFont('Arial', 20))

    def regim(self):
        if self.ordinary.isChecked():
           print("ordinary")
           self.regim_ob = True
           self.text.setVisible(False)
        elif self.go.isChecked():
           print("go")
           self.regim_go = True
           self.text.setVisible(True)
        else:
           print("not_go")
           self.regim_not = True
           self.text.setVisible(True)

    def run(self):
        self.flag = True
        self.dict = {}
        self.info.setText("")
        kol = self.tableWidget.columnCount()
        for i in range(kol):
            for j in range(kol):
                u = self.tableWidget.item(i, j)
                if u and u.text():
                    if not u.text().isdigit():
                        self.info.setText("В таблице найдены не числовые символы. Замените их на цифры.")
                        break
                    else:
                        self.info.setText("Таблица создана верно.")
                        if self.alp[i] not in self.dict:
                            self.dict[self.alp[i]] = {self.alp[j]: int(u.text())}
                        elif self.alp[i] in self.dict:
                            self.dict[self.alp[i]].update({self.alp[j]: int(u.text())})
                        if self.alp[j] not in self.dict:
                            self.dict[self.alp[j]] = {self.alp[i]: int(u.text())}
                        else:
                            self.dict[self.alp[j]].update({self.alp[i]: int(u.text())})
        if len(self.dict) == 0:
            self.flag = False
            self.info.setText("Таблица не создана или создана неверно.")
        print(self.dict)

    def examination(self):
        self.info.setText("")
        self.start = self.start_tex.toPlainText().upper()
        self.end = self.end_tex.toPlainText().upper()
        fl = True
        if not self.flag:
            self.info.setText("Сначала проверьте таблицу.")
        elif len(self.start) == 0:
            self.info.setText("Введите стартовую вершину.")
            fl = False
        elif len(self.end) == 0:
            self.info.setText("Введите конечную вершину.")
            fl = False
        elif len(self.start) > 1 or len(self.end) > 1:
            self.info.setText("Нужна одна буква английского алфавита.")
            fl = False
        elif self.start.isdigit() or ord(self.start.upper()) < 65 or ord(self.start.upper()) > 90:
            self.info.setText("Стартовая вершина должна быть на английском языке.")
            fl = False
        elif self.end.isdigit() or ord(self.end.upper()) < 65 or ord(self.end.upper()) > 90:
            self.info.setText("Конечная вершина должна быть на английском языке.")
            fl = False
        elif self.start.upper() not in self.alp or self.end.upper() not in self.alp:
            self.info.setText("Таких вершин нет в таблице. Измените таблицу или укажите другие вершины.")
            fl = False
        elif self.start == self.end:
            self.info.setText("Не используйте одинаковые вершины.")
            fl = False
        elif self.regim_not or self.regim_go:
            self.ver = self.text.toPlainText().upper()
            if len(self.ver) > 1:
                self.info.setText("Нужна одна буква английского алфавита.")
                fl = False
            elif self.ver.isdigit() or ord(self.ver.upper()) < 65 or ord(self.ver.upper()) > 90:
                self.info.setText("Дополнительная вершина должна быть на английском языке.")
                fl = False
            elif self.ver.upper() not in self.alp:
                self.info.setText("Таких вершин нет в таблице. Измените таблицу или укажите другие вершины.")
                fl = False
        elif not self.regim_ob:
            self.info.setText("Выберите режим.")
            fl = False
        elif self.regim_ob:
            fl = True
        else:
            self.info.setText("Задание получено, выполняется расчет.")
        if self.flag and fl and self.start in self.dict and self.end in self.dict:
            self.Dijkstra()
            self.flag = False
            self.alp = list(string.ascii_uppercase)
        elif (self.start not in self.dict or self.end not in self.dict) and self.flag:
            self.info.setText("Таких вершин нет в таблице. Измените таблицу или укажите другие вершины.")
        elif not self.flag:
            self.info.setText("Сначала проверьте таблицу.")
        
    def find(self):
        min_val = 1000000
        for k in self.costs:
            cost_ = self.costs[k]
            if cost_ < min_val and k not in self.mas:
                min_val = cost_
                self.min_way = k
        return self.min_way

    def Dijkstra(self):
        for i in self.dict:
            if i != self.start:
                if i not in self.dict[self.start]:
                    self.costs[i] = 1000000
                else:
                    self.costs[i] = self.dict[self.start][i]
        node = self.find()
        while node:
            cost = self.costs[node]
            neir = self.dict[node]
            for j in neir:
                new_cost = cost + neir[j]
                if j in self.costs and new_cost < self.costs[j]:
                    self.costs[j] = new_cost
            if node not in self.mas:
                self.mas.append(node)
                node = self.find()
            else:
                break
        ver = True
        self.ways = self.all_way(self.start, self.end, [self.start])
        if self.regim_not:
            filtered_list = list(filter(lambda x: self.ver not in x[0], self.ways))
            if len(filtered_list) == 0:
                self.info.setText("Нет пути без вершины %s. Заполните таблицу верно." % (self.ver))
                ver = False
        elif self.regim_go:
            filtered_list = list(filter(lambda x: self.ver in x[0], self.ways))
            if len(filtered_list) == 0:
                self.info.setText("Через вершину %s пройти нельзя. Заполните таблицу верно." % (self.ver))
                ver = False
        else:
            filtered_list = self.ways[:]
        if ver:
            self.ways = sorted(filtered_list, key=lambda x: [x[1], x[0]])
            self.Print()
        
    def way(self, mas):
        kol_way = 0
        for i in range(len(mas) - 1):
            kol_way += self.dict[mas[i]][mas[i+1]]
        return kol_way

    def all_way(self, st, en, obj):
        if st == en:
            t = self.way(obj)
            self.ways.append(["-".join(obj), t])
        else:
            for i in self.dict[st]:
                if not (i in obj):
                    self.all_way(i, en, obj + [i])
        return self.ways

    def Print(self):
        self.table_otvet.setVisible(True)
        self.label_5.setVisible(True)
        self.table_otvet.setColumnCount(2)
        self.table_otvet.setRowCount(len(self.ways))
        self.table_otvet.resizeColumnsToContents()
        for x in range(2):
            self.table_otvet.setColumnWidth(x, 215)
        for x in range(len(self.ways)):
            self.table_otvet.setRowHeight(x, 70)
        self.table_otvet.setHorizontalHeaderLabels(["Путь", "Длина пути"])
        for i in range(len(self.ways)):
            item1 = QTableWidgetItem(self.ways[i][0])
            self.table_otvet.setItem(i, 0, item1)
            item1.setFlags(Qt.ItemIsUserCheckable)
            item2 = QTableWidgetItem(str(self.ways[i][1]))
            self.table_otvet.setItem(i, 1, item2)
            item2.setFlags(Qt.ItemIsDragEnabled)
            item1.setFont(QFont('Arial', 20))
            item2.setFont(QFont('Arial', 20))
            if i == 0:
                item1.setBackground(QColor(127, 255, 0))
                item2.setBackground(QColor(127, 255, 0))
                item1.setForeground(QBrush(QColor(0, 0, 0)))
                item2.setForeground(QBrush(QColor(0, 0, 0)))
                
            else:
                item1.setForeground(QBrush(QColor(0, 0, 0)))
                item2.setForeground(QBrush(QColor(0, 0, 0)))
        self.costs = {}
        self.mas = []
        self.neir = {}
        self.min_way = 0
        self.ways = []
        self.regim_ob = False
        self.regim_go = False
        self.regim_not = False

    def reset(self):
        self.alp = list(string.ascii_uppercase)
        self.dict = {}
        self.start = ""
        self.end = ""
        self.info.setText("")
        self.start_tex.setPlainText("")
        self.end_tex.setPlainText("")
        self.text.setPlainText("")
        self.costs = {}
        self.mas = []
        self.neir = {}
        self.min_way = 0
        self.ways = []
        self.flag = False
        self.ver = ""
        self.spinBox.setValue(1)
        self.regim_ob = False
        self.regim_go = False
        self.regim_not = False
        self.text.setVisible(False)
        self.table_otvet.setVisible(False)
        self.label_5.setVisible(False)
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0)
        while (self.tableWidget.columnCount() > 0):
            self.tableWidget.removeColumn(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.setObjectName("MainWindow")
    ex.setStyleSheet("#MainWindow{border-image:url(fon.png)}")
    ex.show()
    sys.exit(app.exec_())
