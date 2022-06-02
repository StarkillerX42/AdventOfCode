#include <string>
#include <string.h>
#include <iostream>
#include <sstream>
#include <vector>
#include <fstream>
#include <map>
using namespace std;


int count_path(map<string, string> orbits, string start) {
    int count=0;
    bool in_list = false;
    for (const auto &p: orbits) {
        if (p.first == start) {
            in_list = true;
        }
    }
    if (!in_list) {
        return 0;
    }
    while (start != "COM") {
        start = orbits[start];
        count++;
    }
    return count;
}


vector<string> generate_path(map<string, string> orbits, string start) {
    vector<string> path;
    bool in_list = false;
    for (const auto &p: orbits) {
        if (p.first == start) {
            in_list = true;
        }
    }
    if (!in_list) {
        return path;
    }
    while (start != "COM") {
        path.push_back(start);
        start = orbits[start];
    }
    return path;
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
        file_path = "dat/day_6_test.txt";
    } else {
        file_path = "dat/day_6.txt";
    }

    map<string, string>orbits;
    map<string, int> counts;
    string line, parent, child;
    ifstream inputs(file_path);
    if (inputs.is_open()) {
        while (inputs.good()) {
            getline(inputs, parent, ')');
            getline(inputs, child);
            if (parent == "") {
                break;
            }
            if (verbose) {
                cout << parent << " ) " << child << endl;
            }
            // sscanf(line.c_str(), "%s)%s", &parent, &child);
            orbits[child] = parent;
        }
    }

    cout << "Distance from D is " << count_path(orbits, "D") << endl;
    int count = 0;
    for (const auto &p: orbits) {
        // cout << p.first << "\t" << p.second << endl;
        bool found_parent = false;
        for (const auto &c: counts) {
            if (c.first ==  p.first) {
                counts[p.first] = c.second + 1;
                count += c.second + 1;
                found_parent = true;
                break;
            }
        }
        if (!found_parent) {
            count += count_path(orbits, p.first);
        }
    }

    cout << "Part 1: " << count << endl;

    vector <string> my_path, s_path;
    my_path = generate_path(orbits, "YOU");
    s_path = generate_path(orbits, "SAN");

    int m_steps = 0;
    int s_steps = 0, part_2 = 0;
    for (auto const &m: my_path) {
        s_steps = 0;
        cout << "My: " << m << endl;
        for (auto const &s: s_path) {
            s_steps++;
            if (m == s && !part_2) {
                cout << "Meet: " << s_steps << endl;
                part_2 = m_steps + s_steps - 3;
            }
        }
        m_steps++;
    }
    cout << "Part 2: " << part_2 << endl;
}
