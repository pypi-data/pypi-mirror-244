from common import BreakPointHit, BreakPointPairError, FunctionData
from gui.CallStackView import CallStackView, StandardItem
from gui.SourceEdit import SourceEdit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QSplitter, QWidget, QStatusBar, QFileDialog, QAction, QMessageBox
from PyQt5.QtGui import QStandardItemModel
from pathlib import Path
import json
import sys
import zipfile
import tempfile
import os


def keystoint(x):
    return {int(k): v for k, v in x.items()}


def adjust_file_path(filename: str) -> str:
    if Path(filename).is_file():
        return filename

    newpath = Path.cwd().joinpath(filename)
    if Path(newpath).is_file():
        return newpath

    return None


def zipDir(dirpath: str, outFullName: str) -> None:
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename),
                      os.path.join(fpath, filename))
    zip.close()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('流程图')
        self.resize(1200, 900)

        self._createMenuBar()

        # You can't set a QLayout directly on the QMainWindow. You need to create a QWidget
        # and set it as the central widget on the QMainWindow and assign the QLayout to that.
        mainWnd = QWidget()
        self.setCentralWidget(mainWnd)
        layout = QHBoxLayout()
        mainWnd.setLayout(layout)

        splitter = QSplitter(Qt.Horizontal)

        # Left is QTreeView
        treeView = CallStackView()
        treeModel = QStandardItemModel()
        treeView.setModel(treeModel)

        # Right is QTextEdit
        sourceEdit = SourceEdit()

        splitter.addWidget(treeView)
        splitter.addWidget(sourceEdit)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 6)
        layout.addWidget(splitter)

        treeView.selectionModel().selectionChanged.connect(sourceEdit.selectionChanged)
        treeView.selectionModel().selectionChanged.connect(self.selectionChanged)
        self.treeView: CallStackView = treeView
        self.sourceEdit: SourceEdit = sourceEdit

        self.tempdir = None
        self.filename = ''

    def _fillContent(self, rootNode) -> None:
        filepath = ''
        if (len(sys.argv) == 2):
            filepath = adjust_file_path(sys.argv[1])

        if filepath:
            self._parse_file(rootNode, filepath)

    def _createMenuBar(self) -> None:
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")

        openAct = QAction('&Open', self)
        openAct.triggered.connect(self._open_file)
        fileMenu.addAction(openAct)

        saveAct = QAction('&Save', self)
        saveAct.triggered.connect(self._save_file)
        fileMenu.addAction(saveAct)

        helpMenu = menuBar.addMenu("&Help")
        statusBar = QStatusBar()
        self.setStatusBar(statusBar)
        statusBar.showMessage("...")

    def _save_file(self) -> None:
        # 保存代码到零时目录
        self.treeView._save(self.tempdir.name)
        zipDir(self.tempdir.name, self.filename)

    def _open_file(self) -> None:
        if self.tempdir:
            self.tempdir.cleanup()
            self.tempdir = None

        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open zip file', '', 'ZIP Files (*.zip)')
        if filename:
            zf = zipfile.ZipFile(filename)
            self.tempdir = tempfile.TemporaryDirectory()
            zf.extractall(self.tempdir.name)
            self.treeView.clear()
            self.sourceEdit.setCodeFolder(self.tempdir.name)
            rootNode = self.treeView.model().invisibleRootItem()
            self._parse_file(rootNode, Path(
                self.tempdir.name).joinpath('monitor.json'))
            self.treeView.expandAll()
            self.filename = filename

    def _parse_file(self, rootNode, filefullpath: str) -> None:
        stack = []
        nDepth = 0
        curRootNode = rootNode
        with open(filefullpath, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            hits = data['hits']
            functions = keystoint(data['functions'])

            for num, hit in enumerate(hits, 1):
                curItem = BreakPointHit()
                curItem.assign(hit)

                paired = False
                if stack:
                    topItem = stack[-1][0]
                    if curItem.pairWith(topItem):
                        if curItem.isStart:
                            raise BreakPointPairError(num, curItem)
                        paired = True

                if paired:
                    curRootNode = stack[-1][1]
                    stack.pop()
                    nDepth = nDepth - 1
                else:
                    if not curItem.isStart:
                        raise BreakPointPairError(num, hit)
                    stack.append((curItem, curRootNode))
                    nDepth = nDepth + 1
                    node = StandardItem(curItem.funtionName)
                    node.offset = curItem.offset
                    data = FunctionData()
                    data.assign(functions[node.offset])
                    node.functionData = data
                    curRootNode.appendRow(node)
                    curRootNode = node

    def selectionChanged(self, selected, deselected) -> None:
        if not selected.indexes():
            return

        selectedIndex = selected.indexes()[0]
        item: StandardItem = selectedIndex.model().itemFromIndex(selectedIndex)
        if not item.functionData:
            return

        # 确定函数名所在的行
        filefullpath = item.functionData.fileName
        self.statusBar().showMessage(
            f"{filefullpath}({item.functionData.startLineNumber})")
