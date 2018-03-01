package weather.service;

import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.springframework.stereotype.Service;
import weather.domain.*;

import java.util.Collection;
import java.util.List;
import java.util.Random;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static org.joda.time.Period.hours;

@Service
public class TestWeatherDataProvider implements WeatherDataProvider {
    
    private double withVariation(double base) {
        return withVariation(base, 0.1);
    }

    private double withVariation(double base, double maxD) {
        double maxDAbsolute = base * maxD;
        return base + (new Random().nextDouble() * maxDAbsolute * 2) - maxDAbsolute;
    }

    @Override
    public CompletableFuture<List<ActualWeather>> getCurrentWeather(Collection<City> cities) {
        return CompletableFuture.completedFuture(
                cities.stream().map(
                        city -> new ActualWeather(new WeatherKey(getName(), city, new DateTime(DateTimeZone.UTC)),
                                new WeatherData(withVariation(10.0), withVariation(0.9), withVariation(300), withVariation(5.0))
                        )
                ).collect(Collectors.toList())
        );
    }

    @Override
    public CompletableFuture<List<Forecast>> getForecast(Collection<City> cities) {
        // I swear I don't do that in production
        return CompletableFuture.completedFuture(
                cities.stream().flatMap(
                        city -> IntStream.range(1, 15)
                                .mapToObj((i) -> new Forecast(
                                        new ForecastKey(getName(), city, new DateTime(DateTimeZone.UTC).plus(hours(i * 3)), new DateTime(DateTimeZone.UTC)),
                                        new WeatherData(withVariation(10.0, i * 0.05), withVariation(0.9, i * 0.05), withVariation(300, i * 0.05), withVariation(5.0, i * 0.05)))
                                )
                ).collect(Collectors.toList())
        );
    }

    @Override
    public String getName() {
        return "testWdp";
    }
}
