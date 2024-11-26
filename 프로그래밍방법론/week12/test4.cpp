#include <iostream>
#include <string>
using namespace std;

string langchage(string text,string target,string replacement)
{
    // 처음 등장하는 위치 찾기
    size_t pos = text.find(target);
    // 문자열 교체
    if (pos != string::npos) {
        text.replace(pos, target.length(), replacement);
        cout << "교체 후 문장: " << text << endl;
    }
    else {
        cout << target << " 을 찾을 수 없음" << endl;
    }

    return text;
}

int main() 
{
    string text = "I love Apples and APPLES";
    string target1 = "Apples";
    string target2 = "APPLES";
    string replace1 = "Oranges";

    string newtext = langchage(text, target1, replace1);
    string newnewtext = langchage(newtext, target2, replace1);
    
    // 출력
    cout << newnewtext << endl;

    return 0;
}
