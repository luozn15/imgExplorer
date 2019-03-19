
"""
imgExplorer
基于视觉知识管理的组织型设计研究课程组分享

作者：luozn15
github: https://github.com/luozn15/imgExplorer
最后编辑：2019年3月17日
"""

import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QCheckBox, QApplication, QLabel, QMessageBox, QMainWindow, QGroupBox, QScrollArea, QLineEdit
from PyQt5.QtGui import QPixmap
 
 
class Explorer(QWidget):
    
    path='./imgs3/'
    dirs=[]
    currentDir=1
    currentDirSize=0
    currentFile=0

    projectInfo=[]
    infoList=[]
    infoIndex=[]

    infoLabel=[]

    img=''

    infoEdit=[]

    checkBox=[]
    #checkList=['火车站', '地铁/轻轨站', '其它', '城市中心', '城市边缘', '郊外', '等候式', '通过式', '结合式', '宽敞的站前广场', '必要的集散空间', '垂直组织集约化用地', '其它', '换乘地铁', '换乘巴士', '换乘其它', '商业', '餐饮', '办公', '居住', '娱乐', '其它', '简约', '适中', '复杂', '上跨式', '侧立式' ,'其它', '线性', '非线性', '混合']
    #checkListGroup=['类型', '城市区位', '客流模式', '前广场', '换乘', '附属功能', '形式复杂度', '与铁道关系', '线性/非线性']
    checkList=[]
    checkListGroup=[]

    
    df=[]

    
    def getPreviousImg(self):
        files=os.listdir(self.path+str(self.currentDir))
        self.currentDirSize=len(files)
        if self.currentFile - 1 >= 1:
            self.currentFile -= 1
        else:
            QMessageBox.question(self, 'Message',"已经是项目第一张图片", QMessageBox.Yes, QMessageBox.Yes)

        self.img=self.path + str(self.currentDir) + '/' + str(self.currentFile) + '.jpg'

    def getNextImg(self):
        files=os.listdir(self.path+str(self.currentDir))
        self.currentDirSize=len(files)
        if self.currentFile + 1 <= self.currentDirSize:
            self.currentFile += 1
        else:
            reply=QMessageBox.question(self, 'Message',"完成该项目?", QMessageBox.Yes |QMessageBox.No, QMessageBox.No)
            if reply==QMessageBox.Yes:
                
                self.save()

                self.currentDir += 1
                self.currentFile = 1
                self.rSetInfoList()
                self.setCheckBox()
                self.navigationEdit.setText(str(self.currentDir))
                #QApplication.processEvents()

                
        #self.img=self.path+self.dirs[currentDir-1]+'/'+files[currentFile-1]
        self.img=self.path + str(self.currentDir) + '/' + str(self.currentFile) + '.jpg'

    def setImg(self):
        self.pixmap = QPixmap(self.img)
        width=self.pixmap.width()
        height=self.pixmap.height()
        if height/width > 6/15:
            self.pixmap=self.pixmap.scaledToHeight(600)
        else:
            self.pixmap=self.pixmap.scaledToWidth(1500)
        self.imgLabel.setPixmap(self.pixmap)
        #print(self.pixmap.width(),self.pixmap.height())

    def previousClicked(self):
        #print('previousClicked')
        self.getPreviousImg()
        self.setImg()

    def nextClicked(self):
        #print('nextClicked')
        self.getNextImg()
        self.setImg()


    def setInfoList(self):
        self.infoList=self.projectInfo.iloc[self.currentDir-1].tolist()
        self.infoLabel=[]
        infoVbox = QVBoxLayout()
        infoHbox =[] 
        for i in range(len(self.infoIndex)):
            infoHbox.append(QHBoxLayout())
            self.infoLabel.append(QLabel(self.infoIndex[i]+':\t'))
            self.infoEdit.append(QLineEdit(self))
            self.infoEdit[i].setText(str(self.infoList[i]))
            infoHbox[i].addWidget(self.infoLabel[i])
            infoHbox[i].addWidget(self.infoEdit[i])
            infoVbox.addLayout(infoHbox[i])
        self.infoGroup.setLayout(infoVbox)

    def rSetInfoList(self):
        self.infoList=self.projectInfo.iloc[self.currentDir-1].tolist()
        for i in range(len(self.infoIndex)):
            self.infoLabel[i].setText(self.infoIndex[i]+':\t')
            self.infoEdit[i].setText(str(self.infoList[i]))

    def navigationConfirm(self):
        self.save()

        self.currentDir=int(self.navigationEdit.text())
        self.currentFile=1
        
        self.img=self.path + str(self.currentDir) + '/' + str(self.currentFile) + '.jpg'
        self.setImg()
        self.rSetInfoList()
        self.setCheckBox()
        

    def nextProject(self):
        self.save()

        self.currentDir+=1
        self.currentFile=1
        
        self.img=self.path + str(self.currentDir) + '/' + str(self.currentFile) + '.jpg'
        self.setImg()
        self.rSetInfoList()
        self.setCheckBox()
        self.navigationEdit.setText(str(self.currentDir))

    def setCheckBox(self):
        try:
            status = self.df[str(self.currentDir)].tolist()
            #print(status)
            for i in range(len(self.checkBox)):
                self.checkBox[i].setCheckState(status[i]==1)        
        except BaseException:
            for i in range(len(self.checkBox)):
                self.checkBox[i].setCheckState(False)

    def save(self):
        temp=[]
        for i in range(len(self.checkBox)):
            if self.checkBox[i].checkState() > 0:
                temp.append(1)
            else:
                temp.append(0)
        self.df[str(self.currentDir)]=temp
        self.df=self.df.sort_index(axis=1)
        group = self.df['Group']
        self.df.drop(labels=['Group'], axis=1,inplace = True)
        self.df.insert(0, 'Group', group)
        self.df.to_csv('tags.csv',encoding='GBK')

        temp=[]
        for edit in self.infoEdit:
            temp.append(edit.text())
        self.projectInfo.loc[self.currentDir-1]=temp
        #print(self.projectInfo.loc[self.currentDir-1])
        self.projectInfo.to_csv('projectInfo.csv',index=False)

    def __init__(self):
        super().__init__()

        self.projectInfo=pd.read_csv('projectInfo.csv',engine='python')
        self.infoIndex=self.projectInfo.columns.tolist()
        

        self.getNextImg()
        try:
            self.df=pd.read_csv('tags.csv',engine='python',index_col='Tags')
        except Exception as e:
            reply=QMessageBox.information(self, 'Warning',"找不到tags.csv,请依格式创建tags.csv", QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                sys.exit(0)

        self.checkList=self.df.index.tolist()
        self.checkListGroup=self.df['Group'].tolist()
        self.initUI()
      
    def initUI(self):      
        
        #info
        self.infoGroup = QGroupBox("Project_Infomation")
        self.setInfoList()

        #img
        self.imgLabel = QLabel(self)
        self.setImg()
        
        #leftVboxLayout
        leftVboxLayout = QVBoxLayout()
        leftVboxLayout.addWidget(self.infoGroup)
        leftVboxLayout.addStretch(1)
        leftVboxLayout.addWidget(self.imgLabel)
        
        #navigationEdit
        self.navigationEdit = QLineEdit(self)

        #navigationConfirmButton
        self.navigationConfirmButton = QPushButton("go to this project")
        self.navigationConfirmButton.clicked.connect(self.navigationConfirm)
        #nextProjectButton
        self.nextProjectButton = QPushButton("next project")
        self.nextProjectButton.clicked.connect(self.nextProject)


        #checkBox
        self.checkVboxlayout = QVBoxLayout()
        #count=0
        for i in range(len(self.checkList)):
            #if i == 0 or i == 3 or i == 6 or i == 9 or i == 13 or i == 16 or i == 22 or i == 25 or i == 28:
            if self.checkListGroup[i] == self.checkListGroup[i]:
                self.checkVboxlayout.addWidget(QLabel('\t'+self.checkListGroup[i]))
                #count += 1
            self.checkBox.append(QCheckBox(self.checkList[i], self))
            self.checkVboxlayout.addWidget(self.checkBox[i])
            self.checkVboxlayout.addStretch(1)
        self.setCheckBox()

        #scrollArea
        self.scrollWidget=QWidget()
        self.scrollWidget.setLayout(self.checkVboxlayout)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.scrollWidget)

        #button
        self.previousButton = QPushButton("PREVIOUS")
        self.previousButton.clicked.connect(self.previousClicked)
        self.nextButton = QPushButton("NEXT")
        self.nextButton.clicked.connect(self.nextClicked)
        
        self.buttonHboxlayout = QHBoxLayout()
        self.buttonHboxlayout.addStretch(1)
        self.buttonHboxlayout.addWidget(self.previousButton)
        self.buttonHboxlayout.addWidget(self.nextButton)
        

        #rightVboxLayout
        rightVboxLayout = QVBoxLayout()
        rightVboxLayout.addWidget(self.navigationEdit)
        rightVboxLayout.addWidget(self.navigationConfirmButton)
        rightVboxLayout.addWidget(self.nextProjectButton)
        #rightVboxLayout.addStretch(1)
        rightVboxLayout.addWidget(self.scrollArea)
        rightVboxLayout.addLayout(self.buttonHboxlayout)
        


        wholeHbox = QHBoxLayout()
        wholeHbox.addLayout(leftVboxLayout)
        wholeHbox.addStretch(1)
        wholeHbox.addLayout(rightVboxLayout)

        self.setLayout(wholeHbox)            
        self.setGeometry(50,50,50,50)
        self.setWindowTitle('imgExplorer') 
        self.setMinimumSize(1000,600)
        self.show()
         
         
if __name__ == '__main__':
     
    app = QApplication(sys.argv)
    app.setStyle('WindowsVista')
    ex = Explorer()
    sys.exit(app.exec_())