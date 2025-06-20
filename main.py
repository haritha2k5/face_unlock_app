from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel 
import cv2
from insightface.app import FaceAnalysis
import numpy as np
import base64
import os
from colorama import Fore, Style


class UnlockRequest(BaseModel):
    image_base64: str
app=FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/",response_class=HTMLResponse)
def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

    
#Initialize the FaceAnalysis app
face_app=FaceAnalysis(name='buffalo_l')
face_app.prepare(ctx_id=0 if cv2.cuda.getCudaEnabledDeviceCount()>0 else -1)

#Load and embed all known faces
known_embeddings=[]

for filename in os.listdir("known_faces"):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join("known_faces", filename)
        img = cv2.imread(path)
        faces = face_app.get(img)
        if faces:
            known_embeddings.append(faces[0].embedding)
            print(Fore.GREEN + f"[LOADED] {filename}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"[SKIPPED] No face in {filename}" + Style.RESET_ALL)

@app.post("/unlock")
async def unlock_face(request: UnlockRequest):
    try:
        #Decode the base64 image
        print(Fore.CYAN + "[INFO] Decoding base64 image" + Style.RESET_ALL)
        img_data = base64.b64decode(request.image_base64)
        nparr = np.frombuffer(img_data, np.uint8)
        test_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        print(Fore.CYAN + "[INFO] Received image for verification" + Style.RESET_ALL)

        test_faces = face_app.get(test_img)
        if not test_faces:
            print(Fore.RED + "[FAIL] No face detected in test image" + Style.RESET_ALL)
            return {"status": "denied", "reason": "No face detected"}
        
        test_embedding = test_faces[0].embedding
        
        for i,known_embedding in enumerate(known_embeddings):
            similarity = np.dot(known_embedding, test_embedding) / (
        np.linalg.norm(known_embedding) * np.linalg.norm(test_embedding)
        )
            print(Fore.YELLOW + f"[DEBUG] Similarity: {similarity:.3f}" + Style.RESET_ALL)

            if similarity > 0.5:
                print(Fore.GREEN + "[SUCCESS] Match found! Unlock allowed." + Style.RESET_ALL)
                return {"status": "unlocked", "similarity": round(float(similarity),3)}
    
        print(Fore.RED + "[FAIL] No match found." + Style.RESET_ALL)
        return {"status": "denied", "similarity": round(float(similarity),3)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
