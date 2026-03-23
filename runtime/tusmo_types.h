// runtime/tusmo_types.h

#ifndef TUSMO_TYPES_H
#define TUSMO_TYPES_H

#include <stdbool.h>
#include <stddef.h>

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
    // Typed 1D array types (for dynamic arrays)
    TUSMO_TIX_TIRO, TUSMO_TIX_ERAY, TUSMO_TIX_JAJAB, TUSMO_TIX_MIYAA, TUSMO_TIX_XARAF,
    // Nested 2D array types
    TUSMO_TIX_TIRO_NESTED, TUSMO_TIX_ERAY_NESTED, TUSMO_TIX_JAJAB_NESTED,
    TUSMO_TIX_MIYAA_NESTED, TUSMO_TIX_XARAF_NESTED,
    // Nested 3D array types  
    TUSMO_TIX_TIRO_NESTED2, TUSMO_TIX_ERAY_NESTED2, TUSMO_TIX_JAJAB_NESTED2,
    TUSMO_TIX_MIYAA_NESTED2, TUSMO_TIX_XARAF_NESTED2
} TusmoType;

typedef struct { 
    TusmoType type; 
    union { 
        int as_tiro; 
        char* as_eray; 
        double as_jajab; 
        bool as_miyaa; 
        char as_xaraf; 
        struct TusmoQaamuus* as_qaamuus; 
        TusmoTixMixed* as_tix; 
        // Typed 1D array types (for dynamic arrays)
        TusmoTixTiro* as_tiro_tix;
        TusmoTixEray* as_eray_tix;
        TusmoTixJajab* as_jajab_tix;
        TusmoTixMiyaa* as_miyaa_tix;
        TusmoTixXaraf* as_xaraf_tix;
        // Nested 2D array types
        TusmoTixTiroNested* as_tiro_nested;
        TusmoTixErayNested* as_eray_nested;
        TusmoTixJajabNested* as_jajab_nested;
        TusmoTixMiyaaNested* as_miyaa_nested;
        TusmoTixXarafNested* as_xaraf_nested;
        // Nested 3D array types  
        TusmoTixTiroNested2* as_tiro_nested2;
        TusmoTixErayNested2* as_eray_nested2;
        TusmoTixJajabNested2* as_jajab_nested2;
        TusmoTixMiyaaNested2* as_miyaa_nested2;
        TusmoTixXarafNested2* as_xaraf_nested2;
    } value; 
} TusmoValue;

#endif // TUSMO_TYPES_H
