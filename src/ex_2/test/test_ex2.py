import pytest
import main
from utils.counter import Counter

# @pytest.fixture(scope="function")
# def my_counter(request):
#     return Counter(initial_value=request.initial_value, name=request.name)


@pytest.fixture
def my_counter(request):
    return Counter(
        initial_value=request.param["initial_value"], name=request.param["name"]
    )

@pytest.fixture
def dirty_basket_counter(request):
    return Counter(initial_value=request.param["initial_value"], name="Dirty Basket")

@pytest.fixture
def clean_basket_counter(request):
    return Counter(initial_value=request.param["initial_value"], name="Clean Basket")

@pytest.fixture
def tree_fruit_counter(request):
    return Counter(initial_value=request.param["initial_value"], name="Tree Fruits")

@pytest.fixture
def worker_counter(request):
    return Counter(initial_value=request.param["initial_value"], name="Worker Counter")

# @pytest.fixture
# def mock_counters_test_move_from_dirty_to_clean_basket():
#     dirty_basket_counter = Counter(initial_value=5, name="Dirty Basket")
#     clean_basket_counter = Counter(initial_value=0, name="Clean Basket")
#     worker_counter = Counter(initial_value=0, name="Worker Count")

#     return dirty_basket_counter, clean_basket_counter, worker_counter


@pytest.mark.parametrize(
    "my_counter", [{"name": "Test Counter", "initial_value": 0}], indirect=True
)
def test_counter_increment(my_counter):
    assert my_counter.increment() == 1
    assert my_counter.increment() == 2


@pytest.mark.parametrize(
    "my_counter", [{"name": "Test Counter", "initial_value": 0}], indirect=True
)
def test_counter_decrement(my_counter):
    assert my_counter.decrement() == -1
    assert my_counter.decrement() == -2


@pytest.mark.parametrize(
    ("tree_fruit_counter", "worker_counter"),
    [
        ({"initial_value": 5}, {"initial_value": 0}),
        ({"initial_value": 0}, {"initial_value": 0}),
    ],
    indirect=["tree_fruit_counter", "worker_counter"]
)
def test_collect_fruit(tree_fruit_counter, worker_counter):
    tree_fruit_counter_initial_value = tree_fruit_counter.value
    worker_counter_initial_value = worker_counter.value
    # Call the _collect_fruit function with the specified counters
    main._collect_fruit("Test Farmer", tree_fruit_counter, worker_counter)
    # Verify the expected behavior
    assert tree_fruit_counter.value == tree_fruit_counter_initial_value - 1
    assert worker_counter.value == worker_counter_initial_value + 1
    assert worker_counter.value == 0 or worker_counter.value == 1, "Value must be 0 or 1"
