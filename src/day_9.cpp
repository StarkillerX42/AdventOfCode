#include <string>
#include <string.h>
#include <iostream>
#include <sstream>
#include <vector>
#include <fstream>
#include <algorithm>
using namespace std;


template <typename T>
std::ostream& operator<<(std::ostream& output, std::vector<T> const& values)
{
    for (auto const& value : values)
    {
        output << value << endl;
    }
    return output;
}


void display_array(int x[], int n) {
    for (int i=0; i < n; i++) {
        cout << x[i] << " ";
    }
    cout << endl;
}


void display_vector(vector<int> x) {
    for (auto const &xi : x) {
        cout << xi << " ";
    }
    cout << endl;
}


int factorial(int x) {
    if (x==1 || x==0) {
        return 1;
    } else {
        return x * factorial(x - 1);
    }
}

/*
int opcode(int mode, vector <int> values, vector <int> *code, int verbose) {
    switch (mode) {
        case 1:
            case 1:
                if (verbose) {
                    printf("Opcode 1: %d@%d->%d\n", code.at(values[2]),
                        code.at(2], code.at(values[2]) + code.at(values[1]]);
                }
                code[values[2]]= code[code[i+1]] + code[code[i+2]];
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
                    cout << "Opcode 3, taking input: " << inputs[input_i] << " with input_i " << input_i << endl;
                }
                code[code[i+1]] = inputs[input_i];
                input_i++;
                i += 2;
                break;
            case 4:
                if (verbose) {
                    cout << "Out: " << code[code[i+1]] << endl;
                }
                outputs.push_back(code[code[i+1]]);
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

    }
    
    return 0;
}*/


vector<int> int_code(vector<int> code, vector<int> inputs, int verbose) {
    int i=0;
    int count = 0;
    bool keep_looping = true;
    int input_i = 0;
    int base = 0;
    vector<int> outputs;
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
                    cout << "Opcode 3, taking input: " << inputs[input_i] << " with input_i " << input_i << endl;
                }
                code[code[i+1]] = inputs[input_i];
                input_i++;
                i += 2;
                break;
            case 4:
                if (verbose) {
                    cout << "Out: " << code[code[i+1]] << endl;
                }
                outputs.push_back(code[code[i+1]]);
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
                int x0, x1, x2;
                switch (code[i] % 100 - code[i] % 10) {
                    case 0:
                        x0 = code[code[i]];
                        break;
                    case 10:
                        x0 = code[i];
                }
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
                switch (x0) {
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
                        code[x1] = inputs.at(input_i);
                        input_i++;
                        i += 2;
                        break;
                    case 4:
                        // cout << "Out: " << code[x1] << endl;
                        outputs.push_back(code[x1]);
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
    if (verbose >= 2) {
        for (auto const& value : code) {
                std::cout << value << ", ";
        }
        cout << endl;
    }

    return outputs;
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
        file_path = "dat/day_7_test.txt";
    } else {
        file_path = "dat/day_7.txt";
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

    vector<int> out_1;
    int part_1 = 0, part_2 = 0;
    int phase_setting[] = {4,3,2,1,0};
    int n = sizeof(phase_setting) / sizeof(phase_setting[0]);
    vector <int> ins;

    // sort(phase_setting, phase_setting + n);
    // display_array(phase_setting, n);
    // // cout << "There are " << n << " elements in phase_setting" << endl;
    // for (int i=0; i<1; i++) {
    //     out_1 = {0};
    //     for (int j=0; j<n; j++) {
    //         ins = {phase_setting[j], out_1.at(out_1.size() - 1)};
    //         out_1 = int_code(opcode, ins, verbose);
    //     }
    //     if (verbose) {
    //         display_array(phase_setting, n);
    //         cout << i << "->" << out_1.at(out_1.size() - 1) << endl;
    //     }
    //     next_permutation(phase_setting, phase_setting + n);
    //     part_1 = max(out_1.at(out_1.size() - 1), part_1);
    // }

    cout << "================= Part 2 ===================" << endl;
    int phase_setting_2[] = {9, 8, 7, 6, 5};
    // int phase_setting_2[] = {4, 3, 2, 1, 0};
    vector<int> out_2 = {0};
    // sort(phase_setting_2, phase_setting_2 + n);
    // for (int i=0; i<factorial(n); i++) {
        for (int k=0; k<10000; k++) {
            for (int j=0; j<n; j++) {
                if (k==0) {
                    ins = {phase_setting_2[j], out_2.at(out_2.size()-1)};
                } else {
                    ins = {phase_setting_2[j]};
                    for (auto const &p: out_2) {
                        ins.push_back(p);
                    }
                }
                display_vector(ins);
                out_2 = int_code(opcode, ins, verbose);
            }
        }
        display_array(phase_setting_2, n);
        display_vector(out_2);
        // cout << i << "->" << out << endl;
        // next_permutation(phase_setting_2, phase_setting_2 + n);
        // part_2 = max(out, part_2);
    // }

    // cout << "Part 1: " << part_1 << endl;
    // cout << "Part 2: " << part_2 << endl;

}
