#include <iostream>

int main() {
    int space = 2;
    int stars = 1;
    for (int i = 0;i < 3;i++) {
        int n = 0;
        while (n != space) {
            std::cout << " ";
            n++;
        }
        space--;
        for (int j = 0;j < stars;j++) {
            std::cout << "* ";
        }
        std::cout << '\n';
        stars++;
    }
    for (int j = 0;j < 2;j++) {
        space++;
        int nn = 0;
        while (nn != space) {
            std::cout << " ";
            nn++;
        }
        stars--;
        for (int i = 0;i < stars-1;i++) {
            std::cout << " *";
        }
        std::cout << '\n';
        
    }
    return 0;
}