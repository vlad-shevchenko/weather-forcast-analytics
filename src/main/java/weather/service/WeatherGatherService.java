package weather.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import weather.domain.City;
import weather.repository.ActualWeatherRepository;
import weather.repository.ForecastRepository;

import java.util.ArrayList;
import java.util.List;

@Service
@ConfigurationProperties(prefix = "app.weather")
public class WeatherGatherService {

    private static final Logger logger = LoggerFactory.getLogger(WeatherGatherService.class);

    private List<WeatherDataProvider> weatherDataProviders;
    private ActualWeatherRepository actualWeatherRepository;
    private ForecastRepository forecastRepository;
    private List<City> cities = new ArrayList<>();

    @Autowired
    public WeatherGatherService(List<WeatherDataProvider> weatherDataProviders, ActualWeatherRepository actualWeatherRepository, ForecastRepository forecastRepository) {
        this.weatherDataProviders = weatherDataProviders;
        this.actualWeatherRepository = actualWeatherRepository;
        this.forecastRepository = forecastRepository;
    }

    @Scheduled(cron = "0 30 * * * *")
    public void gatherWeatherData() {
        logger.info("Initiating gathering weather data. Cities: {}", cities.toString());
        weatherDataProviders.forEach(wdp -> {
            logger.info("Gathering weather data using {}", wdp.getClass().getName());
            wdp.getCurrentWeather(cities).thenAccept(actualWeatherRepository::saveAll);
            wdp.getForecast(cities).thenAccept(forecastRepository::saveAll);
        });
    }


    public List<City> getCities() {
        return cities;
    }
}
