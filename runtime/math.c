// runtime/math.c

#include "tusmo_runtime.h"
#include <math.h>

// --- Math Functions ---

double tusmo_sin(double x) {
    return sin(x);
}

double tusmo_cos(double x) {
    return cos(x);
}

double tusmo_sqrt(double x) {
    return sqrt(x);
}

double tusmo_abs_d(double x) {
    return fabs(x);
}

double tusmo_pow(double base, double exp) {
    return pow(base, exp);
}

double tusmo_floor(double x) {
    return floor(x);
}

double tusmo_ceil(double x) {
    return ceil(x);
}

double tusmo_round(double x) {
    return round(x);
}
