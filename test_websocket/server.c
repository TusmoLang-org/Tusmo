#include "tusmo_runtime.h"

typedef struct Xiriiriye Xiriiriye;
struct Xiriiriye {
    char* Aqoonsi;
};

typedef struct WebXiriiriye WebXiriiriye;
struct WebXiriiriye {
    char* socket_handle;
    bool waa_xiran;
};

void Xiriiriye_dhis(Xiriiriye* kan) {
    kan->Aqoonsi = "";
}

char* Xiriiriye_samee_server(Xiriiriye* kan, char* port) {
    return tusmo_socket_create_server(port);
}

int Xiriiriye_dhageyso(Xiriiriye* kan, int saf_sugid_ugu_badan) {
    return tusmo_socket_listen(kan->Aqoonsi, saf_sugid_ugu_badan);
}

char* Xiriiriye_aqbal(Xiriiriye* kan) {
    return tusmo_socket_accept(kan->Aqoonsi);
}

char* Xiriiriye_kuxirmo(Xiriiriye* kan, char* host, char* port) {
    return tusmo_socket_connect(host, port);
}

int Xiriiriye_dir(Xiriiriye* kan, char* xogta) {
    return tusmo_socket_send(kan->Aqoonsi, xogta);
}

char* Xiriiriye_soo_hel(Xiriiriye* kan, int size) {
    return tusmo_socket_receive(kan->Aqoonsi, size);
}

void Xiriiriye_xir(Xiriiriye* kan) {
    tusmo_socket_close(kan->Aqoonsi);
}

bool Xiriiriye_waa_ansax(Xiriiriye* kan) {
    return tusmo_socket_is_valid(kan->Aqoonsi);
}

Xiriiriye* _create_Xiriiriye() {
    Xiriiriye* kan = GC_MALLOC(sizeof(Xiriiriye));
    Xiriiriye_dhis(kan);
    return kan;
}

void WebXiriiriye_dhis(WebXiriiriye* kan) {
    kan->socket_handle = "";
    kan->waa_xiran = false;
}

void WebXiriiriye_kor_u_qaad(WebXiriiriye* kan, char* client_socket_handle, char* ws_key) {
    tusmo_ws_send_upgrade_response(client_socket_handle, tusmo_ws_generate_accept_key(ws_key));
    kan->socket_handle = client_socket_handle;
    kan->waa_xiran = true;
}

int WebXiriiriye_dir_qoraal(WebXiriiriye* kan, char* fariin) {
    printf("DEBUG dir_qoraal: socket='%s', waa_xiran=%d, msg='%s'\n", kan->socket_handle, kan->waa_xiran, fariin);
    if ((kan->waa_xiran == false)) {
    return 1;
    }
    int result = tusmo_ws_send_text(kan->socket_handle, fariin);
    printf("DEBUG send_text result: %d\n", result);
    return result;
}

int WebXiriiriye_dir_binary(WebXiriiriye* kan, char* xog) {
    if ((kan->waa_xiran == false)) {
    return 1;
    }
    return tusmo_ws_send_binary(kan->socket_handle, xog, 0);
}

TusmoQaamuus* WebXiriiriye_soo_hel_fariin(WebXiriiriye* kan) {
    if ((kan->waa_xiran == false)) {
    TusmoQaamuus* __tusmo_temp_1 = tusmo_qaamuus_create();
    TusmoQaamuus* qalad = __tusmo_temp_1;
    return qalad;
    }
    return tusmo_ws_decode_frame(kan->socket_handle);
}

int WebXiriiriye_dir_ping(WebXiriiriye* kan) {
    if ((kan->waa_xiran == false)) {
    return 1;
    }
    return tusmo_ws_send_ping(kan->socket_handle);
}

int WebXiriiriye_dir_pong(WebXiriiriye* kan) {
    if ((kan->waa_xiran == false)) {
    return 1;
    }
    return tusmo_ws_send_pong(kan->socket_handle);
}

void WebXiriiriye_xir(WebXiriiriye* kan, int cod, char* sabab) {
    if (kan->waa_xiran) {
    tusmo_ws_send_close(kan->socket_handle, cod, sabab);
    kan->waa_xiran = false;
    }
}

bool WebXiriiriye_ma_xiran(WebXiriiriye* kan) {
    return kan->waa_xiran;
}

WebXiriiriye* _create_WebXiriiriye() {
    WebXiriiriye* kan = GC_MALLOC(sizeof(WebXiriiriye));
    WebXiriiriye_dhis(kan);
    return kan;
}

int main(void) {
    GC_INIT();
    Xiriiriye* server = _create_Xiriiriye();
    char* handle;
    handle = Xiriiriye_samee_server(server, "8080");
    if ((strcmp(handle, "") != 0)) {
    printf("%s", "WebSocket server created on port 8080" 
);
    fflush(stdout);
    printf("\n");
    fflush(stdout);
    int listen_result;
    listen_result = Xiriiriye_dhageyso(server, 5);
    if ((listen_result == 0)) {
    printf("%s", "Waiting for client connection..." 
);
    fflush(stdout);
    printf("\n");
    fflush(stdout);
    char* client_handle;
    client_handle = Xiriiriye_aqbal(server);
    if ((strcmp(client_handle, "") != 0)) {
    printf("%s", "Client connected!" 
);
    fflush(stdout);
    printf("\n");
    fflush(stdout);
    WebXiriiriye* ws = _create_WebXiriiriye();
    WebXiriiriye_kor_u_qaad(ws, client_handle, "test_key");
    printf("%s", "WebSocket upgraded!" 
);
    fflush(stdout);
    printf("\n");
    fflush(stdout);
    printf("%s", "Sending JSON message..." 
);
    fflush(stdout);
    printf("\n");
    fflush(stdout);
    char* json_msg;
    json_msg = "{\"message\": \"Hello from Tusmo!\"}";
    int sent;
    sent = WebXiriiriye_dir_qoraal(ws, json_msg);
    printf("%s", "Sent bytes: " 
);
    fflush(stdout);
    printf("\n");
    fflush(stdout);
    printf("%d", sent 
);
    fflush(stdout);
    printf("\n");
    fflush(stdout);
    }
    }
    Xiriiriye_xir(server);
    printf("%s", "Server closed" 
);
    fflush(stdout);
    printf("\n");
    fflush(stdout);
    }
    return 0;
}
