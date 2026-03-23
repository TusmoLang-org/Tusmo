// runtime/array.c

#include "tusmo_runtime.h"

size_t tusmo_bounds_check(size_t idx, size_t size) {
    if (idx >= size) {
        fprintf(stderr, "Cilad Farsamo: Waxaad dhaaftay Xudduudii ahyd => %zu Waxaad u talaabtay xuduuda => %zu  \n", size,idx);
        exit(1);
    }
    return idx;
}

static void tusmo_tix_data_finalizer(void* obj, void* client_data) {
    void** data_ptr = (void**)obj;
    if (*data_ptr) {
        free(*data_ptr);
        *data_ptr = NULL;
    }
}

static inline void tusmo_hp_grow_if_needed(void** data, size_t* capacity, size_t new_size, size_t elem_size) {
    if (__builtin_expect(new_size > *capacity, 0)) {
        size_t new_capacity = (*capacity == 0) ? 8 : *capacity * 2;
        if (new_capacity < new_size) new_capacity = new_size;
        *data = realloc(*data, new_capacity * elem_size);
        if (!*data) { perror("realloc failed"); exit(1); }
        *capacity = new_capacity;
    }
}

TusmoTixTiro* tusmo_hp_tix_tiro_create(size_t cap) {
    TusmoTixTiro* tix = GC_MALLOC(sizeof(TusmoTixTiro));
    tix->data = malloc(cap * sizeof(int));
    tix->size = 0; tix->capacity = cap;
    GC_REGISTER_FINALIZER(tix, tusmo_tix_data_finalizer, NULL, NULL, NULL);
    return tix;
}

TusmoTixEray* tusmo_hp_tix_eray_create(size_t cap) {
    TusmoTixEray* tix = GC_MALLOC(sizeof(TusmoTixEray));
    tix->data = malloc(cap * sizeof(char*));
    tix->size = 0; tix->capacity = cap;
    GC_REGISTER_FINALIZER(tix, tusmo_tix_data_finalizer, NULL, NULL, NULL);
    return tix;
}

TusmoTixJajab* tusmo_hp_tix_jajab_create(size_t cap) {
    TusmoTixJajab* tix = GC_MALLOC(sizeof(TusmoTixJajab));
    tix->data = malloc(cap * sizeof(double));
    tix->size = 0; tix->capacity = cap;
    GC_REGISTER_FINALIZER(tix, tusmo_tix_data_finalizer, NULL, NULL, NULL);
    return tix;
}

TusmoTixMiyaa* tusmo_hp_tix_miyaa_create(size_t cap) {
    TusmoTixMiyaa* tix = GC_MALLOC(sizeof(TusmoTixMiyaa));
    tix->data = malloc(cap * sizeof(bool));
    tix->size = 0; tix->capacity = cap;
    GC_REGISTER_FINALIZER(tix, tusmo_tix_data_finalizer, NULL, NULL, NULL);
    return tix;
}

TusmoTixXaraf* tusmo_hp_tix_xaraf_create(size_t cap) {
    TusmoTixXaraf* tix = GC_MALLOC(sizeof(TusmoTixXaraf));
    tix->data = malloc(cap * sizeof(char));
    tix->size = 0; tix->capacity = cap;
    GC_REGISTER_FINALIZER(tix, tusmo_tix_data_finalizer, NULL, NULL, NULL);
    return tix;
}

TusmoTixMixed* tusmo_tix_mixed_create(size_t initial_capacity) {
    TusmoTixMixed* tix = GC_MALLOC(sizeof(TusmoTixMixed));
    tix->data = GC_MALLOC(initial_capacity * sizeof(TusmoValue));
    tix->size = 0;
    tix->capacity = initial_capacity;
    return tix;
}

void tusmo_hp_tix_tiro_append(TusmoTixTiro* tix, int value) {
    tusmo_hp_grow_if_needed((void**)&tix->data, &tix->capacity, tix->size + 1, sizeof(int));
    tix->data[tix->size++] = value;
}

void tusmo_hp_tix_eray_append(TusmoTixEray* tix, char* value) {
    tusmo_hp_grow_if_needed((void**)&tix->data, &tix->capacity, tix->size + 1, sizeof(char*));
    tix->data[tix->size++] = value;
}

void tusmo_hp_tix_jajab_append(TusmoTixJajab* tix, double value) {
    tusmo_hp_grow_if_needed((void**)&tix->data, &tix->capacity, tix->size + 1, sizeof(double));
    tix->data[tix->size++] = value;
}

