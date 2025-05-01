# Load UI image paths and sizes
EXT_UI_ELEMENTS = {
    "costumers": {
        "paths": [f"Assets/images/ui/costumer{i}.png" for i in range(1, 6)],
        "size": (256, 256)
    },
    "pizza_timer": {
        "paths": [
            "Assets/images/ui/full_time.png",
            *[f"Assets/images/ui/pt{i}.png" for i in range(1, 12)],
            "Assets/images/ui/run_out.png"
        ],
        "size": (128, 128)
    },
    "health": {
        "paths": [f"Assets/images/ui/a_{i}h.png" for i in range(1, 8)],
        "size": (128, 128)
    },
    "nitro": {
        "paths": [
            "Assets/images/ui/nitro_locked.png",
            "Assets/images/ui/nitro_unlocked.png"
        ],
        "size": (128, 128)
    },
    "costumer_label": {
        "paths": ["Assets/images/ui/costumer_label.png"],
        "size": (128, 128)
    }
}