package weather.service;

import org.joda.time.DateTime;
import org.springframework.stereotype.Service;
import weather.domain.*;

import java.util.List;
import java.util.Random;
import java.util.concurrent.CompletableFuture;
import java.util.function.IntFunction;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static org.joda.time.Period.hours;

@Service
public class TestWeatherDataProvider implements WeatherDataProvider {
    
    private double withVariation(double base) {
        return withVariation(base, base * 0.1);
    }

    private double withVariation(double base, double maxD) {
        double maxDAbs = base * maxD;
        return base + (new Random().nextDouble() * maxDAbs * 2) - maxDAbs;
    }

    @Override
    public CompletableFuture<ActualWeather> getCurrentWeather(String city) {
        return CompletableFuture.completedFuture(new ActualWeather(new WeatherKey("Kiyv", new DateTime()),
                new WeatherData(withVariation(10.0), withVariation(0.9), withVariation(300), withVariation(5.0))));
    }

    @Override
    public CompletableFuture<List<Forecast>> getForecast(String city) {
        IntFunction<Forecast> weatherDataSupplier = (i) -> new Forecast(
                new ForecastKey("Kyiv", new DateTime().plus(hours(i * 6)), new DateTime()),
                new WeatherData(withVariation(10.0, i*0.05), withVariation(0.9, i*0.05), withVariation(300, i*0.05), withVariation(5.0, i*0.05)));
        return CompletableFuture.completedFuture(
                IntStream.range(1, 15)
                        .mapToObj(weatherDataSupplier)
                        .collect(Collectors.toList())
        );
    }
}
