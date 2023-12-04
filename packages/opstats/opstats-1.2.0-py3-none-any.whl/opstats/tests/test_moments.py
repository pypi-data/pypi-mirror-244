import numpy

from opstats.moments import Moments, MomentCalculator

from opstats.tests.base import BaseTestCases

# Use an even number of elements to get uneven sample sizes when dividing into three lists.
RANDOM_INTS = list(numpy.random.randint(1, 100, 1000))
RANDOM_FLOATS = list(numpy.random.rand(1000))


class TestMomentCalculator(BaseTestCases.TestMoments):
    def test_invalid_parameters(self) -> None:
        with self.assertRaisesRegex(ValueError, 'Argument "sample_variance" must be a bool, received'):
            MomentCalculator(sample_variance=None)  # type: ignore

        with self.assertRaisesRegex(ValueError, 'Argument "sample_variance" must be a bool, received'):
            MomentCalculator(sample_variance='')  # type: ignore

        with self.assertRaisesRegex(ValueError, 'Argument "bias_adjust" must be a bool, received'):
            MomentCalculator(bias_adjust=None)  # type: ignore

        with self.assertRaisesRegex(ValueError, 'Argument "bias_adjust" must be a bool, received'):
            MomentCalculator(bias_adjust='')  # type: ignore

    def test_none(self) -> None:
        empty = Moments()
        calculator = MomentCalculator()
        calculator.add(None)  # type: ignore
        result = calculator.get()
        self.compare_moments(empty, result)

    def test_empty(self) -> None:
        empty = Moments()
        result = self.calculate([])
        self.compare_moments(empty, result)

    def test_single_value(self) -> None:
        data_points = [1.0]
        scipy_result = self.calculate_scipy(data_points)
        result = self.calculate(data_points)
        self.compare_moments(scipy_result, result)

    def test_zeros(self) -> None:
        data_points = [0.0, 0.0]
        scipy_result = self.calculate_scipy(data_points)
        result = self.calculate(data_points)
        self.compare_moments(scipy_result, result)

    def test_ones(self) -> None:
        data_points = [1.0, 1.0, 1.0]
        scipy_result = self.calculate_scipy(data_points)
        result = self.calculate(data_points)
        self.compare_moments(scipy_result, result)

    def test_sample_variance_integer(self) -> None:
        scipy_result = self.calculate_scipy(RANDOM_INTS, sample_variance=True)
        result = self.calculate(RANDOM_INTS, sample_variance=True)
        self.compare_moments(scipy_result, result)

    def test_population_variance_integers(self) -> None:
        scipy_result = self.calculate_scipy(RANDOM_INTS)
        result = self.calculate(RANDOM_INTS)
        self.compare_moments(scipy_result, result)

    def test_sample_bias_integers(self) -> None:
        scipy_result = self.calculate_scipy(RANDOM_INTS, sample_variance=True, bias_adjust=True)
        result = self.calculate(RANDOM_INTS, sample_variance=True, bias_adjust=True)
        self.compare_moments(scipy_result, result)

    def test_population_bias_integers(self) -> None:
        scipy_result = self.calculate_scipy(RANDOM_INTS, bias_adjust=True)
        result = self.calculate(RANDOM_INTS, bias_adjust=True)
        self.compare_moments(scipy_result, result)

    def test_sample_variance_floats(self) -> None:
        scipy_result = self.calculate_scipy(RANDOM_FLOATS, sample_variance=True)
        result = self.calculate(RANDOM_FLOATS, sample_variance=True)
        self.compare_moments(scipy_result, result)

    def test_population_variance_floats(self) -> None:
        scipy_result = self.calculate_scipy(RANDOM_FLOATS)
        result = self.calculate(RANDOM_FLOATS)
        self.compare_moments(scipy_result, result)

    def test_sample_bias_floats(self) -> None:
        scipy_result = self.calculate_scipy(RANDOM_FLOATS, sample_variance=True, bias_adjust=True)
        result = self.calculate(RANDOM_FLOATS, sample_variance=True, bias_adjust=True)
        self.compare_moments(scipy_result, result)

    def test_population_bias_floats(self) -> None:
        scipy_result = self.calculate_scipy(RANDOM_FLOATS, bias_adjust=True)
        result = self.calculate(RANDOM_FLOATS, bias_adjust=True)
        self.compare_moments(scipy_result, result)
