from fastapi import FastAPI, UploadFile , File
from BSEP_framework_alamarah import BSEP as AlInmaaParser
from typing import Optional, Annotated
from pydantic import BaseModel
import traceback, tempfile, os

app = FastAPI()

supported_types = ["alinmaa", "alrajhi"]
alinmaa_parser = AlInmaaParser()

@app.post("/bsp")
async def bank_statements_parser(document: Annotated[UploadFile, File()], doc_type:str="alinmaa"):
    
    
    assert document.content_type == "application/pdf", "Document should be in PDF format"
    assert doc_type in supported_types, f"Supported types are [{','.join(supported_types)}]"
    
    doc = await document.read()
    
    tmpf, path = tempfile.mkstemp(suffix=".pdf")
    print(f"\n\n{path}\n\n")
    with open(path, 'wb') as f:
        
        f.write(doc)
        
        try:
            results = alinmaa_parser(document_path=path, num_processes=5)
            return results.to_json()
        except Exception as e:
            with open("./log.err", "w") as ef:
                ef.write(traceback.format_exc())
    
    os.close(tmpf)
    return {}