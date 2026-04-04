import os
import sys

# ==========================================
# 1. 注入关键环境变量 (解决底层 C++ 库报错问题)
# ==========================================
# 指向你当前运行环境的真实路径
CONDA_ENV = "/home/luca/anaconda3/envs/llm"

os.environ["PROJ_LIB"] = os.path.join(CONDA_ENV, "share/proj")
os.environ["GDAL_DATA"] = os.path.join(CONDA_ENV, "share/gdal")
# 启用无头模式，避免在没有显式调用图形界面的后台引发段错误 (SIGSEGV)
os.environ["QT_QPA_PLATFORM"] = "offscreen"

# ==========================================
# 2. 导入 QGIS 相关模块
# ==========================================
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsPrintLayout,
    QgsLayoutItemMap,
    QgsLayoutItemLabel,
    QgsLayoutItemScaleBar,
    QgsLayoutExporter,
    QgsLayoutPoint,
    QgsLayoutSize,
    QgsUnitTypes,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsTextFormat
)
from PyQt5.QtGui import QFont, QColor


def create_and_export_layout():
    """核心排版与出图逻辑"""
    project = QgsProject.instance()
    # 清理当前项目，确保每次运行的环境是干净的
    project.clear()

    # ---------------------------------------------------------
    # [关键修复] 构造一个临时矢量图层，用于计算地图范围和比例尺
    # 在独立脚本中没有 QGIS 界面，绝对不能使用 iface
    # ---------------------------------------------------------
    layer = QgsVectorLayer("Polygon?crs=EPSG:4326", "Test_Polygon", "memory")
    provider = layer.dataProvider()
    feat = QgsFeature()
    # 画一个简单的测试多边形块
    geom = QgsGeometry.fromWkt("POLYGON((116.0 39.0, 117.0 39.0, 117.0 40.0, 116.0 40.0, 116.0 39.0))")
    feat.setGeometry(geom)
    provider.addFeatures([feat])
    layer.updateExtents()
    project.addMapLayer(layer)

    # ---------------------------------------------------------
    # 开始构建 Print Layout
    # ---------------------------------------------------------
    manager = project.layoutManager()
    layout_name = "Automated_Export_Layout"

    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(layout_name)
    manager.addLayout(layout)

    # 1. 添加地图框
    map_item = QgsLayoutItemMap(layout)
    map_item.setKeepLayerSet(False)
    map_item.attemptMove(QgsLayoutPoint(10, 25, QgsUnitTypes.LayoutMillimeters))
    map_item.attemptResize(QgsLayoutSize(277, 175, QgsUnitTypes.LayoutMillimeters))

    # 将地图的显示范围设定为刚刚创建的临时图层的范围
    # 如果你想缩小一点看全景，可以对 extent 进行 scale，例如 layer.extent().scale(1.2)
    map_item.setExtent(layer.extent())
    layout.addLayoutItem(map_item)

    # 2. 添加主标题
    title_item = QgsLayoutItemLabel(layout)
    title_item.setText("自动化测试图层导出")

    # ---------------------------------------------------------
    # 修复 DeprecationWarning: 使用 QgsTextFormat 替代直接 setFont
    # ---------------------------------------------------------
    text_format = QgsTextFormat()
    text_format.setFont(QFont("Microsoft YaHei", 20, QFont.Bold))
    text_format.setColor(QColor("black"))
    title_item.setTextFormat(text_format)
    # ---------------------------------------------------------

    title_item.adjustSizeToText()
    title_item.attemptMove(QgsLayoutPoint(10, 8, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(title_item)

    # 3. 添加比例尺
    scalebar = QgsLayoutItemScaleBar(layout)
    scalebar.setStyle('Single Box')
    scalebar.setLinkedMap(map_item)  # 绑定到地图框
    scalebar.applyDefaultSize()
    scalebar.attemptMove(QgsLayoutPoint(200, 185, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(scalebar)

    # 4. 导出为 PDF
    # 输出到脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    export_path = os.path.join(current_dir, "output_map.pdf")

    exporter = QgsLayoutExporter(layout)
    pdf_settings = QgsLayoutExporter.PdfExportSettings()

    print("开始渲染并导出 PDF...")
    result = exporter.exportToPdf(export_path, pdf_settings)

    if result == QgsLayoutExporter.Success:
        print(f"✅ 出图成功！文件已保存至: {export_path}")
    else:
        print("❌ 出图失败，请检查路径权限。")


def main():
    # ==========================================
    # 3. 安全初始化 QGIS Application
    # ==========================================
    print("正在初始化 QGIS 环境...")
    QgsApplication.setPrefixPath(CONDA_ENV, True)
    # False 表示在没有 GUI 应用程序的环境中启动
    qgs = QgsApplication([], False)
    qgs.initQgis()

    try:
        # 执行主要的业务逻辑
        create_and_export_layout()
    except Exception as e:
        print(f"❌ 运行过程中发生异常: {e}")
    finally:
        # ==========================================
        # 4. 完美清理，防止出现段错误 (SIGSEGV)
        # ==========================================
        qgs.exitQgis()
        print("QGIS 环境已安全卸载。")


if __name__ == '__main__':
    main()
