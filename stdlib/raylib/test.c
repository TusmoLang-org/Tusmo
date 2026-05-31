#ifndef TUSMO_CORE_TYPES_H
#define TUSMO_CORE_TYPES_H
#define TUSMO_TYPES_H
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdarg.h>

// Forward declarations
struct TusmoQaamuus;
typedef struct TusmoTixMixed TusmoTixMixed;
typedef struct TusmoTixGeneric TusmoTixGeneric;
typedef struct TusmoTixTiro TusmoTixTiro;
typedef struct TusmoTixEray TusmoTixEray;
typedef struct TusmoTixJajab TusmoTixJajab;
typedef struct TusmoTixMiyaa TusmoTixMiyaa;
typedef struct TusmoTixXaraf TusmoTixXaraf;
typedef struct TusmoTixTiroNested TusmoTixTiroNested;
typedef struct TusmoTixErayNested TusmoTixErayNested;
typedef struct TusmoTixJajabNested TusmoTixJajabNested;
typedef struct TusmoTixMiyaaNested TusmoTixMiyaaNested;
typedef struct TusmoTixXarafNested TusmoTixXarafNested;
typedef struct TusmoTixTiroNested2 TusmoTixTiroNested2;
typedef struct TusmoTixErayNested2 TusmoTixErayNested2;
typedef struct TusmoTixJajabNested2 TusmoTixJajabNested2;
typedef struct TusmoTixMiyaaNested2 TusmoTixMiyaaNested2;
typedef struct TusmoTixXarafNested2 TusmoTixXarafNested2;

typedef enum {
    TUSMO_TIRO, TUSMO_ERAY, TUSMO_JAJAB, TUSMO_MIYAA, TUSMO_XARAF,
    TUSMO_QAAMUUS, TUSMO_TIX, TUSMO_WAXBA,
    TUSMO_TIX_TIRO, TUSMO_TIX_ERAY, TUSMO_TIX_JAJAB, TUSMO_TIX_MIYAA, TUSMO_TIX_XARAF,
    TUSMO_TIX_TIRO_NESTED, TUSMO_TIX_ERAY_NESTED, TUSMO_TIX_JAJAB_NESTED,
    TUSMO_TIX_MIYAA_NESTED, TUSMO_TIX_XARAF_NESTED,
    TUSMO_TIX_TIRO_NESTED2, TUSMO_TIX_ERAY_NESTED2, TUSMO_TIX_JAJAB_NESTED2,
    TUSMO_TIX_MIYAA_NESTED2, TUSMO_TIX_XARAF_NESTED2
} TusmoType;

typedef struct TusmoValue {
    TusmoType type;
    union {
        int as_tiro;
        char* as_eray;
        double as_jajab;
        bool as_miyaa;
        char as_xaraf;
        void* as_waxba;
        struct TusmoQaamuus* as_qaamuus;
        TusmoTixMixed* as_tix;
        TusmoTixTiro* as_tiro_tix;
        TusmoTixEray* as_eray_tix;
        TusmoTixJajab* as_jajab_tix;
        TusmoTixMiyaa* as_miyaa_tix;
        TusmoTixXaraf* as_xaraf_tix;
        TusmoTixTiroNested* as_tiro_nested;
        TusmoTixErayNested* as_eray_nested;
        TusmoTixJajabNested* as_jajab_nested;
        TusmoTixMiyaaNested* as_miyaa_nested;
        TusmoTixXarafNested* as_xaraf_nested;
        TusmoTixTiroNested2* as_tiro_nested2;
        TusmoTixErayNested2* as_eray_nested2;
        TusmoTixJajabNested2* as_jajab_nested2;
        TusmoTixMiyaaNested2* as_miyaa_nested2;
        TusmoTixXarafNested2* as_xaraf_nested2;
    } value;
} TusmoValue;

// Structs definitions
typedef struct TusmoTixTiro { int* data; size_t size; size_t capacity; } TusmoTixTiro;
typedef struct TusmoTixEray { char** data; size_t size; size_t capacity; } TusmoTixEray;
typedef struct TusmoTixJajab { double* data; size_t size; size_t capacity; } TusmoTixJajab;
typedef struct TusmoTixMiyaa { bool* data; size_t size; size_t capacity; } TusmoTixMiyaa;
typedef struct TusmoTixXaraf { char* data; size_t size; size_t capacity; } TusmoTixXaraf;
typedef struct TusmoTixMixed { TusmoValue* data; size_t size; size_t capacity; } TusmoTixMixed;
typedef struct TusmoTixGeneric { void** data; size_t size; size_t capacity; } TusmoTixGeneric;

typedef struct TusmoTixTiroNested { TusmoTixTiro** data; size_t size; size_t capacity; } TusmoTixTiroNested;
typedef struct TusmoTixErayNested { TusmoTixEray** data; size_t size; size_t capacity; } TusmoTixErayNested;
typedef struct TusmoTixJajabNested { TusmoTixJajab** data; size_t size; size_t capacity; } TusmoTixJajabNested;
typedef struct TusmoTixMiyaaNested { TusmoTixMiyaa** data; size_t size; size_t capacity; } TusmoTixMiyaaNested;
typedef struct TusmoTixXarafNested { TusmoTixXaraf** data; size_t size; size_t capacity; } TusmoTixXarafNested;

typedef struct TusmoTixTiroNested2 { TusmoTixTiroNested** data; size_t size; size_t capacity; } TusmoTixTiroNested2;
typedef struct TusmoTixErayNested2 { TusmoTixErayNested** data; size_t size; size_t capacity; } TusmoTixErayNested2;
typedef struct TusmoTixJajabNested2 { TusmoTixJajabNested** data; size_t size; size_t capacity; } TusmoTixJajabNested2;
typedef struct TusmoTixMiyaaNested2 { TusmoTixMiyaaNested** data; size_t size; size_t capacity; } TusmoTixMiyaaNested2;
typedef struct TusmoTixXarafNested2 { TusmoTixXarafNested** data; size_t size; size_t capacity; } TusmoTixXarafNested2;

typedef struct TusmoQaamuusEntry {
    char* key;
    TusmoValue value;
    struct TusmoQaamuusEntry* next;
} TusmoQaamuusEntry;

typedef struct TusmoQaamuus {
    TusmoQaamuusEntry** entries;
    size_t capacity;
    size_t count;
} TusmoQaamuus;

// Safety macros
#define TUSMO_SAFE_DIV(a, b, f, l) \
    ((b) == 0 ? (fprintf(stderr, "\n\033[1;31m[!] CILAD SOCDAALKA:\033[0m Isku day inaad u qaybiso 0! (Division by zero)\n\033[90m" "---------------------------------------------" "\033[0m\n\033[94mFaylka:\033[0m   %s\n\033[94mSaddarka:\033[0m %d\n\033[1;35m// Xisaabtaada dib u baro! Sidee 0 wax ugu qaybin kartaa?\033[0m\n", f, l), exit(1), (a)) : ((a) / (b)))

#define TUSMO_SAFE_MOD(a, b, f, l) \
    ((b) == 0 ? (fprintf(stderr, "\n\033[1;31m[!] CILAD SOCDAALKA:\033[0m Isku day inaad %s (modulo) ka qaado 0! (Modulo by zero)\n\033[90m" "---------------------------------------------" "\033[0m\n\033[94mFaylka:\033[0m   %s\n\033[94mSaddarka:\033[0m %d\n\033[1;35m// 0 waxba kama soo haro marka la qaybiyo! Dib u eeg.\033[0m\n", "%", f, l), exit(1), (a)) : ((a) % (b)))

#define TUSMO_SAFE_ACCESS(p, f, l) (p)
#endif // TUSMO_CORE_TYPES_H

typedef struct {
    double x;
    double y;
} Boos2D;

typedef struct {
    char r;
    char g;
    char b;
    char a;
} Midab;

typedef struct {
    double x;
    double y;
    double width;
    double height;
} AfarGees;

