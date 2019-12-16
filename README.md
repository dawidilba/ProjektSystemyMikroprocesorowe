# ProjektSystemyMikroprocesorowe

Rozpoznawanie Gestów FRDM KL 
Projekt zrealizujemy w oparciu o wbudowany akcelerometr, który będzie przetwarzał wykonywane gesty przez poruszanie płytką na zmiany przyspieszenia. Następnie przez magistralę I2C0, która służy do połączenia akcelerometru dane będą przechodzić do UARTa (0 lub 2) a stamtąd do zewnętrznego urządzenia (komputer). Dane będą zapisywane przez specjalnie napisany skrypt w pythonie ze zdefiniowanymi wielkościami ramki danych. Program będzie je interpretował i wizualizował. Gesty(np. kółko) będą proste, różniące się od siebie i powtarzane, aby zwiększyć precyzję niezbyt precyzyjnego akcelerometru MMA8451Q.
Dodatkowo z wykorzystaniem Machine Learningu chcielibyśmy, aby dane z akcelerometru były rozpoznawane jako gesty tak, aby móc je wykorzystać do jakiejś akcji (np. zapalenie i gaszenie diody).

Analiza problemu:
Akcelermetr jest to przedmiot mierzący przyspieszenia linowe i kątowe

Plan realizacji:
Projekt zostanie wykonany na platformie FRDM KL46Z z wykorzsystaniem wbudowanego akcelerometru MMA8451Q (jest czujnikiem przyspieszenia z czułością pracy ±2g, ±4g, ±8g, ±16g). Na podstawie zmierzonych wartosci z czujnika które przez interejs wyjsciowy I2C(0) zostaną nam przesłane będziemy okreslać położenie płytki wzgledem punktu poprzedniego. Dane za pomocą interfejsu szeregowego UART zostaną wysłane do (komputera) gdzie z wykrozsytaniem pythona dane odbierzemy i przetworzymy.
Na początku projekt zostanei wykonany schodkowo punkt po punkcie (plik plan.txt). W momencie gdy każdy z elementów będzie działać prawidłowo nastąpi obsługa danych w czasie rzeczywistym i wizualizowanei pozycji płytki na ekranie komputera. 


