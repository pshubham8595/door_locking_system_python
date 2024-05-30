import os

import firebase_admin
from firebase_admin import credentials, firestore

jsonFilePath = os.path.join("firebase_creds/doorlocking-2b551-firebase-adminsdk-hptt1-f57f304451.json")
cred = credentials.Certificate(jsonFilePath)
firebase_admin.initialize_app(cred)
db = firestore.client()


def checkOpenLockStatus(userId):
    doc_ref = db.collection("LockingData").document(userId)
    doc = doc_ref.get()
    open_value = False

    if doc.exists:
        open_value = doc.to_dict().get('openLock')
    else:
        open_value = False

    print("Fetched OpenLock value: ", open_value)
    return open_value


# receivedStatus = checkOpenLockStatus("user12345")
# print("Received Status: ",receivedStatus)