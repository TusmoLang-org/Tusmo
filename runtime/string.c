// runtime/string.c

#include "tusmo_runtime.h"
#include <ctype.h>

char* tusmo_str_format(const char* format, ...) {
    va_list args1, args2;
    va_start(args1, format);
    va_copy(args2, args1);
    int size = vsnprintf(NULL, 0, format, args1);
    va_end(args1);
    if (size < 0) return NULL;
    char* buffer = GC_MALLOC(size + 1);
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
    char* result = GC_MALLOC(len + 1);
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
    char* result = GC_MALLOC(len + 1);
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
    char* result = GC_MALLOC(len + 1);
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
    return strdup(str);
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
    char* result = GC_MALLOC(result_len + 1);
    strncpy(result, str, result_len);
    result[result_len] = '\0';
    return result;
}

// kuBadal(old, new) - replace all occurrences
char* tusmo_str_replace(const char* str, const char* old_str, const char* new_str) {
    if (!str || !old_str || !new_str) return "";
    if (strlen(old_str) == 0) return strdup(str);
    
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
    
    if (count == 0) return strdup(str);
    
    // Calculate new length
    size_t result_len = str_len + count * (new_len - old_len);
    char* result = GC_MALLOC(result_len + 1);
    
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
        tusmo_hp_tix_eray_append(result, str ? strdup(str) : strdup(""));
        return result;
    }
    if (strlen(delimiter) == 0) {
        TusmoTixEray* result = tusmo_hp_tix_eray_create(1);
        tusmo_hp_tix_eray_append(result, strdup(str));
        return result;
    }
    
    TusmoTixEray* result = tusmo_hp_tix_eray_create(4);
    char* str_copy = strdup(str);
    char* token = strtok(str_copy, delimiter);
    while (token != NULL) {
        tusmo_hp_tix_eray_append(result, strdup(token));
        token = strtok(NULL, delimiter);
    }
    free(str_copy);
    return result;
}
