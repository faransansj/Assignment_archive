#include <iostream>
using namespace std;

class Square; 

class Rectangle {
private:
    double width, height;
public:
    Rectangle(double w, double h) : width(w), height(h) {}
    friend void calculateArea(const Rectangle& rect, const Square& square);
};

class Square {
private:
    double side;
public:
    Square(double s) : side(s) {}
    friend void calculateArea(const Rectangle& rect, const Square& square);
};

void calculateArea(const Rectangle& rect, const Square& square) {
    double rectArea = rect.width * rect.height;
    double squareArea = square.side * square.side;

    // 출력
    cout << "Rectangle Area: " << rectArea << endl;
    cout << "Square Area: " << squareArea << endl;
}

int main() {
    Rectangle rect(10.0, 5.0);  
    Square square(4.0);         

    // calculateArea 함수 호출
    calculateArea(rect, square);

    return 0;
}
