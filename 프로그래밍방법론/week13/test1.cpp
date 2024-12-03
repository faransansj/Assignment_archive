#include <iostream>
#include <vector>

int main() {
    // 벡터 초기화
    std::vector<int> vec = {2, 4, 6, 8};

    // 벡터의 모든 요소를 더하기 위한 변수
    int sum = 0;

    // iterator를 사용하여 벡터의 모든 요소에 접근
    for (std::vector<int>::iterator it = vec.begin(); it != vec.end(); ++it) {
        sum += *it;  // iterator가 가리키는 값에 더함
    }

    // 결과 출력
    std::cout << "벡터의 모든 요소의 합: " << sum << std::endl;

    return 0;
}
