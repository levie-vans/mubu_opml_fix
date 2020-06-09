import os,sys
import urllib.parse as parse
import xml.etree.ElementTree as ET
import json
import re

def fix_file(path):
	path = os.path.abspath(path)
	print("当前目录为"+path)
	for import_file in os.listdir(path):
		if os.path.splitext(import_file)[1] == ".opml":
			print("开始转换'%s'"%(import_file))
			curr_file = path + "/" + import_file
			with open(curr_file, "r+") as f:
				read_data = f.read()
				f.seek(0)
				f.truncate()
				f.write(re.sub("/[\u0000]|[\u0001]|[\u0002]|[\u0003]|[\u0004]|[\u0005]|[\u0006]|[\u0007]|[\u0008]|[\u000b]|[\u000c]|[\u000d]|[\u000e]|[\u000f]|[\u0010]|[\u0011]|[\u0012]|[\u0013]|[\u0014]|[\u0015]|[\u0016]|[\u0017]|[\u0018]|[\u0019]|[\u001a]|[\u001b]|[\u001c]|[\u001d]|[\u001e]|[\u001f]|[\u001c]|[\u007f]/gm","123",read_data))
				print("删除'%s'不可见控制符完成..."%(import_file))
			f.close()

			tree = ET.parse(curr_file)
			root = tree.getroot()
			
			for outline in root.iter('outline'):
				attr = outline.attrib
				imgage_str = ""
				url = ""
				if "_transno_images" in attr:
					imgage_str = parse.unquote(outline.attrib["_transno_images"])
				if "_images" in attr:
					imgage_str = parse.unquote(outline.attrib["_images"])
				if imgage_str != "":
					json_images = json.loads(imgage_str)
					for j in json_images:
						url += "![](https://api2.mubu.com/v3/" + j["uri"] + ")"
					print("\t" + attr["text"]+"转换完成\r\n")
					attr["text"] = attr["text"] + url
				for tag in list(attr):
					if tag[0:5] == "_mubu" or tag == "_transno_images" or tag == "_images":
						del attr[tag]
			tree.write(path + "/" + os.path.splitext(import_file)[0] + "_fixed.opml", encoding='UTF-8')
if __name__ == '__main__':
	print("命令行参数使用: python3 mubu_opml_fix.py 目录\r\n")
	if len(sys.argv) < 2:
		input_dir = input("请输入或拖入待转换文件所在目录后回车，当前目录请直接回车\r\n") or "./"
	else:
		input_dir = sys.argv[1]
	fix_file(input_dir)
#	sys.exit()
	