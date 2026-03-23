// runtime/io.c

#include "tusmo_runtime.h"
#include <math.h>


// --- Generic Printing Implementations ---
void prints_tix_tiro(TusmoTixTiro* tix) {
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        printf("%d", tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_eray(TusmoTixEray* tix) {
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        printf("\"%s\"", tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_jajab(TusmoTixJajab* tix) {
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        printf("%f", tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_miyaa(TusmoTixMiyaa* tix) {
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        printf(tix->data[i] ? "true" : "false");
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_xaraf(TusmoTixXaraf* tix) {
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        printf("'%c'", tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_mixed(TusmoTixMixed* tix) {
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        tusmo_qor_dynamic_value(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

static int is_valid_ptr(void* ptr) {
    if (ptr == NULL) return 0;
    uintptr_t addr = (uintptr_t)ptr;
    if (addr < 4096) return 0;
    return 1;
}



void prints_tix_generic(void* tix_ptr) {
    if (tix_ptr == NULL) {
        printf("NULL");
        return;
    }
    
    // Try as TusmoTixMixed first
    TusmoTixMixed* as_mixed = (TusmoTixMixed*)tix_ptr;
    if (as_mixed->data != NULL && as_mixed->size > 0 && as_mixed->size < 100000) {
        TusmoValue* first_elem = &as_mixed->data[0];
        if (first_elem->type >= 0 && first_elem->type <= 20) {
            prints_tix_mixed(as_mixed);
            return;
        }
    }
    
    // Treat as TusmoTixGeneric
    TusmoTixGeneric* tix = (TusmoTixGeneric*)tix_ptr;
    if (tix->data == NULL || tix->size == 0) {
        printf("[]");
        return;
    }
    
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        if (i > 0) printf(", ");
        void* elem = tix->data[i];
        if (elem == NULL) {
            printf("null");
            continue;
        }
        
        // Try each known type - just check if data pointer is valid
        // 3D nested arrays
        TusmoTixTiroNested2* as_tiro_nested2 = (TusmoTixTiroNested2*)elem;
        if (as_tiro_nested2->data != NULL && as_tiro_nested2->size > 0) {
            prints_tix_tiro_nested2(as_tiro_nested2);
            continue;
        }
        TusmoTixErayNested2* as_eray_nested2 = (TusmoTixErayNested2*)elem;
        if (as_eray_nested2->data != NULL && as_eray_nested2->size > 0) {
            prints_tix_eray_nested2(as_eray_nested2);
            continue;
        }
        
        // 2D nested arrays
        TusmoTixTiroNested* as_tiro_nested = (TusmoTixTiroNested*)elem;
        if (as_tiro_nested->data != NULL && as_tiro_nested->size > 0) {
            prints_tix_tiro_nested(as_tiro_nested);
            continue;
        }
        TusmoTixErayNested* as_eray_nested = (TusmoTixErayNested*)elem;
        if (as_eray_nested->data != NULL && as_eray_nested->size > 0) {
            prints_tix_eray_nested(as_eray_nested);
            continue;
        }
        
        // 1D arrays
        TusmoTixTiro* as_tiro = (TusmoTixTiro*)elem;
        if (as_tiro->data != NULL && as_tiro->size > 0) {
            prints_tix_tiro(as_tiro);
            continue;
        }
        TusmoTixEray* as_eray = (TusmoTixEray*)elem;
        if (as_eray->data != NULL && as_eray->size > 0) {
            prints_tix_eray(as_eray);
            continue;
        }
        TusmoTixJajab* as_jajab = (TusmoTixJajab*)elem;
        if (as_jajab->data != NULL && as_jajab->size > 0) {
            prints_tix_jajab(as_jajab);
            continue;
        }
        TusmoTixMiyaa* as_miyaa = (TusmoTixMiyaa*)elem;
        if (as_miyaa->data != NULL && as_miyaa->size > 0) {
            prints_tix_miyaa(as_miyaa);
            continue;
        }
        TusmoTixXaraf* as_xaraf = (TusmoTixXaraf*)elem;
        if (as_xaraf->data != NULL && as_xaraf->size > 0) {
            prints_tix_xaraf(as_xaraf);
            continue;
        }
        
        // Fallback
        printf("<unknown>");
    }
    printf("]");
}

// ============================================================================
// --- NESTED ARRAY PRINTING (Option 4: Type-specific, no GC issues) ---
// Each nested type has its own print function with known element types.
// GC-traced pointers mean data is always valid.
// ============================================================================

// --- 2D Nested Array Printing ---
// Each element is a typed 1D array pointer, so we can call prints_tix_xxx directly

void prints_tix_tiro_nested(TusmoTixTiroNested* tix) {
    if (tix == NULL || tix->data == NULL) {
        printf("[]");
        return;
    }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_tiro(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_eray_nested(TusmoTixErayNested* tix) {
    if (tix == NULL || tix->data == NULL) {
        printf("[]");
        return;
    }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_eray(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_jajab_nested(TusmoTixJajabNested* tix) {
    if (tix == NULL || tix->data == NULL) {
        printf("[]");
        return;
    }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_jajab(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_miyaa_nested(TusmoTixMiyaaNested* tix) {
    if (tix == NULL || tix->data == NULL) {
        printf("[]");
        return;
    }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_miyaa(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_xaraf_nested(TusmoTixXarafNested* tix) {
    if (tix == NULL || tix->data == NULL) {
        printf("[]");
        return;
    }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_xaraf(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

// --- 3D Nested Array Printing ---
// Each element is a 2D nested array pointer

void prints_tix_tiro_nested2(TusmoTixTiroNested2* tix) {
    if (tix == NULL || tix->data == NULL) {
        printf("[]");
        return;
    }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_tiro_nested(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_eray_nested2(TusmoTixErayNested2* tix) {
    if (tix == NULL || tix->data == NULL) {
        printf("[]");
        return;
    }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_eray_nested(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_jajab_nested2(TusmoTixJajabNested2* tix) {
    if (tix == NULL || tix->data == NULL) {
        printf("[]");
        return;
    }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_jajab_nested(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_miyaa_nested2(TusmoTixMiyaaNested2* tix) {
    if (tix == NULL || tix->data == NULL) {
        printf("[]");
        return;
    }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_miyaa_nested(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_xaraf_nested2(TusmoTixXarafNested2* tix) {
    if (tix == NULL || tix->data == NULL) {
        printf("[]");
        return;
    }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_xaraf_nested(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void tusmo_qor_dynamic_value(TusmoValue val) {
    switch (val.type) {
        case TUSMO_TIRO:  printf("%d", val.value.as_tiro); break;
        case TUSMO_ERAY:  printf("%s", val.value.as_eray); break;
        case TUSMO_JAJAB: printf("%f", val.value.as_jajab); break;
        case TUSMO_MIYAA: printf(val.value.as_miyaa ? "run" : "been"); break;
        case TUSMO_XARAF: printf("%c", val.value.as_xaraf); break;
        case TUSMO_QAAMUUS: tusmo_qaamuus_print(val.value.as_qaamuus); break;
        case TUSMO_TIX:  prints_tix_mixed(val.value.as_tix); break;
        case TUSMO_WAXBA: printf("waxba"); break;
        // Typed 1D arrays
        case TUSMO_TIX_TIRO: prints_tix_tiro(val.value.as_tiro_tix); break;
        case TUSMO_TIX_ERAY: prints_tix_eray(val.value.as_eray_tix); break;
        case TUSMO_TIX_JAJAB: prints_tix_jajab(val.value.as_jajab_tix); break;
        case TUSMO_TIX_MIYAA: prints_tix_miyaa(val.value.as_miyaa_tix); break;
        case TUSMO_TIX_XARAF: prints_tix_xaraf(val.value.as_xaraf_tix); break;
        // Nested 2D arrays
        case TUSMO_TIX_TIRO_NESTED: prints_tix_tiro_nested(val.value.as_tiro_nested); break;
        case TUSMO_TIX_ERAY_NESTED: prints_tix_eray_nested(val.value.as_eray_nested); break;
        case TUSMO_TIX_JAJAB_NESTED: prints_tix_jajab_nested(val.value.as_jajab_nested); break;
        case TUSMO_TIX_MIYAA_NESTED: prints_tix_miyaa_nested(val.value.as_miyaa_nested); break;
        case TUSMO_TIX_XARAF_NESTED: prints_tix_xaraf_nested(val.value.as_xaraf_nested); break;
        // Nested 3D arrays
        case TUSMO_TIX_TIRO_NESTED2: prints_tix_tiro_nested2(val.value.as_tiro_nested2); break;
        case TUSMO_TIX_ERAY_NESTED2: prints_tix_eray_nested2(val.value.as_eray_nested2); break;
        case TUSMO_TIX_JAJAB_NESTED2: prints_tix_jajab_nested2(val.value.as_jajab_nested2); break;
        case TUSMO_TIX_MIYAA_NESTED2: prints_tix_miyaa_nested2(val.value.as_miyaa_nested2); break;
        case TUSMO_TIX_XARAF_NESTED2: prints_tix_xaraf_nested2(val.value.as_xaraf_nested2); break;
        default:          printf("<nooc aan la aqoon>"); break;
    }
}

char* hel_str(void) {
    size_t size = 100;
    size_t len = 0;
    char* buffer = malloc(size);

    if (buffer == NULL) return NULL;

    int c;
    while ((c = getchar()) != '\n' && c != EOF) {
        buffer[len++] = c;

        if (len == size) {
            size *= 2;
            char* new_buffer = realloc(buffer, size);
            if (!new_buffer) {
                free(buffer);
                return NULL;
            }
            buffer = new_buffer;
        }
    }

    buffer[len] = '\0';
    return buffer;
}
