#include <iostream>
#include <fstream>
#include <vector>
using namespace std;


void read_file(string file_name) {
    ifstream inFile(file_name);
    int nLines = 0;
    string line;
    int lLen;
    if (inFile.is_open() ) {
        while (! inFile.eof()) {
            getline(inFile, line);
            if (!line.empty()) {
                nLines++;
                lLen = line.length();
            }
        }
    }
    inFile.close();
    inFile.open(file_name);
    cout << nLines << "x" << lLen << endl;
    int vals[lLen][nLines];
    if (inFile.is_open()) {
        int j = 0;
        while (! inFile.eof()) {
            inFile >> line;
            for (int i=0;i<lLen;i++) {
                vals[i][j] = int (line[i]);
            }
            j++;
        }
    }
    cout << sizeof
}


int main() {
    read_file("dat/day_12_test.txt");
    return 0;
}