char* XarafWeyn(char* s);
char* XarafYar(char* s);
char* kaReeb(char* s);
char* Bkareeb(char* s);
char* Mkareeb(char* s);
char* kuBadal(char* s, char* d, char* c);
int sooRaadi(char* s, char* d);
bool lagaHelay(char* s, char* d);
TusmoTixEray* qaybi(char* s, char* d);
bool majiraa(TusmoQaamuus* q, char* fure);
void tir(TusmoQaamuus* q, char* fure);
char* nooc(TusmoValue x);
int dherer(TusmoValue x);
char* eray(TusmoValue x);
int tiro(TusmoValue x);
double jajab(TusmoValue x);
bool miyaa(TusmoValue x);
int qor_tiro(char x);
char qor_xaraf(int x);
int uguYar(int a, int b);
int uguWeyn(int a, int b);
int qaado(int x);
void jooji(int code);
bool daaqadaMaXirantahay();
void bilowDaaqada(int ballac, int dheer, char* cinwaan);
void bilowSawirka();
void xirDaaqada();
void dhameeySawirka();
void nadiifiShaashada(Midab midab);
void qoraalKuQor(char* qoraal, int x, int y, int cabir, Midab midab);
char* cusboonaysiiQoraalGalis(char* qoraal, int max_length);
bool sameeBadhan(int x, int y, int w, int h, char* qoraal, Midab bg, Midab fg);
void sawirQoraalGalis(int x, int y, int w, int h, char* qoraal, Midab bg, Midab border, Midab text_color);
char* xarafIlaaEray(int code);
int helFureXaraf();
char* qoraalJajab(char* qoraal, int bilow_idx, int dhererka);
bool laRiixayFalaartaBidix();
bool istaabasho(Boos2D meesha, AfarGees rec);
Boos2D helBooskaFalaarta();
void sawirAfarGeesXariiqan(double x, double y, double w, double h, Midab midab);
TusmoTixEray* amrd = NULL;
#define JAALLE (Midab){ 253, 249, 0, 255 }
#define CAGAAR (Midab){ 0, 228, 48, 255 }
#define CAD (Midab){ 255, 255, 255, 255 }
#define CAS (Midab){ 230, 41, 55, 255 }
#define MADOW (Midab){ 0, 0, 0, 255 }
#define BULUUG (Midab){ 0, 121, 241, 255 }
#define FURE_BACKSPACE 259
#define GUJI_BIDIX 0
char* user_input;
bool was_clicked;
bool submit_btn;
/* Embedded C from /home/mubaarak/Desktop/Tusmo/stdlib/array.tus:4 */

#include "tusmo_runtime.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>

size_t tusmo_bounds_check(size_t idx, size_t size) {
    if (idx >= size) {
        fprintf(stderr, "\n\033[1;31m[!] CILAD SOCDAALKA:\033[0m Waxaad dhaaftay xadka tixda!\n\033[90m---------------------------------------------\033[0m\n\033[94mXajmiga:\033[0m %zu\n\033[94mBooska:\033[0m  %zu\n", size, idx);
        exit(1);
    }
    return idx;
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
    TusmoTixTiro* tix = malloc(sizeof(TusmoTixTiro));
    tix->data = malloc(cap * sizeof(int));
    tix->size = 0; tix->capacity = cap;
    return tix;
}

TusmoTixEray* tusmo_hp_tix_eray_create(size_t cap) {
    TusmoTixEray* tix = malloc(sizeof(TusmoTixEray));
    tix->data = malloc(cap * sizeof(char*));
    tix->size = 0; tix->capacity = cap;
    return tix;
}

TusmoTixJajab* tusmo_hp_tix_jajab_create(size_t cap) {
    TusmoTixJajab* tix = malloc(sizeof(TusmoTixJajab));
    tix->data = malloc(cap * sizeof(double));
    tix->size = 0; tix->capacity = cap;
    return tix;
}

TusmoTixMiyaa* tusmo_hp_tix_miyaa_create(size_t cap) {
    TusmoTixMiyaa* tix = malloc(sizeof(TusmoTixMiyaa));
    tix->data = malloc(cap * sizeof(bool));
    tix->size = 0; tix->capacity = cap;
    return tix;
}

TusmoTixXaraf* tusmo_hp_tix_xaraf_create(size_t cap) {
    TusmoTixXaraf* tix = malloc(sizeof(TusmoTixXaraf));
    tix->data = malloc(cap * sizeof(char));
    tix->size = 0; tix->capacity = cap;
    return tix;
}

TusmoTixMixed* tusmo_tix_mixed_create(size_t initial_capacity) {
    TusmoTixMixed* tix = malloc(sizeof(TusmoTixMixed));
    tix->data = malloc(initial_capacity * sizeof(TusmoValue));
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
        tix->data = realloc(tix->data, tix->capacity * sizeof(TusmoValue));
    }
    tix->data[tix->size++] = value;
}

// --- Insert at Index ---

