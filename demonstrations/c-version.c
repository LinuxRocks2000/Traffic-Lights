// Most annoying traffic light system in the world. Serves as more of an example than anything; you really shouldn't use this sort of pattern.

#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h>
#include <inttypes.h>

#define TOP      0
#define BOTTOM   1
#define LEFT     2
#define RIGHT    3
#define GREEN    0
#define RED      1
#define YELLOW   2

typedef _Bool bool;

void set(int sock, uint8_t x, uint8_t y, uint8_t which, uint8_t color){
    write(sock, "S", 1);
    write(sock, &x, 1); // Otherwise it will segfault because it'll think the raw int is actually a pointer
    write(sock, &y, 1);
    write(sock, &which, 1);
    write(sock, &color, 1);
}

void update(int sock){
    write(sock, "U", 1);
}

void safeExit(int sock){
    write(sock, "E", 1);
}

void reset(int sock){
    write(sock, "R", 1);
}

void destroy(int sock){
    write(sock, "D", 1);
}

int main(){
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    unsigned int port = 2000;
    address.sin_port = htons(port);
    bool looping = 1;
    while (looping){
        if (port >= 2050){
            printf("I have tried every port between 2000 and 2050. The server is either not running or is running on the wrong port.\n");
            return 1;
        }
        else if (connect(sockfd, (struct sockaddr*)&address, sizeof(address))){
            port ++;
            printf("Connection failed on port %d. Trying port %d.\n", port - 1, port);
        }
        else{
            printf("Successfully connected to port %d!\n", port);
            looping = 0;
        }
    }
    unsigned int tick = 0;
    while (1){
        usleep(2000000);
        tick ++;
        for (int x = 0; x < 5; x ++){
            for (int y = 0; y < 5; y ++){
                if ((tick + x) % 2 == 0){
                    set(sockfd, x, y, BOTTOM, RED);
                    set(sockfd, x, y, TOP, RED);
                    set(sockfd, x, y, LEFT, GREEN);
                    set(sockfd, x, y, RIGHT, GREEN);
                }
                else{
                    set(sockfd, x, y, BOTTOM, GREEN);
                    set(sockfd, x, y, TOP, GREEN);
                    set(sockfd, x, y, LEFT, RED);
                    set(sockfd, x, y, RIGHT, RED);
                }
            }
        }
        update(sockfd);
    }
    return 0;
}
