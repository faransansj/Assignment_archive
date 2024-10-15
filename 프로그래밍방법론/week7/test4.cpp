#include <iostream>
#include <string>
#include <vector>
using namespace std;

class Book
{
public:
    string title, author;
    Book(string bookTitle, string bookAuthor)
        :title(bookTitle), author(bookAuthor) {}
};

class BookList
{
private:
    vector<Book> books; // book list 

public:
    // add book
    void addBook(const string& title, const string& author)
    {
        books.emplace_back(title, author);
        cout << "도서 \"" << title << "\"가 추가되었습니다." << endl;
    }

    // print book list 
    void displayBooks() const
    {
        if (books.empty())
        {
            cout << "현재 도서 목록이 비어 있습니다." << endl;
            return;
        }

        cout << "도서 목록:" << endl;
        for (const auto& book : books)
        {
            cout << "제목: " << book.title << ", 저자: " << book.author << endl;
        }
    }
};

int main()
{
    int input_num;
    string input_title, input_author;

    BookList myBookList;
    while (true)
    {
        cout << "도서관 관리시스템" << endl
            << "1) 도서 목록 조회" << endl
            << "2) 도서 추가 " << endl
            << "3) 종료" << endl
            << "입력 : ";
        cin >> input_num;
        if (input_num == 1)
        {
            myBookList.displayBooks();
        }

        if (input_num == 2)
        {
            cout << "작품명을 입력하세요 : ";
            cin >> input_title;
            cout << "작가명을 입력하세요 : ";
            cin >> input_author;
            myBookList.addBook(input_title, input_author);
        }
        if (input_num == 3)
        {
            break;
        }
        //else 뭔가 에러가남
        //{
        //    cout << "올바른 입력이 아닙니다." << endl;
        //}
    }
    return 0;
}