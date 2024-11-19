#include <iostream>
using namespace std;

// Animal class 
class Animal 
{
public:
    virtual void sound() = 0;
    virtual ~Animal() {}
};

// Dog class 
class Dog : public Animal 
{
public:
    // sound() overriding
    void sound() override 
    {
        cout << "Dog" << endl;
    }
};

// Cat class 
class Cat : public Animal {
public:
    // sound() overriding 
    void sound() override {
        cout << "Cat" << endl;
    }
};

int main() {
    Animal* emp;
    Dog man;
    Cat eng;

    //Dog
    emp = &man;
    emp -> sound();

    //Cat 
    emp = &eng;
    emp -> sound();

    return 0;
}
