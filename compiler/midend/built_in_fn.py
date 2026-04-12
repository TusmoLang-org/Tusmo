functions_ = {
    "tix_cayiman": {"return_type": None, "feature": "array"}, 
    "nooc": {"return_type": "eray"},
    "dherer": {"return_type": "tiro"},
    "hel": {"return_type": "eray", "feature": "io"},
    
    # Type Conversion Functions
    "eray":  {"return_type": "eray", "feature": "conversion"},
    "tiro":  {"return_type": "tiro", "feature": "conversion"},
    "jajab": {"return_type": "jajab", "feature": "conversion"},
    "miyaa": {"return_type": "miyaa", "feature": "conversion"},
    "xaraf": {"return_type": "xaraf", "feature": "conversion"},

    # Character/ASCII Conversion
    "qor_tiro": {"return_type": "tiro", "feature": "char"},  # char → ASCII (int)
    "qor_xaraf": {"return_type": "xaraf", "feature": "char"},  # ASCII (int) → char

    # String Methods (as function calls - for semantic analysis)
    "kuBadal": {"return_type": "eray", "feature": "string"},
    "kaReeb": {"return_type": "eray", "feature": "string"},
    "Bkareeb": {"return_type": "eray", "feature": "string"},
    "Mkareeb": {"return_type": "eray", "feature": "string"},
    "XarafWeyn": {"return_type": "eray", "feature": "string"},
    "XarafYar": {"return_type": "eray", "feature": "string"},
    "sooRaadi": {"return_type": "tiro", "feature": "string"},
    "lagaHelay": {"return_type": "miyaa", "feature": "string"},
    "qaybi": {"return_type": "tix:eray", "feature": "string"},

    "tusmo_os_system": {"return_type": "tiro", "feature": "os"},
    "koobi": {"return_type": "waxbo", "feature": "os"},
    "nuqul": {"return_type": "waxbo", "feature": "os"},
    "u_dhaqaaji": {"return_type": "waxbo", "feature": "os"},
    "aqri_fayl": {"return_type": "eray", "feature": "os"},
    "qor_fayl": {"return_type": "waxbo", "feature": "os"},
    "isku_dar_waddo": {"return_type": "eray", "feature": "os"},
    "cabbir_fayl": {"return_type": "tiro", "feature": "os"},

    # Math Functions
    "tusmo_sin": {"return_type": "jajab", "feature": "math"},
    "tusmo_cos": {"return_type": "jajab", "feature": "math"},
    "tusmo_sqrt": {"return_type": "jajab", "feature": "math"},
    "tusmo_abs": {"return_type": "jajab", "feature": "math"},
    "tusmo_pow": {"return_type": "jajab", "feature": "math"},
    "tusmo_floor": {"return_type": "jajab", "feature": "math"},
    "tusmo_ceil": {"return_type": "jajab", "feature": "math"},
    "tusmo_round": {"return_type": "jajab", "feature": "math"},
}
