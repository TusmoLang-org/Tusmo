#include "tusmo_runtime.h"

#define TIJAABO_NUMBER 500
typedef struct {
    int x;
    int y;
} TijaaboQaab;

char* fariin;
int isku_dar(int a, int b) {
    int __tusmo_temp_1 = (a + b);
    return __tusmo_temp_1;
}

void tusmo_main() {
    printf("%s%d", ("Constant waa: " ? "Constant waa: " : "waxbo"), TIJAABO_NUMBER 
);
    fflush(stdout);
    printf("\n");
    fflush(stdout);
    printf("%s%s", ("Fariinta waa: " ? "Fariinta waa: " : "waxbo"), (fariin ? fariin : "waxbo") 
);
    fflush(stdout);
    printf("\n");
    fflush(stdout);
    int jawaab;
    jawaab = isku_dar(10, 20);
    printf("%s%d", ("Jawaabta isku_dar waa: " ? "Jawaabta isku_dar waa: " : "waxbo"), jawaab 
);
    fflush(stdout);
    printf("\n");
    fflush(stdout);
    TijaaboQaab q;
    q = (TijaaboQaab){ 100, 200 };
    printf("%s%d%s%d", ("Qaab x: " ? "Qaab x: " : "waxbo"), q.x, (" y: " ? " y: " : "waxbo"), q.y 
);
    fflush(stdout);
    printf("\n");
    fflush(stdout);
}

int main(void) {
    fariin = tusmo_strdup("Waan shaqaynayaa!");
    tusmo_main();
    if (fariin) tusmo_free_eray(fariin);
    return 0;
}