void tusmo_hp_tix_miyaa_append(TusmoTixMiyaa* tix, bool value) {
    tusmo_hp_grow_if_needed((void**)&tix->data, &tix->capacity, tix->size + 1, sizeof(bool));
    tix->data[tix->size++] = value;
}

void tusmo_hp_tix_xaraf_append(TusmoTixXaraf* tix, char value) {
    tusmo_hp_grow_if_needed((void**)&tix->data, &tix->capacity, tix->size + 1, sizeof(char));
    tix->data[tix->size++] = value;
}

void tusmo_tix_mixed_append(TusmoTixMixed* tix, TusmoValue value) {
    if (tix->size >= tix->capacity) {
        tix->capacity = (tix->capacity == 0) ? 8 : tix->capacity * 2;
        tix->data = GC_REALLOC(tix->data, tix->capacity * sizeof(TusmoValue));
    }
    tix->data[tix->size++] = value;
}

// --- Insert at Index ---

void tusmo_hp_tix_tiro_insert(TusmoTixTiro* tix, size_t index, int value) {
    if (index > tix->size) { // Allow inserting at end (index == size)
        fprintf(stderr, "tix_tiro_insert: index %zu out of bounds (size %zu)\n", index, tix->size);
        exit(1);
    }
    tusmo_hp_grow_if_needed((void**)&tix->data, &tix->capacity, tix->size + 1, sizeof(int));
    memmove(&tix->data[index + 1], &tix->data[index], (tix->size - index) * sizeof(int));
    tix->data[index] = value;
    tix->size++;
}

void tusmo_hp_tix_eray_insert(TusmoTixEray* tix, size_t index, char* value) {
    if (index > tix->size) {
        fprintf(stderr, "tix_eray_insert: index %zu out of bounds (size %zu)\n", index, tix->size);
        exit(1);
    }
    tusmo_hp_grow_if_needed((void**)&tix->data, &tix->capacity, tix->size + 1, sizeof(char*));
    memmove(&tix->data[index + 1], &tix->data[index], (tix->size - index) * sizeof(char*));
    tix->data[index] = value;
    tix->size++;
}

void tusmo_hp_tix_jajab_insert(TusmoTixJajab* tix, size_t index, double value) {
    if (index > tix->size) {
        fprintf(stderr, "tix_jajab_insert: index %zu out of bounds (size %zu)\n", index, tix->size);
        exit(1);
    }
    tusmo_hp_grow_if_needed((void**)&tix->data, &tix->capacity, tix->size + 1, sizeof(double));
    memmove(&tix->data[index + 1], &tix->data[index], (tix->size - index) * sizeof(double));
    tix->data[index] = value;
    tix->size++;
}

void tusmo_hp_tix_miyaa_insert(TusmoTixMiyaa* tix, size_t index, bool value) {
    if (index > tix->size) {
        fprintf(stderr, "tix_miyaa_insert: index %zu out of bounds (size %zu)\n", index, tix->size);
        exit(1);
    }
    tusmo_hp_grow_if_needed((void**)&tix->data, &tix->capacity, tix->size + 1, sizeof(bool));
    memmove(&tix->data[index + 1], &tix->data[index], (tix->size - index) * sizeof(bool));
    tix->data[index] = value;
    tix->size++;
}

void tusmo_hp_tix_xaraf_insert(TusmoTixXaraf* tix, size_t index, char value) {
    if (index > tix->size) {
        fprintf(stderr, "tix_xaraf_insert: index %zu out of bounds (size %zu)\n", index, tix->size);
        exit(1);
    }
    tusmo_hp_grow_if_needed((void**)&tix->data, &tix->capacity, tix->size + 1, sizeof(char));
    memmove(&tix->data[index + 1], &tix->data[index], (tix->size - index) * sizeof(char));
    tix->data[index] = value;
    tix->size++;
}

void tusmo_tix_mixed_insert(TusmoTixMixed* tix, size_t index, TusmoValue value) {
    if (index > tix->size) {
        fprintf(stderr, "tix_mixed_insert: index %zu out of bounds (size %zu)\n", index, tix->size);
        exit(1);
    }
    if (tix->size >= tix->capacity) {
        tix->capacity = (tix->capacity == 0) ? 8 : tix->capacity * 2;
        tix->data = GC_REALLOC(tix->data, tix->capacity * sizeof(TusmoValue));
    }
    memmove(&tix->data[index + 1], &tix->data[index], (tix->size - index) * sizeof(TusmoValue));
    tix->data[index] = value;
    tix->size++;
}

