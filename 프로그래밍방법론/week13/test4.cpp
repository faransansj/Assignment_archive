#include <iostream>
#include <map>

int main() {
    // 맵 초기화
    std::map<int, std::string> colorMap = {
        {1, "red"},
        {2, "blue"},
        {3, "green"}
    };

    // 키가 2인 요소를 찾고 출력
    std::map<int, std::string>::iterator it = colorMap.find(2);

    if (it != colorMap.end()) {
        std::cout << "키 2의 값: " << it->second << std::endl; 
    }
    else {
        std::cout << "키 2를 찾을 수 없습니다." << std::endl;
    }

    return 0;
}
