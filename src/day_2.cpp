#include <cstdio>
#include <cstdlib>
#include <stdexcept>
using namespace std;


bool verbose=false;

int int_code(int code[], int code_len){
    int i;
    for (i=0; i<code_len; i=i+4) {
        if (code[i] == 1) {
            if (verbose) {
                printf("Opcode 1: %d %d %d %d\n", code[i], code[i + 1],
                       code[i + 2], code[i + 3]);

            }
            if (code[i + 1] + code[i + 2] == 19690720){
                printf("Part 2: %d", code[i + 1] * 100 + code[i + 2]);
            }
            code[code[i + 3]] = code[code[i + 1]] + code[code[i + 2]];
        }
        else if (code[i] == 2) {
            if (verbose) {
                printf("Opcode 2: %d %d %d %d\n", code[i], code[i + 1],
                       code[i + 2], code[i + 3]);
            }
            if (code[i + 1] + code[i + 2] == 19690720){
                printf("Part 2: %d", code[i + 1] * 100 + code[i + 2]);
            }
            code[code[i + 3]] = code[code[i + 1]] * code[code[i + 2]];
        }
        else if (code[i] == 99) {
            if (verbose) {
                printf("Leaving int_code\n");
            }
            return code[0];
        }
        else {
            printf("Invalid code: %d\n", code[i]);
            throw std::invalid_argument("Invalid initializer");
        }
    }
    return code[0];
}

void get_inputs(FILE *file_pointer, int *code, int n_vals) {

    int i;
    fseek(file_pointer, 0L, SEEK_SET);
    for (i=0; i<n_vals; i++) {
        fscanf(file_pointer, "%d,", &code[i]);
    }
}


int main() {
    FILE* fp = fopen("dat/day_2.txt", "r");
    if (fp == NULL) {
        printf("File does not exist\n");
        exit(1);
    }
    fseek(fp, 0L, SEEK_END);
    int n_chars = ftell(fp);
    fseek(fp, 0L, SEEK_SET);
    int n_vals = 1;
    char line[n_chars];
    fscanf(fp, "%s\n", line);
    int i;
    for (i=0; i<sizeof(line); i++) {
        if (line[i] == ',') {
            n_vals++;
        }
    }
    if (verbose) {
        printf("File contains %d values\n", n_vals);
    }
    int opcode[n_vals];
    get_inputs(fp, opcode, n_vals);
    opcode[1] = 12;
    opcode[2] = 2;
    // Part 1 run
    int x = int_code(opcode, n_vals);
    printf("Part 1: %d\n", x);
    int j;
    for (i=0; i<=99; i++){
        for (j=0; j<=99; j++) {
            get_inputs(fp, opcode, n_vals);
            opcode[1] = i;
            opcode[2] = j;
            x = int_code(opcode, n_vals);
            if (x  == 19690720) {
                printf("Part 2: %d %d %d\n", i, j, 100 * i + j);
            }
        }
    }

    return 0;
}
