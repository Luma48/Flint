# Project Imports
from managers.Resource_Manager import get_resource

#===================================================================================================================================
# Path's to Bubble Images                                                                                                   
#===================================================================================================================================
def bubble_image_path(bubble_type: str) -> str:
    base_path = "Packaged_Resources/Images/Bubbles/"
    
    bubble_map = {
        "clear": "Intermission_Bubble.png",
        "diary": "Diary_Bubble.png",
        "fairy": "Pixel_Speech_Bubble.png",
        "fairy2": "Pixel_Speech_Bubble.png",
        "system": "System_Speech_Bubble.png",
        "select": "Selectbox_Bubble.png",
        "kanban": "Signpost_Bubble.png",
        "housou": "Robo_Speech_Bubble.png",
        "majo": "Mimi_Speech_Bubble.png",
        "adv": "Swoon_Speech_Bubble.png",
        "adv_select": "Swoon_Select_Bubble.png",
        "small": "Small_Speech_Bubble.png",
    }
    
    filename = bubble_map.get(bubble_type, "Speech_Bubble.png")
    return get_resource(f"{base_path}{filename}")