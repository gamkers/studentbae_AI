
def success_response(data=None):
    if data:
        return {"data": data, "status": "success", "message": "200[OK]"}
    else:
        return {"status": "success", "message": "200[OK]"}

def unsuccess_response():
    return {"status": "Failed"}