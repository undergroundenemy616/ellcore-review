**Понятность и читаемость кода**:

Читаемость кода на данном проекте в целом достаточно хороша, благодаря структурированному подходу к организации классов и функций. Однако есть несколько заметных вопросов, связанных с соблюдением соглашений по стилю кода PEP 8, которые, если их решить, значительно улучшат общую читаемость и поддерживаемость кода.

1.  PEP 8: E302. В соответствии со стандартом PEP 8, между функциями или определениями классов должно быть две пустые строки. Нарушение этого принципа обнаружено в файле goods.services.py на строке 22. Это улучшает визуальное разделение между различными секциями кода.
2.  PEP 8: E111. Отступы в коде должны быть кратными четырём пробелам. Это соглашение облегчает чтение кода и его структурирование. Отступ, который не является кратным 4 пробелам, найден в goods.services.py на строке 23.
3.  Согласно PEP 8, имена классов должны следовать соглашению CamelCase, что облегчает их идентификацию в коде. Например, в users.hash.py на строке 6 имя класса не следует этому соглашению.

+ Дублирование импортов, импорты не отсортированы по pep и все все что пайчарм выделяет желтым цветом.

Рекомендуется провести рефакторинг кода с целью приведения его в соответствие со стандартами PEP 8. Это не только сделает ваш код более читаемым, но и облегчит работу с ним другим разработчикам, так как PEP 8 является общепринятым стандартом стиля кода для Python.

Также может быть полезно использовать автоматические инструменты проверки стиля кода, такие как flake8 или pylint, чтобы обеспечить постоянное соблюдение этих стандартов.

**Архитектура**:
Архитектура приложения в целом соответствует стандартам и рекомендациям для проектов на FastAPI. Приложение правильно разделено на модели, роутеры, сервисы и прочие компоненты, что обеспечивает гибкость и поддерживаемость кода.

Однако, в процессе ревью было замечено, что в сервисах присутствует логика, связанная с HTTP исключениями. Это может создать проблемы с точки зрения разделения ответственности и принципов чистого кода. Идеально, сервисы должны отвечать только за бизнес-логику, в то время как работа с HTTP исключениями должна быть вынесена на уровень роутеров или других компонентов, которые непосредственно работают с HTTP запросами и ответами.

Сервисы должны возвращать данные или кидать бизнес-исключения, которые затем перехватываются на уровне роутера и преобразуются в соответствующие HTTP исключения. Это обеспечит более четкое разделение ответственности и сделает код более удобным для чтения и поддержки. Кроме того, такой подход улучшит тестируемость, так как сервисы можно будет тестировать независимо от HTTP инфраструктуры.

**Тестирование**:

Отсутствие тестов в текущем проекте — это серьезная проблема, которая может привести к большому количеству ошибок в проде и увеличению времени на обнаружение и исправление этих ошибок. 

Пирамида тестирования — это концепция, которая показывает, как идеально должны быть распределены тесты в вашем приложении. На нижнем уровне пирамиды находятся юнит-тесты, которые проверяют отдельные модули или функции в изоляции. Они должны быть наиболее многочисленными, так как они быстрые, легко пишутся и поддерживаются.

На следующем уровне находятся интеграционные тесты, которые проверяют взаимодействие между различными модулями или слоями приложения. Они позволяют обнаружить проблемы, которые могут возникнуть при взаимодействии различных частей системы.

На вершине пирамиды находятся E2E (end-to-end) тесты, которые проверяют работу всего приложения в целом. Их обычно меньше всего, так как они сложнее в написании и поддержке, и они обычно требуют больше времени для выполнения.

Для написания тестов в Python обычно используется фреймворк pytest. Он обеспечивает удобный и гибкий интерфейс для написания тестов на всех уровнях пирамиды тестирования. Pytest поддерживает как классический подход к написанию тестов, так и функциональный стиль, который позволяет писать более модульные и гибкие тесты. Pytest также имеет широкий спектр плагинов, которые позволяют расширить его функциональность и адаптировать под специфические задачи тестирования.

**Прочее**:
1. Давайте все таки вместо принтов использовать полноценное логирование (https://docs.python.org/3/library/logging.html)
2. Советую обратить внимание на этот гайд по построению проектов на фастапи (https://github.com/zhanymkanov/fastapi-best-practices)