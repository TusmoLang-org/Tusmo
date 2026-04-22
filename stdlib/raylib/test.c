#include "tusmo_runtime.h"


#include "raylib.h"

#define Color Color
#define Vector2 Vector2
#define Rectangle Rectangle
#define CAD WHITE
#define MADOW BLACK
#define CAS RED
#define BULUUG BLUE
#define CAGAAR GREEN
#define JAALLE YELLOW
#define GUJI_BIDIX MOUSE_LEFT_BUTTON
#define FURE_BACKSPACE KEY_BACKSPACE
#define FURE_ENTER KEY_ENTER
char* user_input;
bool was_clicked;
bool submit_btn;
void bilow(int ballac, int dheer, char* cinwaan) {
    InitWindow(ballac, dheer, cinwaan);
}

bool daaqadu_ma_xirantahay() {
    return WindowShouldClose();
}

void bilaaw_sawirka() {
    BeginDrawing();
}

void dhameey_sawirka() {
    EndDrawing();
}

void nadiifi_asalka(Color midab) {
    ClearBackground(midab);
}

void kuqor(char* qoraal, int x, int y, int cabir, Color midab) {
    DrawText(qoraal, x, y, cabir, midab);
}

void xir_daaqada() {
    CloseWindow();
}

void sawir_leydi(int x, int y, int w, int h, Color midab) {
    DrawRectangle(x, y, w, h, midab);
}

void sawir_leydi_xuduud(int x, int y, int w, int h, Color midab) {
    DrawRectangleLines(x, y, w, h, midab);
}

void sawir_goobo(int x, int y, double r, Color midab) {
    DrawCircle(x, y, r, midab);
}

void dhig_fps(int x, int y) {
    DrawFPS(x, y);
}

Vector2 booska_mouse() {
    return GetMousePosition();
}

bool guduud_leydi(Vector2 mouse, Rectangle rec) {
    return CheckCollisionPointRec(mouse, rec);
}

bool guji_bidix_ayaa_dhacay() {
    return IsMouseButtonPressed(GUJI_BIDIX);
}

bool badhan(int x, int y, int w, int h, char* qoraal, Color bg, Color fg) {
    bool hover;
    hover = guduud_leydi(booska_mouse(), (Rectangle){ x, y, w, h });
    if (hover) {
    DrawRectangleRec((Rectangle){ x, y, w, h }, Fade(bg, 0.85));
    }
    else {
    DrawRectangleRec((Rectangle){ x, y, w, h }, bg);
    }
    DrawText(qoraal, (x + 12), (y + 10), 20, fg);
    return (hover && guji_bidix_ayaa_dhacay());
}

int hel_fure_char() {
    return GetCharPressed();
}

char* qoraal_jajab(char* qoraal, int bilow_idx, int dhererka) {
    return TextSubtext(qoraal, bilow_idx, dhererka);
}

char* xaraf_ilaa_eray(int code) {
    return TextFormat("%c", code);
}

char* qoraal_geli_update(char* qoraal, int ugu_badnaan) {
    int furaha;
    furaha = hel_fure_char();
    while ((furaha > 0)) {
    if ((((furaha >= 32) && (furaha <= 125)) && (strlen(qoraal) < ugu_badnaan))) {
    qoraal = tusmo_concat_cstr(qoraal, xaraf_ilaa_eray(furaha));
    }
    furaha = hel_fure_char();
    }
    if ((IsKeyPressed(FURE_BACKSPACE) && (strlen(qoraal) > 0))) {
    qoraal = qoraal_jajab(qoraal, 0, (strlen(qoraal) - 1));
    }
    return qoraal;
}

void sawir_qoraal_geli(int x, int y, int w, int h, char* qoraal, Color bg, Color border, Color text_color) {
    DrawRectangleRec((Rectangle){ x, y, w, h }, bg);
    DrawRectangleLines(x, y, w, h, border);
    DrawText(qoraal, (x + 10), (y + 10), 20, text_color);
}

int main(void) {
    user_input = "";
    was_clicked = false;
    bilow(800, 600, "Tusmo Raylib - Text Input Test");
    while ((daaqadu_ma_xirantahay() == false)) {
    bilaaw_sawirka();
    nadiifi_asalka(MADOW);
    kuqor("Type something and press the Submit button:", 100, 50, 24, CAD);
    sawir_qoraal_geli(100, 100, 400, 50, user_input, CAD, BULUUG, JAALLE);
    user_input = qoraal_geli_update(user_input, 30);
    submit_btn = badhan(100, 170, 200, 50, "Submit", CAS, MADOW);
    if ((submit_btn == true)) {
    was_clicked = true;
    }
    if ((was_clicked == true)) {
    kuqor(tusmo_concat_cstr("You typed: ", user_input), 100, 240, 24, CAGAAR);
    kuqor("Press BACKSPACE to clear and try again!", 100, 270, 18, JAALLE);
    }
    dhameey_sawirka();
    }
    xir_daaqada();
    return 0;
}
