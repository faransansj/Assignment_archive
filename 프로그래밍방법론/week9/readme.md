### 1
Person 클래스를 작성하고, 복사 생성자를 구현하여 이름(name)을 복사하세
요. main에서 객체를 복사하고 복사된 객체의 이름을 출력하세요.
• Person 클래스 선언
• 복사 생성자 구현
• 객체 생성 및 복사

### 2
Parent1과 Parent2 클래스에서 동일한 이름의 show() 메서드를 구현하세요. 이 두 클래스를 상속받는
Child 클래스에서 메서드 충돌을 해결하여 두 메서드를 모두 호출하세요.
• Parent1 클래스 구현 (2점)
• Parent2 클래스 구현 (2점)
• Child 클래스 구현 및 메서드 충돌 해결 (3점)

### 3 
Rectangle 클래스와 Square 클래스를 작성하고, Rectangle의 private 멤버를 접근할 수 있는 friend 함수
를 calculateArea()로 구현하세요. 이 함수는 Rectangle과 Square 객체를 받아 각 면적을 계산하고 출력
합니다.
• Rectangle 클래스 선언 및 멤버 변수(width, height) 선언
• Square 클래스 선언 및 멤버 변수(side) 선언
• friend 함수 구현
• calculateArea() 메소드에서는 width * height 와 side 출력

### 4 
Car 클래스와 Mechanic 클래스를 작성하고, Car 클래스의 private 멤버 변수 engineStatus에 Mechanic 클
래스가 접근할 수 있도록 friend 클래스로 선언하세요. Mechanic 클래스에서 Car 객체의 engineStatus를
출력하는 함수를 작성하세요.
• Car 클래스 선언 및 private 멤버 변수(engineStatus) 선언
• friend 클래스 선언 및 구현
