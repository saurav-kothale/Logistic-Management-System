def add_gst(gst, amount):
    if gst == "GST 5":
        return amount * 1.05
    
    elif gst == "GST 12":
        return amount * 1.12
    
    elif gst == "GST 18":
        return amount * 1.18
    
    elif gst == "GST 28":
        return amount * 1.28