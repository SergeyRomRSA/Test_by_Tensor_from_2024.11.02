#!/bin/bash

filter="foobar-"
old_dir="/opt/misc/"
new_dir="/srv/data/"

filter1="ExecStart="
filter2="WorkingDirectory="

# Проверка существования новой директории
if [[ ! -d "$new_dir" ]]; then
    echo "Целевая директория $new_dir не существует. Создание..."
    mkdir -p "$new_dir" || { echo "Не удалось создать директорию $new_dir"; exit 1; }
fi

# Сортировать список
for unit in $(systemctl list-units --type=service --all | grep "$filter" | awk '{print $1}'); do
    # Остановка юнита
    if systemctl stop "$unit" ; then
        echo "$unit остановлен."

        # Получение пути юнита
        path_unit=$(systemctl show "$unit" -p FragmentPath | sed 's/FragmentPath=//')
        old_path=$(sed -n "/$filter2/s|$filter2||p" "$path_unit")

        # Проверка существования старого пути
        if [[ ! -d "$old_path" ]]; then
            echo "Старый путь $old_path не существует. Пропуск..."
            continue
        fi

        # Перемещение
        if mv "$old_path" "$new_dir" ; then
            echo "Перемещение $old_path выполнено"

            # Редактирование
            sed -i "/$filter1/s|$old_dir|$new_dir|" "$path_unit"
            sed -i "/$filter2/s|$old_dir|$new_dir|" "$path_unit"
            echo "Редактирован файл $path_unit"
        else
            echo "Невозможно перенести директорию... Редактирование файла $path_init отменено"
        fi

        # Запуск юнита
        if systemctl start "$unit" ; then
            echo "$unit запущен."
        else
            echo "Ошибка запуска $unit"
        fi
    else
        echo "Ошибка остановки $unit"
    fi
done

echo "Задача выполнена."