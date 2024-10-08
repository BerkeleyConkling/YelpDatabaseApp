#Berkeley Conkling, milestone3 app code
#Youtube Link of Demo: https://youtu.be/R7j1lueBc0g

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "YelpApp.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class YelpApp(QMainWindow):

    def __init__(self):
        super(YelpApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #added stuff
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)  # associates calling the stateChanged function when the text is changed
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipList.itemSelectionChanged.connect(self.zipChanged)
        self.ui.searchButton.clicked.connect(self.searchButtonPressed)
        self.ui.clearButton.clicked.connect(self.clearButtonPressed)
        self.ui.categoryList.itemSelectionChanged.connect(self.categoryChanged)
    def executeQuery(self, sql_str):#call this to run queries
        try:
            conn = psycopg2.connect("dbname = 'Yelp' user='postgres' host='localhost' password='Cyborg1137!'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state_name FROM business ORDER BY state_name;"
        try:
            results = self.executeQuery(sql_str)
            # print(results)
            for row in results:
                # print(row[0])
                self.ui.stateList.addItem(row[0])
        except:
            print("Load State List Query Failed!")

        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):  # called when state value has changed
        self.ui.cityList.clear()
        # print("here")
        state = self.ui.stateList.currentText()

        # only do all of this if a state is actually selected
        if self.ui.stateList.currentIndex() >= 0:
            sql_str = "SELECT distinct city_name FROM business WHERE state_name ='" + state + "' ORDER BY city_name;"
            # print(sql_str)
            try:
                results = self.executeQuery(sql_str)
                # print(results)
                for row in results:
                    # print(row)
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query Failed!")



    def cityChanged(self):

        self.ui.zipList.clear()

        #self.ui.businessList.clear()
        #print("here3")

        # only do all of this if a city is actually selected
        if len(self.ui.cityList.selectedItems()) > 0 and self.ui.stateList.currentIndex()>= 0:
            #print("here")
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT distinct zip FROM business WHERE city_name ='" + city + "' ORDER BY zip;"
            # print(sql_str)
            try:
                results = self.executeQuery(sql_str)
                #print(results)
                for row in results:
                    # print(row)
                    self.ui.zipList.addItem(row[0])
            except:
                print("Query Failed!")

    def zipChanged(self):
        self.ui.categoryList.clear()
        self.ui.numBusinessDisplay.clear()
        self.ui.totalPopulationDisplay.clear()
        self.ui.averageIncomeDisplay.clear()
        #print("here2")
        if (self.ui.topCatTable.rowCount() > 0):
            self.ui.topCatTable.clear()
        if(self.ui.businessTable.rowCount() > 0):
            self.ui.businessTable.clear()
        if (self.ui.popularBusinessTable.rowCount() > 0):
            self.ui.popularBusinessTable.clear()
        if (self.ui.succesfulBusinessTable.rowCount() > 0):
            self.ui.succesfulBusinessTable.clear()

        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and len(self.ui.zipList.selectedItems()) > 0:
            #print("here1")
            zipCode = self.ui.zipList.selectedItems()[0].text()

            sql_str = "SELECT bc.cat_name, COUNT(bc.business_id) AS num_businesses FROM Business b JOIN BusinessCategory bc ON b.business_id = bc.business_id WHERE b.zip = '" + zipCode + "' GROUP BY bc.cat_name ORDER BY num_businesses DESC;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.topCatTable.setColumnCount(len(results[0]))  # set columns
                self.ui.topCatTable.setRowCount(len(results))  # set rows
                #self.ui.topCatTable.setHorizontalHeaderLabels(['Category Name', '#Businesses'])
                self.ui.topCatTable.resizeColumnsToContents()
                self.ui.topCatTable.setColumnWidth(0, 200)
                self.ui.topCatTable.setColumnWidth(1, 100)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.topCatTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Cat Table Query Failed!")

            sql_str = "SELECT COUNT(*) AS num_businesses FROM Business WHERE zip = '" + zipCode + "';"
            try:
                result = self.executeQuery(sql_str)
                #print(result[0][0])
                self.ui.numBusinessDisplay.addItem(str(result[0][0]))
            except:
                print("couldn't get num businesses in zip")


            sql_str = "SELECT population FROM ZipCode WHERE zip = '" + zipCode + "';"

            try:
                result = self.executeQuery(sql_str)
                #print(result[0][0])
                self.ui.totalPopulationDisplay.addItem(str(result[0][0]))
            except:
                print("couldn't get total population in zip")

            sql_str = "SELECT avg_income FROM ZipCode WHERE zip = '" + zipCode + "';"

            try:
                result = self.executeQuery(sql_str)
                # print(result[0][0])
                self.ui.averageIncomeDisplay.addItem("$" + str(result[0][0]))
            except:
                print("couldn't get total population in zip")

    def searchButtonPressed(self):
        self.ui.categoryList.clear()
        if (self.ui.businessTable.rowCount() > 0):
            self.ui.businessTable.clear()
        if (self.ui.popularBusinessTable.rowCount() > 0):
            self.ui.popularBusinessTable.clear()
        if (self.ui.succesfulBusinessTable.rowCount() > 0):
            self.ui.succesfulBusinessTable.clear()

        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and len(self.ui.zipList.selectedItems()) > 0:
            #print("here1")
            zipCode = self.ui.zipList.selectedItems()[0].text()
            sql_str = "SELECT business_name, street_address, city_name, review_rating, review_count, num_checkins FROM business WHERE zip = '" + zipCode + "' ORDER BY city_name;"
            # print(sql_str)
            #print("here4")
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.setColumnCount(len(results[0]))  # set columns
                self.ui.businessTable.setRowCount(len(results))  # set rows

                self.ui.businessTable.setColumnWidth(0, 250)
                self.ui.businessTable.setColumnWidth(1, 150)
                self.ui.businessTable.setColumnWidth(2, 100)
                self.ui.businessTable.setColumnWidth(3, 50)
                self.ui.businessTable.setColumnWidth(4, 50)
                self.ui.businessTable.setColumnWidth(5, 25)
                #self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Street address', 'City', 'Review Rating', 'Review Count', '#Checkins'])


                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Business TableQuery Failed!")



            sql_str = "SELECT DISTINCT Category.cat_name FROM Business JOIN BusinessCategory ON Business.business_id = BusinessCategory.business_id JOIN Category ON BusinessCategory.cat_name = Category.cat_name WHERE Business.zip = '" + zipCode + "';"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    # print(row)
                    self.ui.categoryList.addItem(row[0])
            except:
                print("Category Query Failed")

            sql_str = "SELECT business_name, review_rating, review_count FROM Business WHERE zip = '" + zipCode + "' AND popularity_score > 0;"

            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.popularBusinessTable.setColumnCount(len(results[0]))  # set columns
                self.ui.popularBusinessTable.setRowCount(len(results))  # set rows
                self.ui.popularBusinessTable.resizeColumnsToContents()
                self.ui.popularBusinessTable.setColumnWidth(0, 200)
                self.ui.popularBusinessTable.setColumnWidth(1, 50)
                self.ui.popularBusinessTable.setColumnWidth(2, 50)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.popularBusinessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Popularity Table Query Failed!")

            sql_str = "SELECT business_name, review_count, num_checkins FROM Business WHERE zip = '" + zipCode + "' AND success_score > 0;"

            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.succesfulBusinessTable.setColumnCount(len(results[0]))  # set columns
                self.ui.succesfulBusinessTable.setRowCount(len(results))  # set rows
                self.ui.succesfulBusinessTable.resizeColumnsToContents()
                self.ui.succesfulBusinessTable.setColumnWidth(0, 200)
                self.ui.succesfulBusinessTable.setColumnWidth(1, 50)
                self.ui.succesfulBusinessTable.setColumnWidth(2, 50)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.succesfulBusinessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("")

    def clearButtonPressed(self):
        self.ui.cityList.clear()
        self.ui.zipList.clear()

    def categoryChanged(self):
        if (self.ui.businessTable.rowCount() > 0):
            self.ui.businessTable.clear()
        if self.ui.stateList.currentIndex() >= 0 and len(self.ui.cityList.selectedItems()) > 0 and len(self.ui.zipList.selectedItems()) > 0 and len(self.ui.categoryList.selectedItems()) > 0:
            #print("here1")
            zipCode = self.ui.zipList.selectedItems()[0].text()
            catName = self.ui.categoryList.selectedItems()[0].text()
            sql_str = f'''
                SELECT b.business_name, b.street_address, b.city_name, b.review_rating, b.review_count, b.num_checkins
                FROM Business b 
                JOIN BusinessCategory bc ON b.business_id = bc.business_id 
                JOIN Category c ON bc.cat_name = c.cat_name
                WHERE b.zip = '{zipCode}' AND c.cat_name = '{catName}';
                '''
            # print(sql_str)
            #print("here4")
            try:
                results = self.executeQuery(sql_str)

                style = "::section {""background-color: #f3f3f3; }"

                self.ui.businessTable.setColumnCount(len(results[0]))  # set columns
                self.ui.businessTable.setRowCount(len(results))  # set rows

                self.ui.businessTable.setColumnWidth(0, 250)
                self.ui.businessTable.setColumnWidth(1, 150)
                self.ui.businessTable.setColumnWidth(2, 100)
                self.ui.businessTable.setColumnWidth(3, 50)
                self.ui.businessTable.setColumnWidth(4, 50)
                self.ui.businessTable.setColumnWidth(5, 25)
                #self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Street address', 'City', 'Review Rating', 'Review Count', '#Checkins'])


                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Category Table Query Failed!")







if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YelpApp()
    window.show()
    sys.exit(app.exec_())