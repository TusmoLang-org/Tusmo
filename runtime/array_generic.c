#include "tusmo_runtime.h"

static inline void tusmo_hp_grow_if_needed(void** data, size_t* capacity, size_t new_size, size_t elem_size) {
    if (__builtin_expect(new_size > *capacity, 0)) {
        size_t new_capacity = (*capacity == 0) ? 8 : *capacity * 2;
        if (new_capacity < new_size) new_capacity = new_size;
        *data = GC_REALLOC(*data, new_capacity * elem_size);
        *capacity = new_capacity;
    }
}


// --- Implementation for the Generic Array ---

TusmoTixGeneric* tusmo_tix_generic_create(size_t cap) {
    TusmoTixGeneric* tix = GC_MALLOC(sizeof(TusmoTixGeneric));
    tix->data = GC_MALLOC(cap * sizeof(void*));
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_generic_append(TusmoTixGeneric* tix, void* value) {
    tusmo_hp_grow_if_needed((void**)&tix->data, &tix->capacity, tix->size + 1, sizeof(void*));
    tix->data[tix->size++] = value;
}

void tusmo_tix_generic_insert(TusmoTixGeneric* tix, size_t index, void* value) {
    if (index > tix->size) {
        fprintf(stderr, "Cilad: Tusmo, index-ka %zu wuu ka weyn yahay cabbirka %zu\n", index, tix->size);
        exit(1);
    }
    tusmo_hp_grow_if_needed((void**)&tix->data, &tix->capacity, tix->size + 1, sizeof(void*));
    if (index < tix->size) {
        memmove(&tix->data[index + 1], &tix->data[index], (tix->size - index) * sizeof(void*));
    }
    tix->data[index] = value;
    tix->size++;
}

void* tusmo_tix_generic_pop(TusmoTixGeneric* tix, size_t index) {
    if (index >= tix->size) {
        fprintf(stderr, "Cilad: Tusmo, index-ka %zu wuu ka baxsan yahay xadka %zu\n", index, tix->size);
        exit(1);
    }
    void* val = tix->data[index];
    if (index < tix->size - 1) {
        memmove(&tix->data[index], &tix->data[index + 1], (tix->size - 1 - index) * sizeof(void*));
    }
    tix->size--;
    return val;
}

bool tusmo_tix_generic_remove(TusmoTixGeneric* tix, void* value) {
    for (size_t i = 0; i < tix->size; i++) {
        if (tix->data[i] == value) {
            tusmo_tix_generic_pop(tix, i);
            return true;
        }
    }
    return false;
}