void tusmo_hp_tix_tiro_insert(TusmoTixTiro* tix, size_t index, int value) {
    if (index > tix->size) {
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
        tix->data = realloc(tix->data, tix->capacity * sizeof(TusmoValue));
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
        fprintf(stderr, "tix_mixed_pop: index %zu out of range\n", index);
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
            char* removed = tusmo_hp_tix_eray_pop(tix, i);
            if (removed) free(removed);
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

static bool tusmo_values_equal(TusmoValue a, TusmoValue b) {
    if (a.type != b.type) return false;
    switch (a.type) {
        case TUSMO_TIRO: return a.value.as_tiro == b.value.as_tiro;
        case TUSMO_JAJAB: return a.value.as_jajab == b.value.as_jajab;
        case TUSMO_ERAY: return strcmp(a.value.as_eray, b.value.as_eray) == 0;
        case TUSMO_MIYAA: return a.value.as_miyaa == b.value.as_miyaa;
        case TUSMO_XARAF: return a.value.as_xaraf == b.value.as_xaraf;
        case TUSMO_WAXBA: return true;
        default: return false;
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

#define TUSMO_NESTED_GROW(tix, elem_type)     if (tix->size >= tix->capacity) {         size_t new_cap = tix->capacity == 0 ? 8 : tix->capacity * 2;         tix->data = realloc(tix->data, new_cap * sizeof(elem_type));         tix->capacity = new_cap;     }

TusmoTixTiroNested* tusmo_tix_tiro_nested_create(size_t cap) {
    TusmoTixTiroNested* tix = malloc(sizeof(TusmoTixTiroNested));
    tix->data = cap > 0 ? malloc(cap * sizeof(TusmoTixTiro*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_tiro_nested_append(TusmoTixTiroNested* tix, TusmoTixTiro* value) {
    TUSMO_NESTED_GROW(tix, TusmoTixTiro*);
    tix->data[tix->size++] = value;
}

TusmoTixErayNested* tusmo_tix_eray_nested_create(size_t cap) {
    TusmoTixErayNested* tix = malloc(sizeof(TusmoTixErayNested));
    tix->data = cap > 0 ? malloc(cap * sizeof(TusmoTixEray*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_eray_nested_append(TusmoTixErayNested* tix, TusmoTixEray* value) {
    TUSMO_NESTED_GROW(tix, TusmoTixEray*);
    tix->data[tix->size++] = value;
}

TusmoTixJajabNested* tusmo_tix_jajab_nested_create(size_t cap) {
    TusmoTixJajabNested* tix = malloc(sizeof(TusmoTixJajabNested));
    tix->data = cap > 0 ? malloc(cap * sizeof(TusmoTixJajab*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_jajab_nested_append(TusmoTixJajabNested* tix, TusmoTixJajab* value) {
    TUSMO_NESTED_GROW(tix, TusmoTixJajab*);
    tix->data[tix->size++] = value;
}

TusmoTixMiyaaNested* tusmo_tix_miyaa_nested_create(size_t cap) {
    TusmoTixMiyaaNested* tix = malloc(sizeof(TusmoTixMiyaaNested));
    tix->data = cap > 0 ? malloc(cap * sizeof(TusmoTixMiyaa*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_miyaa_nested_append(TusmoTixMiyaaNested* tix, TusmoTixMiyaa* value) {
    TUSMO_NESTED_GROW(tix, TusmoTixMiyaa*);
    tix->data[tix->size++] = value;
}

TusmoTixXarafNested* tusmo_tix_xaraf_nested_create(size_t cap) {
    TusmoTixXarafNested* tix = malloc(sizeof(TusmoTixXarafNested));
    tix->data = cap > 0 ? malloc(cap * sizeof(TusmoTixXaraf*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_xaraf_nested_append(TusmoTixXarafNested* tix, TusmoTixXaraf* value) {
    TUSMO_NESTED_GROW(tix, TusmoTixXaraf*);
    tix->data[tix->size++] = value;
}

TusmoTixTiroNested2* tusmo_tix_tiro_nested2_create(size_t cap) {
    TusmoTixTiroNested2* tix = malloc(sizeof(TusmoTixTiroNested2));
    tix->data = cap > 0 ? malloc(cap * sizeof(TusmoTixTiroNested*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_tiro_nested2_append(TusmoTixTiroNested2* tix, TusmoTixTiroNested* value) {
    if (tix->size >= tix->capacity) {
        size_t new_cap = tix->capacity == 0 ? 8 : tix->capacity * 2;
        tix->data = realloc(tix->data, new_cap * sizeof(TusmoTixTiroNested*));
        tix->capacity = new_cap;
    }
    tix->data[tix->size++] = value;
}

TusmoTixErayNested2* tusmo_tix_eray_nested2_create(size_t cap) {
    TusmoTixErayNested2* tix = malloc(sizeof(TusmoTixErayNested2));
    tix->data = cap > 0 ? malloc(cap * sizeof(TusmoTixErayNested*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_eray_nested2_append(TusmoTixErayNested2* tix, TusmoTixErayNested* value) {
    if (tix->size >= tix->capacity) {
        size_t new_cap = tix->capacity == 0 ? 8 : tix->capacity * 2;
        tix->data = realloc(tix->data, new_cap * sizeof(TusmoTixErayNested*));
        tix->capacity = new_cap;
    }
    tix->data[tix->size++] = value;
}

TusmoTixJajabNested2* tusmo_tix_jajab_nested2_create(size_t cap) {
    TusmoTixJajabNested2* tix = malloc(sizeof(TusmoTixJajabNested2));
    tix->data = cap > 0 ? malloc(cap * sizeof(TusmoTixJajabNested*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_jajab_nested2_append(TusmoTixJajabNested2* tix, TusmoTixJajabNested* value) {
    if (tix->size >= tix->capacity) {
        size_t new_cap = tix->capacity == 0 ? 8 : tix->capacity * 2;
        tix->data = realloc(tix->data, new_cap * sizeof(TusmoTixJajabNested*));
        tix->capacity = new_cap;
    }
    tix->data[tix->size++] = value;
}

TusmoTixMiyaaNested2* tusmo_tix_miyaa_nested2_create(size_t cap) {
    TusmoTixMiyaaNested2* tix = malloc(sizeof(TusmoTixMiyaaNested2));
    tix->data = cap > 0 ? malloc(cap * sizeof(TusmoTixMiyaaNested*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_miyaa_nested2_append(TusmoTixMiyaaNested2* tix, TusmoTixMiyaaNested* value) {
    if (tix->size >= tix->capacity) {
        size_t new_cap = tix->capacity == 0 ? 8 : tix->capacity * 2;
        tix->data = realloc(tix->data, new_cap * sizeof(TusmoTixMiyaaNested*));
        tix->capacity = new_cap;
    }
    tix->data[tix->size++] = value;
}

TusmoTixXarafNested2* tusmo_tix_xaraf_nested2_create(size_t cap) {
    TusmoTixXarafNested2* tix = malloc(sizeof(TusmoTixXarafNested2));
    tix->data = cap > 0 ? malloc(cap * sizeof(TusmoTixXarafNested*)) : NULL;
    tix->size = 0;
    tix->capacity = cap;
    return tix;
}

void tusmo_tix_xaraf_nested2_append(TusmoTixXarafNested2* tix, TusmoTixXarafNested* value) {
    if (tix->size >= tix->capacity) {
        size_t new_cap = tix->capacity == 0 ? 8 : tix->capacity * 2;
        tix->data = realloc(tix->data, new_cap * sizeof(TusmoTixXarafNested*));
        tix->capacity = new_cap;
    }
    tix->data[tix->size++] = value;
}

void tusmo_tix_tiro_nested_extend(TusmoTixTiroNested* dest, TusmoTixTiroNested* src) {
    for (size_t i = 0; i < src->size; i++) {
        tusmo_tix_tiro_nested_append(dest, src->data[i]);
    }
}

void tusmo_tix_eray_nested_extend(TusmoTixErayNested* dest, TusmoTixErayNested* src) {
    for (size_t i = 0; i < src->size; i++) {
        tusmo_tix_eray_nested_append(dest, src->data[i]);
    }
}

void tusmo_tix_jajab_nested_extend(TusmoTixJajabNested* dest, TusmoTixJajabNested* src) {
    for (size_t i = 0; i < src->size; i++) {
        tusmo_tix_jajab_nested_append(dest, src->data[i]);
    }
}

void tusmo_tix_miyaa_nested_extend(TusmoTixMiyaaNested* dest, TusmoTixMiyaaNested* src) {
    for (size_t i = 0; i < src->size; i++) {
        tusmo_tix_miyaa_nested_append(dest, src->data[i]);
    }
}

void tusmo_tix_xaraf_nested_extend(TusmoTixXarafNested* dest, TusmoTixXarafNested* src) {
    for (size_t i = 0; i < src->size; i++) {
        tusmo_tix_xaraf_nested_append(dest, src->data[i]);
    }
}

void tusmo_hp_tix_tiro_extend(TusmoTixTiro* dest, TusmoTixTiro* src) {
    for (size_t i = 0; i < src->size; i++) {
        tusmo_hp_tix_tiro_append(dest, src->data[i]);
    }
}

void tusmo_hp_tix_eray_extend(TusmoTixEray* dest, TusmoTixEray* src) {
    for (size_t i = 0; i < src->size; i++) {
        tusmo_hp_tix_eray_append(dest, tusmo_strdup(src->data[i]));
    }
}

void tusmo_hp_tix_jajab_extend(TusmoTixJajab* dest, TusmoTixJajab* src) {
    for (size_t i = 0; i < src->size; i++) {
        tusmo_hp_tix_jajab_append(dest, src->data[i]);
    }
}

void tusmo_hp_tix_miyaa_extend(TusmoTixMiyaa* dest, TusmoTixMiyaa* src) {
    for (size_t i = 0; i < src->size; i++) {
        tusmo_hp_tix_miyaa_append(dest, src->data[i]);
    }
}

void tusmo_hp_tix_xaraf_extend(TusmoTixXaraf* dest, TusmoTixXaraf* src) {
    for (size_t i = 0; i < src->size; i++) {
        tusmo_hp_tix_xaraf_append(dest, src->data[i]);
    }
}

void tusmo_tix_mixed_extend(TusmoTixMixed* dest, TusmoTixMixed* src) {
    for (size_t i = 0; i < src->size; i++) {
        tusmo_tix_mixed_append(dest, src->data[i]);
    }
}

// Deep Free Routines
void tusmo_free_tix_tiro(TusmoTixTiro* tix) {
    if (!tix) return;
    if (tix->data) free(tix->data);
    free(tix);
}

void tusmo_free_tix_eray(TusmoTixEray* tix) {
    if (!tix) return;
    if (tix->data) {
        for (size_t i = 0; i < tix->size; i++) {
            if (tix->data[i]) free(tix->data[i]);
        }
        free(tix->data);
    }
    free(tix);
}

void tusmo_free_tix_jajab(TusmoTixJajab* tix) {
    if (!tix) return;
    if (tix->data) free(tix->data);
    free(tix);
}

void tusmo_free_tix_miyaa(TusmoTixMiyaa* tix) {
    if (!tix) return;
    if (tix->data) free(tix->data);
    free(tix);
}

void tusmo_free_tix_xaraf(TusmoTixXaraf* tix) {
    if (!tix) return;
    if (tix->data) free(tix->data);
    free(tix);
}

void tusmo_free_tix_mixed(TusmoTixMixed* tix) {
    if (!tix) return;
    if (tix->data) {
        free(tix->data);
    }
    free(tix);
}

void tusmo_free_tix_tiro_nested(TusmoTixTiroNested* tix) {
    if (!tix) return;
    if (tix->data) {
        for (size_t i = 0; i < tix->size; i++) {
            tusmo_free_tix_tiro(tix->data[i]);
        }
        free(tix->data);
    }
    free(tix);
}

void tusmo_free_tix_eray_nested(TusmoTixErayNested* tix) {
    if (!tix) return;
    if (tix->data) {
        for (size_t i = 0; i < tix->size; i++) {
            tusmo_free_tix_eray(tix->data[i]);
        }
        free(tix->data);
    }
    free(tix);
}

// Generic list routines from array_generic.c
TusmoTixGeneric* tusmo_tix_generic_create(size_t cap) {
    TusmoTixGeneric* tix = malloc(sizeof(TusmoTixGeneric));
    tix->data = malloc(cap * sizeof(void*));
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

void tusmo_tix_generic_extend(TusmoTixGeneric* dest, TusmoTixGeneric* src) {
    for (size_t i = 0; i < src->size; i++) {
        tusmo_tix_generic_append(dest, src->data[i]);
    }
}

/* Embedded C from /home/mubaarak/Desktop/Tusmo/stdlib/eray.tus:4 */

#include "tusmo_runtime.h"
#include <ctype.h>

char* tusmo_str_format(const char* format, ...) {
    va_list args1, args2;
    va_start(args1, format);
    va_copy(args2, args1);
    int size = vsnprintf(NULL, 0, format, args1);
    va_end(args1);
    if (size < 0) return NULL;
    char* buffer = malloc(size + 1);
    if (!buffer) return NULL;
    vsnprintf(buffer, size + 1, format, args2);
    va_end(args2);
    return buffer;
}

static const char* tusmo_safe_cstr(const char* value) {
    if (!value) {
        return "";
    }
    uintptr_t addr = (uintptr_t)value;
    if (addr < 4096) {
        return "";
    }
    return value;
}

char* tusmo_concat_cstr(const char* left, const char* right) {
    const char* safe_left = tusmo_safe_cstr(left);
    const char* safe_right = tusmo_safe_cstr(right);
    return tusmo_str_format("%s%s", safe_left, safe_right);
}

// --- String Methods ---

// XarafWeyn() - convert to uppercase
char* tusmo_str_upper(const char* str) {
    if (!str) return "";
    size_t len = strlen(str);
    char* result = malloc(len + 1);
    for (size_t i = 0; i < len; i++) {
        result[i] = toupper(str[i]);
    }
    result[len] = '\0';
    return result;
}

// XarafYar() - convert to lowercase
char* tusmo_str_lower(const char* str) {
    if (!str) return "";
    size_t len = strlen(str);
    char* result = malloc(len + 1);
    for (size_t i = 0; i < len; i++) {
        result[i] = tolower(str[i]);
    }
    result[len] = '\0';
    return result;
}

// kaReeb() - trim whitespace from both ends
char* tusmo_str_trim(const char* str) {
    if (!str) return "";
    while (*str == ' ' || *str == '\t' || *str == '\n' || *str == '\r') {
        str++;
    }
    if (*str == '\0') return "";
    const char* end = str + strlen(str) - 1;
    while (end > str && (*end == ' ' || *end == '\t' || *end == '\n' || *end == '\r')) {
        end--;
    }
    size_t len = end - str + 1;
    char* result = malloc(len + 1);
    strncpy(result, str, len);
    result[len] = '\0';
    return result;
}

// Bkareeb() - left trim (trim start only)
char* tusmo_str_ltrim(const char* str) {
    if (!str) return "";
    while (*str == ' ' || *str == '\t' || *str == '\n' || *str == '\r') {
        str++;
    }
    return tusmo_strdup(str);
}

// Mkareeb() - right trim (trim end only)
char* tusmo_str_rtrim(const char* str) {
    if (!str) return "";
    size_t len = strlen(str);
    if (len == 0) return "";
    const char* end = str + len - 1;
    while (end >= str && (*end == ' ' || *end == '\t' || *end == '\n' || *end == '\r')) {
        end--;
    }
    size_t result_len = end - str + 1;
    char* result = malloc(result_len + 1);
    strncpy(result, str, result_len);
    result[result_len] = '\0';
    return result;
}

// kuBadal(old, new) - replace all occurrences
char* tusmo_str_replace(const char* str, const char* old_str, const char* new_str) {
    if (!str || !old_str || !new_str) return "";
    if (strlen(old_str) == 0) return tusmo_strdup(str);
    
    size_t old_len = strlen(old_str);
    size_t new_len = strlen(new_str);
    size_t str_len = strlen(str);
    
    // Count occurrences
    size_t count = 0;
    const char* p = str;
    while ((p = strstr(p, old_str)) != NULL) {
        count++;
        p += old_len;
    }
    
    if (count == 0) return tusmo_strdup(str);
    
    // Calculate new length
    size_t result_len = str_len + count * (new_len - old_len);
    char* result = malloc(result_len + 1);
    
    char* dest = result;
    p = str;
    while (*p) {
        const char* found = strstr(p, old_str);
        if (!found) {
            strcpy(dest, p);
            break;
        }
        size_t seg_len = found - p;
        memcpy(dest, p, seg_len);
        dest += seg_len;
        memcpy(dest, new_str, new_len);
        dest += new_len;
        p = found + old_len;
    }
    result[result_len] = '\0';
    return result;
}

// sooRaadi(substr) - find first occurrence, returns index or -1
int tusmo_str_find(const char* str, const char* substr) {
    if (!str || !substr) return -1;
    const char* found = strstr(str, substr);
    if (!found) return -1;
    return (int)(found - str);
}

// lagaHelay(substr) - check if string contains substring, returns bool
bool tusmo_str_contains(const char* str, const char* substr) {
    if (!str || !substr) return false;
    return strstr(str, substr) != NULL;
}

// qaybi(delimiter) - split into array
TusmoTixEray* tusmo_str_split(const char* str, const char* delimiter) {
    if (!str || !delimiter) {
        TusmoTixEray* result = tusmo_hp_tix_eray_create(1);
        tusmo_hp_tix_eray_append(result, str ? tusmo_strdup(str) : tusmo_strdup(""));
        return result;
    }
    if (strlen(delimiter) == 0) {
        TusmoTixEray* result = tusmo_hp_tix_eray_create(1);
        tusmo_hp_tix_eray_append(result, tusmo_strdup(str));
        return result;
    }
    
    TusmoTixEray* result = tusmo_hp_tix_eray_create(4);
    char* str_copy = tusmo_strdup(str);
    char* token = strtok(str_copy, delimiter);
    while (token != NULL) {
        tusmo_hp_tix_eray_append(result, tusmo_strdup(token));
        token = strtok(NULL, delimiter);
    }
    free(str_copy);
    return result;
}

void tusmo_free_eray(char* str) {
    if (str) {
        free(str);
    }
}

/* Embedded C from /home/mubaarak/Desktop/Tusmo/stdlib/qaamuus.tus:4 */

#include "tusmo_runtime.h"
#include <string.h>
#include <stdio.h>

#define QAAMUUS_INITIAL_CAPACITY 16

// A simple djb2 hash function for strings
static unsigned long hash_key(const char* key) {
    unsigned long hash = 5381;
    int c;
    while ((c = *key++)) {
        hash = ((hash << 5) + hash) + c; // hash * 33 + c
    }
    return hash;
}

TusmoQaamuus* tusmo_qaamuus_create() {
    TusmoQaamuus* qaamuus = (TusmoQaamuus*)malloc(sizeof(TusmoQaamuus));
    qaamuus->capacity = QAAMUUS_INITIAL_CAPACITY;
    qaamuus->count = 0;
    qaamuus->entries = (TusmoQaamuusEntry**)malloc(sizeof(TusmoQaamuusEntry*) * qaamuus->capacity);
    for (size_t i = 0; i < qaamuus->capacity; i++) {
        qaamuus->entries[i] = NULL;
    }
    return qaamuus;
}

static void tusmo_qaamuus_resize(TusmoQaamuus* qaamuus) {
    if (qaamuus->count < qaamuus->capacity * 0.75) return;

    size_t new_capacity = qaamuus->capacity * 2;
    TusmoQaamuusEntry** new_entries = (TusmoQaamuusEntry**)malloc(sizeof(TusmoQaamuusEntry*) * new_capacity);
    for (size_t i = 0; i < new_capacity; i++) new_entries[i] = NULL;

    for (size_t i = 0; i < qaamuus->capacity; i++) {
        TusmoQaamuusEntry* entry = qaamuus->entries[i];
        while (entry) {
            TusmoQaamuusEntry* next = entry->next;
            unsigned long index = hash_key(entry->key) % new_capacity;
            entry->next = new_entries[index];
            new_entries[index] = entry;
            entry = next;
        }
    }

    qaamuus->entries = new_entries;
    qaamuus->capacity = new_capacity;
}

void tusmo_qaamuus_set(TusmoQaamuus* qaamuus, const char* key, TusmoValue value) {
    tusmo_qaamuus_resize(qaamuus);
    unsigned long index = hash_key(key) % qaamuus->capacity;
    TusmoQaamuusEntry* entry = qaamuus->entries[index];

    while (entry != NULL) {
        if (strcmp(entry->key, key) == 0) {
            entry->value = value;
            return;
        }
        entry = entry->next;
    }

    TusmoQaamuusEntry* new_entry = (TusmoQaamuusEntry*)malloc(sizeof(TusmoQaamuusEntry));
    new_entry->key = (char*)malloc(strlen(key) + 1);
    strcpy(new_entry->key, key);
    new_entry->value = value;
    new_entry->next = qaamuus->entries[index];
    qaamuus->entries[index] = new_entry;
    qaamuus->count++;
}

// Forward declaration for recursive printing
void tusmo_qor_walbo(TusmoValue val);

void tusmo_qaamuus_print(TusmoQaamuus* qaamuus) {
    printf("{");
    int first = 1;
    for (size_t i = 0; i < qaamuus->capacity; i++) {
        TusmoQaamuusEntry* entry = qaamuus->entries[i];
        while (entry) {
            if (!first) {
                printf(", ");
            }
            printf("\"%s\": ", entry->key);
            tusmo_qor_walbo(entry->value);
            first = 0;
            entry = entry->next;
        }
    }
    printf("}");
}

TusmoValue tusmo_qaamuus_get(TusmoQaamuus* qaamuus, const char* key) {
    unsigned long index = hash_key(key) % qaamuus->capacity;
    TusmoQaamuusEntry* entry = qaamuus->entries[index];

    while (entry != NULL) {
        if (strcmp(entry->key, key) == 0) {
            return entry->value;
        }
        entry = entry->next;
    }

    // Return TUSMO_WAXBA if not found
    TusmoValue not_found;
    not_found.type = TUSMO_WAXBA;
    not_found.value.as_waxba = NULL;
    return not_found;
}

void tusmo_qaamuus_delete(TusmoQaamuus* qaamuus, const char* key) {
    unsigned long index = hash_key(key) % qaamuus->capacity;
    TusmoQaamuusEntry* entry = qaamuus->entries[index];
    TusmoQaamuusEntry* prev = NULL;

    while (entry != NULL) {
        if (strcmp(entry->key, key) == 0) {
            if (prev == NULL) {
                qaamuus->entries[index] = entry->next;
            } else {
                prev->next = entry->next;
            }
            qaamuus->count--;
            return;
        }
        prev = entry;
        entry = entry->next;
    }
}

bool tusmo_qaamuus_has_key(TusmoQaamuus* qaamuus, const char* key) {
    unsigned long index = hash_key(key) % qaamuus->capacity;
    TusmoQaamuusEntry* entry = qaamuus->entries[index];

    while (entry != NULL) {
        if (strcmp(entry->key, key) == 0) {
            return true;
        }
        entry = entry->next;
    }
    return false;
}

void tusmo_free_qaamuus(TusmoQaamuus* q) {
    if (!q) return;
    for (size_t i = 0; i < q->capacity; i++) {
        TusmoQaamuusEntry* entry = q->entries[i];
        while (entry) {
            TusmoQaamuusEntry* next = entry->next;
            free(entry);
            entry = next;
        }
    }
    free(q->entries);
    free(q);
}

/* Embedded C from /home/mubaarak/Desktop/Tusmo/stdlib/core.tus:8 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdarg.h>
#include <ctype.h>

// Forward declarations of printing functions
void prints_tix_tiro(TusmoTixTiro* tix);
void prints_tix_eray(TusmoTixEray* tix);
void prints_tix_jajab(TusmoTixJajab* tix);
void prints_tix_miyaa(TusmoTixMiyaa* tix);
void prints_tix_xaraf(TusmoTixXaraf* tix);
void prints_tix_mixed(TusmoTixMixed* tix);
void prints_tix_generic(void* tix);
void prints_tix_tiro_nested(TusmoTixTiroNested* tix);
void prints_tix_eray_nested(TusmoTixErayNested* tix);
void prints_tix_jajab_nested(TusmoTixJajabNested* tix);
void prints_tix_miyaa_nested(TusmoTixMiyaaNested* tix);
void prints_tix_xaraf_nested(TusmoTixXarafNested* tix);
void prints_tix_tiro_nested2(TusmoTixTiroNested2* tix);
void prints_tix_eray_nested2(TusmoTixErayNested2* tix);
void prints_tix_jajab_nested2(TusmoTixJajabNested2* tix);
void prints_tix_miyaa_nested2(TusmoTixMiyaaNested2* tix);
void prints_tix_xaraf_nested2(TusmoTixXarafNested2* tix);
void tusmo_qor_walbo(TusmoValue val);
void tusmo_qaamuus_print(TusmoQaamuus* qaamuus);

// Helper functions
char* tusmo_strdup(const char* s) {
    if (!s) return NULL;
    char* copy = malloc(strlen(s) + 1);
    if (copy) strcpy(copy, s);
    return copy;
}

// Convert any TusmoValue to a string (eray)
char* tusmo_to_eray(TusmoValue val) {
    char* buffer = malloc(128); // Allocate a buffer
    switch (val.type) {
        case TUSMO_TIRO:
            snprintf(buffer, 128, "%d", val.value.as_tiro);
            break;
        case TUSMO_JAJAB:
            snprintf(buffer, 128, "%f", val.value.as_jajab);
            break;
        case TUSMO_ERAY:
            free(buffer);
            return tusmo_strdup(val.value.as_eray); 
        case TUSMO_MIYAA:
            free(buffer);
            return tusmo_strdup(val.value.as_miyaa ? "run" : "been");
        case TUSMO_XARAF:
            snprintf(buffer, 128, "%c", val.value.as_xaraf);
            break;
        case TUSMO_QAAMUUS:
            free(buffer);
            return tusmo_strdup("<qaamuus>");
        case TUSMO_TIX:
            free(buffer);
            return tusmo_strdup("<tix>");
        case TUSMO_WAXBA:
            free(buffer);
            return tusmo_strdup("<waxba>");
        default:
            free(buffer);
            return tusmo_strdup("<nooc aan la menneyn>");
    }
    return buffer;
}

int tusmo_dherer(TusmoValue val) {
    switch (val.type) {
        case TUSMO_ERAY:
            return val.value.as_eray ? (int)strlen(val.value.as_eray) : 0;
        case TUSMO_TIX:
            return val.value.as_tix ? (int)val.value.as_tix->size : 0;
        case TUSMO_TIX_TIRO:
            return val.value.as_tiro_tix ? (int)val.value.as_tiro_tix->size : 0;
        case TUSMO_TIX_ERAY:
            return val.value.as_eray_tix ? (int)val.value.as_eray_tix->size : 0;
        case TUSMO_TIX_JAJAB:
            return val.value.as_jajab_tix ? (int)val.value.as_jajab_tix->size : 0;
        case TUSMO_TIX_MIYAA:
            return val.value.as_miyaa_tix ? (int)val.value.as_miyaa_tix->size : 0;
        case TUSMO_TIX_XARAF:
            return val.value.as_xaraf_tix ? (int)val.value.as_xaraf_tix->size : 0;
        case TUSMO_TIX_TIRO_NESTED:
            return val.value.as_tiro_nested ? (int)val.value.as_tiro_nested->size : 0;
        case TUSMO_TIX_ERAY_NESTED:
            return val.value.as_eray_nested ? (int)val.value.as_eray_nested->size : 0;
        case TUSMO_TIX_TIRO_NESTED2:
            return val.value.as_tiro_nested2 ? (int)val.value.as_tiro_nested2->size : 0;
        case TUSMO_TIX_ERAY_NESTED2:
            return val.value.as_eray_nested2 ? (int)val.value.as_eray_nested2->size : 0;
        case TUSMO_WAXBA:
            return 0;
        default:
            return 0;
    }
}

// Convert any TusmoValue to an integer (tiro)
int tusmo_to_tiro(TusmoValue val) {
    switch (val.type) {
        case TUSMO_TIRO:
            return val.value.as_tiro;
        case TUSMO_JAJAB:
            return (int)val.value.as_jajab;
        case TUSMO_ERAY:
            return atoi(val.value.as_eray);
        case TUSMO_MIYAA:
            return val.value.as_miyaa ? 1 : 0;
        case TUSMO_XARAF:
            return (int)val.value.as_xaraf;
        default:
            return 0;
    }
}

// Convert any TusmoValue to a double (jajab)
double tusmo_to_jajab(TusmoValue val) {
    switch (val.type) {
        case TUSMO_TIRO:
            return (double)val.value.as_tiro;
        case TUSMO_JAJAB:
            return val.value.as_jajab;
        case TUSMO_ERAY:
            return atof(val.value.as_eray);
        case TUSMO_MIYAA:
            return val.value.as_miyaa ? 1.0 : 0.0;
        case TUSMO_XARAF:
            return (double)val.value.as_xaraf;
        default:
            return 0.0;
    }
}

// Convert any TusmoValue to a boolean (miyaa)
bool tusmo_to_miyaa(TusmoValue val) {
    switch (val.type) {
        case TUSMO_TIRO:
            return val.value.as_tiro != 0;
        case TUSMO_JAJAB:
            return val.value.as_jajab != 0.0;
        case TUSMO_ERAY:
            return val.value.as_eray != NULL && val.value.as_eray[0] != '\0';
        case TUSMO_MIYAA:
            return val.value.as_miyaa;
        case TUSMO_XARAF:
            return val.value.as_xaraf != '\0';
        default:
            return false;
    }
}

// Convert any TusmoValue to a char (xaraf)
char tusmo_to_xaraf(TusmoValue val) {
    switch (val.type) {
        case TUSMO_TIRO:
            return (char)val.value.as_tiro;
        case TUSMO_JAJAB:
            return (char)val.value.as_jajab;
        case TUSMO_ERAY:
            return val.value.as_eray != NULL ? val.value.as_eray[0] : '\0';
        case TUSMO_MIYAA:
            return val.value.as_miyaa ? '1' : '0';
        case TUSMO_XARAF:
            return val.value.as_xaraf;
        default:
            return '\0';
    }
}

char* tusmo_type_of(TusmoValue val) {
    switch (val.type) {
        case TUSMO_TIRO:   return "tiro";
        case TUSMO_JAJAB:  return "jajab";
        case TUSMO_ERAY:   return "eray";
        case TUSMO_MIYAA:  return "miyaa";
        case TUSMO_XARAF:  return "xaraf";
        case TUSMO_QAAMUUS:return "qaamuus";
        case TUSMO_TIX:    return "tix";
        case TUSMO_WAXBA:  return "waxba";
        default:           return "unknown";
    }
}

// Printing Arrays
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
        tusmo_qor_walbo(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_generic(void* tix_ptr) {
    if (tix_ptr == NULL) {
        printf("waxbo");
        return;
    }
    TusmoTixMixed* as_mixed = (TusmoTixMixed*)tix_ptr;
    if (as_mixed->data != NULL && as_mixed->size > 0 && as_mixed->size < 100000) {
        TusmoValue* first_elem = &as_mixed->data[0];
        if (first_elem->type >= 0 && first_elem->type <= 20) {
            prints_tix_mixed(as_mixed);
            return;
        }
    }
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
            printf("waxbo");
            continue;
        }
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
        printf("<unknown>");
    }
    printf("]");
}

void prints_tix_tiro_nested(TusmoTixTiroNested* tix) {
    if (tix == NULL || tix->data == NULL) { printf("[]"); return; }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_tiro(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_eray_nested(TusmoTixErayNested* tix) {
    if (tix == NULL || tix->data == NULL) { printf("[]"); return; }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_eray(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_jajab_nested(TusmoTixJajabNested* tix) {
    if (tix == NULL || tix->data == NULL) { printf("[]"); return; }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_jajab(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_miyaa_nested(TusmoTixMiyaaNested* tix) {
    if (tix == NULL || tix->data == NULL) { printf("[]"); return; }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_miyaa(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_xaraf_nested(TusmoTixXarafNested* tix) {
    if (tix == NULL || tix->data == NULL) { printf("[]"); return; }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_xaraf(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_tiro_nested2(TusmoTixTiroNested2* tix) {
    if (tix == NULL || tix->data == NULL) { printf("[]"); return; }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_tiro_nested(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_eray_nested2(TusmoTixErayNested2* tix) {
    if (tix == NULL || tix->data == NULL) { printf("[]"); return; }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_eray_nested(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_jajab_nested2(TusmoTixJajabNested2* tix) {
    if (tix == NULL || tix->data == NULL) { printf("[]"); return; }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_jajab_nested(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_miyaa_nested2(TusmoTixMiyaaNested2* tix) {
    if (tix == NULL || tix->data == NULL) { printf("[]"); return; }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_miyaa_nested(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void prints_tix_xaraf_nested2(TusmoTixXarafNested2* tix) {
    if (tix == NULL || tix->data == NULL) { printf("[]"); return; }
    printf("[");
    for (size_t i = 0; i < tix->size; i++) {
        prints_tix_xaraf_nested(tix->data[i]);
        if (i + 1 < tix->size) printf(", ");
    }
    printf("]");
}

void tusmo_qor_walbo(TusmoValue val) {
    switch (val.type) {
        case TUSMO_TIRO:  printf("%d", val.value.as_tiro); break;
        case TUSMO_ERAY:  printf("%s", val.value.as_eray ? val.value.as_eray : "waxbo"); break;
        case TUSMO_JAJAB: printf("%f", val.value.as_jajab); break;
        case TUSMO_MIYAA: printf(val.value.as_miyaa ? "run" : "been"); break;
        case TUSMO_XARAF: printf("%c", val.value.as_xaraf); break;
        case TUSMO_QAAMUUS: tusmo_qaamuus_print(val.value.as_qaamuus); break;
        case TUSMO_TIX:  prints_tix_mixed(val.value.as_tix); break;
        case TUSMO_WAXBA: printf("waxba"); break;
        case TUSMO_TIX_TIRO: prints_tix_tiro(val.value.as_tiro_tix); break;
        case TUSMO_TIX_ERAY: prints_tix_eray(val.value.as_eray_tix); break;
        case TUSMO_TIX_JAJAB: prints_tix_jajab(val.value.as_jajab_tix); break;
        case TUSMO_TIX_MIYAA: prints_tix_miyaa(val.value.as_miyaa_tix); break;
        case TUSMO_TIX_XARAF: prints_tix_xaraf(val.value.as_xaraf_tix); break;
        case TUSMO_TIX_TIRO_NESTED: prints_tix_tiro_nested(val.value.as_tiro_nested); break;
        case TUSMO_TIX_ERAY_NESTED: prints_tix_eray_nested(val.value.as_eray_nested); break;
        case TUSMO_TIX_JAJAB_NESTED: prints_tix_jajab_nested(val.value.as_jajab_nested); break;
        case TUSMO_TIX_MIYAA_NESTED: prints_tix_miyaa_nested(val.value.as_miyaa_nested); break;
        case TUSMO_TIX_XARAF_NESTED: prints_tix_xaraf_nested(val.value.as_xaraf_nested); break;
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

/* Embedded C from /home/mubaarak/Desktop/Tusmo/stdlib/raylib/muuqaal.tus:5 */

#define Color RaylibColor
#define Vector2 RaylibVector2
#define Rectangle RaylibRectangle
#include "stdlib/raylib/raylib.h"
#undef Color
#undef Vector2
#undef Rectangle

void Tusmo_ClearBackground(Midab color) {
    ClearBackground(*(RaylibColor*)&color);
}
void Tusmo_DrawRectangle(double x, double y, double w, double h, Midab color) {
    DrawRectangle((int)x, (int)y, (int)w, (int)h, *(RaylibColor*)&color);
}
void Tusmo_DrawRectangleLines(double x, double y, double w, double h, Midab color) {
    DrawRectangleLines((int)x, (int)y, (int)w, (int)h, *(RaylibColor*)&color);
}
void Tusmo_DrawCircle(double x, double y, double rad, Midab color) {
    DrawCircle((int)x, (int)y, (float)rad, *(RaylibColor*)&color);
}
TusmoValue Tusmo_LoadTexture(const char* fileName) {
    Texture2D* t = malloc(sizeof(Texture2D));
    *t = LoadTexture(fileName);
    return (TusmoValue){ .type = TUSMO_WAXBA, .value.as_waxba = t };
}
void Tusmo_DrawTextureEx(TusmoValue texVal, Boos2D position, float rotation, float scale, Midab tint) {
    if (!texVal.value.as_waxba || ((Texture2D*)texVal.value.as_waxba)->id == 0) return;
    RaylibVector2 p = { (float)position.x, (float)position.y };
    DrawTextureEx(*(Texture2D*)texVal.value.as_waxba, p, rotation, scale, *(RaylibColor*)&tint);
}

/* Embedded C from /home/mubaarak/Desktop/Tusmo/stdlib/raylib/qoraal.tus:5 */

#define Color RaylibColor
#define Vector2 RaylibVector2
#define Rectangle RaylibRectangle
#include "stdlib/raylib/raylib.h"
#undef Color
#undef Vector2
#undef Rectangle

TusmoValue Tusmo_LoadFont(const char* fileName) {
    Font* f = malloc(sizeof(Font));
    *f = LoadFont(fileName);
    return (TusmoValue){ .type = TUSMO_WAXBA, .value.as_waxba = f };
}
void Tusmo_DrawTextEx(TusmoValue fontVal, const char *text, Boos2D position, float fontSize, float spacing, Midab tint) {
    if (!fontVal.value.as_waxba) return;
    RaylibVector2 p = { (float)position.x, (float)position.y };
    DrawTextEx(*(Font*)fontVal.value.as_waxba, text, p, fontSize, spacing, *(RaylibColor*)&tint);
}
void Tusmo_DrawText(const char *text, int posX, int posY, int fontSize, Midab color) {
    DrawText(text, posX, posY, fontSize, *(RaylibColor*)&color);
}

/* Embedded C from /home/mubaarak/Desktop/Tusmo/stdlib/raylib/gashiga.tus:15 */

#define Color RaylibColor
#define Vector2 RaylibVector2
#define Rectangle RaylibRectangle
#include "stdlib/raylib/raylib.h"
#undef Color
#undef Vector2
#undef Rectangle

Boos2D Tusmo_GetMousePosition() {
    RaylibVector2 pos = GetMousePosition();
    Boos2D bpos = { (double)pos.x, (double)pos.y };
    return bpos;
}

/* Embedded C from /home/mubaarak/Desktop/Tusmo/stdlib/raylib/iskudhac.tus:5 */

#define Color RaylibColor
#define Vector2 RaylibVector2
#define Rectangle RaylibRectangle
#include "stdlib/raylib/raylib.h"
#undef Color
#undef Vector2
#undef Rectangle

bool Tusmo_CheckCollisionPointRec(Boos2D point, AfarGees rec) {
    RaylibVector2 p = { (float)point.x, (float)point.y };
    RaylibRectangle r = { (float)rec.x, (float)rec.y, (float)rec.width, (float)rec.height };
    return CheckCollisionPointRec(p, r);
}
bool Tusmo_CheckCollisionRecs(AfarGees rec1, AfarGees rec2) {
    RaylibRectangle r1 = { (float)rec1.x, (float)rec1.y, (float)rec1.width, (float)rec1.height };
    RaylibRectangle r2 = { (float)rec2.x, (float)rec2.y, (float)rec2.width, (float)rec2.height };
    return CheckCollisionRecs(r1, r2);
}

/* Embedded C from /home/mubaarak/Desktop/Tusmo/stdlib/raylib/dhexgalka.tus:9 */

#define Color RaylibColor
#define Vector2 RaylibVector2
#define Rectangle RaylibRectangle
#include "stdlib/raylib/raylib.h"
#undef Color
#undef Vector2
#undef Rectangle

void Tusmo_DrawRectangleRec(AfarGees rec, Midab color) {
    RaylibRectangle r = { (float)rec.x, (float)rec.y, (float)rec.width, (float)rec.height };
    DrawRectangleRec(r, *(RaylibColor*)&color);
}


char* XarafWeyn(char* s) {
    char* __tusmo_temp_1 = tusmo_str_upper(s);
    if (s) tusmo_free_eray(s);
    return __tusmo_temp_1;
}

char* XarafYar(char* s) {
    char* __tusmo_temp_2 = tusmo_str_lower(s);
    if (s) tusmo_free_eray(s);
    return __tusmo_temp_2;
}

char* kaReeb(char* s) {
    char* __tusmo_temp_3 = tusmo_str_trim(s);
    if (s) tusmo_free_eray(s);
    return __tusmo_temp_3;
}

char* Bkareeb(char* s) {
    char* __tusmo_temp_4 = tusmo_str_ltrim(s);
    if (s) tusmo_free_eray(s);
    return __tusmo_temp_4;
}

char* Mkareeb(char* s) {
    char* __tusmo_temp_5 = tusmo_str_rtrim(s);
    if (s) tusmo_free_eray(s);
    return __tusmo_temp_5;
}

char* kuBadal(char* s, char* d, char* c) {
    char* __tusmo_temp_6 = tusmo_str_replace(s, d, c);
    if (s) tusmo_free_eray(s);
    if (d) tusmo_free_eray(d);
    if (c) tusmo_free_eray(c);
    return __tusmo_temp_6;
}

int sooRaadi(char* s, char* d) {
    int __tusmo_temp_7 = tusmo_str_find(s, d);
    if (s) tusmo_free_eray(s);
    if (d) tusmo_free_eray(d);
    return __tusmo_temp_7;
}

bool lagaHelay(char* s, char* d) {
    bool __tusmo_temp_8 = tusmo_str_contains(s, d);
    if (s) tusmo_free_eray(s);
    if (d) tusmo_free_eray(d);
    return __tusmo_temp_8;
}

TusmoTixEray* qaybi(char* s, char* d) {
    TusmoTixEray* __tusmo_temp_9 = tusmo_str_split(s, d);
    if (s) tusmo_free_eray(s);
    if (d) tusmo_free_eray(d);
    return __tusmo_temp_9;
}

bool majiraa(TusmoQaamuus* q, char* fure) {
    bool __tusmo_temp_10 = tusmo_qaamuus_has_key(q, fure);
    if (fure) tusmo_free_eray(fure);
    return __tusmo_temp_10;
}

void tir(TusmoQaamuus* q, char* fure) {
    tusmo_qaamuus_delete(q, fure);
    if (fure) tusmo_free_eray(fure);
}

char* nooc(TusmoValue x) {
    char* __tusmo_temp_11 = tusmo_type_of(x);
    return __tusmo_temp_11;
}

int dherer(TusmoValue x) {
    int __tusmo_temp_12 = tusmo_dherer(x);
    return __tusmo_temp_12;
}

char* eray(TusmoValue x) {
    char* __tusmo_temp_13 = tusmo_to_eray(x);
    return __tusmo_temp_13;
}

int tiro(TusmoValue x) {
    int __tusmo_temp_14 = tusmo_to_tiro(x);
    return __tusmo_temp_14;
}

double jajab(TusmoValue x) {
    double __tusmo_temp_15 = tusmo_to_jajab(x);
    return __tusmo_temp_15;
}

bool miyaa(TusmoValue x) {
    bool __tusmo_temp_16 = tusmo_to_miyaa(x);
    return __tusmo_temp_16;
}

int qor_tiro(char x) {
    int __tusmo_temp_17 = (int)(x);
    return __tusmo_temp_17;
}

char qor_xaraf(int x) {
    char __tusmo_temp_18 = (char)(x);
    return __tusmo_temp_18;
}

int uguYar(int a, int b) {
    if ((a < b)) {
    int __tusmo_temp_19 = a;
    return __tusmo_temp_19;
    }
    else {
    int __tusmo_temp_20 = b;
    return __tusmo_temp_20;
    }
}

int uguWeyn(int a, int b) {
    if ((a > b)) {
    int __tusmo_temp_21 = a;
    return __tusmo_temp_21;
    }
    else {
    int __tusmo_temp_22 = b;
    return __tusmo_temp_22;
    }
}

int qaado(int x) {
    if ((x < 0)) {
    int __tusmo_temp_23 = (0 - x);
    return __tusmo_temp_23;
    }
    else {
    int __tusmo_temp_24 = x;
    return __tusmo_temp_24;
    }
}

void jooji(int code) {
    exit(code);
}

bool daaqadaMaXirantahay() {
    bool __tusmo_temp_25 = WindowShouldClose();
    return __tusmo_temp_25;
}

void bilowDaaqada(int ballac, int dheer, char* cinwaan) {
    InitWindow(ballac, dheer, cinwaan);
    if (cinwaan) tusmo_free_eray(cinwaan);
}

void bilowSawirka() {
    BeginDrawing();
}

void xirDaaqada() {
    CloseWindow();
}

void dhameeySawirka() {
    EndDrawing();
}

void nadiifiShaashada(Midab midab) {
    Tusmo_ClearBackground(midab);
}

void qoraalKuQor(char* qoraal, int x, int y, int cabir, Midab midab) {
    Tusmo_DrawText(qoraal, x, y, cabir, midab);
    if (qoraal) tusmo_free_eray(qoraal);
}

char* cusboonaysiiQoraalGalis(char* qoraal, int max_length) {
    int furaha;
    furaha = helFureXaraf();
    while ((furaha > 0)) {
    if ((((furaha >= 32) && (furaha <= 125)) && (dherer((TusmoValue){ .type = TUSMO_ERAY, .value.as_eray = qoraal }) < max_length))) {
    if (qoraal) tusmo_free_eray(qoraal);
    qoraal = tusmo_concat_cstr(qoraal, xarafIlaaEray(furaha));
    }
    furaha = helFureXaraf();
    }
    if ((IsKeyPressed(FURE_BACKSPACE) && (dherer((TusmoValue){ .type = TUSMO_ERAY, .value.as_eray = qoraal }) > 0))) {
    if (qoraal) tusmo_free_eray(qoraal);
    qoraal = qoraalJajab(tusmo_strdup(qoraal), 0, (dherer((TusmoValue){ .type = TUSMO_ERAY, .value.as_eray = qoraal }) - 1));
    }
    char* __tusmo_temp_26 = qoraal;
    return __tusmo_temp_26;
}

bool sameeBadhan(int x, int y, int w, int h, char* qoraal, Midab bg, Midab fg) {
    AfarGees rec;
    rec = (AfarGees){ jajab((TusmoValue){ .type = TUSMO_TIRO, .value.as_tiro = x }), jajab((TusmoValue){ .type = TUSMO_TIRO, .value.as_tiro = y }), jajab((TusmoValue){ .type = TUSMO_TIRO, .value.as_tiro = w }), jajab((TusmoValue){ .type = TUSMO_TIRO, .value.as_tiro = h }) };
    bool hover;
    hover = istaabasho(helBooskaFalaarta(), rec);
    if (hover) {
    Tusmo_DrawRectangleRec(rec, bg);
    }
    else {
    Tusmo_DrawRectangleRec(rec, bg);
    }
    qoraalKuQor(tusmo_strdup(qoraal), (x + 12), (y + 10), 20, fg);
    bool __tusmo_temp_27 = (hover && laRiixayFalaartaBidix());
    if (qoraal) tusmo_free_eray(qoraal);
    return __tusmo_temp_27;
}

void sawirQoraalGalis(int x, int y, int w, int h, char* qoraal, Midab bg, Midab border, Midab text_color) {
    Tusmo_DrawRectangleRec((AfarGees){ jajab((TusmoValue){ .type = TUSMO_TIRO, .value.as_tiro = x }), jajab((TusmoValue){ .type = TUSMO_TIRO, .value.as_tiro = y }), jajab((TusmoValue){ .type = TUSMO_TIRO, .value.as_tiro = w }), jajab((TusmoValue){ .type = TUSMO_TIRO, .value.as_tiro = h }) }, bg);
    sawirAfarGeesXariiqan(jajab((TusmoValue){ .type = TUSMO_TIRO, .value.as_tiro = x }), jajab((TusmoValue){ .type = TUSMO_TIRO, .value.as_tiro = y }), jajab((TusmoValue){ .type = TUSMO_TIRO, .value.as_tiro = w }), jajab((TusmoValue){ .type = TUSMO_TIRO, .value.as_tiro = h }), border);
    qoraalKuQor(tusmo_strdup(qoraal), (x + 10), (y + 10), 20, text_color);
    if (qoraal) tusmo_free_eray(qoraal);
}

char* xarafIlaaEray(int code) {
    char* __tusmo_temp_28 = tusmo_strdup(TextFormat("%c", code));
    return __tusmo_temp_28;
}

int helFureXaraf() {
    int __tusmo_temp_29 = GetCharPressed();
    return __tusmo_temp_29;
}

char* qoraalJajab(char* qoraal, int bilow_idx, int dhererka) {
    char* __tusmo_temp_30 = tusmo_strdup(TextSubtext(qoraal, bilow_idx, dhererka));
    if (qoraal) tusmo_free_eray(qoraal);
    return __tusmo_temp_30;
}

bool laRiixayFalaartaBidix() {
    bool __tusmo_temp_31 = IsMouseButtonPressed(GUJI_BIDIX);
    return __tusmo_temp_31;
}

bool istaabasho(Boos2D meesha, AfarGees rec) {
    bool __tusmo_temp_32 = Tusmo_CheckCollisionPointRec(meesha, rec);
    return __tusmo_temp_32;
}

Boos2D helBooskaFalaarta() {
    Boos2D __tusmo_temp_33 = Tusmo_GetMousePosition();
    return __tusmo_temp_33;
}

void sawirAfarGeesXariiqan(double x, double y, double w, double h, Midab midab) {
    Tusmo_DrawRectangleLines(x, y, w, h, midab);
}

int main(int argc, char* argv[]) {
    amrd = tusmo_hp_tix_eray_create(argc);
    for (int i = 0; i < argc; i++) {
        tusmo_hp_tix_eray_append(amrd, tusmo_strdup(argv[i]));
    }
    user_input = tusmo_strdup("");
    was_clicked = false;
    bilowDaaqada(800, 600, tusmo_strdup("Tusmo Raylib - Final Somali API Test"));
    while ((daaqadaMaXirantahay() == false)) {
    bilowSawirka();
    nadiifiShaashada(MADOW);
    qoraalKuQor(tusmo_strdup("Raylib using improved Tusmo Structs & Somali Names!"), 100, 50, 24, CAD);
    sawirQoraalGalis(100, 100, 400, 50, tusmo_strdup(user_input), CAD, BULUUG, JAALLE);
    if (user_input) tusmo_free_eray(user_input);
    user_input = cusboonaysiiQoraalGalis(tusmo_strdup(user_input), 30);
    submit_btn = sameeBadhan(100, 170, 200, 50, tusmo_strdup("Submit"), CAS, MADOW);
    if ((submit_btn == true)) {
    was_clicked = true;
    }
    if ((was_clicked == true)) {
    qoraalKuQor(tusmo_concat_cstr("You typed: ", user_input), 100, 240, 24, CAGAAR);
    qoraalKuQor(tusmo_strdup("Press BACKSPACE to clear and try again!"), 100, 270, 18, JAALLE);
    }
    dhameeySawirka();
    }
    xirDaaqada();
    if (user_input) tusmo_free_eray(user_input);
    if (amrd) tusmo_free_tix_eray(amrd);
    return 0;
}
