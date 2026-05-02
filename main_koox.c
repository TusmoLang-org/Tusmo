#include "tusmo_runtime.h"

typedef struct Xisaabiye Xisaabiye;
struct Xisaabiye {
    int wadarta;
};

void Xisaabiye_dhis(Xisaabiye* kan, int bilowga) {
    TUSMO_SAFE_ACCESS(kan, "/home/mubaarak/Desktop/Tusmo/lib_koox.tus", 7)->wadarta = bilowga;
}

void Xisaabiye_ku_dar(Xisaabiye* kan, int x) {
    TUSMO_SAFE_ACCESS(kan, "/home/mubaarak/Desktop/Tusmo/lib_koox.tus", 11)->wadarta = (TUSMO_SAFE_ACCESS(kan, "/home/mubaarak/Desktop/Tusmo/lib_koox.tus", 11)->wadarta + x);
}

int Xisaabiye_hel_wadarta(Xisaabiye* kan) {
    int __tusmo_temp_1 = TUSMO_SAFE_ACCESS(kan, "/home/mubaarak/Desktop/Tusmo/lib_koox.tus", 15)->wadarta;
    return __tusmo_temp_1;
}

Xisaabiye* _create_Xisaabiye(int bilowga) {
    Xisaabiye* kan = (Xisaabiye*)malloc(sizeof(Xisaabiye));
    Xisaabiye_dhis(kan, bilowga);
    return kan;
}

void tusmo_main() {
    Xisaabiye* xisaab;
    xisaab = _create_Xisaabiye(10);
    Xisaabiye_ku_dar(TUSMO_SAFE_ACCESS(xisaab, "main_koox.tus", 6), 20);
    Xisaabiye_ku_dar(TUSMO_SAFE_ACCESS(xisaab, "main_koox.tus", 7), 5);
    int jawaab;
    jawaab = Xisaabiye_hel_wadarta(TUSMO_SAFE_ACCESS(xisaab, "main_koox.tus", 9));
    printf("%s%d", ("Wadarta waa: " ? "Wadarta waa: " : "waxbo"), jawaab 
);
    fflush(stdout);
    printf("\n");
    fflush(stdout);
}

int main(void) {
    tusmo_main();
    return 0;
}
