from pathlib import Path
import boto3
import json

file_name = str(Path(__file__).parent / "images" / "lista-material-escolar.jpeg")

def get_document(file_name:str)->bytearray:
    with open(file_name,"rb") as file:
        img = file.read()

    return img

def detect_file_text(file_path)->None:
    client = boto3.client("textract")
    doc_bytes = get_document(file_path)
    response = client.detect_document_text(Document={"Bytes":doc_bytes})
    try:

        with open("response_2.json","w") as response_file:
            response_file.write(json.dumps(response))
    except IOError:
        pass

def get_line():
    with open("response_2.json","rb") as f:
        data = json.loads(f.read())["Blocks"]
        text = [block["Text"] for block in data if block["BlockType"] == "LINE"]
    return text

if __name__ == "__main__":
    detect_file_text(file_name)
    result = get_line()
    print(result)