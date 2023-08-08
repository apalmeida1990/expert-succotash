import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from typing import List
from time import time, sleep, strftime
from utils.counter import Counter
from utils.logger import Logger

logger = Logger.get_logger(logger_name="ex_2")
TOTAL_FRUITS = 50
MAX_FARMER_THREADS = 3
MAX_CLEANER_THREADS = 3


def _print_counters(
    tree_fruits: Counter,
    dirty_basket: Counter,
    clean_basket: Counter,
    farmers: List[Counter],
    cleaners: List[Counter],
):
    """Prints the current state of the counters.

    Args:
        tree_fruits (Counter): The counter for the fruits on the tree.
        dirty_basket (Counter): The counter for the fruits on the dirty basket.
        clean_basket (Counter): The counter for the fruits on the clean basket.
        farmers (List[Counter]): The counters for the farmers collecting fruits.
        cleaners (List[Counter]): The counters for the cleaners cleaning fruits.
    """
    while clean_basket.value < TOTAL_FRUITS:
        date_log_str = f"{strftime('%Y-%m-%d %H:%M:%S')}"
        fruit_baskets_log = f"{tree_fruits.name} ({tree_fruits.value} fruits) - {dirty_basket.name} ({dirty_basket.value}) - {clean_basket.name} ({clean_basket.value})"
        farmers_log = f"Farmers: {', '.join([f'{farmer.name} ({farmer.value})' for farmer in farmers])}"
        cleaners_log = f"Cleaners: {', '.join([f'{cleaner.name} ({cleaner.value})' for cleaner in cleaners])}"
        logger.info(
            f"{date_log_str} - {fruit_baskets_log} - {farmers_log} - {cleaners_log}"
        )
        sleep(1)


def _collect_fruit(worker_name: str, tree_fruits: Counter, worker_count: Counter):
    """
        Collects fruit from the tree.
        Assumption: Process of removing fruit from the tree takes between 3 to 6 seconds (e.g. cutting the fruit from the tree)

    Args:
        worker_name (str): Fictional name of the worker.
        tree_fruits (Counter): The counter for the fruits on the tree. In this case, the tree_fruits counter is decremented.
        worker_count (Counter): The counter that keeps track if the worker is doing something. This counter is not shared between threads, it is a single counter for each thread.
    """
    fruits_on_tree = tree_fruits.decrement()
    worker_count.increment()

    wait_time = random.randint(3, 6)
    logger.debug(f"{worker_name} is waiting {wait_time} seconds to collect fruit.")
    sleep(wait_time)

    logger.debug(
        f"{worker_name} collected fruit. Fruits currently on tree: {fruits_on_tree}"
    )


def _deposit_on_dirty_basket(
    worker_name: str, dirty_basket: Counter, worker_count: Counter
):
    """
        Deposits fruit on the dirty basket.
        Assumption: As soon worker cuts the fruit from the tree, it is deposited on the dirty basket.
                    To simulate to process of walk into the dirty basket, a sleep of 1 second is added.
                    Simulates that 2 workers are working at the same time. One is cutting the fruit from the tree, the other is walking to the dirty basket.

    Args:
        worker_name (str): Fictional name of the worker.
        dirty_basket (Counter): The counter for the fruits on the dirty basket. In this case, the dirty_basket counter is incremented.
        worker_count (Counter): The counter that keeps track if the worker is doing something. This counter is not shared between threads, it is a single counter for each thread.
    """
    sleep(1)
    fruits_on_dirty_basket = dirty_basket.increment()
    worker_count.decrement()
    logger.debug(
        f"{worker_name} added fruit to dirty basket. Fruits currently on dirty basket: {fruits_on_dirty_basket}"
    )


def _collect_from_dirty_basket_and_wash(
    worker_name: str, dirty_basket: Counter, worker_count: Counter
):
    """
        Grab fruit from the dirty basket and wash it.
        Assumption: The process of washing the fruit takes between 2 to 4 seconds before it is deposited on the clean basket.

    Args:
        worker_name (str): Fictional name of the worker.
        dirty_basket (Counter): The counter for the fruits on the dirty basket. In this case, the dirty_basket counter is decremented.
        worker_count (Counter): The counter that keeps track if the worker is doing something. This counter is not shared between threads, it is a single counter for each thread.
    """
    fruits_on_dirty_basket = dirty_basket.decrement()
    worker_count.increment()

    wait_time = random.randint(2, 4)
    logger.debug(f"{worker_name} is waiting {wait_time} seconds to collect fruit.")
    sleep(wait_time)

    logger.debug(
        f"{worker_name} removed fruit from dirty basket. Fruits currently on dirty basket: {fruits_on_dirty_basket}"
    )


def _deposit_on_clean_basket(
    worker_name: str, clean_basket: Counter, worker_count: Counter
):
    """
        Deposits fruit on the clean basket.
        Assumption: As soon worker washes the fruit, it is deposited on the clean basket immediately.
                    The clean basket is not in the same location as the dirty basket, so it takes 1 second to walk to the clean basket.

    Args:
        worker_name (str): Fictional name of the worker.
        clean_basket (Counter): The counter for the fruits on the clean basket. In this case, the clean_basket counter is incremented.
        worker_count (Counter): The counter that keeps track if the worker is doing something. This counter is not shared between threads, it is a single counter for each thread.
    """
    sleep(1)
    fruits_on_clean_basket = clean_basket.increment()
    worker_count.decrement()
    logger.debug(
        f"{worker_name} added fruit to clean basket. Fruits currently on clean basket: {fruits_on_clean_basket}"
    )


