#!/bin/bash

filter="foobar-"
old_dir="/opt/misc/"
new_dir="/srv/data/"

filter1="ExecStart="
filter2="WorkingDirectory="


# Сортировать список
for unit in $(systemctl list-units --type=service --all | grep "$filter" | awk "{print $1}"); do
    # Остановка юнита
    if systemctl stop "$unit" ; then
        echo "$unit остановлен."

        # Получение пути юнита
        path_unit=$(systemctl show $unit -p FragmentPath | sed 's/FragmentPath=//')
        old_path=$(sed -n "/$filter2/s|$filter2||p" $path_unit)

        # Перемещение
        if mv "$old_path" "$new_dir" ; then
            echo "Перемещение $old_path выполнено"

            # Редактирование
            sed -i "/$filter1/s|$old_dir|$new_dir|" $path_unit
            sed -i "/$filter2/s|$old_dir|$new_dir|" $path_unit
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

echo "Задача выполнена"