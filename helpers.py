import os
import pickle
import streamlit as st

def format_names(object):
       return object.name

def render_svg_and_title(svg_string, title:str="RollForGroup"):
    """Renders the given SVG string."""
    # Encode as base 64
    import base64
    b64 = base64.b64encode(svg_string.encode("utf-8")).decode("utf-8")

    # Add some CSS on top
    css = """
    <style>
       .logo-title-container {
       display: flex;
       align-items: center;
       }
    </style>
    """

    html = f"""
    {css}
    <div class="logo-title-container">
        <img src="data:image/svg+xml;base64,{b64}" style="max-height: 120px;">
        <h1 style="font-size: 2em; color: orange; margin-left: 10px;">{title}</h1>
    </div>
    """
    return html

def load_objects(object_type:str) -> dict:
       objects = {}
       print(f"Loading from: {object_type}")
       for filename in os.listdir(object_type):
              filepath = os.path.join(object_type, filename)
              print(f"Loading file: {filepath}")
              with open(filepath, 'rb') as f:
                     obj = pickle.load(f)
                     objects[obj.id] = obj
       return objects

def save_object(object, object_type:str) -> None:
       if object_type not in ["players", "games"]:
              raise ValueError("The 'object_type' argument must be 'players' or 'games'.")
       filename = f"{object.id}.{object_type[:-1]}"
       filepath = f"{object_type}/{filename}"
       print(filepath)
       with open(filepath, 'wb') as f:
              pickle.dump(object, f)
       print(f"File '{filename}' saved successfully.")

def delete_object(object, object_type:str) -> None:
       formatted_object_type = object_type[:-1]
       # delete from session state
       if object.id in st.session_state[f"{formatted_object_type}_dict"]:
              del(st.session_state[f"{formatted_object_type}_dict"][object.id])
       # delete file
       filename = f"{object.id}.{formatted_object_type}"
       filepath = os.path.join(object_type, filename)
       print(f"deleting from: {filepath}")
       if os.path.exists(filepath):
              os.remove(filepath)
              print(f"File '{filename}' deleted successfully.")
       else:
              print(f"File '{filename}' not found in the specified folder.")
