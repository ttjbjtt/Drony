import os

def get_images_in_directory(directory):
    if not os.path.exists(directory):
        return []
    return [{"name": f, "folder": os.path.basename(directory)} for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