def move_from_tree_to_dirty_basket(
    worker_name: str, tree_fruits: Counter, dirty_basket: Counter, worker_count: Counter
):
    """
        Simulates the process of moving fruit from the tree to the dirty basket as soon as no other worker is doing the same process.
        The locks ensure that the process is atomic and that the counters are updated correctly, Simulating that only one worker can access the tree or the dirty basket at a time.
        As soon as the tree is empty (tree_fruits == 0), the worker stops collecting fruit and returns.

    Args:
        worker_name (str): Fictional name of the worker.
        tree_fruits (Counter): The counter for the fruits on the tree.
        dirty_basket (Counter): The counter for the fruits on the dirty basket.
        worker_count (Counter): The counter that keeps track if the worker is doing something. This counter is not shared between threads, it is a single counter for each thread.
    """
    while True:
        with tree_fruits.lock:
            if tree_fruits.get_value() == 0:
                logger.warning("No more fruits to collect!")
                return
            _collect_fruit(worker_name, tree_fruits, worker_count)

        with dirty_basket.lock:
            _deposit_on_dirty_basket(worker_name, dirty_basket, worker_count)


def move_from_dirty_to_clean_basket(
    worker_name: str,
    dirty_basket: Counter,
    clean_basket: Counter,
    worker_count: Counter,
):
    """
        Simulates the process of grabbing fruit from the dirty basket, washing it and depositing it on the clean basket as soon as no other worker is doing the same process.
        Imagine that only exists one sink to wash the fruit.
        As soon the clean basket is full (clean_basket == total of fruits originally on the tree), the worker stops and returns.

    Args:
        worker_name (str): Fictional name of the worker.
        dirty_basket (Counter): The counter for the fruits on the dirty basket.
        clean_basket (Counter): The counter for the fruits on the clean basket.
        worker_count (Counter): The counter that keeps track if the worker is doing something. This counter is not shared between threads, it is a single counter for each thread.
    """
    while True:
        with dirty_basket.lock and clean_basket.lock:
            if (
                dirty_basket.get_value() == 0
                and clean_basket.get_value() == TOTAL_FRUITS
            ):
                logger.warning("No more fruits to wash!")
                return
            elif dirty_basket.get_value() == 0:
                continue
            _collect_from_dirty_basket_and_wash(
                worker_name, dirty_basket, worker_count
            )

        with clean_basket.lock:
            _deposit_on_clean_basket(worker_name, clean_basket, worker_count)


def process_fruits():
    """
    Main function that simulates the process of collecting and washing fruits.
    Manages the threads and the counters.
    Decided to not set counters as globals because this way you can restrict the access to the counters and make sure that only the threads that need to access the counter can do it.
    I try to avoid the use of global variables because any other process can access them and modify them, which can be dangerous and lead to unexpected results.
    """
    print("Starting fruit collection and washing...")
    # Start the timer
    start_time = time()

    # Initialize the counters
    tree_fruits_counter = Counter(initial_value=TOTAL_FRUITS, name="Tree Fruits")
    dirty_basket_counter = Counter(name="Dirty Basket")
    clean_basket_counter = Counter(name="Clean Basket")
    farmers_counters = [
        Counter(name=f"Farmer {i+1}") for i in range(MAX_FARMER_THREADS)
    ]
    cleaners_counters = [
        Counter(name=f"Cleaner {i+1}") for i in range(MAX_CLEANER_THREADS)
    ]

    # ThreadPoolExecutor allows us to share memory between threads
    with ThreadPoolExecutor(
        max_workers=MAX_FARMER_THREADS + MAX_CLEANER_THREADS,
    ) as executor:
        # Submit the tasks for execution
        tasks = [
            executor.submit(
                move_from_tree_to_dirty_basket,
                f"Farmer {i+1}",
                tree_fruits_counter,
                dirty_basket_counter,
                farmers_counters[i],
            )
            for i in range(MAX_FARMER_THREADS)
        ] + [
            executor.submit(
                move_from_dirty_to_clean_basket,
                f"Cleaner {i+1}",
                dirty_basket_counter,
                clean_basket_counter,
                cleaners_counters[i],
            )
            for i in range(MAX_CLEANER_THREADS)
        ]

        # Start the thread to print counters
        printer_thread = threading.Thread(
            target=_print_counters,
            args=(
                tree_fruits_counter,
                dirty_basket_counter,
                clean_basket_counter,
                farmers_counters,
                cleaners_counters,
            ),
        )
        printer_thread.start()

        # Wait for the tasks to finish and collect the results
        # results won't be used for anything, but we need to wait for the tasks to finish
        for future in as_completed(tasks):
            try:
                result = future.result()
            except Exception as e:
                logger.error(f"Error while executing task: {e}")

        # Wait for the printer thread to finish
        printer_thread.join()

        # Print the results
        logger.info(f"Total fruits on tree: {tree_fruits_counter.value}")
        logger.info(f"Total fruits collected: {dirty_basket_counter.value}")
        logger.info(f"Total fruits washed: {clean_basket_counter.value}")
        logger.info(f"Total time taken: {time() - start_time}")


if __name__ == "__main__":
    process_fruits()
