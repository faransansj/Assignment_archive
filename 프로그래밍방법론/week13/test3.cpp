#include <iostream>
#include <vector>

int main() {
    // 벡터 초기화
    std::vector<int> vec = { 5, 10, 15, 20, 25 };

    // iterator를 사용하여 벡터의 요소를 순회하며 값이 15보다 큰 요소 출력
    std::cout << "값이 15보다 큰 요소: ";
    for (std::vector<int>::iterator it = vec.begin(); it != vec.end(); ++it) {
        if (*it > 15) {
            std::cout << *it << " ";  // iterator가 가리키는 값이 15보다 크면 출력
        }
    }
    std::cout << std::endl;

    return 0;
}
