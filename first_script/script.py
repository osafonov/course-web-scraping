import json
import xml.etree.ElementTree as ET


def parse_xml():
    result = []

    tree = ET.parse('cats.xml')
    root = tree.getroot()

    for child in root:
        for grandchild in child:
            if grandchild.tag == 'fact':
                result.append(grandchild.text)

    with open('cat_result.txt', 'w') as f:
        f.write('\n'.join(result))



def parse_xml2():
    result = []

    tree = ET.parse('cats.xml')
    root = tree.getroot()

    print(root.text)



def parse_json():
    with open('cats.json', 'r') as f:
        data = json.load(f)

    print(data)


if __name__ == '__main__':
    # parse_xml()
    # parse_xml2()
    parse_json()
