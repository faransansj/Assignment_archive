#include <iostream>
using namespace std;

// Person class 
class Person
{
public:
    virtual void introduce() 
    {
        cout << "나는 사람" << endl;
    }
    virtual ~Person() {}
};

// studnet class 
class Student : virtual public Person
{
public:
    // intro() overriding
    void introduce() override
    {
        cout << "나는 학생" << endl;
    }
};

// engineer class 
class Teacher : virtual public Person 
{
public:
    // introduce() overriding 
    void introduce() override 
    {
        cout << "나는 선생" << endl;
    }
};

// 다중상속
class StudentTeacher : public Student, public Teacher
{
public:
    // introduce() overriding
    void introduce() override 
    {
        cout << "나는 학생, 나는 선생" << endl;
    }
};



int main() {
    Person* per;
    Student stu;
    Teacher tea;
    StudentTeacher snt;

    //student 
    per = &stu;
    per ->introduce();

    //teacher 
    per = &tea;
    per -> introduce();

    //student teacher 
    per = &snt;
    per -> introduce();

    return 0;
}
