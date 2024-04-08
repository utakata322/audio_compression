Запуск скрипта происходит через Git Bash с помощью команды: 
bash run.sh <input_path> <output_path> <time_stretch_ratio>, где: 
<input_path> - путь файла, который необходимо преобразовать; 
<output_path> - путь файла, который получился после преобразования;
<time_stretch_ratio> - коэфициент r сжатия(растяжения) аудио, если 0 < r < 1, то аудио растянется, если r > 1, то сожмётся;
Например:
bash run.sh test_mono.wav output_signal.wav 2
