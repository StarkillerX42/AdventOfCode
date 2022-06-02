#include <string>
#include <string.h>
#include <iostream>
#include <sstream>
#include <vector>
#include <fstream>
using namespace std;


template <typename T>
std::ostream& operator<<(std::ostream& output, std::vector<T> const& values)
{
    for (auto const& value : values)
    {
        output << value << std::endl;
    }
    return output;
}


int int_code(vector<int> code, int storage, int verbose) {
    int i=0;
    int count = 0;
    bool keep_looping = true;
    while (keep_looping) {
        switch (code[i]) {
            case 1:
                if (verbose) {
                    printf("Opcode 1: %d@%d->%d\n", code[code[i+3]],
                        code[i+3], code[code[i+1]] + code[code[i+2]]);
                }
                code[code[i+3]]= code[code[i+1]] + code[code[i+2]];
                i += 4;
                break;
            case 2:
                if (verbose) {
                    printf("Opcode 2: %d@%d->%d\n", code[code[i+3]],
                        code[i+3], code[code[i+1]] * code[code[i+2]]);
                }
                code[code[i+3]]= code[code[i+1]] * code[code[i+2]];
                i += 4;
                break;
            case 3:
                if (verbose) {
                    printf("Opcode 3: %d@%d->%d\n", code[code[i+1]],
                    code[i+1], storage);
                }
                code[code[i+1]] = storage;
                i += 2;
                break;
            case 4:
                if (verbose) {
                    printf("Opcode 4: %d@storage->%d\n", storage,
                    code[code[i+1]]);
                }
                storage = code[code[i+1]];
                i += 2;
                break;
            case 5:
                if (code[i+1] != 0) {
                    if (verbose) {
                        printf("Opcode 5: Jumping to %d\n", code[i+2]);
                    }
                    i = code[i+2];
                } else {
                    if (verbose) {
                        printf("Opcode 5: Not jumping\n");
                    }
                    i += 3;
                }
                break;
            case 6:
                if (code[i+1] == 0) {
                    if (verbose) {
                        printf("Opcode 5: Jumping to %d\n", code[i+2]);
                    }
                    i = code[i+2];
                } else {
                    if (verbose) {
                        printf("Opcode 5: Not jumping\n");
                    }
                    i += 3;
                }
                break;
            case 7:
                if (code[code[i+1]] < code[code[i+2]]) {
                    code[code[i+3]] = 1;
                } else {
                    code[code[i+3]] = 0;
                }
                i += 4;
                break;
            case 8:
                if (code[code[i+1]] == code[code[i+2]]) {
                    code[code[i+3]] = 1;
                } else {
                    code[code[i+3]] = 0;
                }
                i += 4;
                break;
            case 99:
                keep_looping = false;
                break;
            default:
                if (verbose) {
                    printf("Parameter Mode: %d->%d %d %d\n",
                    code[i],
                    (code[i] % 100),
                    (code[i] % 1000) - (code[i] % 100),
                    (code[i] % 10000) - (code[i] % 1000));
                }
                int x1, x2;
                switch (code[i] % 1000 - code[i] % 100) {
                    case 0:
                        x1 = code[code[i+1]];
                        break;
                    case 100:
                        x1 = code[i+1];
                        break;
                }
                switch (code[i] % 10000 - code[i] % 1000) {
                    case 0:
                        x2 = code[code[i+2]];
                        break;
                    case 1000:
                        x2 = code[i+2];
                        break;
                }
                switch (code[i] % 100) {
                    // Check instruction type
                    
                    case 1:
                        code[code[i+3]] = x1 + x2;
                        i += 4;
                        break;
                    case 2:
                        code[code[i+3]] = x1 * x2;
                        i += 4;
                        break;
                    case 3:
                        code[x1] = storage;
                        i += 2;
                        break;
                    case 4:
                        storage = code[x1];
                        i += 2;
                        break;
                    case 5:
                        if (x1 != 0) {
                            i = x2;
                        } else {
                            i += 3;
                        }
                        break;
                    case 6:
                        if (x1 == 0) {
                            i = x2;
                        } else {
                            i += 3;
                        }
                        break;
                    case 7:
                        if (x1 < x2) {
                            code[code[i+3]] = 1;
                        } else {
                            code[code[i+3]] = 0;
                        }
                        i += 4;
                        break;
                    case 8:
                        if (x1 == x2) {
                            code[code[i+3]] = 1;
                        } else {
                            code[code[i+3]] = 0;
                        }
                        i += 4;
                        break;

                }
                break;
        }
        if (count > 1000) {
            break;
        }
        count++;
    }
    if (verbose) {
        for (auto const& value : code) {
                std::cout << value << ", ";
        }
        cout << endl;
    }

    return storage;
}

int main(int argc, char *argv[]) { 
    int verbose=0;
    int test=0;
    char **ptr;
    for (ptr=argv; *ptr !=NULL ; ptr++) {

        if (!strcmp(*ptr, "-v")){
            verbose++;
        }
        if (!strcmp(*ptr, "-t")){
            test = 1;
        }
    }
    if (verbose >= 1) {
        cout << "Verbosity: " << verbose << endl;
        cout <<"Testing: " << test << endl;
    }

    string file_path;
    if (test) {
        file_path = "dat/day_5_test.txt";
    } else {
        file_path = "dat/day_5.txt";
    }

    vector<int> opcode;

    int next_int;
    string line;
    stringstream sline;
    ifstream inputs(file_path);
    if (inputs.is_open()) {
        while (inputs.good()){
            getline(inputs, line, ',');
            sline << line;
            sline >> next_int;
            sline.clear();
            opcode.push_back(next_int);
        }
    }
    if (verbose >= 2) {
        for (auto const& value: opcode) {
            cout << value << ", ";
        }
        cout << endl;
    }
    if (verbose >= 1) {
        cout << "There are " << opcode.size() << " characters in the code" << endl;
    }
    int part_1 = int_code(opcode, 1, verbose);
    cout << "Part 1: " << part_1 << endl;
    
    int part_2 = int_code(opcode, 5, verbose);
    cout << "Part 2: " << part_2 << endl;

}
