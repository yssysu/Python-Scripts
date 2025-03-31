import os
from qgis.core import QgsVectorLayer, QgsProject, QgsVectorFileWriter

print("请确认你的文件输出路径是否更改(y/n)")
# 定义输出文件夹
output_folder = 'path/to/your/files'

# 确保输出文件夹存在
if not os.path.isdir(output_folder):
    print(f"输出文件夹不存在，创建中: {output_folder}")
    try:
        os.makedirs(output_folder, exist_ok=True)
    except Exception as e:
        print(f"创建输出文件夹失败: {e}")
else:
    print(f"输出文件夹存在: {output_folder}")

# 获取项目中所有图层
layers = QgsProject.instance().mapLayers().values()

if not layers:
    print("项目中没有加载任何图层！")
else:
    # 遍历所有图层
    for layer in layers:
        # 检查图层有效性
        if not isinstance(layer, QgsVectorLayer) or not layer.isValid():
            print(f"图层 '{layer.name()}' 无效或不是矢量图层，跳过！")
            continue

        # 构建输出路径
        output_path = os.path.join(output_folder, f"{layer.name()}.shp")

        # 检查目标文件是否存在
        if os.path.exists(output_path):
            print(f"输出文件已存在，将覆盖: {output_path}")
            try:
                os.remove(output_path)  # 删除已有文件
            except Exception as e:
                print(f"无法删除现有文件: {e}")
                continue

        # 导出图层
        print(f"开始导出图层: {layer.name()} 至 {output_path}")
        error_code, error_message = QgsVectorFileWriter.writeAsVectorFormat(
            layer,
            output_path,
            "utf-8",             # 编码
            layer.crs(),         # 坐标参考系统
            "ESRI Shapefile"     # 输出格式
        )

        # 检查导出结果
        if error_code == QgsVectorFileWriter.NoError:
            print(f"图层 '{layer.name()}' 导出成功！文件路径: {output_path}")
        else:
            print(f"图层 '{layer.name()}' 导出失败！错误码: {error_code}, 错误信息: {error_message}")

print("所有图层操作完成！")