// --- Remove by Index (Pop) ---

int tusmo_hp_tix_tiro_pop(TusmoTixTiro* tix, size_t index) {
    if (index >= tix->size) {
        fprintf(stderr, "tix_tiro_pop: index %zu out of range\n", index);
        exit(1);
    }
    int value = tix->data[index];
    memmove(&tix->data[index], &tix->data[index + 1], (tix->size - index - 1) * sizeof(int));
    tix->size--;
    return value;
}

char* tusmo_hp_tix_eray_pop(TusmoTixEray* tix, size_t index) {
    if (index >= tix->size) {
        fprintf(stderr, "tix_eray_pop: index %zu out of range\n", index);
        exit(1);
    }
    char* value = tix->data[index];
    memmove(&tix->data[index], &tix->data[index + 1], (tix->size - index - 1) * sizeof(char*));
    tix->size--;
    return value;
}

double tusmo_hp_tix_jajab_pop(TusmoTixJajab* tix, size_t index) {
    if (index >= tix->size) {
        fprintf(stderr, "tix_jajab_pop: index %zu out of range\n", index);
        exit(1);
    }
    double value = tix->data[index];
    memmove(&tix->data[index], &tix->data[index + 1], (tix->size - index - 1) * sizeof(double));
    tix->size--;
    return value;
}

bool tusmo_hp_tix_miyaa_pop(TusmoTixMiyaa* tix, size_t index) {
    if (index >= tix->size) {
        fprintf(stderr, "tix_miyaa_pop: index %zu out of range\n", index);
        exit(1);
    }
    bool value = tix->data[index];
    memmove(&tix->data[index], &tix->data[index + 1], (tix->size - index - 1) * sizeof(bool));
    tix->size--;
    return value;
}

char tusmo_hp_tix_xaraf_pop(TusmoTixXaraf* tix, size_t index) {
    if (index >= tix->size) {
        fprintf(stderr, "tix_xaraf_pop: index %zu out of range\n", index);
        exit(1);
    }
    char value = tix->data[index];
    memmove(&tix->data[index], &tix->data[index + 1], (tix->size - index - 1) * sizeof(char));
    tix->size--;
    return value;
}

TusmoValue tusmo_tix_mixed_pop(TusmoTixMixed* tix, size_t index) {
    if (index >= tix->size) {
        fprintf(stderr, ": index %zu out of range\n", index);
        exit(1);
    }
    TusmoValue value = tix->data[index];
    memmove(&tix->data[index], &tix->data[index + 1], (tix->size - index - 1) * sizeof(TusmoValue));
    tix->size--;
    return value;
}

TusmoValue tusmo_tix_mixed_get(TusmoTixMixed* tix, size_t index) {
    if (index >= tix->size) {
        fprintf(stderr, "Index %zu out of range\n", index);
        exit(1);
    }
    return tix->data[index];
}

