# encoding: UTF-8

'''
STUB模块相关的GUI控制组件
'''


from vnpy.service.event import Event
from vnpy.service.event.vtEvent import *
from vnpy.appDesktop.windows.uiBasicWidget import QtGui, QtCore, QtWidgets, BasicCell

from vnpy.service.tradeStrategy.language import text



########################################################################
class StrategyEngineWidget(QtWidgets.QWidget):
    """STUB引擎管理组件"""
    signal = QtCore.Signal(type(Event()))

    #----------------------------------------------------------------------
    def __init__(self, strategyManager, eventEngine, parent=None):
        """Constructor"""
        super(StrategyEngineWidget, self).__init__(parent)

        self.strategyManager = strategyManager
        self.eventEngine = eventEngine

        self.strategyLoaded = False

        self.initUi()
        self.registerEvent()

        # 记录日志
        self.strategyManager.writeStubLog(text.STUB_ENGINE_STARTED)

    #----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle(text.STUB_STRATEGY)

        # 按钮
        loadButton = QtWidgets.QPushButton(text.LOAD_STRATEGY)
        initAllButton = QtWidgets.QPushButton(text.INIT_ALL)
        startAllButton = QtWidgets.QPushButton(text.START_ALL)
        stopAllButton = QtWidgets.QPushButton(text.STOP_ALL)
        savePositionButton = QtWidgets.QPushButton(text.SAVE_POSITION_DATA)

        loadButton.clicked.connect(self.load)
        initAllButton.clicked.connect(self.initAll)
        startAllButton.clicked.connect(self.startAll)
        stopAllButton.clicked.connect(self.stopAll)
        savePositionButton.clicked.connect(self.strategyManager.savePosition)

        # 滚动区域，放置所有的StubStrategyManager
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        # STUB组件的日志监控
        self.stubLogMonitor = QtWidgets.QTextEdit()
        self.stubLogMonitor.setReadOnly(True)
        self.stubLogMonitor.setMaximumHeight(200)

        # 设置布局
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(loadButton)
        hbox2.addWidget(initAllButton)
        hbox2.addWidget(startAllButton)
        hbox2.addWidget(stopAllButton)
        hbox2.addWidget(savePositionButton)
        hbox2.addStretch()

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox2)
        vbox.addWidget(self.scrollArea)
        vbox.addWidget(self.stubLogMonitor)
        self.setLayout(vbox)

    #----------------------------------------------------------------------
    def initStrategyManager(self):
        """初始化策略管理组件界面"""
        w = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout()

        for name in list(self.strategyManager.strategyDict.keys()):
            #strategyManager = StubStrategyManager(self.strategyManager, self.eventEngine, name)
            vbox.addWidget(strategyManager)

        vbox.addStretch()

        w.setLayout(vbox)
        self.scrollArea.setWidget(w)

    #----------------------------------------------------------------------
    def initAll(self):
        """全部初始化"""
        for name in list(self.strategyManager.strategyDict.keys()):
            self.strategyManager.initStrategy(name)

    #----------------------------------------------------------------------
    def startAll(self):
        """全部启动"""
        for name in list(self.strategyManager.strategyDict.keys()):
            self.strategyManager.startStrategy(name)

    #----------------------------------------------------------------------
    def stopAll(self):
        """全部停止"""
        for name in list(self.strategyManager.strategyDict.keys()):
            self.strategyManager.stopStrategy(name)

    #----------------------------------------------------------------------
    def load(self):
        """加载策略"""
        if not self.strategyLoaded:
            self.strategyManager.loadSetting()
            self.initStrategyManager()
            self.strategyLoaded = True
            self.strategyManager.writeStubLog(text.STRATEGY_LOADED)

    #----------------------------------------------------------------------
    def updateStubLog(self, event):
        """更新STUB相关日志"""
        log = event.dict_['data']
        content = '\t'.join([log.logTime, log.logContent])
        self.stubLogMonitor.append(content)

    #----------------------------------------------------------------------
    def registerEvent(self):
        """注册事件监听"""
        self.signal.connect(self.updateStubLog)
        self.eventEngine.register(EVENT_STUB_LOG, self.signal.emit)

    #----------------------------------------------------------------------
    def closeEvent(self, event):
        """关闭窗口时的事件"""
        reply = QtWidgets.QMessageBox.question(self, text.SAVE_POSITION_DATA,
                                           text.SAVE_POSITION_QUESTION, QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.strategyManager.savePosition()

        event.accept()










