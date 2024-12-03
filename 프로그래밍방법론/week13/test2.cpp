#include <iostream>
#include <vector>

int main() {
    // 벡터 초기화
    std::vector<int> vec = { 1, 2, 3, 4 };

    // iterator를 사용하여 벡터의 각 요소를 2배로 증가시킴
    for (std::vector<int>::iterator it = vec.begin(); it != vec.end(); ++it) {
        *it *= 2;  // iterator가 가리키는 값을 2배로 증가
    }

    // 수정된 벡터 출력
    std::cout << "수정된 벡터: ";
    for (std::vector<int>::iterator it = vec.begin(); it != vec.end(); ++it) {
        std::cout << *it << " ";  // 각 요소 출력
    }
    std::cout << std::endl;

    return 0;
}