// --- Generic Nested Array Access ---
// Handles type-switching for accessing elements of arrays stored in TusmoValue.
// This is needed for dynamic arrays (tix) that contain typed nested arrays.
TusmoValue tusmo_tix_mixed_get_nested(TusmoValue arr_val, size_t index) {
    switch (arr_val.type) {
        case TUSMO_TIX:
            return tusmo_tix_mixed_get(arr_val.value.as_tix, index);
        case TUSMO_TIX_TIRO:
            return (TusmoValue){.type = TUSMO_TIRO, .value.as_tiro = arr_val.value.as_tiro_tix->data[index]};
        case TUSMO_TIX_ERAY:
            return (TusmoValue){.type = TUSMO_ERAY, .value.as_eray = arr_val.value.as_eray_tix->data[index]};
        case TUSMO_TIX_JAJAB:
            return (TusmoValue){.type = TUSMO_JAJAB, .value.as_jajab = arr_val.value.as_jajab_tix->data[index]};
        case TUSMO_TIX_MIYAA:
            return (TusmoValue){.type = TUSMO_MIYAA, .value.as_miyaa = arr_val.value.as_miyaa_tix->data[index]};
        case TUSMO_TIX_XARAF:
            return (TusmoValue){.type = TUSMO_XARAF, .value.as_xaraf = arr_val.value.as_xaraf_tix->data[index]};
        case TUSMO_TIX_TIRO_NESTED:
            return (TusmoValue){.type = TUSMO_TIX_TIRO, .value.as_tiro_tix = arr_val.value.as_tiro_nested->data[index]};
        case TUSMO_TIX_ERAY_NESTED:
            return (TusmoValue){.type = TUSMO_TIX_ERAY, .value.as_eray_tix = arr_val.value.as_eray_nested->data[index]};
        case TUSMO_TIX_JAJAB_NESTED:
            return (TusmoValue){.type = TUSMO_TIX_JAJAB, .value.as_jajab_tix = arr_val.value.as_jajab_nested->data[index]};
        case TUSMO_TIX_MIYAA_NESTED:
            return (TusmoValue){.type = TUSMO_TIX_MIYAA, .value.as_miyaa_tix = arr_val.value.as_miyaa_nested->data[index]};
        case TUSMO_TIX_XARAF_NESTED:
            return (TusmoValue){.type = TUSMO_TIX_XARAF, .value.as_xaraf_tix = arr_val.value.as_xaraf_nested->data[index]};
        case TUSMO_TIX_TIRO_NESTED2:
            return (TusmoValue){.type = TUSMO_TIX_TIRO_NESTED, .value.as_tiro_nested = arr_val.value.as_tiro_nested2->data[index]};
        case TUSMO_TIX_ERAY_NESTED2:
            return (TusmoValue){.type = TUSMO_TIX_ERAY_NESTED, .value.as_eray_nested = arr_val.value.as_eray_nested2->data[index]};
        case TUSMO_TIX_JAJAB_NESTED2:
            return (TusmoValue){.type = TUSMO_TIX_JAJAB_NESTED, .value.as_jajab_nested = arr_val.value.as_jajab_nested2->data[index]};
        case TUSMO_TIX_MIYAA_NESTED2:
            return (TusmoValue){.type = TUSMO_TIX_MIYAA_NESTED, .value.as_miyaa_nested = arr_val.value.as_miyaa_nested2->data[index]};
        case TUSMO_TIX_XARAF_NESTED2:
            return (TusmoValue){.type = TUSMO_TIX_XARAF_NESTED, .value.as_xaraf_nested = arr_val.value.as_xaraf_nested2->data[index]};
        default:
            fprintf(stderr, "Unsupported array type for nested access: %d\n", arr_val.type);
            exit(1);
    }
}

// --- Remove by Value ---

bool tusmo_hp_tix_tiro_remove(TusmoTixTiro* tix, int value) {
    for (size_t i = 0; i < tix->size; i++) {
        if (tix->data[i] == value) {
            tusmo_hp_tix_tiro_pop(tix, i);
            return true;
        }
    }
    return false;
}

bool tusmo_hp_tix_eray_remove(TusmoTixEray* tix, char* value) {
    for (size_t i = 0; i < tix->size; i++) {
        if (strcmp(tix->data[i], value) == 0) {
            tusmo_hp_tix_eray_pop(tix, i);
            return true;
        }
    }
    return false;
}

bool tusmo_hp_tix_jajab_remove(TusmoTixJajab* tix, double value) {
    for (size_t i = 0; i < tix->size; i++) {
        if (tix->data[i] == value) {
            tusmo_hp_tix_jajab_pop(tix, i);
            return true;
        }
    }
    return false;
}

bool tusmo_hp_tix_miyaa_remove(TusmoTixMiyaa* tix, bool value) {
    for (size_t i = 0; i < tix->size; i++) {
        if (tix->data[i] == value) {
            tusmo_hp_tix_miyaa_pop(tix, i);
            return true;
        }
    }
    return false;
}

bool tusmo_hp_tix_xaraf_remove(TusmoTixXaraf* tix, char value) {
    for (size_t i = 0; i < tix->size; i++) {
        if (tix->data[i] == value) {
            tusmo_hp_tix_xaraf_pop(tix, i);
            return true;
        }
    }
    return false;
}

// Helper for mixed value equality
static bool tusmo_values_equal(TusmoValue a, TusmoValue b) {
    if (a.type != b.type) return false;
    switch (a.type) {
        case TUSMO_TIRO: return a.value.as_tiro == b.value.as_tiro;
        case TUSMO_JAJAB: return a.value.as_jajab == b.value.as_jajab;
        case TUSMO_ERAY: return strcmp(a.value.as_eray, b.value.as_eray) == 0;
        case TUSMO_MIYAA: return a.value.as_miyaa == b.value.as_miyaa;
        case TUSMO_XARAF: return a.value.as_xaraf == b.value.as_xaraf;
        case TUSMO_WAXBA: return true;
        default: return false; // Complex types (arrays/dicts) not supported for simple equality yet
    }
}

