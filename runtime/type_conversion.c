// runtime/type_conversion.c

#include "type_conversion.h"
#include "tusmo_runtime.h" // for tusmo_strdup
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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
            // Check for non-empty string
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
