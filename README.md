# ProjektSystemyMikroprocesorowe

Rozpoznawanie Gestów FRDM KL 
Projekt zrealizujemy w oparciu o wbudowany akcelerometr, który będzie przetwarzał wykonywane gesty przez poruszanie płytką na zmiany przyspieszenia. Następnie przez magistralę I2C0, która służy do połączenia akcelerometru dane będą przechodzić do UARTa (0 lub 2) a stamtąd do zewnętrznego urządzenia (komputer). Dane będą zapisywane przez specjalnie napisany skrypt w pythonie ze zdefiniowanymi wielkościami ramki danych. Program będzie je interpretował i wizualizował. Gesty(np. kółko) będą proste, różniące się od siebie i powtarzane, aby zwiększyć precyzję niezbyt precyzyjnego akcelerometru MMA8451Q.
Dodatkowo z wykorzystaniem Machine Learningu chcielibyśmy, aby dane z akcelerometru były rozpoznawane jako gesty tak, aby móc je wykorzystać do jakiejś akcji (np. zapalenie i gaszenie diody).

Założenie funkcjonalne znajdują się w pliku opis.pdf