bool tusmo_tix_mixed_remove(TusmoTixMixed* tix, TusmoValue value) {
    for (size_t i = 0; i < tix->size; i++) {
        if (tusmo_values_equal(tix->data[i], value)) {
            tusmo_tix_mixed_pop(tix, i);
            return true;
        }
    }
    return false;
}

// ============================================================================
// --- NESTED ARRAY IMPLEMENTATIONS (Option 4: Type-specific nested arrays) ---
// These use GC-tracked pointers (TusmoTixTiro**, TusmoTixTiro***, etc.)
// so that Boehm GC can trace and update pointers when objects move.
// ============================================================================

// --- Helper macro for growing nested arrays ---
#define TUSMO_NESTED_GROW(tix, elem_type) \
    if (tix->size >= tix->capacity) { \
        size_t new_cap = tix->capacity == 0 ? 8 : tix->capacity * 2; \
        tix->data = GC_REALLOC(tix->data, new_cap * sizeof(elem_type)); \
        tix->capacity = new_cap; \
    }

// ============================================================================
// --- 2D NESTED ARRAYS (TusmoTixXXXNested) ---
// Holds pointers to 1D typed arrays (e.g., TusmoTixTiro** = array of TusmoTixTiro*)
// ============================================================================

// TusmoTixTiroNested - 2D array of integers
TusmoTixTiroNested* tusmo_tix_tiro_nested_create(size_t cap) {
    TusmoTixTiroNested* tix = GC_MALLOC(sizeof(TusmoTixTiroNested));
    tix->data = cap > 0 ? GC_MALLOC(cap * sizeof(TusmoTixTiro*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_tiro_nested_append(TusmoTixTiroNested* tix, TusmoTixTiro* value) {
    TUSMO_NESTED_GROW(tix, TusmoTixTiro*);
    tix->data[tix->size++] = value;
}

// TusmoTixErayNested - 2D array of strings
TusmoTixErayNested* tusmo_tix_eray_nested_create(size_t cap) {
    TusmoTixErayNested* tix = GC_MALLOC(sizeof(TusmoTixErayNested));
    tix->data = cap > 0 ? GC_MALLOC(cap * sizeof(TusmoTixEray*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_eray_nested_append(TusmoTixErayNested* tix, TusmoTixEray* value) {
    TUSMO_NESTED_GROW(tix, TusmoTixEray*);
    tix->data[tix->size++] = value;
}

// TusmoTixJajabNested - 2D array of floats
TusmoTixJajabNested* tusmo_tix_jajab_nested_create(size_t cap) {
    TusmoTixJajabNested* tix = GC_MALLOC(sizeof(TusmoTixJajabNested));
    tix->data = cap > 0 ? GC_MALLOC(cap * sizeof(TusmoTixJajab*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_jajab_nested_append(TusmoTixJajabNested* tix, TusmoTixJajab* value) {
    TUSMO_NESTED_GROW(tix, TusmoTixJajab*);
    tix->data[tix->size++] = value;
}

// TusmoTixMiyaaNested - 2D array of booleans
TusmoTixMiyaaNested* tusmo_tix_miyaa_nested_create(size_t cap) {
    TusmoTixMiyaaNested* tix = GC_MALLOC(sizeof(TusmoTixMiyaaNested));
    tix->data = cap > 0 ? GC_MALLOC(cap * sizeof(TusmoTixMiyaa*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_miyaa_nested_append(TusmoTixMiyaaNested* tix, TusmoTixMiyaa* value) {
    TUSMO_NESTED_GROW(tix, TusmoTixMiyaa*);
    tix->data[tix->size++] = value;
}

// TusmoTixXarafNested - 2D array of chars
TusmoTixXarafNested* tusmo_tix_xaraf_nested_create(size_t cap) {
    TusmoTixXarafNested* tix = GC_MALLOC(sizeof(TusmoTixXarafNested));
    tix->data = cap > 0 ? GC_MALLOC(cap * sizeof(TusmoTixXaraf*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_xaraf_nested_append(TusmoTixXarafNested* tix, TusmoTixXaraf* value) {
    TUSMO_NESTED_GROW(tix, TusmoTixXaraf*);
    tix->data[tix->size++] = value;
}

// ============================================================================
// --- 3D NESTED ARRAYS (TusmoTixXXXNested2) ---
// Holds pointers to 2D nested arrays (e.g., TusmoTixTiroNested**)
// ============================================================================

// TusmoTixTiroNested2 - 3D array of integers
TusmoTixTiroNested2* tusmo_tix_tiro_nested2_create(size_t cap) {
    TusmoTixTiroNested2* tix = GC_MALLOC(sizeof(TusmoTixTiroNested2));
    tix->data = cap > 0 ? GC_MALLOC(cap * sizeof(TusmoTixTiroNested*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_tiro_nested2_append(TusmoTixTiroNested2* tix, TusmoTixTiroNested* value) {
    if (tix->size >= tix->capacity) {
        size_t new_cap = tix->capacity == 0 ? 8 : tix->capacity * 2;
        tix->data = GC_REALLOC(tix->data, new_cap * sizeof(TusmoTixTiroNested*));
        tix->capacity = new_cap;
    }
    tix->data[tix->size++] = value;
}

// TusmoTixErayNested2 - 3D array of strings
TusmoTixErayNested2* tusmo_tix_eray_nested2_create(size_t cap) {
    TusmoTixErayNested2* tix = GC_MALLOC(sizeof(TusmoTixErayNested2));
    tix->data = cap > 0 ? GC_MALLOC(cap * sizeof(TusmoTixErayNested*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_eray_nested2_append(TusmoTixErayNested2* tix, TusmoTixErayNested* value) {
    if (tix->size >= tix->capacity) {
        size_t new_cap = tix->capacity == 0 ? 8 : tix->capacity * 2;
        tix->data = GC_REALLOC(tix->data, new_cap * sizeof(TusmoTixErayNested*));
        tix->capacity = new_cap;
    }
    tix->data[tix->size++] = value;
}

// TusmoTixJajabNested2 - 3D array of floats
TusmoTixJajabNested2* tusmo_tix_jajab_nested2_create(size_t cap) {
    TusmoTixJajabNested2* tix = GC_MALLOC(sizeof(TusmoTixJajabNested2));
    tix->data = cap > 0 ? GC_MALLOC(cap * sizeof(TusmoTixJajabNested*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_jajab_nested2_append(TusmoTixJajabNested2* tix, TusmoTixJajabNested* value) {
    if (tix->size >= tix->capacity) {
        size_t new_cap = tix->capacity == 0 ? 8 : tix->capacity * 2;
        tix->data = GC_REALLOC(tix->data, new_cap * sizeof(TusmoTixJajabNested*));
        tix->capacity = new_cap;
    }
    tix->data[tix->size++] = value;
}

// TusmoTixMiyaaNested2 - 3D array of booleans
TusmoTixMiyaaNested2* tusmo_tix_miyaa_nested2_create(size_t cap) {
    TusmoTixMiyaaNested2* tix = GC_MALLOC(sizeof(TusmoTixMiyaaNested2));
    tix->data = cap > 0 ? GC_MALLOC(cap * sizeof(TusmoTixMiyaaNested*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_miyaa_nested2_append(TusmoTixMiyaaNested2* tix, TusmoTixMiyaaNested* value) {
    if (tix->size >= tix->capacity) {
        size_t new_cap = tix->capacity == 0 ? 8 : tix->capacity * 2;
        tix->data = GC_REALLOC(tix->data, new_cap * sizeof(TusmoTixMiyaaNested*));
        tix->capacity = new_cap;
    }
    tix->data[tix->size++] = value;
}

// TusmoTixXarafNested2 - 3D array of chars
TusmoTixXarafNested2* tusmo_tix_xaraf_nested2_create(size_t cap) {
    TusmoTixXarafNested2* tix = GC_MALLOC(sizeof(TusmoTixXarafNested2));
    tix->data = cap > 0 ? GC_MALLOC(cap * sizeof(TusmoTixXarafNested*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_xaraf_nested2_append(TusmoTixXarafNested2* tix, TusmoTixXarafNested* value) {
    if (tix->size >= tix->capacity) {
        size_t new_cap = tix->capacity == 0 ? 8 : tix->capacity * 2;
        tix->data = GC_REALLOC(tix->data, new_cap * sizeof(TusmoTixXarafNested*));
        tix->capacity = new_cap;
    }
    tix->data[tix->size++] = value;
}
