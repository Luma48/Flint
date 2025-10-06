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
        "fairy": "Pixel_Speach_Bubble.png",
        "fairy2": "Pixel_Speach_Bubble.png",
        "system": "System_Speach_Bubble.png",
        "select": "Selectbox_Bubble.png",
        "kanban": "Signpost_Bubble.png",
        "housou": "Robo_Speach_Bubble.png",
        "majo": "Mimi_Speach_Bubble.png",
        "adv": "Swoon_Speach_Bubble.png",
        "adv_select": "Swoon_Select_Bubble.png",
        "small": "Small_Speach_Bubble.png",
    }
    
    filename = bubble_map.get(bubble_type, "Speach_Bubble.png")
    return get_resource(f"{base_path}{filename}")