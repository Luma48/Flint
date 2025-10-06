from typing import List, Tuple

#===================================================================================================================================
# Bubble Block Structure                                                                                                    
#===================================================================================================================================
class BubbleBlock:
    def __init__(
        self,
        stage_npc: str,
        bubble_type: str,
        position: Tuple[int, int, int, int],
        pages: List[str],
        bubble_sound: str,
    ):
        self.stage_npc = stage_npc
        self.bubble_type = bubble_type
        self.position = position
        self.pages = pages
        self.bubble_sound = bubble_sound
