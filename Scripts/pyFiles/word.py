from docx import Document
import os

def image_from_word(docx_path, output_folder):
    """
    从 Word 文档中按顺序提取图片并保存到指定文件夹，并提取对应的题注。
    :param docx_path: Word 文档的路径
    :param output_folder: 输出图片的文件夹
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 加载 Word 文档
    doc = Document(docx_path)

    # 初始化图片计数
    image_count = 0

    # 遍历文档的 XML 元素，按顺序提取图片和文本
    for block in doc.element.body.iter():
        # 检查是否为图片
        if block.tag.endswith("blip"):  # 图片的 XML 标签
            # 获取图片数据
            r_id = block.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
            if r_id:
                rel = doc.part.rels[r_id]
                image_data = rel.target_part.blob

                # 确定图片的扩展名
                content_type = rel.target_part.content_type
                extension = content_type.split("/")[-1]

                # 构造图片文件名
                image_filename = f"image_{image_count + 1}.{extension}"
                image_path = os.path.join(output_folder, image_filename)

                # 保存图片
                with open(image_path, "wb") as img_file:
                    img_file.write(image_data)

                print(f"提取图片：{image_filename}")
                image_count += 1

    if image_count == 0:
        print("文档中没有找到图片。")
    else:
        print(f"总共提取了 {image_count} 张图片。")

# 使用示例
docx_path = "path/to/your/file"  # 替换为你的 Word 文档路径
output_folder = "output/file"  # 输出文件夹
image_from_word(docx_path, output_folder)