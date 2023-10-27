from datetime import datetime

from cache_hw.cache_utils import cache_result, cache_update, data_converter


@cache_result
def fibonacci(n):
    if int(n) <= 2:
        return 1
    return fibonacci(int(n) - 1) + fibonacci(int(n) - 2)


n = 20
start_time = datetime.now()
fibonacci_result = fibonacci(n)
end_time = datetime.now()
print(end_time - start_time)
print(f"Число Фібоначчі для n = {n}: {fibonacci_result}")

data = {
    "a": "1",
    "b": "2",
    "c": "3",
    "d": "4",
}


@cache_update
def get_data(n):
    return data.get(n)


@cache_update
def update_data(n, value):
    data.update({n: value})


for n in data:
    get_data_1 = get_data(n)
    print(data_converter(get_data_1, str))
update_data("a", value="aaaaaa")
get_data_2 = get_data("a")
print(data_converter(get_data_2, str))
update_data("a", value="bbbbb")
get_data_3 = get_data("a")
print(data_converter(get_data_3, str))
